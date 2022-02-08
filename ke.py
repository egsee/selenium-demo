#!/usr/bin/python3

from copyreg import constructor
import random
import time
from importlib_metadata import re, sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import pymysql


class WebDriverChrome(object):

    def __init__(self):
        self.driver = self.StartWebdriver()
        self.db = pymysql.connect(host='localhost',
                                  user='root',
                                  password='rootpsd',
                                  database='ke')

    def StartWebdriver(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        # headless

        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')

        # options.add_argument('log-level=3')
        # INFO = 0,
        # WARNING = 1,
        # LOG_ERROR = 2,
        # LOG_FATAL = 3
        # default is 0

        driver = webdriver.Chrome(options=options)
        # hidden 浏览器指纹
        with open('./stealth.min.js') as f:
            js = f.read()
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": js
        })
        return driver

    def RunStart(self):
        op = Options()
        op.page_load_strategy = "eager"
        self.driver.get('https://ke.com')
        self.driver.find_element(
            By.XPATH, "//a[@href='https://cd.fang.ke.com/loupan/']").click()
        try:
            self.RunPerPage(1)
        except Exception as e:
            print(e.print_exc())
            print(e.__traceback__.tb_lineno)
            self.driver.quit()
        self.driver.quit()

    def RunPerPage(self, page):
        page = int(page)
        print('正在获取第' + str(page) + '页内容')
        if page > 1:
            try:
                currentPage = self.driver.find_element(
                    By.CSS_SELECTOR, ".page-box a[data-page=" + '"' + str(page) + '"' + "]")
                currentPage.click()
            except Exception as e:
                print("程序退出:", e)
                sys.exit()
        page += 1
        self.driver.implicitly_wait(3)
        blocks = self.driver.find_elements(By.CLASS_NAME, "resblock-desc-wrapper")
        # try:
        #     blocks = WebDriverWait(self.driver, 10).until(
        #         self.driver.find_elements(By.CLASS_NAME, "resblock-desc-wrapper")
        #     )
        # finally:
        #     self.driver.quit()
        print('blocks', blocks)
        sql = """INSERT IGNORE INTO `new_loupan`(name, addr, house_info, salesman, price) VALUES"""
        n = 1
        for ele in blocks:
            time.sleep(0.1)
            # 户型： 2室 / 3室 / 4室 建面 75-138㎡
            titleNode = ele.find_element(By.CSS_SELECTOR, ".resblock-name>a")
            addr = ele.find_element(By.CLASS_NAME, "resblock-location").text
            house_info = ele.find_element(By.CLASS_NAME, "resblock-room").text
            sales_man = '无'
            # try: 
            #     sales_man = ele.find_element(By.CLASS_NAME, "ke-agent-sj-name").text
            #     sales_man = re.sub(r'新房顾问：\s{0,}(.+)', r'\1', sales_man)
            # except:
            #     sales_man = '无'
            price = ele.find_element(By.CLASS_NAME, "main-price").text
            price = re.sub(r'(.+)\s+元\s?/.+', r'\1', price)
            print('title', titleNode.text)
            print('addr', addr)
            print('house_info', house_info)
            print('price', price)
            print('==========================')
            comma = '' if n == len(blocks) else ','
            n = n + 1
            sql += '(' + '"' + titleNode.text + '"' + ',' + '"' + addr + '"' + ',' + '"' + \
                house_info + '"' + ',' + '"' + sales_man + \
                '"' + ',' + '"' + price + '"' + ')' + comma
            ActionChains(self.driver).move_to_element(titleNode).perform()
        print('正在存储第' + str(page) + '页内容...')
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit()
            print('存储第' + str(page) + '页内容成功！')
        except Exception as e:
            print('存储第' + str(page) + '页内容发生异常！')
            print(e)
            self.db.rollback()
            print(sql)
            sys.exit()
        print('page:', page)
        self.RunPerPage(page)


if __name__ == '__main__':
    Crawl = WebDriverChrome()
    Crawl.RunStart()
