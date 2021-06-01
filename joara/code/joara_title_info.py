from bs4 import BeautifulSoup as bs
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
import urllib.request as req
import pandas as pd
import os

def call_info(infoUrl):#소개글/제목 추출
    site='http://www.joara.com/romancebl/view/book_intro.html?book_code='
    info=[]
    title=[]
    for iu in infoUrl:
        html = req.urlopen(site+str(iu))
        rq = bs(html, "lxml")
        try:
            # 제목 추출
            t=str(rq.select_one('em.ico_new').text)
            title.append(t)
            #소개글 추출
            i=str(rq.select_one('div.t_cont_v').text).replace('\r','').replace('\t','').replace('\n','')
            info.append(i)
        except AttributeError as e:
            info.append('none')#소개글이 뽑히지 않을 경우 None
        print(zip(title,info))
    return zip(title,info)


if __name__ == '__main__':
    os.chdir('./infos/month_not_remove')
    li = os.listdir()

    for i in li:
        print(i)
        data = pd.read_table(i)
        info_li =call_info(data['code'].tolist())#월별 북코드를 통해 소개글/제목 추출

        data=pd.DataFrame(info_li,columns=['title','info'])
        data.to_csv(i, mode='w', sep='\t', index=False)
        print('pass\n=========')

