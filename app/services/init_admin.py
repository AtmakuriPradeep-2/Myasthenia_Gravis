from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.user import User
from app.auth.hashing import hash_password


def create_default_admin(db: Session):
    admin_user = (
        db.query(User)
        .filter(
            (func.lower(User.username) == "admin") |
            (func.lower(User.email) == "admin@example.com")
        )
        .first()
    )

    if not admin_user:
        admin = User(
            username="admin",
            email="admin@example.com",
            hashed_password=hash_password("Admin@123"),
            full_name="System Administrator",
            role="Admin",
            is_active=True
        )
        db.add(admin)
        db.commit()
        print("===================================")
        print("Default Admin Created")
        print("Username : admin / admin@example.com")
        print("Password : Admin@123")
        print("===================================")
    else:
        # Ensure default admin credentials and active state are guaranteed
        admin_user.hashed_password = hash_password("Admin@123")
        admin_user.is_active = True
        db.commit()
        print("===================================")
        print("Default Admin Verified")
        print("Username : admin / admin@example.com")
        print("Password : Admin@123")
        print("===================================")