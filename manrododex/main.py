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
import pathlib

from tqdm import tqdm

from manrododex.downloader import Downloader
from manrododex.exceptions import NoneUUID, LangNotAvail, RequestDidNotSucceed
from manrododex.manga import Manga
from manrododex.system_helper import SysHelper


def main(url_uuid: str, title_settings: tuple, lang: str, selected_vol_chap: str, main_path: pathlib.Path, quality: str,
         threads: int, force_ssl: bool, archive_format: str,
         dry_run: bool) -> int:
    """A comment to keep track of the parameters.

    Parameters:
    ------------
    url_uuid:
        default: No Default.
    title_settings
        default: (None, None, True)
    lang:
        default: 'en'
    selected_vol_chap:
        default: None
    main_path:
        default: current working dir + 'Manga'
    quality:
        default: data
        other option(s): data-saver
    threads:
        default: 1
    force_ssl:
        default: False
        other option(s): True
    archive_format:
        default: cbz
        other option(s): zip
    dry_run:
        default: False
    """
    try:
        main_bar = tqdm(desc="Starting Manga Download",
                        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} chapters",
                        position=0,
                        leave=False)
        manga = Manga(url_uuid, lang)
        main_bar.desc = f"Getting info on {manga.uuid} with language {manga.lang}"
        main_bar.refresh()
        del url_uuid, lang
        # Make the request to get basic info about the manga.
        manga.get_info(title_settings)
        main_bar.desc = f"Downloading : {manga.info['name']}"
        main_bar.refresh()
        del title_settings
        # Make the requests to get the available chapters.
        manga.get_chapters(selected_vol_chap)
        main_bar.total = manga.chapters.qsize()
        main_bar.desc = f"Downloading {manga.info['name']} chapters"
        main_bar.refresh()
        del selected_vol_chap
        # It's now time to download the manga.
        sys_helper = SysHelper(main_path, manga.info["name"], archive_format, dry_run)
        del main_path, archive_format
        # First create the main manga directory where the manga need to be put.
        sys_helper.create_main_manga_dir()
        # Then we create the directory for the manga that have the manga title as name.
        sys_helper.create_manga_dir()
        # Create the series.json
        sys_helper.write_series_json(manga.info)
        del manga.info
        # We can now start downloading.
        downloader = Downloader(manga.chapters, quality, threads, force_ssl, dry_run)
        del manga, quality, threads, force_ssl
        downloader.main(sys_helper, main_bar)
    except (NoneUUID, LangNotAvail, RequestDidNotSucceed):
        return 1

    return 0


def file_main(file, title_settings, lang, selected_vol_chap, main_path, quality, threads, force_ssl, archive_format,
              dry_run):
    """The file should contain at most three things the first being mandatory:
     url/uuid
     custom manga name
     the language"""
    with open(file, "r") as f:
        lines = f.readlines()
        for line in lines:
            line_comp = list(map(lambda x: str(x.strip().strip(" ")), line.strip().split(",")))
            uuid_url = line_comp[0]
            manga_name = line_comp[1]
            language = line_comp[2] if len(line_comp[2]) == 2 or len(line_comp[2]) == 5 else lang
            if len(line_comp) == 3:
                main(uuid_url, (manga_name, None, False), language, selected_vol_chap, main_path, quality,
                     threads, force_ssl, archive_format, dry_run)
            elif len(line_comp) == 2:
                main(uuid_url, (manga_name, None, False), lang, selected_vol_chap, main_path, quality, threads,
                     force_ssl, archive_format, dry_run)
            elif len(line_comp) == 1:
                main(uuid_url, title_settings, lang, selected_vol_chap, main_path, quality, threads, force_ssl,
                     archive_format, dry_run)
