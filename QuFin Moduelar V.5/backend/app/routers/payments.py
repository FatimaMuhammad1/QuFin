from fastapi import APIRouter, HTTPException
import os
import stripe
from pydantic import BaseModel

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_replace")

router = APIRouter()

class CheckoutRequest(BaseModel):
    price_id: str


@router.post("/create-checkout-session")
def create_checkout(req: CheckoutRequest):
    try:
        session = stripe.checkout.Session.create(
            mode="payment",
            payment_method_types=["card"],
            line_items=[{"price": req.price_id, "quantity": 1}],
            success_url=os.getenv("DOMAIN", "http://localhost:8000") + "/?success=true",
            cancel_url=os.getenv("DOMAIN", "http://localhost:8000") + "/?canceled=true",
        )
        return {"url": session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/webhook")
def webhook():
    # Add webhook handling logic here. For now, it's a placeholder.
    return {"status": "ok"}
