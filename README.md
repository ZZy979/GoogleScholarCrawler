# 谷歌学术爬虫

## 依赖项
- Python 3.7
- Scrapy 2.3.0
- PyMySQL 0.10.0

## 配置文件
数据库连接参数等信息存放在config.ini文件中（已被.gitignore忽略），放置在项目根目录下

## 论文引用数爬虫
从数据库读取论文标题，搜索并爬取论文的引用数
- 运行：`scrapy crawl citation`
- 配置文件：
```ini
[MySQL]
host = xxx
port = 3306
user = user
password = xxx
database = xxx
table = xxx

[Proxy]
host = xxx
port = xxx
```
其中MySQL为必需，Proxy为可选
