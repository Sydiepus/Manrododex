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
import json
import logging
from os import path, makedirs, listdir, remove
from shutil import rmtree
from zipfile import ZipFile


def path_exits(given_path):
    return path.exists(given_path)


class SysHelper:
    def __init__(self, main_path, manga_title, archive_format, dry_run):
        self.main_path = main_path
        self.manga_path = path.join(self.main_path, manga_title)
        self.chapter_path = None
        self.archive_format = archive_format
        self.archive_path = None
        self.dry_run = dry_run
        logging.info("SysHelper created with no errors.")

    def create_main_manga_dir(self):
        if self.dry_run:
            logging.debug("Dry run not creating directory.")
            return
        logging.debug("Creating main manga directory at %s", self.main_path)
        if not path.exists(self.main_path):
            makedirs(self.main_path)
        logging.debug("Directory already exists, not creating.")

    def create_manga_dir(self):
        if self.dry_run:
            logging.debug("Dry run not creating directory.")
            return
        logging.debug("Creating main manga directory at %s", self.manga_path)
        if not path.exists(self.manga_path):
            makedirs(self.manga_path)
        logging.debug("Directory already exists, not creating.")

    def create_chapter_dir(self, chapter_name):
        self.chapter_path = path.join(self.manga_path, chapter_name)
        if self.dry_run:
            logging.debug("Dry run not creating directory.")
            return
        logging.debug("Creating main manga directory at %s", self.chapter_path)
        if not path.exists(self.chapter_path):
            makedirs(self.chapter_path)
        logging.debug("Directory already exists, not creating.")

    def forge_img_path(self, img_name, img_ext):
        return path.join(self.chapter_path, f"{img_name}{img_ext}")

    # noinspection PyTypeChecker
    def archive_chapter(self, any_to_fix):
        if self.dry_run:
            logging.debug("Dry run not archiving chapter.")
            return
        if not any_to_fix:
            logging.debug("Archiving directory.")
            archive_mode = "w"
        else:
            # append images to zip.
            logging.debug("Appending images to already existing archive.")
            archive_mode = "a"
        with ZipFile(self.archive_path, mode=archive_mode) as f:
            dir_list = self.get_dir_content()
            for file in dir_list:
                file_path = path.join(self.chapter_path, file)
                logging.debug("Adding file %s", file_path)
                f.write(file_path, path.basename(file_path))
        logging.info("All images added to archive successfully.")
        self.del_dir()

    def check_if_already_exists(self, chapter_name):
        self.chapter_path = path.join(self.manga_path, chapter_name)
        self.archive_path = self.chapter_path + f".{self.archive_format}"
        if self.dry_run:
            logging.debug("Dry run not checking if it already exits.")
            return
        if path.exists(self.chapter_path) and path.exists(self.archive_path):
            logging.info("Folder and Archive already exists !!")
            return "FolderAndArchive"
        elif path.exists(self.chapter_path):
            logging.info("Folder already exists !!")
            return "Folder"
        elif path.exists(self.archive_path):
            logging.info("Archive already exists !!")
            return "Archive"
        else:
            return None

    def get_dir_content(self):
        if self.dry_run:
            logging.debug("Dry run not getting content.")
            return
        return listdir(self.chapter_path)

    def get_archive_content(self):
        if self.dry_run:
            logging.debug("Dry run not getting archive content.")
            return
        with ZipFile(self.archive_path, "r") as f:
            zip_content = f.namelist()
            return zip_content

    def del_archive(self):
        if self.dry_run:
            logging.debug("Dry run not deleting archive.")
            return
        logging.debug("Deleting Archive : %s", self.archive_path)
        remove(self.archive_path)

    def del_dir(self):
        if self.dry_run:
            logging.debug("Dry run not deleting directory.")
            return
        logging.debug("Deleting directory and all it's content : %s", self.chapter_path)
        rmtree(self.chapter_path)

    def write_series_json(self, info):
        if self.dry_run:
            logging.debug("Dry run not writing series.json.")
            return
        series_json = path.join(self.manga_path, "series.json")
        if path.exists(series_json):
            logging.debug("series.json already exists skipping.")
            return
        # format from https://github.com/mylar3/mylar3/wiki/series.json-examples
        data = {
            "metadata": info
        }
        with open(series_json, "w") as s:
            s.write(json.dumps(data, indent=4))
        logging.info("series.json has been written.")
