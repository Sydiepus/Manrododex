import re


def get_uuid(url_uuid):
    print(url_uuid)
    print(re.search("[^/]+-[^/]+-[^/]+-[^/]+-[^/]+", url_uuid).group())
    if "mangadex" in url_uuid:
        for i in url_uuid.split("/"):
            uuid = re.findall(".+-.+-.+-.+", i)
            if len(uuid) == 1:
                uuid = uuid[0]
            else:
                uuid = None
    else:
        uuid = re.findall(".+-.+-.+-.+", url_uuid)
        if len(uuid) == 1:
            uuid = uuid[0]
        else:
            uuid = None
    return uuid


get_uuid("66d82067-2117-4124-b54b89b19c8bde45")