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
import sys

import manrododex.logger as logger
from manrododex.CLI.argparse import initialize_args
from manrododex.main import main, file_main


def cli_handler():
    parser = initialize_args()
    args = parser.parse_args()
    logger.init(args.log_level.upper())
    title_settings = (args.name, args.alttitle_lang, args.deftitle)
    if len(sys.argv) <= 1:
        parser.print_help()
    else:
        if args.File is None:
            main(args.url_uuid, title_settings, args.language, args.selvolchap, args.destination, args.quality,
                 args.threads,
                 args.force_ssl, args.archive_format)
        else:
            file_main(args.File, title_settings, args.language, args.selvolchap, args.destination, args.quality,
                      args.threads,
                      args.force_ssl, args.archive_format)


if __name__ == "__main__":
    cli_handler()
