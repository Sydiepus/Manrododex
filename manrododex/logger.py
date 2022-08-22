import logging
from tempfile import gettempdir


def init(log_level):
    logging.basicConfig(filename=f"{gettempdir()}/manrododex.log", level=log_level)
    logging.info("Started logging.")
