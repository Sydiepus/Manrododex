|logo|

**A manga downloader for mangadex using their** `API <https://api.mangadex.org/docs/>`_

|license| |issues| |pyversions| |CI| |PyPI| |rtfd|

Features
========

- Threads support for faster downloads.
- Uses queue for safe threading and better memory usage.
- Creates a series.json file like mylar. (
  see `Komga <https://komga.org/guides/scan-analysis-refresh.html#import-metadata-generated-by-mylar>`_
  and `mylar3 <https://github.com/mylar3/mylar3/wiki/series.json-examples>`_ )
- Can be used to automate the download of manga in combination with crontabs/Scheduled Tasks.
- Manrododex makes it possible to download multiple manga with little to user interaction.
- A possibly wrong Japanese translation of the name.
- Bugs

Inspiration
===========

I might have stolen some ideas from these awesome projects.

- `manga-py <https://github.com/manga-py/manga-py>`_
- `mangadex-dl <https://github.com/frozenpandaman/mangadex-dl>`_
- `MangaDex.py <https://github.com/Proxymiity/MangaDex.py>`_
- `Qtile <https://github.com/qtile/qtile>`_

Maintainer
==========

`@Sydiepus <https://github.com/Sydiepus>`_ GPG: ``BD1D 09DF 8A49 E7A6 C705 3B8A 7D6C DB7E 575A C12A``

.. |logo| image:: ./logo.gif
    :target: https://manrododex.readthedocs.io/en/latest/
.. |license| image:: https://img.shields.io/github/license/Sydiepus/Manrododex.svg
    :target: https://github.com/Sydiepus/Manrododex/blob/main/LICENSE
.. |issues| image:: https://img.shields.io/github/issues/Sydiepus/Manrododex.svg
    :target: https://github.com/Sydiepus/Manrododex/issues
.. |pyversions| image:: https://img.shields.io/pypi/pyversions/manrododex.svg
    :target: https://pypi.org/project/manrododex/
.. |CI| image:: https://github.com/Sydiepus/Manrododex/actions/workflows/CI.yml/badge.svg
    :target: https://github.com/Sydiepus/Manrododex/actions
.. |PyPI| image:: https://img.shields.io/pypi/v/manrododex.svg
    :target: https://pypi.org/project/manrododex/
.. |rtfd| image:: https://readthedocs.org/projects/manrododex/badge/?version=latest
    :target: https://manrododex.readthedocs.io/en/latest/?badge=latest
