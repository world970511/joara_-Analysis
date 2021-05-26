from bs4 import BeautifulSoup as bs
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
import re
import urllib.request as req
import pandas as pd

def titleCount(url):
    titleList=[]
    html=req.urlopen(url)
    rq= bs(html, "html.parser")
    for t in rq.select('a'):# 베스트에 오른 로맨스판타지 제목 추출
        title=t.text.strip()
        if '[로맨스판타지]' in title:
            titleList.append(re.sub('\<\d.+?\>','',title.replace("[로맨스판타지]","")))
    return titleList


def makeUrl(best,category,m,d,pagelist):
    Title=[]
    for i in range (1,d+1):
        for i2 in pagelist:
            s = best + str(i2) + category +'&cur_year=2021&cur_month='+str(m)+'&cur_day='+str(i)
            Title += titleCount(s)
    return Title

if __name__ == '__main__':
    f=open('1-5월_조아라_로판_투데이베스트_제목.txt','w',encoding='utf-8')
    pagelist=[1,2,3,4,5]#1~100순위가 담긴 페이지 번호
    month=[1,2,3,4,5]#달
    days=[31,28,31,30,17]#날짜
    best='http://www.joara.com/best/today_best_list.html?page_no='# 조아라 투데이베스트 주소
    category='&sl_category=&sl_subcategory=series'#로판 장르/무료 연재분
    t_df=pd.DataFrame()
    t2=[]
    for m in month:
        li=makeUrl(best,category,m,days[m-1],pagelist)
        try:
            t_df[str(m)+'월 로판 투데이베스트']=li#중복을 허용한 목록
            f.writelines('\n'.join(list(set(li))))#중복을 허용하지 않는 목록
            print('pass')
        except ValueError:#ValueError가 있을 경우
            t_df[str(m)+'월 로판 투데이베스트'] = pd.Series(li)#중복을 허용한 목록
            f.writelines('\n'.join(list(set(li))))#중복을 허용하지 않는 목록
            print('pass')

    #엑셀 파일로 저장
    with pd.ExcelWriter('1-5월14일_조아라_로판_투데이베스트_중복제거x.xlsx',mode='w',engine= 'openpyxl') as writer:
        t_df.to_excel(writer,index=False,sheet_name='제목')
    f.close()
