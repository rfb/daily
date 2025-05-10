import os

from datetime import datetime
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

load_dotenv()

TZ = os.environ.get("TZ")
tz = ZoneInfo(TZ)

today = datetime.now(tz)
