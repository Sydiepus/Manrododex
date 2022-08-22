import re

import pytest

import tests

img_l = tests.img_link
ex_img_name = tests.ex_img_name
param = [(u, v) for u, v in zip(img_l, ex_img_name)]


@pytest.mark.parametrize("img_link,ex_img_n", param)
def test_download_image(img_link, ex_img_n):
    img_name = re.search("(x?)([0-9]+)(-)", img_link).group(2)
    assert img_name == ex_img_n
