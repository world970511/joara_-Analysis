from bs4 import BeautifulSoup as bs
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
import re
import urllib.request as req
import pandas as pd
import os

def call_info(infoUrl):#소개글/제목 추출
    site='http://www.joara.com/romancebl/view/book_intro.html?book_code='
    ifFinish='http://www.joara.com/finish/view/book_intro.html?book_code='
    total=[]

    for iu in infoUrl:
        part = []
        html = req.urlopen( site + str(iu))
        rq = bs(html, "lxml")

        try:#AttributeError- 완결된 소설일 경우
            rq.select_one('em.ico_new > a').text
        except:
            html = req.urlopen(ifFinish+ str(iu))
            rq = bs(html, "lxml")

        part.append(iu.replace('\n',''))
        # 제목 추출
        t=re.sub('[<a href="]+.+?[">]','',str(rq.select_one('em.ico_new > a')).replace('</a>','').replace('>',''))
        part.append(t)

        #소개글 추출
        i=remove(str(rq.select_one('div.t_cont_v')))
        part.append(i)
        total.append(part)

    return total

def remove(str):
    remove1= ['<br/>', '<div class="t_cont_v">', '</div>', '\r', '\t', '&lt', '&gt','*']
    remove2=['\n','#','/', '[', ']' , '(' , ')']
    for r in remove1:
        str=str.replace(r,'')
    for r in remove2:
        str = str.replace(r, ' ')
    return  str

if __name__ == '__main__':
    all_data=pd.DataFrame(columns=['code','title','info'])
    os.chdir('./infos/bookcode')
    li = os.listdir()
    m=4

    for i in li:
        print(i)
        with open(i,mode='r',encoding='utf-8') as f:
            f_li= f.readlines()
        info_li =call_info(f_li)#월별 북코드를 통해 소개글/제목 추출
        infodata=pd.DataFrame(info_li,columns=['code','title','info'])
        print(infodata)
        infodata.to_csv(str(m)+'_조아라_로판_투데이베스트_목록(중복있음).txt', mode='w', sep='\t', index=False)

        # 중복제거 및 null 제거
        print('초반 데이터 확인 :', len(infodata))

        infodata = infodata.dropna(how='any')  # Null 값이 존재하는 행 제거
        print('null값이 존재하는가?=', infodata.isnull().values.any())  # Null 값이 존재하는지 확인

        infodata.drop_duplicates(subset=['code'], inplace=True)  # 중복된 소설들을 제거한다
        print('제거 확인 :', len(infodata))
        infodata.to_csv(str(m)+'_조아라_로판_투데이베스트_목록(중복제거).txt', mode='w',sep='\t', index=False)
        m+=1
        print('========pass=========')




