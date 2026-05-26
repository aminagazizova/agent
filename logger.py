import logging
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    encoding="utf-8"
)

logger = logging.getLogger()