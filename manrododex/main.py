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

import manrododex.logger as logger
from manrododex.downloader import Downloader
from manrododex.exceptions import NoneUUID, LangNotAvail, RequestDidNotSucceed
from manrododex.manga import Manga
from manrododex.system_helper import SysHelper


def main(url_uuid, title_settings, lang, selected_vol_chap, main_path, quality, threads, force_ssl, archive_format,
         log_level):
    """A comment to keep track of the parameters.
    Parameters:
    ------------
    url_uuid:
        type: str
        default: No Default.
    title_settings:
        type: tuple
        default: (None, None, True)
    lang:
        type: str
        default: 'en'
    selected_vol_chap:
        type: str
        default: None
    main_path:
        type: str/path
        default: current working dir + 'Manga'
    quality:
        type: str
        default: data
        other option(s): data-saver
    threads:
        type: int
        default: 1
    force_ssl:
        type: bool
        default False
        other option(s): True
    archive_format:
        type: str
        default: cbz
        other option(s): zip
    log_level:
        type: str
        default: INFO
    """
    logger.init(log_level)
    del log_level
    try:
        manga = Manga(url_uuid, lang)
        del url_uuid, lang
        # Make the request to get basic info about the manga.
        manga.get_info(title_settings)
        del title_settings
        # Make the requests to get the available chapters.
        manga.get_chapters(selected_vol_chap)
        del selected_vol_chap
        # It's now time to download the manga.
        sys_helper = SysHelper(main_path, manga.info["title"], archive_format)
        del main_path, archive_format
        # First create the main manga directory where the manga need to be put.
        sys_helper.create_main_manga_dir()
        # Then we create the directory for the manga that have the manga title as name.
        sys_helper.create_manga_dir()
        # We can now start downloading.
        downloader = Downloader(manga.chapters, quality, threads, force_ssl)
        del manga, quality, threads, force_ssl
        downloader.main(sys_helper)
    except (NoneUUID, LangNotAvail, RequestDidNotSucceed):
        return 1

    return 0
