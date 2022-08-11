import re
import logging
import manrododex.http as http


API_URL = "https://api.mangadex.org/manga"

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
        except AttributeError:
            self.uuid = None
            # TODO: if uuid is 'None' execution cannot proceed.
        else:
            self.name = name
            self.desc = None
            self.status = None
            self.langs = None

    def _get_info(self):
        request = http.get(f"{API_URL}/{self.uuid}")

