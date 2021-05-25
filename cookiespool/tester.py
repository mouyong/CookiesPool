import json
import requests
from requests.exceptions import ConnectionError
from cookiespool.db import *


class ValidTester(object):
    def __init__(self, website='default'):
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)
        self.accounts_db = RedisClient('accounts', self.website)
    
    def test(self, username, cookies):
        raise NotImplementedError
    
    def run(self):
        cookies_groups = self.cookies_db.all()
        for username, cookies in cookies_groups.items():
            self.test(username, cookies)


class WeiboValidTester(ValidTester):
    def __init__(self, website='weibo'):
        ValidTester.__init__(self, website)
    
    def test(self, username, cookies):
        print('正在测试Cookies', '用户名', username)
        try:
            cookies = json.loads(cookies)
        except TypeError:
            print('Cookies不合法', username)
            self.cookies_db.delete(username)
            print('删除Cookies', username)
            return
        try:
            test_url = TEST_URL_MAP[self.website]
            response = requests.get(test_url, cookies=cookies, timeout=5, allow_redirects=False)
            if response.status_code == 200:
                print('Cookies有效', username)
            else:
                print(response.status_code, response.headers)
                print('Cookies失效', username)
                self.cookies_db.delete(username)
                print('删除Cookies', username)
        except ConnectionError as e:
            print('发生异常', e.args)


class YuQingSinaValidTester(ValidTester):
    def __init__(self, website='yuqing_sina'):
        ValidTester.__init__(self, website)
    
    def test(self, username, cookies):
        print('正在测试Cookies', '用户名', username)
        try:
            cookies = json.loads(cookies)
        except TypeError:
            print('Cookies不合法', username)
            self.cookies_db.delete(username)
            print('删除Cookies', username)
            return
        try:
            test_url = TEST_URL_MAP[self.website]

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            }

            response = requests.get(test_url, cookies=cookies, headers=headers, timeout=10, allow_redirects=True)

            COOKIE_VALID_FLAG=False
            if response.headers.get('Content-Type') == 'application/json;charset=UTF-8':
                if response.json()['code'] == 20000:
                    COOKIE_VALID_FLAG=True
            else:
                if response.text.find('啊哦，你访问的页面，已经跟着地球去流浪了！') == -1:
                    COOKIE_VALID_FLAG=True

            if COOKIE_VALID_FLAG:
                print('Cookies有效', username)
            else:
                print(response.status_code, response.headers)
                print('Cookies失效', username)
                # self.cookies_db.delete(username)
                print('删除Cookies', username)

                resp = requests.post(url="http://test2.service.cblink.net/api/feishu/notify", json={'user_ids':('ou_088bf5b9e840bf88b91c094a3611bd6c',),'content':'八爪鱼 cookie 已过期'})
                print('飞书通知')
        except ConnectionError as e:
            print('发生异常', e.args)

if __name__ == '__main__':
    YuQingSinaValidTester().run()
