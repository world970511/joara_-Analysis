from konlpy.tag import Komoran
from collections import Counter
from wordcloud import WordCloud
import pandas as pd

def anlay1_count(li):
    count = Counter(li)  # 딕셔너리로 변경
    del count["0"]
    monthBest = count.most_common(10)  # 투베 등장 빈도수가 높은 10개만 반환
    return monthBest

def anlay2_wc(li,s,month):
    ko = Komoran()
    delete = [')', '(', ']', '[', '/', '이메일', '#', '계약작', '미계약작', '커미션', '메일', '작가님', '불펌', '표지', '팬아트',
              '독자님', '수정', '등록', '픽사베이', '문의', '상용가능', '이미지', '연재','none','때문에','그래서','너','우리',
              '하지만','여주','남주','나']
    for d in delete:
         if d in s: s.replace(d, '')

    str=' \n '.join(li)+s

    n = ko.morphs(str)
    for i, v in enumerate(n):
        if len(v) < 2:  # 글자 수가 2 이하인 명사 제외
            n.pop(i)

    count = Counter(n)  # 딕셔너리로 변경
    print(count)
    noun_list = count.most_common(50)  # 빈도수가 높은 50개의 어절만 리스트로 반환
    anlay2_wc_v(noun_list,month)#워드클라우드로 시각화

def  anlay2_wc_v(nl,month):
    # 서울남산장체 폰트를 사용하여 wordcloud를 만든다.
    wc = WordCloud(font_path='C:\\Users\\yhs04\\AppData\\Local\\Microsoft\\Windows\\Fonts\\서울남산 장체EB.ttf', \
                   background_color="white", \
                   width=1500, \
                   height=1000, \
                   max_words=100, \
                   max_font_size=300)

    wc.generate_from_frequencies(dict(nl))
    wc.to_file(str(month)+'월_제목/소개글_단어사용빈도_50.png')


if __name__ == "__main__":
    file = open('1-5.14 로판투베 10.txt', 'w', encoding='utf-8')
    f =pd.read_excel('1-5월14일_조아라_로판_투데이베스트_중복제거x.xlsx')
    f.fillna("0", inplace=True)
    f2=pd.read_excel('1-5월14일_조아라_로판_투데이베스트_소개글_중복제거x.xlsx')
    #s=''

    for i in range(1,6):
        li=f[str(i)+'월 로판 투데이베스트'].tolist()
        li2=f2[str(i)+'월 로판 투데이베스트'].tolist()
        file.writelines(str(i)+'월 로판 투데이베스트 10')
        for i in range (0,10):
            file.writelines('\n'+anlay1_count(li)[i][0]+"/빈도="+ str(anlay1_count(li)[i][1])+'\n')
        #anlay2_wc(li,s,i)



