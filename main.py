import os
import json
import argparse
from modules.creeper import creeper

# change path to your steam workshop path
path = "F:/图片/workshop_backup/431960"
fileFolders = os.listdir(path)

# change path to your output path
outputBase = "F:/图片/wallpaper_engine提取"
# output format: outputBase/autherName/title [id=workshopID]

recorder = []
failed = []

# parse arguments in command line
parser = argparse.ArgumentParser()
parser.add_argument("--target", type=str, default=None)
parser.add_argument("--target-file", type=str, default=None)
parser.add_argument("--retry", type=int, default=0)
args = parser.parse_args()

if args.target != None and args.target_file != None:
    print("参数错误，请不要同时传递target和target-file")
    exit()

elif args.target != None:
    fileFolders = [args.target]
    recorder, failed = creeper(path, fileFolders, outputBase, recorder)
    exit()

elif args.target_file != None:
    with open(args.target_file, "r") as f:
        fileFolders = json.load(f)
    recorder, failed = creeper(path, fileFolders, outputBase, recorder)
    exit()
    
elif args.retry > 0:
    with open("./accessories/failed.json", "r") as f:
        failed = json.load(f)
    if len(failed) != 0:
        for i in range(args.retry):
            print("第" + str(i) + "次重试")
            recorder, failed = creeper(path, failed, outputBase, recorder)
    else:
        print("没有失败的文件夹")
    exit()

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