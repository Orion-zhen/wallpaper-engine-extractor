import os
import sys
import signal
import shutil
import requests
import subprocess
from bs4 import BeautifulSoup
from multiprocessing import Pool
from typing import List, Dict, Union, Tuple


def get_content_info(target_id: str) -> Tuple[Union[str, None], Union[str, None]]:
    baseURL = "https://steamcommunity.com/sharedfiles/filedetails/?id="
    url = baseURL + str(target_id)

    try:
        response = requests.get(url, timeout=30)
        response.encoding = response.apparent_encoding
        html = BeautifulSoup(response.text, "html.parser")
        # find title
        content = html.select(
            "#mainContents > div.workshopItemDetailsHeader > div.workshopItemTitle"
        )
        assert isinstance(content, list) and len(content) == 1, "网页内容获取错误"
        title = content[0].text

        # find author
        author_link = html.select(
            "#rightContents > div > div:nth-child(1) > div.rightDetailsBlock > div > div > a"
        )
        assert (
            isinstance(author_link, list) and len(author_link) == 1
        ), "网页内容获取错误"
        author_homepage_url = author_link[0]["href"]
        author_homepage_content = requests.get(author_homepage_url, timeout=30)
        author_homepage_content.encoding = author_homepage_content.apparent_encoding
        author_html = BeautifulSoup(author_homepage_content.text, "html.parser")
        author_name = author_html.select(
            "#responsive_page_template_content > div.no_header.profile_page.has_profile_background > div.profile_header_bg > div.profile_header_bg_texture > div.profile_header > div.profile_header_content > div.profile_header_centered_persona > div.persona_name > span.actual_persona_name"
        )
        # author's homepage is private
        if len(author_name) == 0:
            author_name = author_html.select(
                "#responsive_page_template_content > div.no_header.profile_page.private_profile > div.profile_header_bg > div > div > div > div.profile_header_centered_persona > div > span.actual_persona_name"
            )
        assert (
            isinstance(author_name, list) and len(author_name) == 1
        ), "网页内容获取错误"
        author_name = author_name[0].text
    except Exception as e:
        print(e)
        print(str(target_id) + "爬取失败")
        return None, None
    return title, author_name


def format_path(content: str) -> str:
    content = content.replace("<", "(")
    content = content.replace(">", ")")
    content = content.replace("!", "！")
    content = content.replace("?", "？")
    content = content.replace("|", " ")
    content = content.replace(":", ".")
    content = content.replace("/", "_")
    content = content.replace('"', "'")
    content = content.replace("*", "×")
    return content


def extract(
    origin_path: str, target_id: str, output_base: str, title: str, author_name: str
) -> bool:
    print("-----------------------------------")
    source_folder = os.path.join(origin_path, target_id)
    output_folder_name = title + " [id=" + target_id + "]"
    output_path = os.path.join(output_base, author_name, output_folder_name)
    if not os.path.exists(output_path):
        try:
            os.makedirs(output_path)
        except:
            print("无法创建这个目录: " + '"' + output_path + '"')
            print("请检查是否有非法字符")
            print("-----------------------------------")
            return False

    # extract from source folder
    # if scene.pkg exists, extract it
    execute_path = "RePKG.exe"
    execute_cmd = [
        execute_path,
        "extract",
        os.path.join(source_folder, "scene.pkg"),
        "-o",
        output_path,
    ]
    if os.path.exists(os.path.join(source_folder, "scene.pkg")):
        # print("执行如下命令:")
        # print(" ".join(execute_cmd))
        status = subprocess.run(execute_cmd)
        if status.returncode != 0:
            print("RePKG.exe 解包失败")
            shutil.rmtree(output_path)
            print("-----------------------------------")
            return False

        # delete .json, .tex and .tex-json files
        # print("删除多余文件...")
        os.remove(os.path.join(output_path, "scene.json"))
        subfolders = os.listdir(output_path)
        # remove extra folders
        for subfolder in subfolders:
            if (
                os.path.isdir(os.path.join(output_path, subfolder))
                and subfolder != "materials"
            ):
                # print("删除 " + subfolder + " 文件夹...")
                shutil.rmtree(os.path.join(output_path, subfolder))
        subfiles = os.listdir(os.path.join(output_path, "materials"))
        for subfile in subfiles:
            if (
                subfile.endswith(".png")
                or subfile.endswith(".gif")
                or subfile.endswith(".jpg")
                or subfile.endswith(".jpeg")
            ):
                shutil.move(
                    os.path.join(output_path, "materials", subfile), output_path
                )
        shutil.rmtree(os.path.join(output_path, "materials"))

    # else just copy files
    else:
        execute_cmd = ["Xcopy", os.path.join(source_folder, "*.*"), output_path]
        # print("执行如下命令:")
        # print(" ".join(execute_cmd))
        subprocess.run(execute_cmd)
    print("-----------------------------------")
    return True


def siginit_handler(signum, frame):
    print("\n中断信号捕获, 正在终止所有进程...")
    pool.terminate()
    pool.join()
    print("警告: metadata未写入, 下次运行时将会从头开始提取")
    sys.exit(1)

def process_single(
    origin_path: str, target_id: str, output_base: str
) -> Union[Dict[str, str], None]:
    signal.signal(signal.SIGINT, siginit_handler)
    
    title, author_name = get_content_info(target_id)
    if title is None or author_name is None:
        return None
    title = format_path(title)
    author_name = format_path(author_name)

    if extract(origin_path, target_id, output_base, title, author_name):
        metadatum = {
            "ID": target_id,
            "title": title,
            "author": author_name,
            "path": os.path.join(
                output_base, author_name, title + " [id=" + target_id + "]"
            ),
        }
        return metadatum
    else:
        return None


def process(
    origin_path: str,
    target_ids: List[str],
    output_base: str,
    parallel_num: int,
) -> Tuple[List[Dict[str, str]], List[str]]:
    args = [(origin_path, target_id, output_base) for target_id in target_ids]

    global pool
    pool =  Pool(processes=parallel_num)
    results = pool.starmap(process_single, args)

    metadata = [result for result in results if result is not None]
    failed = [args[i][1] for i, result in enumerate(results) if result is None]

    return metadata, failed
