import bcrypt
import jwt
import random
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from  fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
import os

load_dotenv()

client = AsyncIOMotorClient("mongodb://127.0.0.1:27017")
db = client["ykuser_database"]
users_collection = db["users"]

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

# Hash password
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Verify password
def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# Generate JWT token
def generate_token(email):
    payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(days=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# Register user
async def register_user(email, password):
    existing_user = await users_collection.find_one({"email": email})
    if existing_user:
        return {"error": "User already exists"}

    hashed_password = hash_password(password)
    from datetime import datetime
    now = datetime.utcnow()
    await users_collection.insert_one({
        "email": email,
        "password": hashed_password,
        "username": email.split("@")[0],
        "createdAt": now,
        "updatedAt": now,
        "profile": {}
    })

    # Generate token
    token = generate_token(email)
    return {"message": "User registered successfully", "token": token}

# Register user with OTP and verify on the same page
async def register_user_with_otp_and_verify(email, password, otp=None):
    existing_user = await users_collection.find_one({"email": email})
    if existing_user:
        # If OTP is provided, verify it
        if otp:
            if existing_user.get("otp") == otp:
                # OTP is correct, complete registration
                await users_collection.update_one(
                    {"email": email},
                    {"$unset": {"otp": ""}, "$set": {"verified": True, "updatedAt": datetime.utcnow()}}
                )
                token = generate_token(email)
                return {"message": "Registration complete. Redirecting to dashboard.", "token": token}
            else:
                return {"error": "Invalid OTP"}
        return {"error": "User already exists. Awaiting OTP verification."}

    # If no OTP is provided, initiate registration
    hashed_password = hash_password(password)
    now = datetime.utcnow()

    # Generate OTP
    generated_otp = str(random.randint(100000, 999999))

    await users_collection.insert_one({
        "email": email,
        "password": hashed_password,
        "username": email.split("@")[0],
        "createdAt": now,
        "updatedAt": now,
        "profile": {},
        "otp": generated_otp,
        "verified": False
    })

    # Send OTP email
    await send_otp_email(email, generated_otp)

    return {"message": "User registered successfully. OTP sent to email."}

# Login user
async def login_user(email, password):
    user = await users_collection.find_one({"email": email})
    if not user or not verify_password(password, user["password"]):
        return {"error": "Invalid credentials"}

    token = generate_token(email)
    return {"message": "Login successful", "token": token}

# Get user profile
async def get_user_profile(email):
    user = await users_collection.find_one({"email": email})
    if not user:
        return {"error": "User not found"}
    return {
        "email": user["email"],
        "username": user.get("username", ""),
        "bio": user.get("profile", {}).get("bio", ""),
        "createdAt": user.get("createdAt"),
        "updatedAt": user.get("updatedAt")
    }

# Update user profile
async def update_user_profile(email, profile_data):
    result = await users_collection.update_one(
        {"email": email},
        {"$set": {"profile": profile_data, "updatedAt": datetime.utcnow()}}
    )
    if result.modified_count == 0:
        return {"error": "Failed to update profile"}
    return {"message": "Profile updated successfully"}

# Get user by email
async def get_user_by_email(email):
    user = await users_collection.find_one({"email": email})
    if not user:
        return None
    return user

# Email server configuration
MAIL_CONFIG = ConnectionConfig(
    MAIL_USERNAME=os.getenv("SMTP_USERNAME"),
    MAIL_PASSWORD=os.getenv("SMTP_PASSWORD"),
    MAIL_FROM=os.getenv("SMTP_USERNAME"),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

async def send_otp_email(email: str, otp: str):
    message = MessageSchema(
        subject="Your OTP Code",
        recipients=[email],
        body=f"Your OTP code is: {otp}",
        subtype="plain",
    )
    fm = FastMail(MAIL_CONFIG)
    await fm.send_message(message)