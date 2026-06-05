# ============================================================
# scheduler.py — Background job that sends follow-up messages
# ============================================================

import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database import get_users_due_for_followup, mark_followup_sent
from config import FOLLOWUP_MESSAGE, FOLLOWUP_HOURS

logger = logging.getLogger(__name__)


async def send_followups(client):
    """
    Runs every 15 minutes.
    Finds users who received a keyword reply but haven't messaged
    back within FOLLOWUP_HOURS, then sends them the follow-up.
    """
    due_users = get_users_due_for_followup(FOLLOWUP_HOURS)

    if not due_users:
        logger.info("[Scheduler] No follow-ups due right now.")
        return

    for user in due_users:
        user_id    = user["user_id"]
        first_name = user.get("first_name", "there")

        message = FOLLOWUP_MESSAGE.format(first_name=first_name)

        try:
            await client.send_message(user_id, message)
            mark_followup_sent(user_id)
            logger.info(f"[Scheduler] Follow-up sent to {first_name} (ID: {user_id})")

        except Exception as e:
            logger.error(f"[Scheduler] Failed to send follow-up to {user_id}: {e}")


def start_scheduler(client):
    """
    Creates and starts the background scheduler.
    Checks every 15 minutes for users due a follow-up.
    """
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        send_followups,
        trigger="interval",
        minutes=15,          # checks every 15 min — lightweight
        args=[client],
        id="followup_job",
        replace_existing=True,
    )

    scheduler.start()
    logger.info("[Scheduler] Started — checking every 15 minutes.")
    return scheduler