import os
import shutil

def processor(path, outputBase, baseCommand, autherName, title, file):
    if autherName == "None":
        autherName = "UnknownAuther"
        
    locals = os.listdir(path + "/" + file)
    outputPath = outputBase + "/" + autherName + "/" + title + " [id=" + file + "]"
    
    # check for illegal characters
    autherName = autherName.replace('<', '(')
    autherName = autherName.replace('>', ')')
    autherName = autherName.replace('!', '！')
    autherName = autherName.replace('?', '？')
    autherName = autherName.replace('|', ' ')
    autherName = autherName.replace(':', '.')
    autherName = autherName.replace('/', '_')
    autherName = autherName.replace('"', "'")
    autherName = autherName.replace('*', '×')
    title = title.replace('<', '(')
    title = title.replace('>', ')')
    title = title.replace('!', '！')
    title = title.replace('?', '？')
    title = title.replace('|', ' ')
    title = title.replace(':', '.')
    title = title.replace('/', '_')
    title = title.replace('"', "'")
    title = title.replace('*', '×')
    
    if not os.path.exists(outputPath):
        try:
            os.makedirs(outputPath)
        except:
            print("无法创建这个目录: " + '"' + outputPath + '"')
            print("请检查是否有非法字符")
            return False
    
    # only extract if scene.pkg exists
    if "scene.pkg" in locals:
        command = baseCommand + "/" + file + "/scene.pkg" + '"' + " " + "-o" + " " + '"' + outputPath + '"'
        print("执行如下命令:")
        print(command)
        os.system(command)
        
        # delete .json, .tex and .tex-json files
        print("删除多余文件...")
        os.remove(outputPath + "/scene.json")
        subfolders = os.listdir(outputPath)
        # remove extra folders
        for subfolder in subfolders:
            if subfolder != "materials":
                shutil.rmtree(outputPath + "/" + subfolder)
        subfiles = os.listdir(outputPath + "/materials")
        for subfile in subfiles:
            if subfile.endswith(".png") or subfile.endswith(".gif") or subfile.endswith(".jpg") or subfile.endswith(".jpeg"):
                shutil.move(outputPath + "/materials/" + subfile, outputPath)
        shutil.rmtree(outputPath + "/materials")
        
    # else just copy files
    else:
        command = "Xcopy" + " " + '"' + path + "/" + file + '"' + " " + '"' + outputPath + '"'
        print("执行如下命令:")
        print(command)
        os.system(command)
    
    return True
            

def fail(file, failed):
    print(str(file) + "爬取失败")
    failed.append(file)
    print("-----------------------------------")
    return failed