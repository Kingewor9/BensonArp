# ============================================================
# main.py — Entry point: starts listener + scheduler
# ============================================================

import os
import logging
from dotenv import load_dotenv
from telethon import TelegramClient, events
from config import KEYWORD_REPLIES
from database import record_incoming_message, update_last_message_time
from scheduler import start_scheduler
from telethon.sessions import StringSession

load_dotenv()

# ── Logging setup ────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ── Telegram client (uses your user account, not a bot) ─────
API_ID       = int(os.getenv("API_ID"))
API_HASH     = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
SESSION_STRING = os.getenv("SESSION_STRING")

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)


# ── Build a fast lookup: lowercase keyword → reply text ─────
# e.g. {"ads": "Scale your business..."}
KEYWORD_MAP = {kw.lower(): reply for kw, reply in KEYWORD_REPLIES.items()}


# ── Message listener ─────────────────────────────────────────
@client.on(events.NewMessage(incoming=True))
async def handle_message(event):
    """
    Fires on every incoming private message.
    - Always updates last_message_time (blocks follow-up if user replied)
    - Only auto-replies when the message is an EXACT keyword match
    """
    # Ignore group chats / channels — private messages only
    if not event.is_private:
        return

    sender     = await event.get_sender()
    user_id    = sender.id
    first_name = sender.first_name or "there"
    raw_text   = event.raw_text.strip()   # preserve original for exact match

    logger.info(f"[Message] From {first_name} ({user_id}): '{raw_text}'")

    # ── Always update last-seen time for this user ───────────
    # This is what prevents the follow-up if they reply before 6 hrs
    update_last_message_time(user_id, first_name)

    # ── Exact keyword check (case-insensitive, whole message only) ──
    # "Ads" matches. "Do you run ads?" does NOT match.
    normalised = raw_text.lower()

    if normalised in KEYWORD_MAP:
        reply_text = KEYWORD_MAP[normalised]

        # Save to DB BEFORE sending (so timing is accurate)
        record_incoming_message(user_id, first_name, raw_text)

        await event.reply(reply_text)
        logger.info(f"[Reply] Sent '{normalised}' response to {first_name}")
    else:
        logger.info(f"[Skip] '{raw_text}' is not an exact keyword — no auto-reply.")


# ── Main ─────────────────────────────────────────────────────
async def main():
    await client.start()
    logger.info("✅ Telegram client started. Listening for messages...")

    # Start the background follow-up scheduler
    start_scheduler(client)

    # Keep the script running indefinitely
    await client.run_until_disconnected()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())