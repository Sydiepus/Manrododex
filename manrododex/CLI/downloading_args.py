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

# https://github.com/manga-py/manga-py/blob/d89501a0f78d498f85114320d6123f59d328a905/manga_py/cli/_args_downloading.py#L2
import os
import pathlib

from manrododex.mangadex_lang_codes import lang_codes


def check_lang(lang):
    if lang in lang_codes:
        return lang
    else:
        return "en"


def _download_args(args_parser):
    args = args_parser.add_argument_group("Downloading options")
    args.add_argument(
        "-p",
        "--path",
        metavar="PATH",
        type=str,
        default=str(os.path.join(pathlib.Path().resolve().absolute(), "Manga")),
        help=(
            "Destination folder: where the manga will be saved.\n"
            "The path will be './%(metavar)s/manga_name/'\n"
        )
    )
    args.add_argument(
        "-t",
        "--threads",
        type=int,
        metavar="THREADS",
        default=1,
        help=(
            "Sets the number of threads to be used.\n"
            "Aka the number of images to be downloaded in parallel.\n"
            "Please don't use a lot of threads as it might get you banned.\n"
        ),
    )
    args.add_argument(
        "-l",
        "--language",
        type=check_lang,
        metavar="LANG",
        default="en",
        help="Set the language in which the chapters should be downloaded with.\n",
    )
    args.add_argument(
        "-ds",
        "--data-saver",
        action="store_const",
        const="data-saver",
        default="data",
        help=(
            "Switch the quality mode from 'data' to 'data-saver'.\n"
            "'data-saver' will download a compressed image instead of upload quality.\n"
        ),
    )
    args.add_argument(
        "-svc",
        "--sel-vol-chap",
        type=str,
        metavar="SEL_VOL_CHAP",
        default=None,
        help=(
            "Select chapters to be downloaded can be singles separated by ','\n"
            "use 'v{num}v' to mark the number as volume.\n"
            "    '/' to make a range.\n"
            "    ',' to start a new rule.\n"
            "e.g: v7v99 would be volume 7 chapter 99.\n"
            "     v1/3v1 would be chapter 1 from vol 1, 2 and 3.\n"
            "     1,4,6 would download chapter 1, 4 and 6 regardless for the volume.\n"
            "     v6v would download volume 6 entirely.\n"
        ),
    )
    args.add_argument(
        "--alt-title-lang",
        type=check_lang,
        metavar="ALT_TITLE_LANG",
        default=None,
        help="Specify the language in we should get the alternative title.\n"
             "Available alternative titles can be seen to the left of the chapters of the manga on the site.\n",
    )
    args.add_argument(
        "--use-alt-title",
        action="store_true",
        default=False,
        help="Whether or not to use the alternative title of the manga.\n"
             "Aka the one that appears to the side of the chapters on the site.\n"
             "Note: this argument can be used with --alt-title-lang to change the language of the alt title.\n"
             "If this argument is not used the program will get the default title even if"
             "the --alttitle-lang is used.\n",
    )
    args.add_argument(
        "--name",
        type=str,
        metavar="NAME",
        default=None,
        help="Set a custom name for the manga.\n"
             "Note: this argument precedes the both of the --alttitle-lang and --deftitle in importance\n",
    )
    args.add_argument(
        "--force-ssl",
        action="store_true",
        default=False,
        help="Force selecting from MangaDex@Home servers that use the standard HTTPS port 443.\n"
             "from https://api.mangadex.org/swagger.html\n",
    )
    args.add_argument(
        "--zip-format",
        action="store_const",
        const="zip",
        default="cbz",
        help="The use of this argument will switch it to zip.\n"
             "By default the cbz archive format will be used.\n",
    )
