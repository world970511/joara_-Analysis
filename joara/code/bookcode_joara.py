import time
from bs4 import BeautifulSoup as bs
import warnings
from calendar import monthrange
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
import re
import urllib.request as req
import os

def get_t_info1(best,category,y,m,d,pagelist):#시작 외의 날짜
    ans_c = []
    for i in range (1,d+1):#url 주소 생성
        for i2 in pagelist:
            s = best + str(i2) + category +'&cur_year=2021'+str(y)+'&cur_month='+str(m)+'&cur_day='+str(i)
            ans_c+=craw(s)
    return ans_c

def get_t_info2(best,category,y,m,d,d2,pagelist):#시작 날짜
    ans_c = []
    for i in range (d,d2+1):#url 주소 생성
        for i2 in pagelist:
            s = best + str(i2) + category +'&cur_year=2021'+y+'&cur_month='+str(m)+'&cur_day='+str(i)
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
    os.chdir('./infos/bookcode')

    pagelist=[1,2,3,4,5]#1~100순위가 담긴 페이지 번호
    best='http://www.joara.com/best/today_best_list.html?page_no='# 조아라 투데이베스트 주소
    category='&sl_category=&sl_subcategory=series'#로판 장르/무료 연재분

    print("찾으시려는 년도 내의 데이터만 수집 가능합니다")
    t = time.time()
    today = time.strftime("%Y-%m-%d", time.gmtime(t)).split('-')
    while True:
        year = int(input('찾으시려는 년도를 말해주세요:'))
        if year > int(today[0]):#년도가 올해 년도보다 클 경우
            print('===================================')
            print('찾을 수 없는 년도입니다. 다시 입력하세요.')
            print('===================================')
            continue
        else:break
    while True:
        start =input('언제부터?(월/일 형식으로 적어주세요 ex(7/7)): ').split('/')
        end=input('언제까지?(월/일 형식으로 적어주세요 ex(7/16)): ').split('/')
        if int(end[0])>int(today[1]):#입력된 기한의 끝의 월이 이번 달보다 클 경우
            print('===================================')
            print('찾을 수 없는 날짜입니다. 다시 입력하세요.')
            print('===================================')
            continue
        elif int(end[0])==int(today[1]) and int(end[1])>int(today[2]):#입력된 기한의 월이 이번 달인데 날짜가 오늘보다 클 경우
            print('===================================')
            print('찾을 수 없는 날짜입니다. 다시 입력하세요.')
            print('===================================')
            continue
        elif end[0]=='' or end[1]==''or end[0]=='0' or end[1]=='0' or start[0]=='' or start[1]==''or start[0]=='0' or start[1]=='0':
            print('===================================')
            print('잘못 입력하셨습니다. 다시 입력하세요')
            print('===================================')
            continue
        else:break


    try:
        for mon in range(int(start[0]),int(end[0])+1):
            if mon!=int(start[0]) or mon!=int(end[0]):
                d=monthrange(year, mon)[1]
                li=get_t_info1(best,category,year,mon,d,pagelist)
                with open(str(year) + '-' + str(mon) + '-' + str(1) + '_' + str(year) + '-' + str(mon) + '' + str(d) + '_북코드.txt', 'w', encoding='utf-8')as f:
                    f.writelines('\n'.join(li))
            else:
                if mon==int(start[0]):
                    d = monthrange(year, mon)[1]
                    li = get_t_info2(best, category, year, mon, start[1],d,pagelist)
                    with open(str(year) + '-' + str(mon) + '-' + start[1] + '_' + str(year) + '-' + str(mon) + '-' + str(d)+ '_북코드.txt', 'w', encoding='utf-8')as f:
                        f.writelines('\n'.join(li))
                else:
                    get_t_info1(best, category, year, mon, end[1], pagelist)
                    with open(str(year)+'-'+str(mon)+'-'+start[1]+'_'+str(year)+'-'+str(mon)+'-'+end[1]+'_북코드.txt', 'w', encoding='utf-8')as f:
                        f.writelines('\n'.join(li))
            print('pass')
    except:print('error. 확인 부탁드립니다')
    print("폴더를 확인해주세요")

