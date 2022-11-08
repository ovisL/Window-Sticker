import requests
from time import time, localtime

from pprint import pprint


def call_ymd():
    a = localtime(time())
    year = a.tm_year
    mon = a.tm_mon
    day = a.tm_mday
    return year*10000+mon*100+day


url = 'https://open.neis.go.kr/hub/mealServiceDietInfo'
params = {
    'type': 'json',
    'ATPT_OFCDC_SC_CODE': 'M10',
    'SD_SCHUL_CODE': '8000075',
    'MLSV_YMD': f'{call_ymd()}',
    'MMEAL_SC_CODE': '2'
}

raw_json = requests.get(url=url, params=params).json()
pprint(raw_json['mealServiceDietInfo'][1]['row'][0]['DDISH_NM'])