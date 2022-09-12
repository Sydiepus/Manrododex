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
import json
import sys

import manrododex.logger as logger
from manrododex.CLI.argparse import initialize_args
from manrododex.main import main, file_main


def print_lang_codes():
    from manrododex.mangadex_lang_codes import lang_codes
    print(json.dumps(lang_codes, indent=4))


def cli_handler():
    parser = initialize_args()
    args = parser.parse_args()
    if args.lang_codes:
        print_lang_codes()
        return
    if not args.dry_run:
        logger.init(args.log_level)
    title_settings = (args.name, args.alt_title_lang, not args.use_alt_title)
    if len(sys.argv) <= 1:
        parser.print_help()
    else:
        if args.File is None:
            main(args.url_uuid, title_settings, args.language, args.sel_vol_chap, args.path, args.data_saver,
                 args.threads,
                 args.force_ssl, args.zip_format, args.dry_run)
        else:
            file_main(args.File, title_settings, args.language, args.sel_vol_chap, args.path, args.data_saver,
                      args.threads,
                      args.force_ssl, args.zip_format, args.dry_run)


if __name__ == "__main__":
    cli_handler()
