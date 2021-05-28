from bs4 import BeautifulSoup as bs
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
import urllib.request as req
import pandas as pd
import os

def call_info(infoUrl):#소개글 추출
    ans=[]
    for i in infoUrl:
        html = req.urlopen(i)
        rq = bs(html, "html.parser")
        try:
            text=rq.select_one('div.t_cont_v').text
            info=str(rq.select_one('div.t_cont_v').text).replace('\r','').replace('\t','').replace('\n','')
            ans.append(info)
        except AttributeError as e:
            ans.append('none')
    return ans


if __name__ == '__main__':
    os.chdir('./infos')
    li = os.listdir()

    for i,s in enumerate (li):
        data = pd.read_table(s)
        print('초반 데이터 확인 :', len(data))

        data.drop_duplicates(subset=['code'], inplace=True)  # 중복된 리뷰들을 제거한다
        print('중복 제거 확인 :', len(data))

        info_li =call_info(data['code'].tolist())
        try:
            data['info'] = info_li
            print('pass')
        except ValueError:  # ValueError가 있을 경우
            data['info'] = pd.Series(info_li)
            print('pass')

        data.to_csv(str(i+1) + "월 조아라 로판 투데이베스트 목록(중복있음).txt", mode='w', sep='\t', index=False)