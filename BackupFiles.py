import shutil
import os
import os.path
import time
import json

def main():
    configFileName = 'backup_config.json'
    if not os.path.exists(configFileName):
        print("在当前目录下，未找到名为 '%s' 的配置文件！" % configFileName)
        configObject = {
           "items": [
                {
                    "name": "",
                    "sourcePath": "",
                    "targetPath": ""
                }
            ]
        }
        with open(configFileName, 'w') as f:
            json.dump(configObject, f, sort_keys=True, indent=2)
        print("已为您创建，请填写配置后再次运行程序。")
        print("配置说明：")
        print('\t "name"：       为该项的标题，可不填')
        print('\t "sourcePath"： 为源文件全路径，必填')
        print('\t "targetPath"： 为目标文件夹全路径，必填')
        print()
        print("提示：")
        print("\t 1.注意文件路径分隔符为 '\\\\' 或 '/'。")
        print('\t 2.如果 "targetPath" 为文件路径（有后缀名），则文件复制后文件名不会修改。')
        exit(0)
    
    dic = readFile(configFileName)
    items = dic['items']
    print(items)
    copyFiles(items)
    print('\n复制成功！！！')

def readFile(configFileName):
    with open(configFileName, 'r') as f:
        dic = json.load(f)
    return dic


def copyFiles(items):
    for item in items:
        sourcePath = item['sourcePath'].strip()
        targetPath = item['targetPath'].strip()
        print(targetPath)
        # 是否修改文件名
        isModifyName = True

        if targetPath.endswith('\\') or targetPath.endswith('/'):
            dirPath = os.path.dirname(targetPath)
            targetPath = dirPath
        elif targetPath.rfind('.') > -1:
            dirPath = os.path.dirname(targetPath)
            isModifyName = False
        else:
            dirPath = targetPath

        if not os.path.exists(dirPath) and dirPath != '':
            print('文件夹 "%s" 不存在！' % dirPath)
            os.makedirs(dirPath)
            print("已创建！\n")

        if not os.path.exists(sourcePath):
            print("源文件 '%s' 不存在！" % sourcePath)
            continue

        if sourcePath != '':
            t = doFileName(sourcePath)
            if isModifyName:
                targetPath = os.path.join(targetPath, '%s_%s.%s' % (t[0], getNowDate(), t[1]))
            
            if os.path.exists(targetPath):
                print('目标文件 "%s" 已经存在！' % targetPath)
                print('退出复制！')
                exit(0)
            else:
                shutil.copy(sourcePath, targetPath)


def doFileName(filePath):
    file = os.path.basename(filePath)
    index = file.rfind('.')
    fileType = file[(index + 1):]
    fileName = file[:index]
    return (fileName, fileType)


def getNowDate():
    now = time.localtime()
    return '%d-%d-%d' % (now.tm_year, now.tm_mon, now.tm_mday)


if __name__ == '__main__':
    main()