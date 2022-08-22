import logging
from time import sleep, time

import requests
from requests import JSONDecodeError
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from manrododex.exceptions import ResultNotOk

API_URL = "https://api.mangadex.org"


class ApiAdapter:
    """Class to make the requests better ?
    well I'm lying here, I just want to objectify everything.
    """
    session = requests.session()
    retries = Retry(total=5,
                    backoff_factor=0.25,
                    status_forcelist=[500, 502, 503, 504])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    lastu_taimo = None

    @classmethod
    def can_i_mauwku_requesto_senpai(cls):
        cuwuent_taimo = time()
        if cls.lastu_taimo:
            deuwuta = cuwuent_taimo - cls.lastu_taimo
            logging.debug("Time since last request '%s'", str(deuwuta))
            if deuwuta >= 0.2:
                return
            else:
                suweep_fuwu = 0.2 - deuwuta
                logging.debug("Waiting '%s'", str(suweep_fuwu))
                sleep(suweep_fuwu)
                cls.lastu_taimo = cuwuent_taimo
                return
        else:
            cls.lastu_taimo = cuwuent_taimo
            return

    # future me : Class methods are different -- they are called by a class, which is passed to the cls parameter of
    # the method. (Sololearn)
    @classmethod
    def make_request(cls, method, endpoint, passed_params=None, passed_headers=None):
        cls.can_i_mauwku_requesto_senpai()
        req = cls.session.request(method, f"{API_URL}{endpoint}", params=passed_params, headers=passed_headers)
        if req.status_code == 200:
            logging.debug("Request successful.")
            try:
                if req.json().get("result") == "ok":
                    return req.json()
                else:
                    raise ResultNotOk("Received response is invalid.")
            except JSONDecodeError:
                logging.error("Failed to decode json.")
                return None
        else:
            logging.error("Failed to make request.")
            return None
