import logging
import re

from manrododex.apiadapter import ApiAdapter
from manrododex.exceptions import NoneUUID

MANGA_ENDPOINT = "/manga"


class Manga:
    """The Manga uhh...yeah

    Parameters :
    -------------
    url_uuid:
        the url or the uuid of the manga that needs to be fetched.
    name :
        the name of the manga if the user want's to manually set it
        otherwise the default one 'the one that you see on the site normally' would be chosen.
    """

    def __init__(self, url_uuid, name):  # , lang):
        try:
            # get the uuid which it's actually a guid.
            # I can validate with a regex I stole from https://stackoverflow.com/a/42048037
            guid_regex = "[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"
            self.uuid = re.search(guid_regex, url_uuid).group()
            logging.debug("the uuid extracted is : %s", self.uuid)
        except AttributeError:
            logging.critical("Failed to extract uuid skipping.")
            self.uuid = None
            raise NoneUUID("Failed to get uuid, execution cannot proceed.")
        else:
            self.name = name
            self.desc = None
            self.status = None
            self.langs = None
            self.chapters = None

    def get_info(self):
        info = ApiAdapter.make_request("get", f"{MANGA_ENDPOINT}/{self.uuid}")["attributes"]
        if not self.name:
            self.name = info["title"].values[0]
        self.desc = info
        # Taking a break commiting to be safe.
        # Note so i don't forget.
        # let the user select the language.
        # chapters SimpleQueue since only image downloading should be threaded.
        # images Queue for threading.
        # not sure if this is right.
