from bs4 import BeautifulSoup
import requests
import time
from modules.suppoter import processor
from modules.suppoter import fail

# Note: file path should be either enclosed by double quotes or no spaces

batch = 50

# change to your repkg path
# either ABSOLUTE path or an executable file in the same directory
repkgPath = "RePKG.exe"
    
def creeper(path, fileFolders, outputBase, recorder):
    
    baseURL = "https://steamcommunity.com/sharedfiles/filedetails/?id="
    baseCommand = repkgPath + " " + "extract" + " " + '"' + path
    
    failed = []
    
    nums = len(fileFolders)
    i = 0

    for file in fileFolders:
        print("-----------------------------------")
        print("正在爬取第" + str(i) + "个文件夹，共" + str(nums) + "个文件夹")
        print("文件夹名：" + file)
        
        if file in recorder:
            print("已爬取")
            print("-----------------------------------")
            continue
        
        url = baseURL + str(file)

        try:
            response = requests.get(url, timeout=30)
            response.encoding = response.apparent_encoding
            html = BeautifulSoup(response.text, "html.parser")
        except:
            failed = fail(file, failed)
            i += 1
            continue
        
        # find title
        try:
            content = html.select("#mainContents > div.workshopItemDetailsHeader > div.workshopItemTitle")
            title = content[0].text
        except:
            failed = fail(file, failed)
            i += 1
            continue
        
        # find auther
        try:
            autherLink = html.select("#rightContents > div > div:nth-child(1) > div.rightDetailsBlock > div > div > a")
            autherURL = autherLink[0]["href"]
        except:
            failed = fail(file, failed)
            i += 1
        
        try:
            findAuther = requests.get(autherURL, timeout=30)
            findAuther.encoding = findAuther.apparent_encoding
            autherHTML = BeautifulSoup(findAuther.text, "html.parser")
        except:
            failed = fail(file, failed)
            i += 1
            continue
        
        try:
            autherName = autherHTML.select("#responsive_page_template_content > div.no_header.profile_page.has_profile_background > div.profile_header_bg > div > div > div > div.profile_header_centered_persona > div.persona_name > span.actual_persona_name")
            autherName = autherName[0].text
        except:
            fail(file, failed)
            i += 1
            continue
        
        if processor(path, outputBase, baseCommand, autherName, title, file):
            # record processed files   
            recorder.append(file)
        else:
            failed = fail(file, failed)

        i += 1
        
        # pause to avoid being banned
        time.sleep(1)
        if i % batch == 0:
            time.sleep(10)
    
    return recorder, failed