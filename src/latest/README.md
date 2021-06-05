## Python-BackupFiles-latest

### 配置文件

如果没有指定配置文件或当前脚本目录下没有 `backup_config.json` 文件，则会在当前目录下创建文件: `backup_config.json`。

- `items`

    - `sourcePath`： 为源文件全路径或相对路径（必填）

    - `targetPath`： 为目标文件夹全路径。如果为空则默认为当前程序目录（必填）
    
    - `isOverwrite`： 是否用最新修改的文件覆盖原有的文件

    - `dateFormat`： 复制后文件名 = 源文件名 + `suffixName`
      （非必填）。日期格式化查看 [文档](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes)

提示：

1. 注意文件路径分隔符为 ` \ ` 或 ` / `。

生成的配置文件：

```json
{
  "items": [
    {
      "sourcePath": "",
      "targetPath": "",
      "dateFormat": "_%Y-%m-%d",
      "isOverwrite": false
    }
  ]
}
```