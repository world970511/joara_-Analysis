import os
import re
import numpy as np
import pandas as pd

def stopwords(data):
    stop =['이메일', '계약작', '미계약작', '커미션', '메일', '작가님', '불펌', '표지', '팬아트', '독자님', '수정', '등록', '픽사베이',
    '문의', '상용가능', '이미지', '연재', '이전','작가','독자','업로드', '월','화','수','목','금','토','일','고정','부정기','정기',
    '취향','여주','남주', '주인공','물','email','트위터','sns','소통','그림','twt','소개글','키워드','twitter','by','none','런칭']

    for s in stop:
        data['info'] = data['info'].apply(lambda x: re.sub(s, "", x))  # 계약 및 연재 관련 단어 제거

    return data['info']


if __name__ == '__main__':
        os.chdir('.\infos\month_not_remove')
        li = os.listdir()

        for i in li:
            data = pd.read_table(i)

            # 훈련 데이터에서 한글과 공백을 제외하고 제거
            data = data.fillna(" ")
            data['info'] = data['info'].apply(lambda x: re.sub(r'[a-zA-Z0-9_-]+@[a-z]+.[a-z]+', "", x))#메일주소 제거
            data['info'] = data['info'].apply(lambda x: re.sub(r"[^a-zA-Zㄱ-ㅎㅏ-ㅣ가-힣 ]", "", x))#특수문자 제거
            data['info']=stopwords(data['info'])
            data['info'].replace('', np.nan, inplace=True)
            data['title'] = data['title'].apply(lambda x: re.sub(r'\(.+?\)', "", x))  # 공지 관련 제거
            data.to_csv()