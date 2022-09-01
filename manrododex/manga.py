#  Copyright (c) 2022 Charbel Assaad
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import logging
import re

from manrododex.apiadapter import ApiAdapter
from manrododex.exceptions import NoneUUID, LangNotAvail
from manrododex.manga_helpers import Chapters

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
            logging.debug("Using alternative title with language '%s'", title_settings[1])
            for i in info_alttitles:
                try:
                    title = i[title_settings[1]]
                    break
                except KeyError:
                    continue
            if not title:
                logging.debug("No altTitle found for '%s' using default one.", title_settings[1])
                title = _get_default_title(info_title)
        logging.debug("Manga title set successfully.")
    else:
        logging.debug("Manga title already given not changing it.")
    logging.debug("Name to be used '%s'", title)
    return title


def _gen_helper(var_gen):
    gen = None
    if var_gen and re.search("(([0-9]+)/([0-9]+))|([0-9]+)", var_gen):
        if "/" in var_gen:
            logging.debug("Generating range.")
            to_gen = var_gen.split("/")
            if int(to_gen[0]) < int(to_gen[-1]):
                gen = [str(i) for i in range(int(to_gen[0]), int(to_gen[-1]) + 1)]
                logging.debug("Range successfully generated.")
            else:
                logging.debug("Failed to generate range, are you sure the range is in ascending order from left to "
                              "right ?")
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
                 v1/3v1 would be chapter 1 from vol 1, 2 and 3.
                 1,4,6 would download chapter 1, 4 and 6 regardless for the volume.
                 v6v would download volume 6 entirely.
                 """
    vol = list()
    chap = list()
    for entry in selected_chapters.strip().split(","):
        try:
            vol_match = re.search("v((([0-9]+)/([0-9]+))|([0-9]+))v", entry).group()
            logging.debug("Entry successfully matched.")
            vol_gen = vol_match.strip("v")
            chap_gen = entry.replace(vol_match, "")
        except AttributeError:
            logging.debug("Entry did not match, defaulting to all volumes.")
            vol_gen = None
            chap_gen = entry
        vol_a = _gen_helper(vol_gen)
        chap_a = _gen_helper(chap_gen)
        vol.extend(vol_a) if type(vol_a) is list else vol.append(vol_a)
        chap.extend(chap_a) if type(chap_a) is list else chap.append(chap_a)
    vol = sorted(list(set(vol)))
    chap = sorted(chap)
    logging.debug("vol/chap list successfully generated.")
    return vol, chap


def _check_ext_url(chap_id):
    """check whether the chapter have an external URL or not.
        True means yes it have an external URL.
        False for no."""
    logging.debug("Checking for external url.")
    info = ApiAdapter.make_request("get", f"{CHAPTER_ENDPOINT}/{chap_id}")["data"]
    if info["attributes"]["externalUrl"] == "null":
        logging.debug("external url found.")
        return True
    else:
        logging.debug("external url not found.")
        return False


def _get_vol_list(info):
    return list(reversed(info.keys()))  # list from last to first volume this is why I reversed it.


def _get_chap_list(info, volumes_list):
    chapters_complete = list()
    for volume in volumes_list:
        chapters = info[volume]["chapters"]
        # workaround for f6e7ce00-e09c-4ed2-b806-eb2fdc7a5f60
        if type(chapters) is dict:
            chapters_list = list(reversed(chapters.keys()))
            chapters_complete.extend(chapters_list)
        else:
            continue
    return chapters_complete


def _get_vol_chap_list(info):
    volumes_list = _get_vol_list(info)
    chapters_complete = _get_chap_list(info, volumes_list)
    return volumes_list, chapters_complete


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
            logging.debug("the uuid extracted is : '%s'", self.uuid)
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
        self.info["name"] = _handle_title(title_settings, info["title"], info["altTitles"])
        del title_settings
        try:
            self.info["description_formatted"] = info["description"][self.lang]
            logging.debug("Using description with language '%s'", self.lang)
        except KeyError:
            logging.debug("No description with language '%s'\n Using the first one in the request.", self.lang)
            try:
                self.info["description_formatted"] = next(iter(info["description"].values()))
                logging.debug("Using description with language '%s'", next(iter(info["description"])))
            except StopIteration:
                logging.critical("No suitable description found setting it to None.")
        self.info["status"] = info["status"]
        try:
            self.info["year"] = int(info["year"])
        except TypeError:
            self.info["year"] = info["year"]
        self.info["age_rating"] = info["contentRating"]
        logging.info("All info fetched successfully.")

    def _chapters_to_queue(self, vol_list, chap_list, info):
        for vol in vol_list:
            try:
                vol_tmp = info[vol]
                for chap in chap_list:
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
                            logging.debug("Item successfully added to queue.")
                        else:
                            logging.debug("no chapter id found skipping.")
                            continue
                    except KeyError:
                        continue
            except KeyError:
                continue

    def get_chapters(self, selected_vol_chap):
        """Make the request to get chapters by language and add them to the chapters SimpleQueue in the following
        format: (vol, chap, chap_id)"""
        info = ApiAdapter.make_request("get",
                                       f"{MANGA_ENDPOINT}/{self.uuid}/aggregate",
                                       passed_params={
                                           "translatedLanguage[]": f"{self.lang}"
                                       })["volumes"]
        # not sure if it's supposed to be fetch or download.
        if selected_vol_chap:
            logging.debug("Using user provided vol/chapters.")
            vol_list, chap_list = _gen_list(selected_vol_chap)
            del selected_vol_chap
            if len(vol_list) == len(chap_list) == 1 and vol_list[0] is chap_list[0] is None:
                # if both are None Download everything.
                logging.debug("Something with the generated vol/chap using all vol/chap.")
                vol_list, chap_list = _get_vol_chap_list(info)
            elif len(vol_list) == 1 and not vol_list[0]:
                # if volume is only None download all volumes and respect user given chapters.
                logging.debug("Using all vol and user given chap.")
                vol_list = _get_vol_list(info)
            elif len(chap_list) == 1 and not chap_list[0]:
                # if chapters is only None download all chapters and respect user given volumes.
                logging.debug("Using user given vol and downloading all chapters.")
                chap_list = _get_chap_list(info, vol_list)
            self._chapters_to_queue(vol_list, chap_list, info)
        else:
            logging.debug("Using all volumes and chapters.")
            vol_list, chap_list = _get_vol_chap_list(info)
            self._chapters_to_queue(vol_list, chap_list, info)
        logging.info("All chapters have been fetched and ready for the next step.")
