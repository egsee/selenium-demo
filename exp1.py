from time import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://www.douyin.com/")
assert "抖音" in driver.title
elem = driver.find_element(By.CLASS_NAME, 'KLzwyB7s mV31vsEW')
print(elem)
elem.send_keys("messi")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
time.sleep(5)
driver.close()