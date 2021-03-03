import logging


def log_game():
    """Initializes console for logging messages"""
    logging.basicConfig(level=logging.INFO)
    logging.info("Welcome to The Froggerithm!")