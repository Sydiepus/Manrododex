from manrododex.apiadapter import ApiAdapter
from manrododex.manga_helpers import Images

AT_HOME_SERVER_ENDPOINT = "/at-home/server"


class Downloader:
    """This class is responsible for downloading the manga.
    Parameters :
    -------------
    manga:
        The Manga object to be downloaded.
    quality:
        The quality of the images to be used, data or data-saver.
    threads:
        The number of threads to be used.
    force_ssl:
        Force selecting from MangaDex@Home servers that use the standard HTTPS port 443.
        from https://api.mangadex.org/swagger.html
    """

    def __init__(self, manga, quality, threads, force_ssl):
        self.manga = manga
        self.quality = quality
        self.threads = threads
        self.force_ssl = force_ssl
        self.images = Images()
        self.volume = None
        self.chapter = None

    def build_images_link(self):
        chapter = self.manga.chapters.get()
        self.volume = chapter[0]
        self.chapter = chapter[1]
        info = ApiAdapter.make_request("get",
                                       f"{AT_HOME_SERVER_ENDPOINT}/f{chapter[-1]}",
                                       passed_params={
                                           "forcePort443": f"{self.force_ssl}"
                                       })
        base_url = info["baseUrl"]
        chapter_hash = info["chapter"]["hash"]
        images = info["chapter"]["dataSaver"] if self.quality == "data-saver" else info["chapter"]["data"]
        for image in images:
            self.images.put(f"{base_url}/{self.quality}/{chapter_hash}/{image}")
