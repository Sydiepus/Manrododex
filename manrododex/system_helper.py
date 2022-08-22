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

#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#
#
#
#
#
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
