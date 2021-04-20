import shutil
import os
import os.path
import time
import json
import re
import sys

ignoreFiles = []
suffixName = ''
overwrite = False


def main():
    if len(sys.argv) > 1:
        configFileName = sys.argv[1]
    else:
        configFileName = 'backup_config.json'
    if not os.path.exists(configFileName):
        print("未找到 '%s' 的配置文件！" % configFileName)
        configObject = {
            "items": [
                {
                    "name": "",
                    "sourcePath": "",
                    "targetPath": ""
                }
            ],
            "profile": {
                "overwrite": False,
                "suffixName": "_%Y-%m-%d",
                "ignoreFiles": [
                    "desktop.ini"
                ]
            }
        }
        with open(os.path.join(os.getcwd(), 'backup_config.json'), 'w') as f:
            json.dump(configObject, f, sort_keys=True, indent=2)
        print('已在 %s 下创建文件: "backup_config.json"，请填写配置后再次运行程序。' % os.getcwd())
        print("配置说明：")
        print('\t "name"：       为该项的标题（非必填）')
        print('\t "sourcePath"： 为源文件全路径或相对路径（必填）')
        print('\t "targetPath"： 为目标文件夹全路径。如果为空则默认为当前程序目录（必填）')
        print('\t "overwrite"：  是否用最新修改的文件覆盖原有的文件')
        print('\t "suffixName"： 复制后文件名 = 源文件名 + suffixName（非必填）')
        print('\t "ignoreFiles"：当 "sourcePath" 为文件夹路径时，忽略复制的所有文件下（非必填）')
        print()
        print("提示：")
        print('\t 1.注意文件路径分隔符为 "\\\\" 或 "/"。')
        print('\t 2.如果 "targetPath" 为文件路径（有后缀名），则文件复制后文件名不会修改。')
        exit(1)

    dic = readFile(configFileName)

    global ignoreFiles, suffixName, overwrite
    if 'profile' in dic:
        ignoreFiles = dic['profile'].get('ignoreFiles', [])
        suffixName = dic['profile'].get('suffixName', "")
        overwrite = dic['profile'].get('overwrite', False)

    items = dic['items']
    copyFilesByConf(items)
    os.system('clear')
    print('\n全部处理完成！！！')


def readFile(configFileName):
    with open(configFileName, 'r') as f:
        dic = json.load(f)
    return dic


def copyFilesByConf(items):
    for i, item in enumerate(items):
        sourcePath = item['sourcePath'].strip()
        targetPath = item['targetPath'].strip()
        # 是否修改文件名
        isModifyNameForFile = True
        # 要创建文件夹路径
        dirPath = targetPath

        print('第%d项' % (i + 1))

        # 以 \ 或 / 结尾的文件夹
        if targetPath.endswith('\\') or targetPath.endswith('/'):
            dirPath = os.path.dirname(targetPath)
            targetPath = dirPath
        # 文件
        elif re.search(r'[^/\\]+\.\w+$', targetPath):
            dirPath = os.path.dirname(targetPath)
            isModifyNameForFile = False

        if not os.path.exists(dirPath) and dirPath != '':
            print('  📁文件夹: "%s"' % dirPath)
            print('  不存在', end='')
            os.makedirs(dirPath)
            print("，已创建！")

        if not os.path.exists(sourcePath):
            print('  📦源文件: "%s"' % sourcePath)
            print('  不存在！\n')
            continue

        if sourcePath != '':
            if os.path.isfile(sourcePath):
                if isModifyNameForFile:
                    targetPath = os.path.join(targetPath, doFileName(sourcePath))
                copyFile(sourcePath, targetPath)
            elif os.path.isdir(sourcePath):
                copyFiles(sourcePath, targetPath)


def copyFiles(sourcePath, targetPath):
    if not os.path.exists(targetPath) and targetPath != '':
        print('  📁文件夹: "%s"' % targetPath)
        print('  不存在', end='')
        os.makedirs(targetPath)
        print("，已创建！")

    ld = os.listdir(sourcePath)
    for file in ld:
        if ignoreFiles.count(file) > 0:
            continue
        filePath = os.path.join(sourcePath, file)
        if os.path.isfile(filePath):
            copyFile(filePath, os.path.join(targetPath, doFileName(filePath)))
        elif os.path.isdir(filePath):
            copyFiles(filePath, os.path.join(targetPath, os.path.basename(filePath)))


def copyFile(sourcePath, targetPath):
    print('\x1B[2J\x1B[0f')
    if os.path.isfile(targetPath):
        if overwrite and os.path.getmtime(sourcePath) > os.path.getmtime(targetPath):
            print('  覆盖文件: "%s" ' % targetPath)
            shutil.copy(sourcePath, targetPath)
            print('  🎉复制成功！\n')
        else:
            print('  📦目标文件: "%s" ' % targetPath)
            print('  已经存在！')
    else:
        print('  📦把文件: "%s"' % sourcePath)
        print('  复制到:   "%s"' % targetPath)
        shutil.copy(sourcePath, targetPath)
        print('  🎉复制成功！\n')


def doFileName(filePath):
    file = os.path.basename(filePath)
    index = file.rfind('.')
    fileType = file[(index + 1):]
    fileName = file[:index]
    fileSuffix = time.strftime(suffixName, time.localtime())
    return '%s%s.%s' % (fileName, fileSuffix, fileType)


if __name__ == '__main__':
    main()
