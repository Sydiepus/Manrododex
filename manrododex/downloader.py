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
import logging
import re
from threading import Thread

from tqdm import tqdm

from manrododex.apiadapter import ApiAdapter
from manrododex.manga_helpers import Images

AT_HOME_SERVER_ENDPOINT = "/at-home/server"


def _chapter_archive_name(vol, chap):
    if vol != "none":
        chapter_name = f"vol-{vol}-chapter-{chap}"
    elif chap == "Oneshot":
        chapter_name = chap
    else:
        chapter_name = f"chapter-{chap}"
    return chapter_name


def _get_image_name(img_link):
    return re.search("(x?)([0-9]+)(-)", img_link).group(2)


def _get_image_ext(img_link):
    return re.search("(-)(.*)(\..*$)", img_link).group(3)


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

    def __init__(self, chapters, quality, threads, force_ssl, dry_run):
        self.chapters = chapters
        self.quality = quality
        self.threads = threads
        self.force_ssl = force_ssl
        self.dry_run = dry_run
        self.images = Images()
        self.chapter_name = None
        logging.info("Downloader created successfully.")

    def _build_images_link(self, sys_helper):
        chapter = self.chapters.get()
        self.chapter_name = _chapter_archive_name(chapter[0], chapter[1])
        logging.debug("Chapter will be named : %s", self.chapter_name)
        exists = sys_helper.check_if_already_exists(self.chapter_name)
        img_check = None
        if exists == "FolderAndArchive":
            # Check Both and complete the one with the most images.
            dir_list = sys_helper.get_dir_content()
            archive_list = sys_helper.get_archive_content()
            if len(dir_list) >= len(archive_list):
                # if directory contains more images delete the archive.
                # or if they're equal delete the archive the directory is easier to handle.
                logging.info("Chapter Directory contains more stuff than the archive, deleting the archive.")
                del archive_list
                sys_helper.del_archive()
                img_check = dir_list
                del dir_list
                exists = None
            elif len(archive_list) > len(dir_list):
                # if archive contains more delete the directory
                logging.info("Archive contains more stuff than the directory, deleting the directory.")
                del dir_list
                sys_helper.del_dir()
                img_check = archive_list
                del archive_list
                exists = "Archive"
        elif exists == "Folder":
            # Folder already exists download the missing images if any.
            logging.info("Completing what's missing from the directory if any.")
            img_check = sys_helper.get_dir_content()
            exists = None
        elif exists == "Archive":
            # Archive already exists download the missing images if any.
            logging.info("Completing what's missing from the archive if any.")
            img_check = sys_helper.get_archive_content()
        sys_helper.create_chapter_dir(self.chapter_name)
        info = ApiAdapter.make_request("get",
                                       f"{AT_HOME_SERVER_ENDPOINT}/{chapter[2]}",
                                       passed_params={
                                           "forcePort443": self.force_ssl
                                       })
        del chapter
        base_url = info["baseUrl"]
        chapter_hash = info["chapter"]["hash"]
        images = info["chapter"]["dataSaver"] if self.quality == "data-saver" else info["chapter"]["data"]
        del info
        for image in images:
            if img_check:
                if f"{_get_image_name(image)}{_get_image_ext(image)}" in img_check:
                    continue
            self.images.put(f"{base_url}/{self.quality}/{chapter_hash}/{image}")
            logging.debug("Image added successfully.")
        logging.info("All required images for the chapter have been added.")
        return exists

    def _download_image(self, sys_helper, bar, thread_desc):
        img_link = self.images.get()
        img_name = _get_image_name(img_link)
        img_ext = _get_image_ext(img_link)
        bar.set_description(f"{thread_desc} Downloading {img_name}{img_ext}")
        img_path = sys_helper.forge_img_path(img_name, img_ext)
        del img_name, img_ext
        ApiAdapter.img_download(img_link, img_path, bar, self.dry_run)
        del img_link
        self.images.task_done()

    def _download_images(self, sys_helper, thread_number, chapter_bar):
        thread_desc = f"Thread nb {thread_number}"
        bar = tqdm(desc=thread_desc,
                   position=thread_number + 1,
                   unit="iB",
                   unit_scale=True,
                   unit_divisor=1024,
                   leave=False)
        while not self.images.empty():
            self._download_image(sys_helper, bar, thread_desc)
            chapter_bar.update(1)
            bar.reset()

    def main(self, sys_helper, main_bar):
        chapter_bar = tqdm(desc="Downloading chapters.",
                           bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} images",
                           position=1,
                           leave=False)
        while not self.chapters.empty():
            any_to_fix = self._build_images_link(sys_helper)
            total = self.images.qsize()
            chapter_bar.__dict__.update({"total": total,
                                         "desc": f"Downloading {self.chapter_name}"})
            if not self.images.empty():
                for i in range(self.threads):
                    Thread(target=self._download_images, args=(sys_helper, i + 1, chapter_bar)).start()
                self.images.join()
            sys_helper.archive_chapter(any_to_fix)
            chapter_bar.reset()
            main_bar.update(1)
