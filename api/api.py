import requests
import json

BASE_API: str = "https://rdb.altlinux.org/api/"

class Ftbfs:
    def __init__(self, json):
        self.branch = json["branch"]
        self.hash = json["hash"]
        self.name = json["name"]
        self.epoch = json["epoch"]
        self.version = json["version"]
        self.release = json["release"]
        self.arch = json["arch"]
        self.updated = json["updated"]
        self.ftbfs_since = json["ftbfs_since"]
        self.url = json["url"]

# sdjfksalfjlskadfsjlkdj
def get_ftbfs(repo: str) -> list[Ftbfs]:
    res = requests.get(BASE_API + "/export/beehive/ftbfs?branch=" + repo)
    resobj = json.loads(res.content)
    return [Ftbfs(el) for el in resobj["ftbfs"]]

def get_log(url: str) -> str:
    res = requests.get(url)
    return res.content.decode("utf-8")
