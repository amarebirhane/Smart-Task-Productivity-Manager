from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, users, tasks, categories, analytics, settings as settings_routes
from app.core.config import settings
from app.db.database import engine
from app.db.init_db import init_db
from app.db.database import SessionLocal
from app.db.alembic_utils import run_upgrade

# Run database migrations
run_upgrade()

# Seed initial data
with SessionLocal() as db:
    init_db(db)


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(tasks.router, prefix=f"{settings.API_V1_STR}/tasks", tags=["tasks"])
app.include_router(categories.router, prefix=f"{settings.API_V1_STR}/categories", tags=["categories"])
app.include_router(analytics.router, prefix=f"{settings.API_V1_STR}/analytics", tags=["analytics"])
app.include_router(settings_routes.router, prefix=f"{settings.API_V1_STR}/settings", tags=["settings"])

@app.get("/")
def root():
    return {"message": "Welcome to Smart Task & Productivity Manager API"}
