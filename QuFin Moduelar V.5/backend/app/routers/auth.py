from fastapi import APIRouter, HTTPException, Depends, File, UploadFile
from pydantic import BaseModel, EmailStr
from app.auth import register_user, login_user, get_user_profile, update_user_profile, register_user_with_otp_and_verify, users_collection, generate_token
from app.dependencies import get_current_user, get_db
from app.models import User
from random import randint
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import shutil
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

router = APIRouter()

# In-memory store for OTPs (use a database in production)
otp_store = {}

class UserRegistration(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserProfile(BaseModel):
    username: str
    bio: str = ""

class EmailRequest(BaseModel):
    email: EmailStr

class OTPVerificationRequest(BaseModel):
    email: EmailStr
    code: int

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = os.getenv("SMTP_USERNAME")  # Set this in your environment variables
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")  # Set this in your environment variables

# Don't crash if SMTP credentials are missing — email sending should be best-effort in dev.
if not SMTP_USERNAME or not SMTP_PASSWORD:
    print("Warning: SMTP_USERNAME or SMTP_PASSWORD not set. Email delivery will be disabled in this environment.")

async def verify_user_otp(email: str, otp: str) -> bool:
    # Placeholder logic for OTP verification
    # Replace this with actual OTP verification logic (e.g., check against a database or cache)
    stored_otp = "123456"  # Example OTP for testing
    return otp == stored_otp

@router.post("/auth/signup")
async def signup(user: UserRegistration):
    result = await register_user_with_otp_and_verify(user.email, user.password)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    # return full result so token (if generated) is forwarded to client
    return result

@router.post("/auth/login")
async def login(user: UserLogin):
    result = await login_user(user.email, user.password)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/auth/profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
    profile = await get_user_profile(current_user["email"])
    return profile

@router.put("/auth/profile")
async def update_profile(profile: UserProfile, current_user: dict = Depends(get_current_user)):
    result = await update_user_profile(current_user["email"], profile.dict())
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return {"message": "Profile updated successfully"}

@router.post("/auth/upload")
async def upload_file(file: UploadFile, current_user: dict = Depends(get_current_user)):
    try:
        file_location = f"uploads/{current_user['email']}/{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"message": "File uploaded successfully", "file_path": file_location}
    except Exception as e:
        raise HTTPException(status_code=500, detail="File upload failed")

@router.post("/send-verification")
async def send_verification_email(request: EmailRequest):
    email = request.email
    otp = randint(100000, 999999)
    otp_store[email] = otp
    # If SMTP not configured, don't attempt to send mail (allow testing in dev)
    if not SMTP_USERNAME or not SMTP_PASSWORD:
        print(f"SMTP not configured — OTP for {email} generated: {otp}")
        return {"message": "OTP generated but email not sent (SMTP not configured)."}

    try:
        # Set up the SMTP server
        server = SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)

        # Create the email
        message = MIMEMultipart()
        message["From"] = SMTP_USERNAME
        message["To"] = email
        message["Subject"] = "Your Verification Code"
        body = f"Your verification code is: {otp}"
        message.attach(MIMEText(body, "plain"))

        # Send the email
        server.sendmail(SMTP_USERNAME, email, message.as_string())
        server.quit()

        return {"message": "Verification email sent."}
    except Exception as e:
        # Don't fail the entire request with a 500 that might be caused by mail server; return informative message
        print(f"Failed to send verification email to {email}: {e}")
        return {"message": "OTP generated but failed to send email (see server logs)."}

@router.post("/verify-code")
async def verify_code(request: OTPVerificationRequest):
    email = request.email
    code = request.code

    if email not in otp_store or otp_store[email] != code:
        raise HTTPException(status_code=400, detail="Invalid or expired verification code.")

    # Verification successful, remove OTP from store
    del otp_store[email]

    # Optionally, mark the user as verified in the database
    db = get_db()
    user = db.query(User).filter(User.email == email).first()
    if user:
        user.is_verified = True
        db.commit()

    return {"message": "Email verified successfully."}

@router.post("/auth/verify-otp")
async def verify_otp(otp_data: dict):
    email = otp_data.get("email")
    otp = otp_data.get("otp")

    if not email or not otp:
        raise HTTPException(status_code=400, detail="Email and OTP are required.")
    try:
        print(f"verify_otp called with: {otp_data}")
        # users_collection is an async motor collection from app.auth
        user = await users_collection.find_one({"email": email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        # Compare as strings to avoid type mismatches (db might store OTP as int or str)
        if str(user.get("otp")) != str(otp):
            raise HTTPException(status_code=400, detail="Invalid OTP.")

        # Clear OTP after successful verification and mark verified
        await users_collection.update_one({"email": email}, {"$unset": {"otp": ""}, "$set": {"verified": True}})

        # Generate a token so frontend can log user in immediately
        token = generate_token(email)
        return {"message": "OTP verified successfully.", "token": token}
    except HTTPException:
        raise
    except Exception as e:
        # Log the exception server-side and return a 500
        print(f"verify_otp error for {email}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during OTP verification")