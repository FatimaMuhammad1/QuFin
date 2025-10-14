from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from . import models


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Return a User by email or None."""
    stmt = select(models.User).where(models.User.email == email)
    result = db.execute(stmt).scalars().first()
    return result


def create_user(db: Session, email: str, hashed_password: str) -> models.User:
    """Create and return a new User (commits the transaction)."""
    # instantiate then set attributes to avoid static analysis issues with
    # SQLAlchemy-generated constructors
    user = models.User(email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
