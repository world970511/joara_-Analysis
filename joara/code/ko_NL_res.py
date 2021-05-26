from konlpy.tag import Komoran
from collections import Counter
from wordcloud import WordCloud
import re

def noun(li):
    k= Komoran()
    n= k.nouns(li)
    for i, v in enumerate(n):
        if len(v) < 2:#글자 수가 2 이하인 어절 제외
            n.pop(i)

    count = Counter(n)#딕셔너리로 변경
    ph_list = count.most_common(50)#빈도수가 높은 100개의 어절만 리스트로 반환
    return ph_list


def visual(ph_list):#서울남산장체 폰트를 사용하여 wordcloud를 만든다.
    wc = WordCloud(font_path='C:\\Users\\yhs04\\AppData\\Local\\Microsoft\\Windows\\Fonts\\서울남산 장체EB.ttf', \
                   background_color="white", \
                   width=1500, \
                   height=1000, \
                   max_words=100, \
                   max_font_size=300)

    wc.generate_from_frequencies(dict(ph_list))
    wc.to_file('keyword.png')

def clean_text(text):
    delete =  ['이메일', '계약작', '미계약작', '커미션', '메일', '작가님', '불펌', '표지', '팬아트', '독자님', '수정', '등록', '픽사베이', '문의', '상용가능',
               '이미지', '연재', '이전','작가','독자','업로드','월','화','수','목','금','토','일','고정','부정기','정기']
    for d in delete:
        if d in text==0:
            text.replace(d,'')
            print("a")
    return text

if __name__ == "__main__":
    with open('1-4월_조아라_로판_투데이베스트_제목.txt', 'r', encoding='utf-8')as f:
        li = f.read()
    with open('1-4월_조아라_로판_투데이베스트_소개글.txt','r',encoding='utf-8')as f2:
        li2= " ".join(f2.readlines())
        ct=clean_text(li2)
    li+='/n'+ct
    noun_list = noun(li)
    visual(noun_list)

