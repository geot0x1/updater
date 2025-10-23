import logging
from logging.handlers import RotatingFileHandler

def get_logger():
    # Configure logger
    logger = logging.getLogger("myapp")
    logger.setLevel(logging.INFO)

    # Console handler
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(ch)

    # Rotating file handler (1 MB, keep 5 backups)
    fh = RotatingFileHandler("app.log", maxBytes=1_000_000, backupCount=5)
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(fh)
    return logger

Logger = get_logger()