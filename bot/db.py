import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if SUPABASE_URL and SUPABASE_SERVICE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
else:
    supabase = None
    print("Warning: Supabase credentials not found.")

def upsert_user(telegram_id: int, name: str):
    """Upsert user into the database."""
    # TODO: Implement upsert logic with dashboard_token generation
    pass

def save_transaction(user_id: str, tx_data: dict):
    """Save a transaction into the database."""
    # TODO: Implement transaction saving
    pass

# TODO: Add functions for get_owed, delete_latest_transaction (undo), etc.
