import manrododex.logger as logger
from manrododex.exceptions import NoneUUID, LangNotAvail
from manrododex.manga import Manga


def main(url_uuid, title_settings, lang, selected_vol_chap, main_path, log_level):
    logger.init(log_level)
    try:
        manga = Manga(url_uuid, lang)
        # Make the request to get basic info about the manga.
        manga.get_info(title_settings)
        # Make the requests to get the available chapters.
        manga.get_chapters(selected_vol_chap)
    except (NoneUUID, LangNotAvail):
        return 1

    return 0


if __name__ == "__main__":
    main("52829b03-4675-4a1e-a4be-742436a6e306", (None, None, True), "en", "v1v", "DEBUG")
