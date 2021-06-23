## 开发

1. 克隆
git clone https://github.com/mouyong/CookiesPool

2. 更新配置文件
```
vim cookiespool/config.py # 修改对应的 redis 配置信息
```

3. 安装依赖
`pip install -r requirments.txt`

4. 运行
`python run.py`

5. 添加新账号
`python importer.py`
格式：账号----密码

退出账号录入，输入 `exit`

注：在 `cookiespool/importer.py` 中配置要添加的站点账号
`conn = RedisClient('accounts', 'weibo')`

## 设置是否无头模式

需要访问浏览器控制端，进行页面操作，如重新登录账号时，修改 cookiespool/generator.py:12，设置 handless=False，然后重新运行 `python run.py`

## API

见 `cookiespool/api.py`。

- 随机获取 1个账号 cookie: `/<website>/random`
- 添加账号：`/<website>/add/<username>/<password>`
- 查看站点可用 cookie 总数：`/<website>/count`
