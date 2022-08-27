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


def _download_args(args_parser):
    args = args_parser.add_argument_group("Downloading options")
    args.add_argument(
        "-t",
        "--max-threads",
        type=int,
        metavar="thread",
        default=1,
        help=(
            "Sets the number of threads to be used."
            "Or the number of images to download in parallel."
        ),
    )
    args.add_argument(
        "-l",
        "--language",
        type=str,
        metavar="lang",
        default="en",
        help="Set the language in which the chapters should be downloaded.",
    )
    args.add_argument(
        "-ds",
        "--quality-mode",
        type=str,
        metavar="quality_mode",
        default="data",
        help=(
            "change the quality mode from 'data' to 'data-saver'."
            "'data-saver' will download a compressed image instead of upload quality."
        ),
    )
    args.add_argument(
        "--name",
        type=str,
        metavar="name",
        default=None,
        help="set a custom manga name for the folder and everything else.",
    )
    args.add_argument(
        "-sc",
        "--selchap",
        type=str,
        metavar="selchap",
        default=None,
        help=(
            "Select chapters to be downloaded can be singles separated by ','"
            "use 'v{num}v' to mark the number as volume."
            "    '/' to make a range."
            "    ',' to start a new rule."
            "e.g: v7v99 would be volume 7 chapter 99."
            "     v1/3v1 would be chapter 1 from vol 1, 2 and 3."
            "     1,4,6 would download chapter 1, 4 and 6 regardless for the volume."
            "     v6v would download volume 6 entirely. 8 9"
        ),
    )
