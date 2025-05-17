import requests
import json

from modules import Configuration

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

def get_ftbfs(repo: str, arch: str) -> list[Ftbfs]:
    res = requests.get(BASE_API + "/export/beehive/ftbfs?branch=" + repo + "&arch=" + arch)
    if (res.status_code != 200):
        print(f"[ERROR]: Failed ftbfs request. {res.text}")
        exit(1)

    resobj = json.loads(res.content)
    return [Ftbfs(el) for el in resobj["ftbfs"]]
