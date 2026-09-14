import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXPORTS_DIR = DATA_DIR / "exports"

ALCHEMY_API_KEY = os.getenv("ALCHEMY_API_KEY")

ALCHEMY_HTTP_URL = (
    f"https://robinhood-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}"
)

ALCHEMY_WS_URL = (
    f"wss://robinhood-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}"
)

TRACKED_WALLET = "0xce7263b5af8331c3baa620db93b44522d5982e35"