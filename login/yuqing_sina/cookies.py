import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class YuQingSinaCookies():
    def __init__(self, username, password, browser):
        self.url = 'http://yuqing.sina.com/staticweb/#/login/login'
        self.browser = browser
        self.wait = WebDriverWait(self.browser, 20)
        self.username = username
        self.password = password
    
    def open(self):
        """
        打开网页输入用户名密码并点击
        :return: None
        """
        self.browser.delete_all_cookies()
        self.browser.get(self.url)
        username = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/layout-login/div/app-routing-login/app-login-enter/div[1]/div/div[2]/div/div[2]/form/nz-form-item[1]/nz-form-control/div/span/nz-input-group/input')))
        password = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/layout-login/div/app-routing-login/app-login-enter/div[1]/div/div[2]/div/div[2]/form/nz-form-item[2]/nz-form-control/div/span/nz-input-group/input')))
        codeInput = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/layout-login/div/app-routing-login/app-login-enter/div[1]/div/div[2]/div/div[2]/form/nz-form-item[3]/nz-form-control/div/span/nz-input-group/input')))
        submit = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/layout-login/div/app-routing-login/app-login-enter/div[1]/div/div[2]/div/div[2]/form/nz-form-item[4]/nz-form-control/div/span/div/button')))
        username.send_keys(self.username)
        password.send_keys(self.password)

        time.sleep(1)
        input('已完成输入验证码并进入下一步？\n')

    def login_exception(self):
        """
        判断是否密码错误
        :return:
        """
        try:
            return WebDriverWait(self.browser, 5).until(
                EC.text_to_be_present_in_element((By.ID, 'errorMsg'), '用户名或密码错误'))
        except TimeoutException:
            return False

    def password_error(self):
        """
        判断是否密码错误
        :return:
        """
        try:
            return WebDriverWait(self.browser, 5).until(
                EC.text_to_be_present_in_element((By.ID, 'errorMsg'), '用户名或密码错误'))
        except TimeoutException:
            return False

    def need_verify(self):
        """
        判断是否密码错误
        :return:
        """
        try:
            return bool(WebDriverWait(self.browser, 5).until(
              EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/nz-modal/div/div[2]/div/div/div/div[2]/div[2]/input'))))
        except TimeoutException:
            return False

    def send_sns_code(self):
        """
        发送验证码
        :return:
        """
        codeInput = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/nz-modal/div/div[2]/div/div/div/div[2]/div[2]/input')))
        sendSnsBtn = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/div/nz-modal/div/div[2]/div/div/div/div[2]/div[2]/button')))
        submit = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[2]/div/nz-modal/div/div[2]/div/div/div/div[2]/div[3]/button')))

        input('已完成输入短信验证码并进入下一步？\n')

    def send_code_error(self):
        """
        判断发送验证码是否出现错误
        :return:
        """
        try:
            # box = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, '')))
            # print(box.get_attribute("textContent"))
            # return bool(box)
          return False
        except TimeoutException:
            return False

    def login_successfully(self):
        """
        判断是否登录成功
        :return:
        """
        try:
            input('waiting\n')
            if True:
               # self.browser.refresh()
                xpathStr = '/html/body/app-root/layout-default/layout-header/div/div[2]/app-navbar-router/ul/li[2]/a'
            else:
                self.browser.get('http://yuqing.sina.com/yqMonitor')
                xpathStr = '/html/body/div[1]/ul[1]/li[2]/a/span'

            return bool(
                WebDriverWait(self.browser, 60).until(EC.presence_of_element_located((By.XPATH, xpathStr))))
        except TimeoutException:
            return False

    def get_cookies(self):
        """
        获取Cookies
        :return:
        """
        return self.browser.get_cookies()
    
    def main(self):
        """
        破解入口
        :return:
        """
        self.open()
        if self.password_error():
            return {
                'status': 2,
                'content': '用户名或密码错误、账号停用保护'
            }

        if self.need_verify():
            self.send_sns_code()

        # if self.send_code_error():
            # pass

        # 如果不需要验证码直接登录成功
        if self.login_successfully():
            cookies = self.get_cookies()
            print(cookies)
            input('waiting\n')
            return {
                'status': 1,
                'content': cookies
            }

        print('登录结束')

if __name__ == '__main__':
    result = YuQingSinaCookies('cblink', 'Sina2021').main()
    print(result)
