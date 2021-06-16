#-*- coding: utf-8 -*-
# https://github.com/umihico/docker-selenium-lambda

from selenium import webdriver
from bs4 import BeautifulSoup
import time
#import os
#import urllib2
#import sys
# Explicit Waits
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# 예외 컨트롤
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

def handler(event=None, context=None):
  options = webdriver.ChromeOptions()
  options.binary_location = "/opt/headless-chromium"
  options.add_argument('--headless')
  options.add_argument('--no-sandbox')
  options.add_argument("--disable-gpu")
  options.add_argument("--window-size=1920x1080")
  options.add_argument("--single-process")
  options.add_argument("--disable-dev-shm-usage")
  driver = webdriver.Chrome("/opt/chromedriver",
                            options=options)
  driver.implicitly_wait(1)
  
  if event['site'] == 'giggle':
    try:
      driver.get('https://gigglehd.com/gg/index.php?act=dispMemberLoginForm')
      driver.find_element_by_css_selector('form#fo_member_login input[placeholder="아이디"]').send_keys('credentials')
      driver.find_element_by_css_selector('form#fo_member_login input[placeholder="비밀번호"]').send_keys('credentials')

      driver.find_element_by_xpath('//*[@id="fo_member_login"]/fieldset/div[2]/input').click()

      driver.get('https://gigglehd.com/gg/attendance')
      driver.find_element_by_xpath('//*[@id="click_button"]/span/button').click()
      message = 'giggle complete check'

      driver.get('https://gigglehd.com/gg/index.php?mid=index&act=dispMemberLogout')
      time.sleep(1)

    except NoSuchElementException as e:
      message = 'giggle Already check!'
      driver.get('https://gigglehd.com/gg/index.php?mid=index&act=dispMemberLogout')
      time.sleep(1)
  elif event['site'] == 'quasarzone':
    driver.get('https://quasarzone.com/login')
    driver.find_element_by_name('login_id').send_keys('credentials')
    driver.find_element_by_name('password').send_keys('credentials')

    driver.find_element_by_xpath('//*[@id="frm"]/div/div[1]/p/a').click()

    '''date = urllib.request.urlopen('http://quasarzone.co.kr').headers['Date']
    s_time = time.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')
    s_sec = s_time.tm_sec
    while True:
      try:
        s_sec += 1
        if s_time.tm_hour >= 0 or s_sec >= 60:
          driver.get('https://quasarzone.com/users/attendance')
          elem = driver.find_elements_by_xpath('//*[@class="active2"]')
          if len(elem) > 0:
            elem[0].click()
            time.sleep(1)
            message = 'quasarzone complete check'
          else:
            message = 'quasarzone Already check!'
          break
        time.sleep(1)
      except TimeoutException as e:
        pass'''
    
    # 위에 주석한 출석체크 부분만 아래에 넣었음
    # lambda trigger를 원래 8시 59분에 실행하게 했는데 그냥 9시 실행으로 바꿈
    driver.get('https://quasarzone.com/users/attendance')
    elem = driver.find_elements_by_xpath('//*[@class="active2"]')
    if len(elem) > 0:
      elem[0].click()
      time.sleep(1)
      message = 'quasarzone complete check'
    else:
      message = 'quasarzone Already check!'

    driver.get('http://quasarzone.co.kr/bbs/logout.php')
    time.sleep(1)
  elif event['site'] == 'x86':
    driver.get('https://x86.co.kr/index.php?mid=main&mode=totalogin&act=dispMemberLoginForm')
    WebDriverWait(driver, 0.5).until(EC.presence_of_element_located((By.ID, 'uid')))
    driver.find_element_by_name('user_id').send_keys('hdj997@gmail.com')
    driver.find_element_by_name('password').send_keys('credentials')

    driver.find_element_by_xpath('//*[@id="fo_member_login"]/fieldset/div[2]/input').click()

    driver.get('https://x86.co.kr/')
    elem = driver.find_elements_by_xpath('//*[@id="attendance_frm"]/a')
    if len(elem) > 0:
      elem[0].click()
      time.sleep(1)
      message = 'x86 complete check'
    else:
      message = 'x86 Already check!'

    driver.get('https://x86.co.kr/index.php?mid=timeline&act=dispMemberLogout')
    time.sleep(1)
  elif event['site'] == 'ygosu':
    driver.get('https://www.ygosu.com/')
    driver.find_element_by_name('login_id').send_keys('credentials')
    driver.find_element_by_name('login_pwd').send_keys('credentials')

    driver.find_element_by_xpath('//*[@id="login_form"]/div[2]/a').click()

    message = 'ygosu complete check'

    driver.get('https://www.ygosu.com/login/logout.yg')
    time.sleep(1)
  elif event['site'] == 'tcafe':
    driver.get('http://www.tcafe2a.com/')
    driver.find_element_by_name('mb_id').send_keys('credentials')
    driver.find_element_by_name('mb_password').send_keys('credentials')

    driver.find_element_by_xpath('//*[@id="ol_before"]/form/fieldset/div[1]/span[2]/button').click()

    driver.get('http://tcafe2a.com/community/attendance')
    driver.find_element_by_xpath('//*[@id="cnftjr"]/div/form/table/tbody/tr/td/img').click()
    message = 'tcafe complete check'

    driver.get('http://tcafe2a.com/bbs/logout.php')
    time.sleep(1)
  else:
    message = 'unknown event'

  driver.quit()
  print(message)
  return(message)

'''if __name__ == "__main__":
  site = sys.argv[1]
  print(site)
  handler({'site' : site})'''
