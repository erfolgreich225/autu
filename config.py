import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGODB_URI = os.getenv("MONGODB_URI")
    # Đã bỏ các biến liên quan đến Telegram
    # TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    # TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    missing = [v for v in ["MONGODB_URI"] if not os.getenv(v)]
    if missing:
        raise EnvironmentError(f"Missing required config vars: {', '.join(missing)}")
