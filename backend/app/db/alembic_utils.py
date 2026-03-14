import os
from alembic.config import Config
from alembic import command

def run_upgrade():
    # Get the project root directory
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    alembic_cfg = Config(os.path.join(base_dir, "alembic.ini"))
    alembic_cfg.set_main_option("script_location", os.path.join(base_dir, "migrations"))
    
    print("Running database migrations...")
    try:
        command.upgrade(alembic_cfg, "head")
        print("Migrations successfully applied.")
    except Exception as e:
        print(f"Error applying migrations: {e}")
