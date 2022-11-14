import json
import os
import requests

CURSEFORGE_API = "https://api.curseforge.com/v1/mods/"
MODRINTH_API = "https://api.modrinth.com/v2/project/"
CF_HEADER = {
    "Accept": "application/json",
    "x-api-key": os.getenv("CF_CORE_KEY"),
}
MODRINTH_HEADER = {
    "Accept": "application/json",
    "User-Agent": "UltrusBot/DownloadCounter/1.0.0",
}

with open("ultrusbot.json", "r") as f:
    data = json.load(f)
modDownloads = {}
total = 0
for mod in data:
    modDownloads[mod] = 0
    for id in data[mod]:
        if id.isnumeric():
            resp = requests.get(CURSEFORGE_API + id, headers=CF_HEADER)
            if resp.status_code == 200:
                modDownloads[mod] += resp.json()["data"]["downloadCount"]
                total += resp.json()["data"]["downloadCount"]
        else:
            resp = requests.get(MODRINTH_API + id, headers=MODRINTH_HEADER)
            if resp.status_code == 200:
                modDownloads[mod] += resp.json()["downloads"]
                total += resp.json()["downloads"]

with open("out/ultrusbot.json", "w") as f:
    json.dump(modDownloads, f)
