import datetime
from time import localtime, time

import requests


def call_ymd():
    a = datetime.date.today()
    year = a.year
    mon = a.month
    day = a.day
    return year*10000+mon*100+day


def return_nextday(date):
    y = int(date/10000)
    m = int((date % 10000)/100)
    d = int((date % 10000) % 100)
    if ((d == 30) and (m == 4 or m == 6 or m == 9 or m == 11)
        or (d == 28) and (m == 2)
            or (d == 31)):
        m += 1
        d = 1
    else:
        d += 1
    if m == 13:
        m = 1
        y += 1
    return y*10000+m*100+d


def call_yo1(date=datetime.date.today()):
    day = date.weekday()
    week = ['월', '화', '수', '목', '금', '토', '일']
    return week[day]


def call_hour():
    a = localtime(time())
    hour = a.tm_hour
    return hour


def pretty_date():
    a = localtime(time())
    return f'{a.tm_year}년 {a.tm_mon}월 {a.tm_mday}일'


def return_menu(MMEAL_SC_CODE, date=call_ymd()):
    url = 'https://open.neis.go.kr/hub/mealServiceDietInfo'
    params = {
        'type': 'json',
        'ATPT_OFCDC_SC_CODE': 'M10',
        'SD_SCHUL_CODE': '8000075',
        'MLSV_YMD': str(date),
        'MMEAL_SC_CODE': str(MMEAL_SC_CODE)
    }
    raw_json = requests.get(url=url, params=params).json()

    y = int(date/10000)
    m = int((date % 10000)/100)
    d = int((date % 10000) % 100)
    if not raw_json.get('mealServiceDietInfo'):
        if datetime.date(y, m, d).weekday() > 4:
            return ['주말입니다']
        if datetime.date.today().month < m:
            return ['업데이트 중']
        return ['없습니다']

    raw_menu = raw_json['mealServiceDietInfo'][1]['row'][0]['DDISH_NM']
    menu_list = raw_menu.split('<br/>')

    new_menu = []
    for menu in menu_list:
        string = menu.split('(')
        if len(string) > 2:
            string = string[0] + '(' + string[1]
        else:
            string = string[0]
        string = ''.join([i for i in string if not i.isdigit()])
        string = string.replace(' ', '')
        new_menu.append(string)
    return new_menu
