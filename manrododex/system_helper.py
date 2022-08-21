from os import path, makedirs


class SysHelper:
    def __init__(self, main_path, manga_title):
        self.main_path = main_path
        self.manga_path = path.join(self.main_path, manga_title)

    def create_main_manga_dir(self):
        if not path.exists(self.main_path):
            makedirs(self.main_path)

    def create_manga_dir(self):
        if not path.exists(self.manga_path):
            makedirs(self.manga_path)

    def create_chapter_dir(self, chapter_name):
        chapter_path = path.join(self.manga_path, chapter_name)
        if not path.exists(chapter_path):
            makedirs(chapter_path)
