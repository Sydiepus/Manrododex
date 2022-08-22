import re

import pytest

import tests

img_l = tests.img_link
ex_img_exte = tests.ex_img_exte
param = [(u, v) for u, v in zip(img_l, ex_img_exte)]


@pytest.mark.parametrize("img_link,ex_img_ext", param)
def test_download_image(img_link, ex_img_ext):
    img_ext = re.search("(-)(.*)(\..*$)", img_link).group(3)
    assert img_ext == ex_img_ext
