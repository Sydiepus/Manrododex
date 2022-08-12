from manrododex.manga import Manga
import logger


def main(url_uuid, manga_name, log_level):
    logger.init(log_level)
    manga = Manga(url_uuid, manga_name)
