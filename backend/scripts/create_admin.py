import sys
import os
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models.user import User
from ..auth.utils import get_password_hash

def create_admin(db: Session, email: str, password: str, full_name: str) -> None:
    """Create an admin user."""
    user = db.query(User).filter(User.email == email).first()
    if user:
        print(f"User with email {email} already exists")
        return

    user = User(
        email=email,
        full_name=full_name,
        hashed_password=get_password_hash(password),
        is_active=True,
        is_admin=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"Admin user {email} created successfully")

def main():
    """Main function to create admin user."""
    if len(sys.argv) != 4:
        print("Usage: python -m scripts.create_admin <email> <password> <full_name>")
        sys.exit(1)

    email = sys.argv[1]
    password = sys.argv[2]
    full_name = sys.argv[3]

    db = SessionLocal()
    try:
        create_admin(db, email, password, full_name)
    finally:
        db.close()

if __name__ == "__main__":
    main() 