import telegram
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from transformer_model import *
import urllib.request as req


# 확진자 출력 함수
def show_corona():
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EC%BD%94%EB%A1%9C%EB%82%98+%ED%99%95%EC%A7%84%EC%9E%90"
    res = req.urlopen(url)
    soup = BeautifulSoup(res, "html.parser")
    p_list = soup.select("#_cs_production_type > div > div.main_tab_area > div > div > ul > li.info_01 > em ")  # 확진자수
    np_list = soup.select('#_cs_production_type > div > div.main_tab_area > div > div > ul > li.info_03 > em')  # 격리해제
    d_list = soup.select('#_cs_production_type > div > div.main_tab_area > div > div > ul > li.info_04 > em')  # 사망자수
    output_result = ""
    p = p_list[0].text
    np = np_list[0].text
    d = d_list[0].text

    output_result = f'''확진자 수 : {p}명
격리해제  : {np}명
사망자      : {d}명'''

    return output_result


# 백신 접종 현황
def show_vaccine():
    url = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&qvt=0&query=%EC%BD%94%EB%A1%9C%EB%82%9819%EB%B0%B1%EC%8B%A0%ED%98%84%ED%99%A9'
    res = req.urlopen(url)
    soup = BeautifulSoup(res, "html.parser")
    vaccine_1_list = soup.select(
        "#_cs_vaccine_info > div > div.main_tab_area > div > div > div > div > dl > dd > strong.value")  # 백신접종률
    vaccine_1 = vaccine_1_list[0].text
    vaccine_2 = vaccine_1_list[1].text
    output_result = ''
    output_result = f'''전국 1차 접종   : {vaccine_1}%
전국 완전 접종  : {vaccine_2}%'''

    return output_result


# 사회적 거리두기
def social_distance(step):
    url = 'http://ncov.mohw.go.kr/regSocdisBoardView.do'
    res = req.urlopen(url)
    soup = BeautifulSoup(res, "html.parser")
    social_distance_list = soup.select('#stepMapAll > p.rssd_descript')
    output_result = ''

    output_result = social_distance_list[abs(step - 4)].text.strip()
    result = f'거리두기 {step}단계\n{output_result}'

    return result


# 선별진료소 검색
def search_area(region):
    driver_path = "C:/chromedriver_win32/chromedriver.exe"
    driver = webdriver.Chrome(driver_path)

    url = "https://www.mohw.go.kr/react/popup_200128_3.html"
    driver.get(url)
    time.sleep(1)
    driver.switch_to.frame('innerSrc')
    input = driver.find_element(By.ID, 'SEARCHVALUE')
    input.send_keys(region)
    input.send_keys(Keys.ENTER)
    time.sleep(1)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    covid_area_list = soup.select('#clinic_container > div.tb_scroll > table > tbody > tr > td.name > strong')

    result = ''
    for i in range(len(covid_area_list)):
        result += covid_area_list[i].text[:-10] + '\n'

    return result


# telegram

token = '2130277129:AAER23EbSO245gt_w9n2Y1H2rwWW5nHIdSQ'
# id = "-680602148"  #그룹


bot = telegram.Bot(token)
try:
    id = bot.getUpdates()[-1].message.chat.id
except:
    id = "-680602148"

info_message = '''
코로나 감염 현황
백신 접종 현황
거리두기 [단계] 예) 거리두기 4
[검색어] 선별진료소 예) 서울 선별진료소 / 중구 선별진료소 
    - 시도 및 시군구, 선별진료소, 전화번호를 통합하여 검색합니다.
    - 검색어 예시 : '서울' 또는 '중구 '또는 '보건소' 또는 '051'(전화번호 일부)
'''

bot.sendMessage(chat_id=id, text=info_message)
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher


### 챗봇 답장
def handler(update, context):
    user_text = update.message.text  # 사용자가 보낸 메세지를 user_text 변수에 저장합니다.
    # 코인예측
    if user_text == "코로나 감염 현황":
        text = show_corona()
        bot.sendMessage(chat_id=id, text=text)
        bot.sendMessage(chat_id=id, text=info_message)

    elif user_text == '백신 접종 현황':
        text = show_vaccine()
        bot.sendMessage(chat_id=id, text=text)
        bot.sendMessage(chat_id=id, text=info_message)

    elif user_text.split()[0] == '거리두기':
        text = social_distance(int(user_text.split()[1]))
        bot.sendMessage(chat_id=id, text=text)
        bot.sendMessage(chat_id=id, text=info_message)

    elif user_text.split()[1] == '선별진료소':
        covid_area = search_area(user_text.split()[0])
        bot.send_message(chat_id=id, text=covid_area)
        text = '''더 많은 진료소 정보를 보고싶다면 아래 사이트를 참조해주세요
https://www.mohw.go.kr/react/popup_200128_3.html
        '''
        bot.sendMessage(chat_id=id, text=text)
        bot.sendMessage(chat_id=id, text=info_message)

    else:
        output = predict(user_text)
        output = output[5:-5].strip()
        bot.send_message(chat_id=id, text=output)


echo_handler = MessageHandler(Filters.text, handler)

dispatcher.add_handler(echo_handler)

updater.start_polling()
updater.idle()