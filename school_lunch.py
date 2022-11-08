import requests
from bs4 import BeautifulSoup
from time import time, localtime


def call_ymd():
    a = localtime(time())
    year = a.tm_year
    mon = a.tm_mon
    day = a.tm_mday
    return year*10000+mon*100+day


def call_yo1():
    week = ['월', '화', '수', '목', '금', '토', '일']
    day = localtime(time()).tm_wday
    return week[day]


def call_hmin():
    a = localtime(time())
    hour = a.tm_hour
    return hour


def pretty_date():
    a = localtime(time())
    return f'{a.tm_year}년 {a.tm_mon}월 {a.tm_mday}일'


def tidy(Text):
    word_list = Text.split()
    res = " ".join(word_list)
    return res


def build_menu_list(li, list):
    for i in li:
        res = i.text
        res = res.replace(" ", "")
        list.append(res)


def extract_str(menu):
    menu = menu.split()
    new_menu = []
    for a in range(1, len(menu)):
        string = menu[a].split('(')
        if len(string) > 2:
            string = string[0] + '(' + string[1]
        else:
            string = string[0]
        string = ''.join([i for i in string if not i.isdigit()])
        string = string.replace(' ', '')
        new_menu.append(string)
    return new_menu


def main_scraper(date):
    URL = f'http://school.cbe.go.kr/cbs-h/M01050705/list?ymd={date}'

    result = requests.get(URL)
    html = result.text
    soup = BeautifulSoup(html, "html.parser")
    li = soup.select('li.tch-lnc-wrap')

    menu = []
    build_menu_list(li, menu)
    return menu


def return_menu(date):
    # 0 : breakfast, 1: lunch, 2: dinner
    raw_meals = main_scraper(date)
    meal_num = len(raw_meals)
    yo1 = call_yo1()
    if meal_num == 0:
        temp = f'오늘은 {yo1}요일' if yo1 == '토' or yo1 == '일' else '업데이트 중...'
        return [temp], [temp], [temp]
    elif meal_num == 1:
        raw_meals.insert(0, 'temp\n없어요')
        raw_meals.append('temp\n없어요')

    elif meal_num == 2:
        raw_meals.append('temp\n없어요')

    breakfast = extract_str(raw_meals[0])
    lunch = extract_str(raw_meals[1])
    dinner = extract_str(raw_meals[2])

    return breakfast, lunch, dinner


print(return_menu(20221110))