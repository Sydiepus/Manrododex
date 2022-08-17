import manrododex.logger as logger
from manrododex.exceptions import NoneUUID, LangNotAvail
from manrododex.manga import Manga


def main(url_uuid, title_settings, lang, log_level):
    logger.init(log_level)
    try:
        manga = Manga(url_uuid, lang)
        # Make the request to get basic info about the manga.
        manga.get_info(title_settings)
        # Make the requests to get the available chapters.
        manga.get_chapters()
    except (NoneUUID, LangNotAvail):
        return 1

    return 0


if __name__ == "__main__":
    main("b98c4daf-be1a-46c8-ad83-21d532995240", (None, None, True), "en", "DEBUG")
