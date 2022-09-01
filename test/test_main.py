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

import os
import pathlib

import pytest

import test
from manrododex.main import main

uuid_url = test.uuid_urls
ex_resp = test.ex_resp_main
param = [(u, v) for u, v in zip(uuid_url, ex_resp)]


@pytest.mark.parametrize("uuid_url_p,ex_resp", param)
def test_main(uuid_url_p, ex_resp):
    maiden = main(uuid_url_p(None, None, True), "en", None,
                  str(os.path.join(pathlib.Path().resolve().absolute(), "Manga")), "data-saver", 3, False, "cbz",
                  "DEBUG", False)
    assert maiden is ex_resp
