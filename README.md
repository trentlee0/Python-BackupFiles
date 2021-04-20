## Python-BackupFiles

> 文件复制备份。

### 配置文件

如果没有指定配置文件或当前脚本目录下没有 `backup_config.json` 文件，则会在当前目录下创建文件: `backup_config.json`。

- `items`

    - `name`： 为该项的标题（非必填）

    - `sourcePath`： 为源文件全路径或相对路径（必填）

    - `targetPath`： 为目标文件夹全路径。如果为空则默认为当前程序目录（必填）

- `profile`

    - `ignoreFiles`：当 `sourcePath` 为文件夹路径时，忽略复制的文件（非必填）

    - `overwrite`： 是否用最新修改的文件覆盖原有的文件

    - `suffixName`： 复制后文件名 = 源文件名 + `suffixName`
      （非必填）。日期格式化查看 [文档](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes)

提示：

1. 注意文件路径分隔符为 ` \ ` 或 ` / `。

2. 如果 `targetPath` 为文件路径（有后缀名），则文件复制后文件名不会修改。

生成的配置文件：

```json
{
  "items": [
    {
      "name": "",
      "sourcePath": "",
      "targetPath": ""
    }
  ],
  "profile": {
    "ignoreFiles": [
      "desktop.ini"
    ],
    "overwrite": false,
    "suffixName": "_%Y-%m-%d"
  }
}
```

### 运行

可以指定配置文件运行。

```shell
python BackupFiles.py [confFile]
```
