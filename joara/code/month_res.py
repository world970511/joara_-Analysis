from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import plotly
import plotly.graph_objects as go
import os
import pandas as pd
import chart_studio
chart_studio.tools.set_credentials_file(username='', api_key='')


from chart_studio.plotly import plot, iplot

def anlay1_count(li):
    count = Counter(li)  # 딕셔너리로 변경
    monthBest = count.most_common(20)  # 투베 등장 빈도수가 높은 20개만 반환
    return dict(monthBest)

def anlay2_wc(m_t,m_i,m):
    okt = Okt()
    total=[]
    stopwords = ['의', '가', '이', '은', '들', '는', '좀', '원', '권', '과', '도', '를', '으로', '자', '에', '와', '한', '하다', '우리', '제',
                 '금','너','나','당신','그녀','남자','을','의','하는','했다','하고','게','아','제','때문','보다','니까','합니다','없이','같다','한테',
                 '소리','그렇게','그리고','얼굴','서','그런','모든','기억','이제','였다','상태','가만히','어쩌다','얼마나','서로','시점','이내','왜','다'
                 '남다','있다','이다','없다','되다','아니다','않다','에서','그렇다','에게', '되어다','내','버리다','들다','버리다','들다','죽다','사람',
                 '가다','생각','나르다','정말', '이번''이라고','그런데','싶다','지다','모르다','좋다','알다','말다','그래서','그것','처럼','것','주다','부터'
                 '그','사랑','리다','말','다시','하나','위해','고','세계','시작','인','진짜','갑자기','로','입술','상황','생활','상관','해도','준비','리다',
                 '한국','아래','여주','남주','부터','주의','이자','예정','거리','누가','주가','세상','자신','무슨','사실','다른','마음','그대','마지막','그냥',
                 '생기','정도','순간','거지','등장','사이','얼마','오늘','내일','모레','인간','이상','사이','가의','오히려','최고','온갖','출처','계획','잘못','당장']


    for sentence in m_t+m_i:
        temp_X = okt.morphs(sentence, stem=True)  # 토큰화
        temp_X = [word for word in temp_X if not word in stopwords]  # 불용어 제거
        total.append(' '.join(temp_X))

    ans=[]
    for t in total:
         ans+=okt.nouns(t)

    count = Counter(ans)  # 딕셔너리로 변경

    for c in list(count):
        if len(c[0])<2 :#단어 길이가 4보다 크거나 2보다 작으면 제거
            del count[c[0]]

    del count['여주']
    del count['남주']
    del count['주인공']
    del count['리다']
    del count['이번']
    del count['모두']
    print(count)

    noun_list = count.most_common(50)  # 빈도수가 높은 50개의 단어만 리스트로 반환

    # 서울남산장체 폰트를 사용하여 wordcloud를 만든다.
    wc = WordCloud(font_path='C:\\Users\\yhs04\\AppData\\Local\\Microsoft\\Windows\\Fonts\\서울남산 장체EB.ttf', \
                   background_color="white", \
                   width=1500, \
                   height=1000, \
                   max_words=100, \
                   max_font_size=300)

    wc.generate_from_frequencies(dict(noun_list))
    f_name='C:\\Users\\yhs04\\PycharmProjects\\joara_1\\result\\'+str(m)+'월_제목_소개글_단어사용빈도_50.png'
    wc.to_file(f_name)


if __name__ == "__main__":
    os.chdir('./infos/month_not_remove')
    li = os.listdir()
    m=1
    for i in li:
        data=pd.read_table(i)['title'].tolist()
        month_res= anlay1_count(data)
        fig = go.Figure([go.Bar(x=list(month_res.keys()), y=list(month_res.values()))])
        fig.update_layout(title_text=str(m)+'월 조아라 로판 투베 등장 빈도 20')
        plotly.offline.plot(fig, filename='C:\\Users\\yhs04\\PycharmProjects\\joara_1\\result\\'+str(m)+'_result.html')
        plot(fig, filename='C:\\Users\\yhs04\\PycharmProjects\\joara_1\\result\\'+str(m)+'_result.html', auto_open=True)
        m+=1

    os.chdir(r'C:\Users\yhs04\PycharmProjects\joara_1\infos\month_remove')
    li2= os.listdir()
    m2=1
    for i in li2:
        data = pd.read_table(i)
        anlay2_wc(data['title'].tolist(),data['info'].tolist(),m2)
        m2+=1





