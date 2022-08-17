# https://stackoverflow.com/a/32773402
import pycountry

"""Use this to check if the right lang code was used before staring to get the info, ..."""
langs = [lang.iso639_1_code
         for lang in pycountry.languages
         if hasattr(lang, 'iso639_1_code')]
