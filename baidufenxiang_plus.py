
from lxml import etree
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv


class BaiduSpider(object):

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.url = 'https://jingyan.baidu.com/user/nucpage/patch&txt=悬赏经验'
        self.positions = []
        self.pageName = ''

    def login(self):
        self.driver.get(self.url)
        login_btn = self.driver.find_element_by_id('user-login')
        login_btn.click()
        # 设置页面等待
        WebDriverWait(driver=self.driver, timeout=10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="TANGRAM__PSP_10__footerULoginBtn"]'))
        )
        time.sleep(2)
        # 转换成输入用户名和密码
        input_thing = self.driver.find_element_by_id('TANGRAM__PSP_10__footerULoginBtn')
        input_thing.click()
        # 输入用户名
        input_phone_number = self.driver.find_element_by_id('TANGRAM__PSP_10__userName')
        input_phone_number.send_keys('15190670945')
        time.sleep(3)
        # 输入密码
        input_password = self.driver.find_element_by_id('TANGRAM__PSP_10__password')
        input_password.send_keys('Ll950218')
        time.sleep(3)
        # 点击登录
        input_login = self.driver.find_element_by_id('TANGRAM__PSP_10__submit')
        input_login.click()
        # 进入主页面
        self.into_page()

    def into_page(self):
        # 进入我的经验页面
        WebDriverWait(driver=self.driver, timeout=10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="my-home-exp"]'))
        )
        time.sleep(2)
        # 跳转到真正的页面
        true_page = self.driver.find_element_by_xpath('//*[@id="wgt-aside"]/div[4]/a')
        true_page.click()
        # 页面切换
        self.driver.switch_to.window(self.driver.window_handles[1])
        time.sleep(10)  # 这里的睡眠时间没有测试,可以稍微改一改
        self.get_page_data()

    def get_page_data(self):
        '''
        这里可以拓展,写个死循环一直取下一个页面的数据
        :return:
        '''
        # 拿到页面数据
        source = self.driver.page_source
        # 处理数据
        self.parse_list_page(source, '普通悬赏')
        # 写入数据
        self.write_csv_second()

    def write_csv_second(self):
        headers = ['class', 'name', 'money']
        with open('baidujingyann.csv', 'w') as fp:
            writer = csv.DictWriter(fp, headers)
            # 写入把表头数据
            writer.writeheader()
            writer.writerows(self.positions)

    def parse_list_page(self, source, class_name):
        html = etree.HTML(source)
        # 获取具体的数据
        divs = html.xpath('//*[@class="query-content"]/ul//div')
        for div in divs:
            print(div)
            money = (div.xpath('.//text()')[0].strip())
            name = div.xpath('.//a//text()')[0].strip()
            position = {
                'class': class_name,
                'name': name,
                'money': money
            }
            self.positions.append(position)
            self.positions = sorted(self.positions, key=lambda x:x['money'], reverse=True)
            print(position)
            print('=' * 20)
            time.sleep(0.5)


if __name__ == '__main__':
    spider = BaiduSpider()
    spider.login()


