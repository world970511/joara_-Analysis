import os
import re
from konlpy.tag import Komoran

def stopwords(str):
    okt = Komoran()

    stop =['이메일', '계약작', '미계약작', '커미션', '메일', '작가님', '불펌', '표지', '팬아트', '독자님', '수정', '등록', '픽사베이',
    '문의', '상용가능', '이미지', '연재', '이전','작가','독자','업로드', '월','화','수','목','금','토','일','고정','부정기','정기',
    '취향','여주','남주', '주인공','주의','사람','우리','너','나','는','기억','사랑','연애','email','트위터','sns','소통','그림','twt',
     '소개글','프롤로그','키워드','twitter','by']

    st= okt.morphs(str)  # 토큰화
    st= [w for w in st if not w in stop]  # 불용어 제거

    return " ".join(st)



if __name__ == '__main__':
        os.chdir(r'C:\Users\yhs04\PycharmProjects\joara_1\infos')
        with open('test.txt', 'r', encoding='utf-8')as f:
            li2 = f.read()
            li2=re.sub(r'[a-zA-Z0-9_-]+@[a-z]+.[a-z]+','',li2)#메일주소 제거
            li2=re.sub(r'[^a-zA-Zㄱ-ㅎㅏ-ㅣ가-힣 ]', '', li2)#한글과 영어, 공백을 제외한 모두를 제거
            li2=stopwords(li2)
        with open('test - 복사본 - 복사본.txt', 'w', encoding='utf-8')as f:
            f.write(li2)
