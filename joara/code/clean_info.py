import os
import re
import numpy as np
import pandas as pd

def stopwords(data):
    stop =['이메일', '계약작', '미계약작', '커미션', '메일', '작가', '불펌', '표지', '팬아트', '독자님', '수정', '등록', '픽사베이',
    '문의', '상용가능', '이미지', '연재', '이전','작가','독자','업로드', '월','화','수','목','금','토','일','고정','부정기','정기',
    '취향','물','트위터','sns','소통','그림','소개글','키워드','런칭','확정 ', '정식','쪽지','스푼','출간','님','자급자족','후보',
     '노블레스','키워드','금']

    for s in stop:
        data= data.apply(lambda x: x.replace(s, " "))  # 계약 및 연재 관련 단어 제거

    data = data.apply(lambda x: x.replace('19', "십구금"))
    data = data.apply(lambda x: x.replace('bl', "비엘"))
    data = data.apply(lambda x: x.replace('BL', "비엘"))
    data = data.apply(lambda x: x.replace('RPG게임', "롤플레잉게임"))
    data = data.apply(lambda x: x.replace('rpg게임', "롤플레잉게임"))
    return data

if __name__ == '__main__':
        os.chdir('.\infos\month_remove')
        li = os.listdir()

        for i in li:
            data = pd.read_table(i)

            # 훈련 데이터에서 한글과 공백을 제외하고 제거
            data = data.fillna(" ")
            #소개글 정리
            data['info']=stopwords(data['info'])
            data['info'] = data['info'].apply(lambda x: re.sub(r"[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", " ", x))#한국어 이외 제거
            data = data.apply(lambda x: x.replace('\s+', " "))  # 공백이 2개 이상일 때 하나로 변경
            data['info'].replace('', np.nan, inplace=True)#null제거

            data['title']=stopwords(data['title'])
            data['title'] = data['title'].apply(lambda x: re.sub(r"[^ㄱ-ㅎㅏ-ㅣ가-힣]", " ", x))#한국어 이외 제거
            data['title'] = data['title'].apply(lambda x: re.sub(r'\([a-zA-Zㄱ-ㅎㅏ-ㅣ가-힣0-9_-]+?\)', "", x))  # 공지 관련 제거
            data['title'].replace('', np.nan, inplace=True)  # null제거


            data.to_csv(i, mode='w',sep='\t', index=False)