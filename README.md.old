<h1 align="center">Manrododex</br>
<sup><sup>マンロードデクス</sup></sup></h1>

### A manga downloader for mangadex using their [API](https://api.mangadex.org/docs/)
![](https://img.shields.io/github/license/Sydiepus/Manrododex)
![](https://img.shields.io/github/issues/Sydiepus/Manrododex)
![](https://img.shields.io/pypi/pyversions/manrododex)
![GitHub Workflow Status](https://github.com/Sydiepus/Manrododex/actions/workflows/CI.yml/badge.svg)
![PyPI](https://img.shields.io/pypi/v/manrododex)
[![Documentation Status](https://readthedocs.org/projects/manrododex/badge/?version=latest)](https://manrododex.readthedocs.io/en/latest/?badge=latest)
## Features

- Threads support for faster downloads.
- Uses queue for safe threading and better memory usage.
- Creates a series.json file like mylar. (
  see [here](https://komga.org/guides/scan-analysis-refresh.html#import-metadata-generated-by-mylar)
  and [here](https://github.com/mylar3/mylar3/wiki/series.json-examples))
- Can be used to automate the download of manga in combination with crontabs/Scheduled Tasks.
- Manrododex makes it possible to download multiple manga with little to user interaction.
- A possibly wrong Japanese translation of the name.
- Bugs

## Inspiration

I might have stolen some ideas from these awesome projects.

- [manga-py](https://github.com/manga-py/manga-py)
- [mangadex-dl](https://github.com/frozenpandaman/mangadex-dl)
- [MangaDex.py](https://github.com/Proxymiity/MangaDex.py)
- [Qtile](https://github.com/qtile/qtile)

## Maintainer

[@Sydiepus](https://github.com/Sydiepus) GPG: ```BD1D 09DF 8A49 E7A6 C705 3B8A 7D6C DB7E 575A C12A```

## Note:

- I'll be taking a break for some time and might not be able to properly test or fix the program.
- Not tested on Windows yet.
- wiki coming soon.

## Simple Instructions

- Install with ```pip install manrododex```
- Download manga
  with ```manrododex https://mangadex.org/title/b98c4daf-be1a-46c8-ad83-21d532995240/my-food-looks-very-cute```
- You don't have to use the full link```b98c4daf-be1a-46c8-ad83-21d532995240``` would work too.
- You can supplement a file with ```-F``` e.g: ```manrododex -F manga.txt```
- The file should be of this format: ```url/uuid, custom manga name, the language```
- For example this is a valid file:

```
https://mangadex.org/title/e1d0056a-fdd3-4f32-af19-50eeb37280ac/new-normal,,
https://mangadex.org/title/9643f5da-c7da-4705-ac5b-4b4a4c7a649e/gleipnir,, tr
https://mangadex.org/title/259dfd8a-f06a-4825-8fa6-a2dcd7274230/yofukashi-no-uta, call of the night,
https://mangadex.org/title/aa6c76f7-5f5f-46b6-a800-911145f81b9b/sono-bisque-doll-wa-koi-wo-suru, Cosplay doll, br
```

- For more options check ```manrododex --help```
