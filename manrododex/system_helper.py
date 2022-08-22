from os import path, makedirs


class SysHelper:
    def __init__(self, main_path, manga_title):
        self.main_path = main_path
        self.manga_path = path.join(self.main_path, manga_title)
        self.chapter_path = None

    def create_main_manga_dir(self):
        if not path.exists(self.main_path):
            makedirs(self.main_path)

    def create_manga_dir(self):
        if not path.exists(self.manga_path):
            makedirs(self.manga_path)

    def create_chapter_dir(self, chapter_name):
        self.chapter_path = path.join(self.manga_path, chapter_name)
        if not path.exists(self.chapter_path):
            makedirs(self.chapter_path)

    def forge_img_path(self, img_name, img_ext):
        return path.join(self.chapter_path, f"{img_name}{img_ext}")
