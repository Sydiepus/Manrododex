from manrododex.manga import Manga
import pytest
import tests


uuid_url = tests.uuid_urls
ex_uuid_url = tests.ex_uuid_urls
param = [(u, ex_u) for u, ex_u in zip(uuid_url, ex_uuid_url)]


@pytest.mark.parametrize("uuid_url_p,ex_uuid_url_p", param)
def test_manga(uuid_url_p, ex_uuid_url_p):
    manga = Manga(uuid_url_p, None)
    assert manga.uuid == ex_uuid_url_p
