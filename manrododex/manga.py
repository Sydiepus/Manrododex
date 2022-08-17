import logging
import re

from manrododex.apiadapter import ApiAdapter
from manrododex.exceptions import NoneUUID, LangNotAvail

MANGA_ENDPOINT = "/manga"
# the uuid is actually a guid.
# I can validate it with a regex I stole from https://stackoverflow.com/a/42048037
GUID_REGEX = "[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"


def _get_default_title(info_title):
    logging.debug("Using default title.")
    return list(info_title.values())[0]


def _handle_title(title_settings, info_title, info_alttitles):
    title = title_settings[0]
    if not title:
        if title_settings[-1]:
            title = _get_default_title(info_title)
        else:
            logging.debug("Using alternative title with language %s", title_settings[1])
            for i in info_alttitles:
                try:
                    title = i[title_settings[1]]
                    break
                except KeyError:
                    continue
            if not title:
                logging.debug("No altTitle found for %s using default one.", title_settings[1])
                title = _get_default_title(info_title)
        logging.debug("Manga title set successfully.")
    else:
        logging.debug("Manga title already given not changing it.")
    logging.debug("Name to be used %s", title)
    return title


class Manga:
    """The Manga uhh...yeah

    Parameters :
    -------------
    url_uuid:
        The url or the uuid of the manga that needs to be fetched.
    title_settings :
        A tuple that contains 3 elements:
            The first:
                Type: str
                Description: a custom title for the manga.
                Default: None, which means to get it from the site.
            The second:
                Type: str
                Description: the language for the altTitle to be used.
                Default: None, which means to use the language of the manga.
            The third:
                Type: bool
                Description: force the usage of the default title - the one you see on the website - regardless of the
                language specified.
                Default: True
    lang:
        the language code in which the user wants to download the
        manga.
    """

    def __init__(self, url_uuid, title_settings, lang):
        try:
            self.uuid = re.search(GUID_REGEX, url_uuid).group()
            logging.debug("the uuid extracted is : %s", self.uuid)
        except AttributeError:
            logging.critical("Failed to extract uuid skipping.")
            self.uuid = None
            raise NoneUUID("Failed to get uuid, execution cannot proceed.")
        else:
            self.info = dict()
            self.lang = lang
            self.title_settings = title_settings

    def get_info(self):
        """Expected response a dictionary with the following keys that interests us:
        title: dict
        altTitles: list containing a dict
        description: dict
        status: str
        availableTranslatedLanguages: list
        year: int
        contentRating: str
        """
        info = ApiAdapter.make_request("get", f"{MANGA_ENDPOINT}/{self.uuid}")["data"]["attributes"]
        logging.debug("Checking if requested language is available.")
        avl_langs = info["availableTranslatedLanguages"]
        if self.lang not in avl_langs:
            logging.critical("Language not available skipping.")
            raise LangNotAvail("Requested language not available for this manga.")
        del avl_langs
        self.info["title"] = _handle_title(self.title_settings, info["title"], info["altTitles"])
        del self.title_settings
        self.info["desc"] = info["description"][self.lang]
        logging.debug("Using description with language %s", self.lang)
        self.info["status"] = info["status"]
        self.info["year"] = info["year"]
        self.info["contentRating"] = info["contentRating"]
        logging.info("All info fetched successfully.")
        # Taking a break committing to be safe.
        # Note so I don't forget.
        # chapters SimpleQueue since only image downloading should be threaded.
        # images Queue for threading.
        # not sure if this is right.

    def get_chapters(self):
        r = ApiAdapter.make_request("get",
                                    f"{MANGA_ENDPOINT}/{self.uuid}/aggregate",
                                    passed_params={
                                        "translatedLanguage[]": f"{self.lang}"
                                    })["volumes"]
