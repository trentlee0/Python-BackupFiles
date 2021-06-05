import os
import os.path as path
import time
import shutil
import json
import sys


def _copyFile(sourcePath, targetPath, isOverwrite=False):
    """复制 sourcePath 文件到 targetPath ，其中 targetPath 可以为目录，如果为目录需要添加 / 或 \\ """

    if path.isdir(targetPath):
        targetPath = path.join(targetPath, path.basename(sourcePath))

    print('复制文件 "%s" 到 "%s"' % (sourcePath, targetPath))

    # 目标文件已存在
    if path.isfile(targetPath):
        if isOverwrite:
            print('文件已存在，覆盖文件...')
            shutil.copy(sourcePath, targetPath)
            print('复制成功！')
        else:
            print('文件已存在，停止复制！')
    else:
        targetDir = path.dirname(targetPath)
        if not path.exists(targetDir):
            print('目录不存在 "%s"' % targetDir)
            os.makedirs(targetDir)
            print('目录创建成功！')
        shutil.copy(sourcePath, targetPath)
        print('文件复制成功！')


def getBackupFilePath(sourcePath, targetPath, dateFormat="_%Y-%m-%d"):
    """获取备份的文件路径其中 targetPath 可以为目录，如果为目录需要添加 / 或 \\"""

    # 文件
    if path.splitext(targetPath)[1] != '':
        dirname = path.dirname(targetPath)
        filename = path.basename(targetPath)
    else:
        dirname = targetPath
        filename = path.basename(sourcePath)

    filenameSuffix = time.strftime(dateFormat, time.localtime())
    fileTuple = path.splitext(filename)
    newFilename = "%s%s%s" % (fileTuple[0], filenameSuffix, fileTuple[1])
    return path.normpath(path.join(dirname, newFilename))


def formatFileTime(filePath, flag='m'):
    """格式化文件或文件夹的修改/创建/访问时间
    :param filePath:
    :param flag:
                'm': modification，修改时间
                'c': creation，创建时间
                'a': access，最后访问时间
    """

    if flag == 'c':
        sTime = path.getctime(filePath)
    elif flag == 'a':
        sTime = path.getatime(filePath)
    else:
        sTime = path.getmtime(filePath)

    lt = time.localtime(sTime)

    return "%d-%02d-%02d %02d:%02d:%02d" % (lt.tm_year, lt.tm_mon, lt.tm_mday, lt.tm_hour, lt.tm_min, lt.tm_sec)


def compareFileTime(sourcePath, targetPath, flag='m'):
    """比较两个文件或文件夹的修改/创建/访问时间，返回时间差，单位为秒
    :param targetPath:
    :param sourcePath:
    :param flag:
                'm': modification，修改时间
                'c': creation，创建时间
                'a': access，最后访问时间
    """

    if flag == 'c':
        s_time = path.getctime(sourcePath)
        t_time = path.getctime(targetPath)
    elif flag == 'a':
        s_time = path.getatime(sourcePath)
        t_time = path.getatime(targetPath)
    else:
        s_time = path.getmtime(sourcePath)
        t_time = path.getmtime(targetPath)

    return int(s_time) - int(t_time)


def copyFile(sourcePath, targetPath, isOverwrite=False, dateFormat="_%Y-%m-%d"):
    """复制文件"""

    backup = getBackupFilePath(sourcePath, targetPath, dateFormat)
    if path.exists(backup):
        if compareFileTime(sourcePath, backup) > 0:
            _copyFile(sourcePath, backup, isOverwrite=isOverwrite)
        else:
            print('复制文件 "%s" 到 "%s"' % (sourcePath, backup))
            print('复制停止：目标文件与源文件修改时间相同或离现在更近！目标文件：%s，源文件：%s' %
                  (formatFileTime(backup), formatFileTime(sourcePath)))
    else:
        _copyFile(sourcePath, backup, isOverwrite=isOverwrite)


def copyDir(sourcePath, targetPath, isOverwrite=False, dateFormat="_%Y-%m-%d"):
    """复制目录下的文件"""

    for file in os.listdir(sourcePath):
        filePath = path.join(sourcePath, file)

        if path.isfile(filePath):
            copyFile(filePath,
                     targetPath,
                     isOverwrite=isOverwrite,
                     dateFormat=dateFormat)
        elif path.isdir(filePath):
            copyDir(filePath,
                    path.join(targetPath, path.basename(filePath)),
                    isOverwrite=isOverwrite,
                    dateFormat=dateFormat)


def procedure(backupConf):
    for item in backupConf:
        sourcePath = path.normpath(item['sourcePath'])
        targetPath = path.normpath(item['targetPath'])
        dateFormat = item.get('dateFormat', "")
        isOverwrite = item.get('isOverwrite', False)

        if path.isfile(sourcePath):
            copyFile(sourcePath, targetPath, isOverwrite, dateFormat)
        elif path.isdir(sourcePath):
            copyDir(sourcePath, targetPath, isOverwrite, dateFormat)


def main():
    if len(sys.argv) > 1:
        configFileName = sys.argv[1]
    else:
        configFileName = 'backup_config.json'

    if not path.exists(configFileName):
        print('未找到 "%s" 的配置文件！' % configFileName)
        configObject = {
            "items": [
                {
                    "sourcePath": "",
                    "targetPath": "",
                    "isOverwrite": False,
                    "dateFormat": "_%Y-%m-%d"
                }
            ]
        }
        with open(path.join(os.getcwd(), 'backup_config.json'), 'w') as f:
            json.dump(configObject, f, sort_keys=True, indent=2)
        print('已在 %s 下创建文件: "backup_config.json"，请填写配置后再次运行程序。' % os.getcwd())
        print("配置文件说明查看： https://github.com/trentlee0/Python-BackupFiles")
        exit(1)

    with open(configFileName, 'r') as f:
        dic = json.load(f)

    items = dic['items']
    procedure(items)
    print('\n全部处理完成！！！')


if __name__ == "__main__":
    main()
