# wallpaper-engine-extractor

一键批量提取wallpaper engine的壁纸(视频或 .pkg文件等)，并按作者和壁纸名存放

## 简介

这是一个自动识别你订阅的壁纸，并从创意工坊上爬取壁纸名和作者的脚本，爬取完成后，会将壁纸文件（视频或图片）按 `作者/壁纸名`的目录提取到你指定的目标文件夹中。其中，对视频、网页、应用格式的壁纸仅复制，对于静态壁纸的.pkg文件，则使用[RePKG](https://github.com/notscuffed/repkg)提取内容后放入目标文件夹

脚本提供了历史记录功能，将已经爬取过的文件的创意工坊ID存放在 `./accessories/history.json`中。如果删除该文件，脚本则会在开始爬取之前先读取目标文件夹中已经存在的文件，重新建立历史记录。所以当你尝试删除 `history.json`时，请确保你指定的目标文件夹中没有文件，或者其中的文件夹遵循 `path/to/your/targetFile/autherName/title [id=workshopID]`的格式，以免历史记录识别失败。其中，`autherName`为作者名，`title`为壁纸名，`workshopID`为壁纸的创意工坊ID，也就是你在wallpaper engine里右键单击壁纸选择在资源管理器中打开后看到的文件夹名。

在脚本执行完后，如果有爬取失败的壁纸，会将其创意工坊ID存放在 `./accessories/failed.json`中，你可以之后运行脚本爬取，或是自行搜索处理

## 部署和使用

直接下载压缩包或在命令行中执行

```powershell
git clone https://github.com/Orion-zhen/wallpaper-engine-extractor.git
cd wallpaper-engine-extractor
```

安装依赖

```powershell
pip install -r requirements.txt
```

进入 `main.py`中，将 `path`修改为你的steam创意工坊路径或你的创意工坊备份。一个典型的路径为 `path/to/your/steam/steamapps/workshop/content/431960`。

将 `outputBase`修改为你想要的输出地址。

在命令行中执行

```powershell
python main.py
```

然后等待爬取和提取完成即可。

[更新] 可选的参数有：

```powershell
python main.py  --target=workshopID
                --target-file=workshopIDs.json
                --retry=times
```

其中，`--target`参数为你指定的想要爬取的壁纸的创意工坊ID，`--target-file`参数为你想要爬取的壁纸的创意工坊ID列表，json文件格式为：

```json
["ID1", "ID2", "ID3", ...]
```

`--retry`参数指定你想重试的次数，如果传入这个参数，脚本会默认从 `./accessories/failed.json`中读取上次爬取失败的文件，并重试你指定的次数。

你还可以通过更改 `./modules/creeper.py`中 `repkgPath`的值来指定你想要的pkg文件提取器，但请将提取器放在和 `main.py`一个文件夹下，或者改为绝对地址。

你还可以通过更改 `./modules/creeper.py`中 `batch`的值来改变每爬取多少个文件后暂停10秒。

## 附注

1. `./accessories/authers.json`本来打算有用的，但我是大飞舞，所以没用了。🥰
2. 如果你wallpaper engine订阅的壁纸太多了，以至于在新电脑上装一个wallpaper engine时需要花相当长的时间；或者你担心以前订阅的壁纸被下架了或删除了，可以将wallpaper engine创意工坊备份一份到本地。方法是：找到创意工坊的目录，一般是 `path/to/your/steam/steamapps/workshop/content/431960`，将431960这个文件夹复制到你的wallpaper engine安装目录下的 `projects`文件夹下，一个典型路径是 `path/to/your/steamlibrary/steamapps/commom/wallpaper_engine/projects`，然后将431690文件夹改名为 `backup`，然后重启wallpaper engine，取消订阅重复的文件就可以了。[具体参考这里](https://help.wallpaperengine.io/zh/steam/backup.html)。
