import re
from manrododex.apiadapter import ApiAdapter
import logging

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
    def __init__(self, url_uuid, name):
        try:
            # get only the uuid
            self.uuid = re.search("[^/]+-[^/]+-[^/]+-[^/]+-[^/]+", url_uuid).group()
            logging.debug("the uuid extracted is : %s", self.uuid)
        except AttributeError:
            logging.critical("Failed to extract uuid skipping.")
            self.uuid = None
            # TODO: if uuid is 'None' execution cannot proceed.
        else:
            self.name = name
            self.desc = None
            self.status = None
            self.langs = None

    def _get_info(self):
        response = ApiAdapter.make_request("get", f"{MANGA_ENDPOINT}/{self.uuid}")
        print(response)

