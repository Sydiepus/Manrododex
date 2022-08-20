import logging
import re

from manrododex.apiadapter import ApiAdapter
from manrododex.chapters import Chapters
from manrododex.exceptions import NoneUUID, LangNotAvail

MANGA_ENDPOINT = "/manga"
CHAPTER_ENDPOINT = "/chapter"
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


def _gen_helper(var_gen):
    gen = None
    if var_gen:
        if "/" in var_gen:
            to_gen = var_gen.split("/")
            if int(to_gen[0]) < int(to_gen[-1]):
                gen = [str(i) for i in range(int(to_gen[0]), int(to_gen[-1]) + 1)]
            else:
                gen = None
        else:
            gen = var_gen
    return gen


def _gen_list(selected_chapters):
    """should return 1 tuple with 2 lists:
            The first should be the volume(s).
            The second the chapter(s).
            use 'v{num}v' to mark the number as volume.
                '/' to make a range.
                ',' to start a new rule.
            e.g: v7v99 would be volume 7 chapter 99.
                 v1/3v1 would be chapter one from vol 1, 2 and 3.
                 1,4,6 would download chapter 1, 2 and 3 it assumes that no volume set aka 'None'.
                 v6v would download volume 6 entirely.
                 """
    vol = list()
    chap = list()
    for entry in selected_chapters.strip().split(","):
        try:
            vol_match = re.search("v[0-9]*/?[0-9]*v", entry).group()
            vol_gen = vol_match.strip("v")
            chap_gen = entry.replace(vol_match, "")
        except AttributeError:
            vol_gen = None
            chap_gen = entry
        vol_a = _gen_helper(vol_gen)
        chap_a = _gen_helper(chap_gen)
        vol.extend(vol_a) if type(vol_a) == list else vol.append(vol_a)
        chap.extend(chap_a) if type(vol_a) == list else chap.append(chap_a)
    generated = (sorted(list(set(vol))), sorted(chap))
    return generated


def _check_ext_url(chap_id):
    """check whether the chapter have an external URL or not.
        True means yes it have an external URL.
        False for no."""
    info = ApiAdapter.make_request("get", f"{CHAPTER_ENDPOINT}/{chap_id}")["data"]
    if info["attributes"]["externalUrl"] == "null":
        return True
    else:
        return False


class Manga:
    """The Manga uhh...yeah

    Parameters :
    -------------
    url_uuid:
        The url or the uuid of the manga that needs to be fetched.
    lang:
        the language code in which the user wants to download the
        manga.
    """

    def __init__(self, url_uuid, lang):
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
            self.chapters = Chapters()
            logging.info("Manga created with no errors.")

    def get_info(self, title_settings):
        """Gets more info about the manga, like:
        title, altTitles, description, status, availableTranslatedLanguages, year, contentRating

        Parameters:
        ------------
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

        Expected response a dictionary with the following keys that interests us:
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
        self.info["title"] = _handle_title(title_settings, info["title"], info["altTitles"])
        del title_settings
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

    def get_chapters(self, selected_vol_chap):
        info = ApiAdapter.make_request("get",
                                       f"{MANGA_ENDPOINT}/{self.uuid}/aggregate",
                                       passed_params={
                                           "translatedLanguage[]": f"{self.lang}"
                                       })["volumes"]
        if selected_vol_chap:
            chap_to_fetch = _gen_list(selected_vol_chap)
            for vol in chap_to_fetch[0]:
                try:
                    vol_tmp = info[vol]
                    for chap in chap_to_fetch[-1]:
                        try:
                            chap_tmp = vol_tmp["chapters"][chap]
                            chap_id = None
                            if chap_tmp["count"] != 1 and _check_ext_url(chap_tmp["id"]):
                                for id_o in chap_tmp["others"]:
                                    if not _check_ext_url(id_o):
                                        chap_id = id_o
                                        break
                            else:
                                chap_id = chap_tmp["id"]
                            if chap_id:
                                self.chapters.put((vol, chap, chap_id))
                            else:
                                continue
                        except KeyError:
                            continue
                except KeyError:
                    continue
        else:
            pass
