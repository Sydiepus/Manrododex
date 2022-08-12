import pytest

import tests
from manrododex.main import main

uuid_url = tests.uuid_urls


@pytest.mark.parametrize("uuid_url_p", uuid_url)
def test_main(uuid_url_p):
    maiden = main(uuid_url_p, None, None)
    assert maiden is None
