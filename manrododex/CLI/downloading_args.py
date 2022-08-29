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


def _download_args(args_parser):
    args = args_parser.add_argument_group("Downloading options")
    args.add_argument(
        "-d",
        "--destination",
        metavar="PATH",
        type=str,
        default=str(os.path.join(pathlib.Path().resolve().absolute(), "Manga")),
        help=(
            "Destination folder: where the manga will be saved. "
            "The path will be './%(metavar)s/manga_name/'"
        )
    )
    args.add_argument(
        "-t",
        "--threads",
        type=int,
        metavar="THREADS",
        default=1,
        help=(
            "Sets the number of threads to be used."
            "Aka the number of images to be downloaded in parallel."
            "Please don't use a lot of threads as it might get you banned."
        ),
    )
    args.add_argument(
        "-l",
        "--language",
        type=str,
        metavar="LANG",
        default="en",
        help="Set the language in which the chapters should be downloaded with.",
    )
    args.add_argument(
        "-ds",
        "--quality",
        type=str,
        metavar="QUALITY",
        default="data",
        help=(
            "Change the quality mode from 'data' to 'data-saver'."
            "'data-saver' will download a compressed image instead of upload quality."
        ),
    )
    args.add_argument(
        "-svc",
        "--selvolchap",
        type=str,
        metavar="SELVOLCHAP",
        default=None,
        help=(
            "Select chapters to be downloaded can be singles separated by ','"
            "use 'v{num}v' to mark the number as volume."
            "    '/' to make a range."
            "    ',' to start a new rule."
            "e.g: v7v99 would be volume 7 chapter 99."
            "     v1/3v1 would be chapter 1 from vol 1, 2 and 3."
            "     1,4,6 would download chapter 1, 4 and 6 regardless for the volume."
            "     v6v would download volume 6 entirely."
        ),
    )
    args.add_argument(
        "--alttitle-lang",
        type=str,
        metavar="ALTTLANG",
        default=None,
        help="Specify the language in we should get the alternative title."
             "Available alternative titles can be seen to the left of the chapters of the manga on the site.",
    )
    args.add_argument(
        "--deftitle",
        type=bool,
        metavar="DEFT",
        default=True,
        help="Whether or not to use the default title of the manga."
             "Aka the one that appears on the site/url."
             "Note: this argument precedes the one of the alternative title in importance."
             "By which i mean that if this argument is set to True the program will get the default title even if"
             "the --alttitle-lang is used.",
    )
    args.add_argument(
        "--name",
        type=str,
        metavar="NAME",
        default=None,
        help="Set a custom name for the manga."
             "Note: this argument precedes the both of the --alttitle-lang and --deftitle in importance",
    )
    args.add_argument(
        "--force-ssl",
        type=bool,
        metavar="FSSL",
        default=False,
        help="Force selecting from MangaDex@Home servers that use the standard HTTPS port 443."
             "from https://api.mangadex.org/swagger.html",
    )
    args.add_argument(
        "--archive-format",
        type=str,
        metavar="AFR",
        default="cbz",
        help="The archive extension to use."
             "Can only be cbz or zip.",
    )
