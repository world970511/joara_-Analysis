from bs4 import BeautifulSoup as bs
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
import re
import urllib.request as req
import pandas as pd
import os


def get_t_info(best,category,y,m,d,pagelist):
    ans_c = []
    for i in range (1,d+1):#url 주소 생성
        for i2 in pagelist:
            s = best + str(i2) + category +'&cur_year='+y+'&cur_month='+str(m)+'&cur_day='+str(i)
            ans_c+=craw(s)
    return ans_c

def craw(s):
    ans_c=[]
    html = req.urlopen(s)
    rq= bs(html, "lxml")
    get=rq.select('td.book_data_intro_form.subject_long > a')# 베스트에 오른 로맨스판타지 북코드추출
    for g in get:
        title=g.text.strip()
        if '[로맨스판타지]' in title:
            c_str=re.search('[<a href="/literature/view/book_intro.html?book_code=].+?>', str(g)).group()
            c_str=c_str.replace('<a href="/literature/view/book_intro.html?book_code=', '').replace('">', '')
            ans_c.append(c_str)
    return ans_c


if __name__ == '__main__':
    os.chdir('./infos/month_not_remove')

    pagelist=[1,2,3,4,5]#1~100순위가 담긴 페이지 번호
    month=[1,2,3,4,5,6,7,8,9,10,11,12]#달
    days=[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]#날짜
    best='http://www.joara.com/best/today_best_list.html?page_no='# 조아라 투데이베스트 주소
    category='&sl_category=&sl_subcategory=series'#로판 장르/무료 연재분

    try:
        year = input('몇년?(숫자만 적어주세요 ex(2021)): ')
        m=input('몇월?(숫자만 적어주세요): ')
        d= input('몇일?(숫자만 적어주세요): ')
    except:
        print("error!")

    t_df=pd.DataFrame()
    t2=[]

    for mon in month[:int(m)]:
        if mon!=m:
            li=get_t_info(best,category,year,mon,days[mon-1],pagelist)
        else:
            li = get_t_info(best, category, year, mon, d, pagelist)
        try:
            t_df['code']=li
            print('pass')
        except ValueError:#ValueError가 있을 경우
            t_df['code']= pd.Series(li)
            print('pass')

        t_df.to_csv(str(mon)+"월_조아라_로판_투데이베스트_목록(중복있음).txt",mode='w' ,sep='\t', index=False)
