from sqlalchemy.orm import Session
from app.crud.user_crud import get_user_by_email, create_user
from app.schemas.user_schema import UserCreate
from app.models.user import User
from app.core.config import settings

def init_db(db: Session) -> None:
    # Check if admin exists
    admin = get_user_by_email(db, email=settings.FIRST_SUPERUSER)
    if not admin:
        admin_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            username="admin",
            first_name="Admin",
            last_name="User",
            password=settings.FIRST_SUPERUSER_PASSWORD,
        )
        create_user(db, admin_in, role="admin")
        print(f"Default admin created: {settings.FIRST_SUPERUSER}")
    else:
        print(f"Default admin already exists: {settings.FIRST_SUPERUSER}")
