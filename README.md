# wallpaper-engine-extractor

这是一个自动识别你订阅的壁纸, 并从创意工坊上爬取壁纸名和作者的脚本, 爬取完成后, 会将壁纸文件（视频或图片）按 `作者/壁纸名` 的目录提取到你指定的目标文件夹中. 其中, 对视频, 网页, 应用格式的壁纸仅复制, 对于静态壁纸的 `.pkg` 文件, 则使用 [RePKG](https://github.com/notscuffed/repkg) 提取内容后放入目标文件夹

在脚本执行完后, 会在提取结果文件夹下生成一个 `metadata.json` 文件, 来记录成功爬取的壁纸的相关信息. 如果有爬取失败的壁纸, 会将其创意工坊ID存放在提取文件夹下的 `failed.json` 中, 你可以之后运行脚本爬取, 或是自行搜索处理

<details>
<summary>change log</summary>

- 2024/11/5: 🚀新增了简单的图形化界面, 更方便使用
- 2024/11/5:
  - 重写了传参逻辑, 现在不用去代码文件里更改参数, 可以直接在命令行中传入所有需要的参数了
  - 完全重构代码, 重写了功能逻辑
  - 增加了多进程功能, 默认使用全部CPU核心并行地爬取和提取壁纸
  - 重写了历史记录和失败记录功能, 现在将会在输出文件夹下生成一个 `metadata.json` 文件来记录爬取的壁纸信息, 一个 `failed.json` 文件来记录爬取失败的壁纸信息
- 2023/5/22: 可选命令行参数, 提取 `.pkg`文件后自动整理删除多余文件

</details>

## 部署和使用

有两种方式可以使用这个仓库, 图形化界面和命令行

### 图形化界面

**获取软件**:

要使用图形化界面, 可以直接从[发布页面](https://github.com/Orion-zhen/wallpaper-engine-extractor/releases)下载 `wallpaper-engine-extractor.exe` 和 `RePKG.exe` 文件

**使用软件**:

双击打开 `wallpaper-engine-extractor.exe`, 此时将出现一个图形界面和一个命令行窗口. 图形界面如下:

![gui-guide](./assets/gui-guide.png)

依次点击按钮选择**创意工坊路径**, **提取路径**和 `RePKG.exe` 路径. 其中, `RePKG.exe` 的路径是你在下载软件时下载到的路径

你可以通过移动滑块数量来更改并行数量, 默认情况下是全部的 CPU 线程数

当一切妥当, 你可以点击**提取**按钮, 然后你会在命令行窗口中看到提取的详细情况. 当提取完成后, 会显示**运行完成**字样, 此时可以安全地关闭图形界面, 命令行窗口也会随之自动关闭

### 命令行

**获取代码**:

直接下载压缩包或在命令行中执行

```shell
git clone https://github.com/Orion-zhen/wallpaper-engine-extractor.git
cd wallpaper-engine-extractor
```

**安装依赖**:

```shell
pip install -r requirements.txt
```

**运行命令**:

命令格式如下:

```shell
usage: main.py [-h] --input INPUT [--recover] --output OUTPUT [--parallel PARALLEL] [--retry RETRY]
                                                                                                          
Wallpaper Engine 壁纸提取器

options:
  -h, --help            查看用法
  --input, -i INPUT     Wallpaper Engine workshop的路径
  --recover, -r         是否恢复上次失败的任务
  --output, -o OUTPUT   提取到的壁纸的保存路径
  --parallel, -p PARALLEL
                        并行处理数量
  --retry RETRY         重试次数
```

简要格式:

```shell
python main.py -i <workshop路径> -o <壁纸提取路径>
```

一个简单的例子:

```shell
python main.py -i "C:\Program Files (x86)\Steam\steamapps\workshop\content\431960" -o "C:\Users\Username\Pictures\wallpapers"
```

## 附注

如果你wallpaper engine订阅的壁纸太多了, 以至于在新电脑上装一个wallpaper engine时需要花相当长的时间；或者你担心以前订阅的壁纸被下架了或删除了, 可以将wallpaper engine创意工坊备份一份到本地. 方法是：找到创意工坊的目录, 一般是 `path/to/your/steam/steamapps/workshop/content/431960`, 将431960这个文件夹复制到你的wallpaper engine安装目录下的 `projects`文件夹下, 一个典型路径是 `path/to/your/steamlibrary/steamapps/commom/wallpaper_engine/projects`, 然后将431690文件夹改名为 `backup`, 然后重启wallpaper engine, 取消订阅重复的文件就可以了. [具体参考这里](https://help.wallpaperengine.io/zh/steam/backup.html)
