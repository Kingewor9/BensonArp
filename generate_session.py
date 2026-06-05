# generate_session.py
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import os
from dotenv import load_dotenv

load_dotenv()

API_ID   = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

with TelegramClient(StringSession(), API_ID, API_HASH) as client:
    print("YOUR SESSION STRING:")
    print(client.session.save())