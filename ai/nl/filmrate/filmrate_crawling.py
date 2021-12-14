from selenium import webdriver
#from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.support.ui import WebDriverWait
import time
import os
import pandas as pd
from datetime import datetime
import chromedriver_autoinstaller


NUM_PAGE_DOWN = 100  # 리뷰 목록 확장 횟수
WAIT_TIME = 1       # 각 단계마다 대기 시간


def exportDataFromCrawling(url, keyword, user_id, user_pw):
    #base_url = 'https://pedia.watcha.com/ko-KR/search?query=%EC%A7%80%EA%B5%AC%EB%A5%BC%20%EC%A7%80%EC%BC%9C%EB%9D%BC&category=contents'
    
    _keyword = keyword
    
    if _keyword == "" :
        _keyword = "지구를 지켜라"    # sample
        #return ""
    
    _user_id = user_id
    _user_pw = user_pw
    
    if _user_id == "" or _user_pw == "" :
        _user_id = "bleachshot@gmail.com"
        _user_pw = "dkfkqldk12!@"
    
    base_url = 'https://pedia.watcha.com/ko-KR/search?query=' + _keyword + '&category=contents'
    
    pathChromeDriver = chromedriver_autoinstaller.install()
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless') #내부 창을 띄울 수 없으므로 설정
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    #driver = webdriver.Chrome('chromedriver',options=chrome_options)
    driver = webdriver.Chrome(executable_path=pathChromeDriver, options=chrome_options)
    driver.get(base_url)
    
    time.sleep(WAIT_TIME)
    
    #로그인 팝업
    driver.find_element_by_css_selector('#root > div > div.css-1xm32e0 > header > nav > div > div > ul > li:nth-child(6) > button').click()
    
    time.sleep(WAIT_TIME)
    
    #로그인하기
    driver.find_element_by_name('email').send_keys(_user_id)
    driver.find_element_by_name('password').send_keys(_user_pw)
    driver.find_element_by_class_name("css-qr0uqd-StylelessButton").click()
    
    time.sleep(WAIT_TIME)
    
    # 검색 리스트에서 클릭
    #movieListItemXpath = '//*[@id="root"]/div/div[1]/section/section/div[3]/div[1]/section/section[2]/div[2]/div[1]/div/ul/li[1]/a'
    movieListItemXpath = '//*[@id="root"]/div/div[1]/section/section/div[3]/div[1]/section/section[1]/div/div[1]/div/ul/li[1]/a/div[1]/div[1]/img'
    driver.find_element_by_xpath(movieListItemXpath).click()
    #movieListItem = WebDriverWait(driver, WEBDRIVER_WAIT_TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, movieListItemXpath)))
    #movieListItem.click()
    
    time.sleep(WAIT_TIME)
    
    # 영화 세부사항?
    movieDetailXpath = '//*[@id="root"]/div/div[1]/section/div/div[2]/div/section/div[2]/div/div/div/div/div[1]'
    sample = driver.find_element_by_xpath(movieDetailXpath).text
    #movieDetail = WebDriverWait(driver, WEBDRIVER_WAIT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, movieDetailXpath)))
    #sample = movieDetail.text
    
    time.sleep(WAIT_TIME)

    # 리뷰 더보기 클릭
    movieReviewMoreXpath = '//*[@id="root"]/div/div[1]/section/div/div[2]/div/div/div/div[1]/div[1]/div/div/section[5]/div[1]/div/header/div/div/a'
    driver.find_element_by_xpath(movieReviewMoreXpath).click()
    #movieReviewMore = WebDriverWait(driver, WEBDRIVER_WAIT_TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, movieReviewMoreXpath)))
    #movieReviewMore.click()
    
    time.sleep(WAIT_TIME)
    
    body = driver.find_element_by_tag_name('body')
    #body = WebDriverWait(driver, WEBDRIVER_WAIT_TIMEOUT).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    
    time.sleep(WAIT_TIME)
    
    # 페이지 다운시켜서 더 많은 리스트가 나오게 한다
    for i in range(NUM_PAGE_DOWN):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.33)
    
    time.sleep(WAIT_TIME)
    
    # 리뷰 내용
    commentsXpath = '//*[@id="root"]/div/div[1]/section/section/div/div/div/ul/div[*]/div[2]/div/span'
    comments = driver.find_elements_by_xpath(commentsXpath)
    #comments = WebDriverWait(driver, WEBDRIVER_WAIT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, commentsXpath)))
    
    # 별점
    ratesXpath = ' //*[@id="root"]/div/div[1]/section/section/div/div/div/ul/div[*]/div[1]/div[2]/span'
    rates = driver.find_elements_by_xpath(ratesXpath)
    #rates = WebDriverWait(driver, WEBDRIVER_WAIT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, ratesXpath)))
    
    data_size = len(comments)
    result = [["" for col in range(2)] for row in range(data_size)]
    
    for i in range(0, data_size):
      result[i][0] = comments[i].text
      result[i][1] = rates[i].text
    
    keyword_nospace = _keyword.replace(" ","_")
    datetime_now = datetime.now()
    datetime_now_str = datetime_now.strftime("%Y%m%d_%H%M%S")
    
    current_path = os.getcwd() + "\\nl\\filmrate\\data"
    result_excel_name = "filmrate_" + keyword_nospace + "_" + datetime_now_str + ".xlsx"
    result_excel_path = current_path + "\\" + result_excel_name
    
    result_excel = pd.DataFrame(result)
    result_excel.to_excel(excel_writer=result_excel_path)
    
    return result_excel_path
