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

from argparse import ArgumentParser, RawTextHelpFormatter

from .downloading_args import _download_args
from .general_args import _gen_args
from .required_args import _required_args


def initialize_args() -> ArgumentParser:
    args_parser = ArgumentParser(
        description=(
            "%(prog)s is a manga downloader for Mangadex using their api.\n"
            "Source-code: https://github.com/Sydiepus/Manrododex\n"
        ),
        formatter_class=RawTextHelpFormatter
    )
    _required_args(args_parser)
    _gen_args(args_parser)
    _download_args(args_parser)
    return args_parser
