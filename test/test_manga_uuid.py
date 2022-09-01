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

import pytest

import test
from manrododex.exceptions import NoneUUID
from manrododex.manga import Manga

uuid_url = test.uuid_urls
ex_uuid_url = test.ex_uuid_urls
param = [(u, ex_u) for u, ex_u in zip(uuid_url, ex_uuid_url)]


@pytest.mark.parametrize("uuid_url_p,ex_uuid_url_p", param)
def test_manga(uuid_url_p, ex_uuid_url_p):
    with pytest.raises(NoneUUID):
        manga = Manga(uuid_url_p, "en")
        assert manga.uuid == ex_uuid_url_p
        raise NoneUUID
