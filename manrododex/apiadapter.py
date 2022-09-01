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
from time import sleep, time

import requests
from requests import JSONDecodeError
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from manrododex.exceptions import ResultNotOk, RequestDidNotSucceed

API_URL = "https://api.mangadex.org"
REPORT_ENDPOINT_URL = "https://api.mangadex.network/report"


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
                cls.lastu_taimo = cuwuent_taimo
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
            raise RequestDidNotSucceed

    @classmethod
    def img_download(cls, img_link, img_path, bar, dry_run):
        should_report = True if not re.search(".*(\.?mangadex.org).*", img_link) else False
        cls.can_i_mauwku_requesto_senpai()
        logging.debug("Downloading img from link : %s", img_link)
        # https://stackoverflow.com/a/62113293
        if dry_run:
            logging.debug("Dry run not downloading img.")
            return
        req = cls.session.request("get", img_link, stream=True)
        success = req.status_code == 200
        if success:
            logging.debug("Request successful.")
            total = int(req.headers.get('content-length', 0))
            bar.total = total
            with open(img_path, "wb") as f:
                for data in req.iter_content(chunk_size=1024):
                    size = f.write(data)
                    bar.update(size)
        if should_report:
            try:
                cached = True if "HIT" in req.headers["X-Cache"] else False
            except KeyError:
                cached = False
            logging.debug("Reporting request to mangadex.")
            # The time function returns the time in seconds.
            # Mangadex wants it in milliseconds.
            duration = req.elapsed.microseconds
            data = {
                "url": img_link,
                "success": success,
                "cached": cached,
                "bytes": len(req.content),
                "duration": duration
            }
            header = {
                "content-type": "application/json"
            }
            # report
            cls.session.request("post", REPORT_ENDPOINT_URL, params=data, headers=header)
        if not success:
            logging.error("Failed to make request.")
            raise RequestDidNotSucceed
