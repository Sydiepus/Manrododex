import manrododex.logger as logger
from manrododex.exceptions import NoneUUID
from manrododex.manga import Manga


def main(url_uuid, manga_name, log_level):
    logger.init(log_level)
    try:
        manga = Manga(url_uuid, manga_name)
    except NoneUUID:
        return
    # Make the request to get basic info about the manga.
    else:
        manga.get_info()
