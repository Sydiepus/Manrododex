import manrododex.logger as logger
from manrododex.exceptions import NoneUUID, LangNotAvail
from manrododex.manga import Manga


def main(url_uuid, title_settings, lang, log_level):
    logger.init(log_level)
    try:
        manga = Manga(url_uuid, title_settings, lang)
    except NoneUUID:
        return 1
    # Make the request to get basic info about the manga.
    else:
        try:
            manga.get_info()
        except LangNotAvail:
            return 1
    return 0
