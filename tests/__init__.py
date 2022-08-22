from manrododex.exceptions import NoneUUID

uuid_urls = ("https://mangadex.org/title/66d82067-2117-4124-b54b-89b19c8bde45/the-idolm-ster-cinderella-girls-mizu-no"
             "-naka-no-tsubomi-doujinshi", "b98c4daf-be1a-46c8-ad83-21d532995240", "dasd")
ex_uuid_urls = ("66d82067-2117-4124-b54b-89b19c8bde45", "b98c4daf-be1a-46c8-ad83-21d532995240", NoneUUID)

ex_resp_main = (0, 0, 1)

gen = ("v7v99", "v1/3v1", "1,4,6", "v6v", "ffg", "v6/v")
ex_gen = ((["7"], ["99"]), (["1", "2", "3"], ["1"]), ([None], ["1", "4", "6"]), (["6"], [None]), ([None], [None]))

img_link = (
"https://uploads.mangadex.org/data/3303dd03ac8d27452cce3f2a882e94b2/1-f7a76de10d346de7ba01786762ebbedc666b412ad0d4b73baa330a2a392dbcdd.png",
"https://uploads.mangadex.org/data-saver/3303dd03ac8d27452cce3f2a882e94b2/1-27e7476475e60ad4cc4cefdb9b2dce29d84f490e145211f6b2e14b13bdb57f33.jpg",
"https://uploads.mangadex.org/data-saver/e54e950ab0b830ff3036d2be72574c1e/26-36abab0bf677ff1b977e3a14dbdda37acf69ebcb0b4efe3979574edafe1a455d.jpg",
"x1-b765e86d5ecbc932cf3f517a8604f6ac6d8a7f379b0277a117dc7c09c53d041e.png",
"x18-41d36bffc607b627590bed2ce328b5dd87301bfc54fac25a96bec19160039c2e.jpg")
ex_img_name = ("1", "1", "26", "1", "18")
ex_img_exte = (".png", ".jpg", ".jpg", ".png", ".jpg")
