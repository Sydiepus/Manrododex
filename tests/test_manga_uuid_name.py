from manrododex.manga import Manga
import pytest


uuid_url = ("https://mangadex.org/title/66d82067-2117-4124-b54b-89b19c8bde45/the-idolm-ster-cinderella-girls-mizu-no-naka-no-tsubomi-doujinshi", "b98c4daf-be1a-46c8-ad83-21d532995240", "dasd")
ex_uuid_url = ("66d82067-2117-4124-b54b-89b19c8bde45", "b98c4daf-be1a-46c8-ad83-21d532995240", None)
param = [(u, ex_u) for u, ex_u in zip(uuid_url, ex_uuid_url)]


@pytest.mark.parametrize("uuid_url_p,ex_uuid_url_p", param)
def test_manga(uuid_url_p, ex_uuid_url_p):
    manga = Manga(uuid_url_p, None)
    assert manga.uuid == ex_uuid_url_p
