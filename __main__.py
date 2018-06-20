import urllib
from ctypes import WinError
from itertools import count

import sys
from urllib.error import HTTPError

from bs4 import BeautifulSoup

import xml.etree.ElementTree as et
import collection.crawler as cw
import pandas as pd

def crawling_pelicana():
    results = []
    RESULT_DIRECTORY = '__result__'
    # for page in count(start=1):
    for page in range(1, 3):
        url = 'http://pelicana.co.kr/store/stroe_search.html?gu=&si='
        html = cw.crawling(url=url)
        # print(html)

        bs = BeautifulSoup(html, 'html.parser')
        tag_table = bs.find('table', attrs={'class' : 'table mt20'})

        # print(bs, file=sys.stderr)
        # print(tag_table, file=sys.stderr)

        tag_tbody = tag_table.find('tbody')
        # print(tag_tbody)
        tags_tr = tag_tbody.findAll('tr')
        # print(tags_tr)

        # print(tags_tr)
        print(page, ":", len(tags_tr), sep=':')

        # 끝 검출
        if len(tags_tr) == 0:
            break

        # print(page, ":", len(tags_tr), sep=':')

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            # print(strings, type(strings))
            name = strings[1]
            address = strings[3]
            # print(address.split())
            sidogu = address.split()[:2]

            results.append( (name, address) + tuple(sidogu) )

    # store
    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gungu'])
    table.to_csv('{0}/pelicana_table.csv'.format(RESULT_DIRECTORY))
    # print(results)

def proc_nene(xml):
    root = et.fromstring(xml)
    element_items = root.findall('item')
    print(element_items)

    results = []
    for element_item in element_items:
        name = element_item.findtext('aname1')
        gungu = element_item.findtext('aname2')
        sido = element_item.findtext('aname3')
        address = element_item.findtext('aname5')

        results.append((name, address, sido, gungu))

    return results

def store_nene(data):
    print(data)
    RESULT_DIRECTORY = '__result__'
    # store
    table = pd.DataFrame(data, columns=['name', 'address', 'sido', 'gungu'])
    # print(table)
    table.to_csv('{0}/nene.csv'.format(RESULT_DIRECTORY))


def preprocessing_kyochon(response):
    # 기본 골자는 이렇다. ##############################################################################################
    # 리스트 안에 튜플들의 집합으로 최종데이터를 추출해내고, 이를 pandas의 데이터프레임을 사용하여 csv 파일로 저장한다.
    # 리스트 안에 튜플들의 집합으로 원하는 데이터를 지정하여 파일에 쓰는 과정을 써넣으면 된다.
    # 이 함수는 디코딩 된 http 응답을 받아 html 문서로부터 데이터를 크롤링 하는 과정을 정의한다.
    # 함수의 관리는 collection.crawler 에서 하고 있다.
    ####################################################################################################################

    bs4_result = BeautifulSoup(response, 'html.parser')

    tag_table = bs4_result.find('div', attrs={'class' : 'shopSchList'})

    shop_list = tag_table.findAll('li')

    results = []
    for shop in shop_list:

        name = shop.find('dt').string
        string_location = shop.find('dd').get_text().replace('\r', '').replace('\n', '').replace('\t', '')
        address = string_location[:string_location.find('(')]

        d = string_location.split(' ', 2)
        sido = d[0]
        gungu = d[1]

        results.append((name, address, sido, gungu))

    print(results)

    return results

def store_kyochon(data):
    RESULT_DIRECTORY = '__result__'

    table = pd.DataFrame(data, columns=['name', 'address', 'sido', 'gungu'])
    table.to_csv('{0}/kyochon_table.csv'.format(RESULT_DIRECTORY))

def crawling_kyochon():

    # ##################################################################################################################
    # 이 함수는 데이터의 존재여부를 판단하여 루프를 도는 제어문만을 포함하도록 한다. ###################################
    # 데이터의 전처리 및 저장은 별도의 함수를 사용하도록 한다 ##########################################################
    # 전처리 : preprocessing_kyochon, 저장 : store_kyochon #############################################################
    ####################################################################################################################
    total = []
    for sido1 in range(1, 18):
        condition = True
        results = []
        for sido2 in count(start=1):
            url = 'http://www.kyochon.com/shop/domestic.asp?sido1={0}&sido2={1}&txtsearch='.format(sido1, sido2)
            result = cw.crawling(url, proc = preprocessing_kyochon)

            if result == None:
                break
            else:
                results.extend(result)
                continue

        total.extend(results)

    print(total)
    store_kyochon(total)

if __name__ == '__main__':
    # pelicana
    # crawling_pelicana()

    # nene
    # cw.crawling(
    #     url = 'http://nenechicken.com/subpage/where_list.asp?target_step2=%s&proc_type=step1&target_step1=%s' % (urllib.parse.quote('전체'), urllib.parse.quote('전체')),
    #     proc = proc_nene,
    #     store = store_nene
    # )

    # kyochon
    crawling_kyochon()
