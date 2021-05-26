from bs4 import BeautifulSoup as bs
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
import re
import urllib.request as req
import pandas as pd

def infoCount(url):
    infoList =[]
    st=''
    html = req.urlopen(url)
    rq = bs(html, "html.parser")
    for t in rq.select('td'):  # 베스트에 오른 로맨스판타지 북코드 추출
        if t.select('a')!=[]:
            i=str(t.select('a'))
            if '[로맨스판타지]'in i:
                infoUrl='http://www.joara.com/romancebl/'+re.sub('["<strong>]+\[+[\w]+\]+[</strong>]+.+[</a>]+\]','',i.replace('[<a href="/literature/',''))
                st=call_info(infoUrl)#소개글 전체 긁어오기
                infoList.append(st)
    return infoList


def call_info(infoUrl):#소개글 추출
    html = req.urlopen(infoUrl)
    rq = bs(html, "html.parser")
    try:
        info=str(rq.select_one('div.t_cont_v').text).replace('\r','').replace('\t','').replace('\n','')
        return info
    except AttributeError as e:
        return 'none'


def makeUrl(best, category, m, d, pagelist):#투데이베스트
    Info = []
    for i in range(1, d + 1):
        for i2 in pagelist:
            s = best + str(i2) + category + '&cur_year=2021&cur_month=' + str(m) + '&cur_day=' + str(i)
            Info += infoCount(s)
    return Info

if __name__ == '__main__':
    f2 = open('1-5월_통합_로판투데이베스트_소개글_중복제거.txt', 'w', encoding='utf-8')
    pagelist=[1,2,3,4,5]#1~100순위가 담긴 페이지 번호
    month=[1,2,3,4,5]#달
    days=[31,28,31,30,14]#날짜

    best='http://www.joara.com/best/today_best_list.html?page_no='# 조아라 투데이베스트 주소
    category='&sl_category=&sl_subcategory=series'#로판 장르/무료 연재분

    for m in month:
        li=makeUrl(best,category,m,days[m-1],pagelist)
        t=str(m)+'월_로판투데이베스트_소개글_중복제거.txt'

        f = open(t, 'w', encoding='utf-8')

        f.writelines('\n'.join(list(set(li))))#중복제거한 내용 텍스트파일로 저장
        f2.writelines('\n'.join(list(set(li))))  #소개글 통합
        print('pass')

    f.close()
    f2.close()