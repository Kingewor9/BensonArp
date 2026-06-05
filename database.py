# ============================================================
# database.py — All MongoDB operations
# ============================================================

import os
from datetime import datetime, timezone
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# ── Connect to MongoDB ───────────────────────────────────────
client = MongoClient(os.getenv("MONGO_URI"))
db = client["telegrambot"]
users_col = db["users"]  # One document per user


# ── Save or update a user record when they message us ───────
def record_incoming_message(user_id: int, first_name: str, keyword: str):
    """
    Called when a user sends a recognised keyword for the first time.
    If the user already exists we DO NOT overwrite their record —
    the scheduler relies on the original first_message_time.
    """
    existing = users_col.find_one({"user_id": user_id})

    if not existing:
        users_col.insert_one({
            "user_id":            user_id,
            "first_name":         first_name,
            "keyword":            keyword,
            "first_message_time": datetime.now(timezone.utc),
            "last_message_time":  datetime.now(timezone.utc),
            "followup_sent":      False,
            "replied":            True,
        })
    else:
        # User came back — update last seen and reset follow-up flag
        users_col.update_one(
            {"user_id": user_id},
            {"$set": {
                "last_message_time": datetime.now(timezone.utc),
                "first_name":        first_name,   # name can change
            }}
        )


# ── Called for ANY incoming message (keyword or not) ────────
def update_last_message_time(user_id: int, first_name: str):
    """
    Every time a user sends ANY message we update last_message_time.
    This prevents the follow-up from firing if they reply before 6 hrs.
    """
    users_col.update_one(
        {"user_id": user_id},
        {"$set": {
            "last_message_time": datetime.now(timezone.utc),
            "first_name":        first_name,
        }},
        upsert=False   # don't create a record just for non-keyword messages
    )


# ── Fetch users eligible for a follow-up message ────────────
def get_users_due_for_followup(hours: int) -> list:
    """
    Returns users where:
      1. A keyword reply was sent (replied=True)
      2. Follow-up has NOT been sent yet (followup_sent=False)
      3. last_message_time is older than `hours` hours ago
         (meaning they haven't sent anything new since the keyword)
    """
    from datetime import timedelta
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)

    return list(users_col.find({
        "replied":       True,
        "followup_sent": False,
        "last_message_time": {"$lte": cutoff},
    }))


# ── Mark follow-up as sent so we never double-send ──────────
def mark_followup_sent(user_id: int):
    users_col.update_one(
        {"user_id": user_id},
        {"$set": {"followup_sent": True}}
    )