import os
import uuid
import logging
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if SUPABASE_URL and SUPABASE_SERVICE_KEY and SUPABASE_URL != "your_supabase_project_url":
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {e}")
        supabase = None
else:
    supabase = None
    print("Warning: Supabase credentials not found or invalid.")

def upsert_user(telegram_id: int, name: str) -> dict:
    """Upsert user into the database and return user record."""
    if not supabase:
        return None
    try:
        # Check if user exists
        result = supabase.table("users").select("*").eq("telegram_id", telegram_id).execute()
        if result.data:
            return result.data[0]
        
        # If not, insert new user
        new_user = {
            "telegram_id": telegram_id,
            "name": name,
            "dashboard_token": str(uuid.uuid4())
        }
        res = supabase.table("users").insert(new_user).execute()
        if res.data:
            return res.data[0]
    except Exception as e:
        logger.error(f"Database error in upsert_user: {e}")
    return None

def save_transaction(user_id: str, tx_data: dict) -> dict:
    """Save a transaction into the database."""
    if not supabase:
        return None
    try:
        new_tx = {
            "user_id": user_id,
            "amount": float(tx_data.get("amount", 0.0)),
            "currency": tx_data.get("currency", "INR"),
            "category": tx_data.get("category", "General"),
            "transaction_type": tx_data.get("transaction_type", "expense"),
            "description": tx_data.get("description", "")
        }
        res = supabase.table("transactions").insert(new_tx).execute()
        if res.data:
            return res.data[0]
    except Exception as e:
        logger.error(f"Database error in save_transaction: {e}")
    return None
