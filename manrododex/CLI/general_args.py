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

import os
from tempfile import gettempdir

# https://github.com/qtile/qtile/blob/master/libqtile/scripts/main.py
try:
    # Python>3.7 can get the version from importlib
    from importlib.metadata import distribution

    VERSION = distribution("manrododex").version
except ModuleNotFoundError:
    try:
        # pkg_resources is required for 3.7
        import pkg_resources

        VERSION = pkg_resources.require("manrododex")[0].version
    except (pkg_resources.DistributionNotFound, ModuleNotFoundError):
        VERSION = "dev"


def check_logger(log):
    if log.upper() in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        return log.upper()
    else:
        return "INFO"


# https://github.com/manga-py/manga-py/blob/d89501a0f78d498f85114320d6123f59d328a905/manga_py/cli/_args_general.py#L4
def _gen_args(args_parser):
    args = args_parser.add_argument_group("General options")
    args.add_argument(
        "--version",
        action="version",
        version=VERSION,
        help=(
            "Shows %(prog)s's version and exit.\n"
        )
    )
    args.add_argument(
        "--log-level",
        type=check_logger,
        metavar="LOGLVL",
        default="INFO",
        help="Set the log level.\n"
             f"Default log file location {os.path.join(gettempdir(), 'manrododex.log')}\n"
             "possible values : 'DEBUG' 'INFO' 'WARNING' 'ERROR' 'CRITICAL'\n",
    )
    args.add_argument(
        "--lang-codes",
        action="store_true",
        default=False,
        help=(
            "Prints the available language codes and exit.\n"
        )
    )
    args.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help=(
            "Run the program without creating/saving anything.\n"
        )
    )
