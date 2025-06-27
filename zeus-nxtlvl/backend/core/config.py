from dotenv import load_dotenv
import os

# Load environment variables from a .env file if present
load_dotenv()

# Example configuration values
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
