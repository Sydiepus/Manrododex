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

# https://stackoverflow.com/a/11155124

def _required_args(args_parser):
    args = args_parser.add_mutually_exclusive_group()
    args.add_argument(
        "url/uuid",
        metavar="URL_UUID",
        type=str,
        nargs="?",
        help=(
            "%(metavar)s, i.e. link or uuid of the manga to be downloaded."
        )
    )
    args.add_argument(
        "-F",
        "--File",
        metavar="FILE",
        default=None,
        type=str,
        nargs="?",
        help=(
            "%(metavar)s, i.e. folder containing the links or uuids of the mangas to be downloaded."
        )
    )
