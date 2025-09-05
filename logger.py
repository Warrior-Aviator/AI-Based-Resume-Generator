import logging

logger = logging.getLogger("resume_gpt")
if not logger.handlers:
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    fmt = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
    ch.setFormatter(fmt)
    logger.addHandler(ch)
