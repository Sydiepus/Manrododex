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
# iso639-1.tsv from https://id.loc.gov/vocabulary/iso639-1.html
import json

lang = dict()

with open("iso639-1.tsv", "r") as f:
    lines = f.readlines()
    for line in lines:
        line_comp = line.split("\t")
        if len(line_comp[1]) == 2:
            lang.update({line_comp[1]: line_comp[2]})

mangadex_exceptions = {
    "zh": "Simplified Chinese",
    "zh-hk": "Traditional Chinese",
    "pt-br": "Brazilian Portugese",
    "es": "Castilian Spanish",
    "es-la": "Latin American Spanish",
    "ja-ro": "Romanized Japanese",
    "ko-ro": "Romanized Korean",
    "zh-ro": "Romanized Chinese"
}

lang.update(mangadex_exceptions)

with open("mangadex-iso639-1.json", "w") as f:
    f.write(json.dumps(lang))
