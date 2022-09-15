Using a file to download
========================

| A file can be used to download manga with ``manrododex -F file``
| The file should contain one entry per line, the syntax is as follows :

::

    the url or uuid, a custom name, language


- the ``custom name`` and ``language`` can be omitted, however to change the language without changing the name you still have to add 2 commas, one for the name and another for the language.
- example of a file:

::

    e1d0056a-fdd3-4f32-af19-50eeb37280ac
    https://mangadex.org/title/9643f5da-c7da-4705-ac5b-4b4a4c7a649e/gleipnir
    https://mangadex.org/title/259dfd8a-f06a-4825-8fa6-a2dcd7274230/yofukashi-no-uta, call of the night,
    https://mangadex.org/title/aa6c76f7-5f5f-46b6-a800-911145f81b9b/sono-bisque-doll-wa-koi-wo-suru, Cosplay doll, br
    https://mangadex.org/title/267db3f7-fd9c-4395-ac36-9ffacd772473/star-martial-god-technique,,
    3f28c47a-bf8d-4e79-83ca-2e64fe906372,,jp

- When no language is given english is going to be used.
- When no custom name is given the default title (the one that appears on the site) will be used unless specified otherwise with the ``--use-alt-title``

