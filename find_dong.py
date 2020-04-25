from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
import time

opts = Options()
opts.headless = True

# This example requires Selenium WebDriver 3.13 or newer
with webdriver.Chrome(options=opts) as driver:
    wait = WebDriverWait(driver, 10)
    
    driver.get("http://localhost:5000?q=당곡2로 16")
    
    #html = driver.execute_script('return document.body.innerHTML')
    
    post_window_name = 'Daum 우편번호 서비스'
    post_window = None
    main_window = None

    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        if driver.title == post_window_name:
            post_window = handle
        else:
            main_window = handle
    
    driver.switch_to.window(post_window)

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe")))
    
    # post list direction in
    driver.switch_to.frame(0)

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "script")))

    tit_address = driver.find_elements_by_xpath("//dt")

    for item in tit_address:

        if item.text != "도로명":
             continue
        
        dd = item.find_element_by_xpath("./following::dd")
        button = dd.find_element_by_class_name("link_post")
        button.click()
    
    driver.switch_to.window(main_window)

    time.sleep(1)
    post_find_result = driver.find_element_by_id("result").text

    post_json = json.loads(post_find_result)
    print(post_json)

    driver.close()
  