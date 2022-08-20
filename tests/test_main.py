import pytest

import tests
from manrododex.main import main

uuid_url = tests.uuid_urls
ex_resp = tests.ex_resp_main
param = [(u, v) for u, v in zip(uuid_url, ex_resp)]


@pytest.mark.parametrize("uuid_url_p,ex_resp", param)
def test_main(uuid_url_p, ex_resp):
    maiden = main(uuid_url_p, (None, "en", True), "en", None, "DEBUG")
    assert maiden is ex_resp
