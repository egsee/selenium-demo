import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


class WebDriverChrome(object):

    def __init__(self):
        self.driver = self.StartWebdriver()

    def StartWebdriver(self):
        options = webdriver.ChromeOptions()

        # options.add_argument("start-maximized")

        # display feature
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # webdriver value
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
        with open('./stealth.min.js') as f:
            js = f.read()
        # hidden 浏览器指纹
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": js
        })
        return driver

    def RunStart(self):
        # self.driver.get('https://bot.sannysoft.com')
        self.driver.get('https://ke.com')
        # body = self.driver.find_element(By.TAG_NAME, 'body')
        search = self.driver.find_element_by_id("keyword-box")
        search.send_keys("万科")
        search.send_keys(Keys.RETURN)
        # self.driver.find_element(By.CLASS_NAME, 'app_close').find_element_by_tag_name('img').click()
        num = 0
        # while num < 5:
        #     print("num=", num)
        #     time.sleep(random.uniform(1, 9))
        #     ActionChains(self.driver).move_by_offset(
        #         random.uniform(-100, 100), random.uniform(-100, 100)).perform()
        #     body.send_keys(Keys.DOWN)
        #     time.sleep(1)
        #     num += 1
        time.sleep(3)
        self.driver.quit()


if __name__ == '__main__':
    Crawl = WebDriverChrome()
    Crawl.RunStart()
