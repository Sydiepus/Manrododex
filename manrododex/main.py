import pathlib

import manrododex.logger as logger
from manrododex.exceptions import NoneUUID, LangNotAvail
from manrododex.manga import Manga
from manrododex.system_helper import SysHelper


def main(url_uuid, title_settings, lang, selected_vol_chap, main_path, log_level):
    """A comment to keep track of the parameters.
    Parameters:
    ------------
    url_uuid:
        type: str
        default: No Default.
    title_settings:
        type: tuple
        default: (None, None, True)
    lang:
        type: str
        default: 'en'
    selected_vol_chap:
        type: str
        default: None
    main_path:
        type: str/path
        default: current working dir + 'Manga'
    log_level:
        type: str
        default: INFO
    """
    logger.init(log_level)
    try:
        manga = Manga(url_uuid, lang)
        # Make the request to get basic info about the manga.
        manga.get_info(title_settings)
        # Make the requests to get the available chapters.
        manga.get_chapters(selected_vol_chap)
        # It's now time to download the manga.
        sys_helper = SysHelper(main_path, manga.info["title"])
        # First create the main manga directory where the manga need to be put.
        sys_helper.create_main_manga_dir()
        # Then we create the directory for the manga that have the manga title as name.
        sys_helper.create_manga_dir()
    except (NoneUUID, LangNotAvail):
        return 1

    return 0


# TODO: remove this before merging with main.
if __name__ == "__main__":
    main("52829b03-4675-4a1e-a4be-742436a6e306", (None, None, True), "en", "v1v",
         str(pathlib.Path().resolve().absolute()), "DEBUG")
