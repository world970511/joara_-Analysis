from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import os
import pandas as pd

def anlay1_count(li):
    count = Counter(li)  # 딕셔너리로 변경
    del count["0"]
    monthBest = count.most_common(10)  # 투베 등장 빈도수가 높은 10개만 반환
    return monthBest

def anlay2_wc(month,m):
    ko = Okt()
    n = ko.morphs(str)
    okt = Okt()
    stopwords = ['의', '가', '이', '은', '들', '는', '좀', '원', '권', '과', '도', '를', '으로', '자', '에', '와', '한', '하다', '여', '남',
                 '녀','을','를','너','나']

    li = []
    for sentence in month['info']:
        temp_X = okt.morphs(sentence, stem=True)  # 토큰화
        temp_X = [word for word in temp_X if not word in stopwords]  # 불용어 제거
        li.append(temp_X)

    for sentence in month['title']:
        temp_X = okt.morphs(sentence, stem=True)  # 토큰화
        temp_X = [word for word in temp_X if not word in stopwords]  # 불용어 제거
        li.append(temp_X)

    for i, v in enumerate(li):
        if len(v) < 2:  # 글자 수가 2 이하인 것 제외
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
    wc.to_file(str(m)+'월_제목/소개글_단어사용빈도_50.png')


if __name__ == "__main__":
    all_data=pd.DataFrame(columns=['title','info'])
    os.chdir('./infos/month_not_remove')
    li = os.listdir()
    m=1
    for i in li:
        print(i,'\n')
        data=pd.read_table(i)
        print(anlay1_count(data['title'].tolist()))

        # 중복된 책을 제거한다
        print('초반 데이터 확인 :', len(data))
        data.drop_duplicates(subset=['title'], inplace=True)
        print('중복 제거 확인 :', len(data))
        # Null 값이 존재하는 행 제거
        data = data.dropna(how='any')
        print('null값이 존재하는가?=', all_data.isnull().values.any())  # Null 값이 존재하는지 확인
        all_data = pd.concat([all_data, data], ignore_index=True, axis=0)
        anlay2_wc(data,m)
        m+=1
        print('\n===================\n')

    all_data.to_csv('1/1~5/31_조아라_투베_로맨스판타지_중복제거.txt',mode='w' ,sep='\t', index=False)




