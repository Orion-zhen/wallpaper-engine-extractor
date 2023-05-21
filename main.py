import os
import json
from modules.creeper import creeper

# change path to your steam workshop path
path = "F:/图片/workshop_backup/431960"
fileFolders = os.listdir(path)

# change path to your output path
outputBase = "F:/图片/wallpaper_engine提取"
# output format: outputBase/autherName/title [id=workshopID]

recorder = []
failed = []

# check if history.json exists
# if not, create one
local = os.listdir("./accessories/")
if "history.json" not in local:
    authNames = os.listdir(outputBase)
    for authName in authNames:
        files = os.listdir(outputBase + "/" + authName)
        for file in files:
            recorder.append(file.split("=")[-1][:-1])
    with open("./accessories/history.json", "w") as f:
        json.dump(recorder, f)

with open("./accessories/history.json", "r") as f:
    recorder = json.load(f)

# start crawling  
recorder, failed = creeper(path, fileFolders, outputBase, recorder)

if len(failed) != 0:
    print("重试中...")
    for i in range(4):
        recorder, failed = creeper(path, failed, outputBase, recorder)
        if len(failed) == 0:
            break

with open("./accessories/history.json", "w") as f:
    json.dump(recorder, f)

with open("./accessories/failed.json", "w") as f:
    json.dump(failed, f)