import logging
from .config import LOG_FILE, ensure_dirs

ensure_dirs()
logger = logging.getLogger("facevision")
logger.setLevel(logging.INFO)
if not logger.handlers:
    h = logging.FileHandler(LOG_FILE, encoding="utf-8")
    h.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    logger.addHandler(h)

def log_event(message):
    logger.info(message)
