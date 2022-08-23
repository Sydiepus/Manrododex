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

import re

from manrododex.apiadapter import ApiAdapter
from manrododex.manga_helpers import Images
from manrododex.system_helper import path_exits

AT_HOME_SERVER_ENDPOINT = "/at-home/server"


def chapter_archive_name(vol, chap):
    if vol != "none":
        chapter_name = f"vol-{vol}-chapter-{chap}"
    elif chap == "Oneshot":
        chapter_name = chap
    else:
        chapter_name = f"chapter-{chap}"
    return chapter_name


class Downloader:
    """This class is responsible for downloading the manga.
    Parameters :
    -------------
    manga:
        The Manga object to be downloaded.
    quality:
        The quality of the images to be used, data or data-saver.
    threads:
        The number of threads to be used.
    force_ssl:
        Force selecting from MangaDex@Home servers that use the standard HTTPS port 443.
        from https://api.mangadex.org/swagger.html
    """

    def __init__(self, manga, quality, threads, force_ssl):
        self.manga = manga
        self.quality = quality
        self.threads = threads
        self.force_ssl = force_ssl
        self.images = Images()
        self.volume = None
        self.chapter = None

    def build_images_link(self):
        chapter = self.manga.chapters.get()
        self.volume = chapter[0]
        self.chapter = chapter[1]
        info = ApiAdapter.make_request("get",
                                       f"{AT_HOME_SERVER_ENDPOINT}/{chapter[2]}",
                                       passed_params={
                                           "forcePort443": self.force_ssl
                                       })
        base_url = info["baseUrl"]
        chapter_hash = info["chapter"]["hash"]
        images = info["chapter"]["dataSaver"] if self.quality == "data-saver" else info["chapter"]["data"]
        for image in images:
            self.images.put(f"{base_url}/{self.quality}/{chapter_hash}/{image}")

    def download_image(self, sys_helper):
        img_link = self.images.get()
        img_name = re.search("(x?)([0-9]+)(-)", img_link).group(2)
        img_ext = re.search("(-)(.*)(\..*$)", img_link).group(3)
        img_path = sys_helper.forge_img_path(img_name, img_ext)
        if path_exits(img_path):
            return
        img = ApiAdapter.img_download(img_link)
        with open(img_path, "wb") as f:
            f.write(img.content)

    def main(self, sys_helper):
        self.build_images_link()
        chapter_name = chapter_archive_name(self.volume, self.chapter)
        sys_helper.create_chapter_dir(chapter_name)
        del chapter_name
        while not self.images.empty():
            self.download_image(sys_helper)
        sys_helper.archive_chapter()
