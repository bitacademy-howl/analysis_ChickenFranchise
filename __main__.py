import urllib
from ctypes import WinError
from itertools import count

import sys
from urllib.error import HTTPError

import time

from datetime import datetime
from bs4 import BeautifulSoup

import xml.etree.ElementTree as et

from selenium import webdriver

import collection.crawler as cw
import pandas as pd

from data_dict import sido_dict, gungu_dict

RESULT_DIRECTORY = '__result__'

def crawling_pelicana():
    results = []
    RESULT_DIRECTORY = '__result__'
    for page in count(start=1):
    # for page in range(1, 3):
        url = 'http://pelicana.co.kr/store/stroe_search.html?gu=&si=&page={0}'.format(page)
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
    table['sido'] = table.sido.apply(lambda v: sido_dict.get(v, v))
    table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))
    table.to_csv('{0}/pelicana_table.csv'.format(RESULT_DIRECTORY))
    # print(results)

def proc_nene(xml):
    root = et.fromstring(xml)
    element_items = root.findall('item')
    # print(element_items)

    results = []
    for element_item in element_items:
        name = element_item.findtext('aname1')
        gungu = element_item.findtext('aname3')
        sido = element_item.findtext('aname2')
        address = element_item.findtext('aname5')

        results.append((name, address, sido, gungu))

    return results

def store_nene(data):
    # store
    table = pd.DataFrame(data, columns=['name', 'address', 'sido', 'gungu'])

    table['sido'] = table.sido.apply(lambda v: sido_dict.get(v, v))
    table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))

    # print(table)
    table.to_csv('{0}/nene_table.csv'.format(RESULT_DIRECTORY))


def preprocessing_kyochon(response):
    # 기본 골자는 이렇다. ##############################################################################################
    # 리스트 안에 튜플들의 집합으로 최종데이터를 추출해내고, 이를 pandas의 데이터프레임을 사용하여 csv 파일로 저장한다.
    # 리스트 안에 튜플들의 집합으로 원하는 데이터를 지정하여 파일에 쓰는 과정을 써넣으면 된다.
    # 이 함수는 디코딩 된 http 응답을 받아 html 문서로부터 데이터를 크롤링 하는 과정을 정의한다.
    # 함수의 관리는 collection.crawler 에서 하고 있다.
    ####################################################################################################################

    bs4_result = BeautifulSoup(response, 'html.parser')

    # 페이지가 존재하지 않을 경우 디폴트 리스폰스는 div 태그가 존재하지 않으며,
    # 아래의 함수 find()는 Null을 리턴하게 된다.
    #
    # 아래는 http응답으로 전송되는 html 문서
    #  <font face="Arial" size=2>
    # <p>Microsoft VBScript ��Ÿ�� ����</font> <font face="Arial" size=2>���� '800a0009'</font>
    # <p>
    # <font face="Arial" size=2>÷�� ����� �߸��Ǿ����ϴ�.: '[number: 25]'</font>
    # <p>
    # <font face="Arial" size=2>/shop/domestic.asp</font><font face="Arial" size=2>, �� 87</font>


    tag_table = bs4_result.find('div', attrs={'class' : 'shopSchList'})

    shop_list = tag_table.findAll('li')

    results = []
    for shop in shop_list:

        # 'NoneType' object has no attribute 'string', AttributeException 발생가능
        # 프로그램 흐름 상 crawler 에서 호출하고 있고, crawler 에서 예외처리가 가능하므로
        # 크롤러에서 해당 exception 발생 시 함수를 수행하지 않고 pass 하도록 처리하여주는 것이 필요하다
        name = shop.find('dt').string

        string_location = shop.find('dd').get_text().replace('\r', '').replace('\n', '').replace('\t', '')
        address = string_location[:string_location.find('(')]

        d = string_location.split(' ', 2)
        sido = d[0]
        gungu = d[1]

        results.append((name, address, sido, gungu))

    # print(results)

    return results

def store_kyochon(data):

    table = pd.DataFrame(data, columns=['name', 'address', 'sido', 'gungu'])

    table['sido'] = table.sido.apply(lambda v: sido_dict.get(v, v))
    table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))

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

def store_goobne(data):

    table = pd.DataFrame(data, columns=['name', 'address', 'sido', 'gungu'])

    table['sido'] = table.sido.apply(lambda v: sido_dict.get(v, v))
    table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))

    table.to_csv('{0}/goobne_table.csv'.format(RESULT_DIRECTORY), encoding='utf-8', mode='w', index=True)

def crawling_goobne(store=None):
# def crawling_goobne():
    url = 'https://www.goobne.co.kr/store/search_store.jsp'

    # 첫 페이지 로딩
    wd = webdriver.Chrome('D:\Howl_Bit\program files\chromedriver\chromedriver.exe')
    wd.get(url)
    time.sleep(5)

    results = []
    # for page in range(1, 3):
    for page in count(start=1):
        # 자바 스크립트 실행
        script = 'store.getList(%d)' % page
        wd.execute_script(script)
        print('%s : success for script execute [%s]' % (datetime.now(), script))
        time.sleep(1)

        # 실행결과 HTML(rendering 된 HTML) 가져오기
        html = wd.page_source

        # parsing with bs4
        bs = BeautifulSoup(html, 'html.parser')
        tag_tbody = bs.find('tbody', attrs={'id' : 'store_list'})
        tags_tr = tag_tbody.findAll('tr')

        # 마지막 검출
        if tags_tr[0].get('class') is None:
            break

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            name = strings[1]
            address = strings[6]
            sidogu = address.split()[:2]
            # 아래와 동일하게 동작한다. 디폴트의 기준에 대해서는 string.split() 한번 더 찾아볼 것
            # sidogu = address.split(' ')[:2]

            results.append( (name, address) + tuple(sidogu) )

            # print(strings)
        # print(tag_tbody)
    # print(results)

    if callable(store):
        store(results)

    return results

if __name__ == '__main__':
    # pelicana
    # crawling_pelicana()

    # nene
    cw.crawling(
        url = 'http://nenechicken.com/subpage/where_list.asp?target_step2=%s&proc_type=step1&target_step1=%s' % (urllib.parse.quote('전체'), urllib.parse.quote('전체')),
        proc = proc_nene,
        store = store_nene
    )

    # # kyochon
    # crawling_kyochon()
    #
    # # goobne
    # crawling_goobne(store_goobne)

