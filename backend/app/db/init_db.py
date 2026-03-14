from sqlalchemy.orm import Session
from app.crud.user_crud import get_user_by_email, get_user_by_username, create_user
from app.schemas.user_schema import UserCreate
from app.models.user import User
from app.core.config import settings

def init_db(db: Session) -> None:
    # Check if admin exists by email or username
    user_by_email = get_user_by_email(db, email=settings.FIRST_SUPERUSER)
    user_by_username = get_user_by_username(db, username=settings.FIRST_SUPERUSER_USERNAME)
    
    if not user_by_email and not user_by_username:
        admin_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            username=settings.FIRST_SUPERUSER_USERNAME,
            first_name="Admin",
            last_name="User",
            password=settings.FIRST_SUPERUSER_PASSWORD,
        )
        create_user(db, admin_in, role="admin")
        print(f"Default admin created: {settings.FIRST_SUPERUSER} ({settings.FIRST_SUPERUSER_USERNAME})")
    else:
        if user_by_email:
            print(f"Default admin already exists with email: {settings.FIRST_SUPERUSER}")
        if user_by_username:
            print(f"Default admin already exists with username: {settings.FIRST_SUPERUSER_USERNAME}")
