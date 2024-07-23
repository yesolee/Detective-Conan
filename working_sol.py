# 0. 패키지 로드
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 1. 데이터 파일 불러오기, 원본 데이터 복사하기
## UnicodeDecodeError 발생: encoding 지정
## 0번째 데이터를 열의 이름으로 지정하고 싶음: 89p. header속성 
df=pd.read_csv('crime.csv', header = 1, encoding='EUC-KR')
df.head()

# 2. 원본 데이터 복사하기(deepcopy로 원본유지)
crime = df.copy()

# 3. 변수명 바꾸기
crime.columns
## 강력범죄는 s, 폭력범죄는 g, 지능범죄는 i로 시작하고 싶음 
## 글자 바꾸기: replace, 리스트+리스트=리스트, 변수할당 적용
crime.columns = ['year','day']\
                + [i.replace(i, "s"+i) for i in crime.columns[2:10]]\
                + [i.replace(i, "g"+i) for i in crime.columns[10:18]]\
                + [i.replace(i, "i"+i) for i in crime.columns[18:27]]
crime.columns
## 행의 요일을 영어로 한번에 바꾸기 :replace()
crime = crime.replace({'월요일':'mon',
                       '화요일':'tue',
                       '수요일':'wed',
                       '목요일':'thu',
                       '금요일':'fri',
                       '토요일':'sat',
                       '일요일':'sun'})
crime.head(7)

## 행의 순서 바꾸기(일>토에서 월>일로): reindex()
len(crime)
crime = crime.reindex([1,2,3,4,5,6,0,
                       8,9,10,11,12,13,7,
                       15,16,17,18,19,20,14,
                       22,23,24,25,26,27,21,
                       29,30,31,32,33,34,28])
crime.head(7)

# 4. 1개 이상의 파생변수 추가
crime = crime.assign(
    total_s=crime.iloc[:,2:10].sum(axis=1),
    total_g=crime.iloc[:,10:18].sum(axis=1),
    total_i=crime.iloc[:,18:27].sum(axis=1),
    total=crime.iloc[:,2:27].sum(axis=1)
)
crime.head()

# 5. 범죄별 연도별 발생 건수 
## 문제1.그래프에 한글 입력 시 에러: 251p 맑은 고딕 폰트 설정
plt.rcParams.update({'font.family':'Malgun Gothic','font.size' : 3})

year_total = crime.groupby('year')\
                  .agg(강력범죄=('total_s','sum'),
                       폭력범죄=('total_g','sum'),
                       지능범죄=('total_i','sum'),
                       합계=('total','sum'))
year_total = year_total.transpose()
year_total.head()

plt.figure(figsize=(10, 4))
year_total.plot.bar(rot=0)
plt.show()
plt.clf()

# 6. 범죄별 요일별 발생건수
## 문제1. Groupby 시 인덱스가 알파벳순으로 정렬됨: reindex 적용
total_day=crime.groupby('day').agg(강력범죄=('total_s','sum'),
                                 폭력범죄=('total_g','sum'),
                                 지능범죄=('total_i','sum'),
                                 합계=('total','sum'))
total_day = total_day.reindex(index=['mon','tue','wed','thu','fri','sat','sun'])
total_day = total_day.transpose()
total_day
plt.figure(figsize=(10, 6))
total_day.plot.bar(rot=0)
plt.show()
plt.clf()

# 7. 연도별 요일별 발생 비율(%)
## 문제1. 연도별 비율을 구하기 위해 연도별 합계가 필요함: transform()
## 소수 둘째자리까지만 보이기 : pd.options.display.float_format 변경
pd.options.display.float_format = '{:.2f}'.format

crime = crime.assign(
    total_s_year = lambda x: x.groupby('year')['total_s'].transform('sum'),
    ratio_s_day = lambda x: x['total_s'] / x['total_s_year'] * 100,
    total_g_year = lambda x: x.groupby('year')['total_g'].transform('sum'),
    ratio_g_day = lambda x: x['total_g'] / x['total_g_year'] * 100,
    total_i_year = lambda x: x.groupby('year')['total_i'].transform('sum'),
    ratio_i_day = lambda x: x['total_i'] / x['total_i_year'] * 100,
    total_year = lambda x: x.groupby('year')['total'].transform('sum'),
    ratio_day = lambda x: x['total'] / x['total_year'] * 100,
)
crime.iloc[:,[0,1,-8,-7,-6,-5,-4,-3,-2,-1]]


# 연도별 요일별 범죄 건수 변화
ratio_year_day = crime.iloc[:,[0,1,-7,-5,-3,-1]]
ratio_year_day.head(7)
plt.figure(figsize=(10, 4))
sns.lineplot(data=ratio_year_day, x='year', y='ratio_s_day', hue='day')
plt.xticks(np.arange(2018,2023))
plt.show()
plt.clf()

sns.lineplot(data=ratio_year_day, x='year', y='ratio_g_day', hue='day')
plt.xticks(np.arange(2018,2023))
plt.show()
plt.clf()

sns.lineplot(data=ratio_year_day, x='year', y='ratio_i_day', hue='day')
plt.xticks(np.arange(2018,2023))
plt.show()
plt.clf()

sns.lineplot(data=ratio_year_day, x='year', y='ratio_day', hue='day')
plt.xticks(np.arange(2018,2023))
plt.show()
plt.clf()

total_day=crime.groupby('day').agg(total_s=('total_s','sum'),
                                 total_g=('total_g','sum'),
                                 total_i=('total_i','sum'),
                                 total=('total','sum'))
total_day = total_day.reindex(index=['mon','tue','wed','thu','fri','sat','sun'])
total_day
total_day = total_day.assign(
    ratio_s = lambda x: x['total_s'] / sum(x['total_s']) * 100,
    ratio_g = lambda x: x['total_g'] / sum(x['total_g']) * 100,
    ratio_i = lambda x: x['total_i'] / sum(x['total_i']) * 100,
    ratio = lambda x: x['total'] / sum(x['total']) * 100
)

ratio_total_day = total_day.iloc[:,4:]
ratio_total_day
sns.lineplot(data= ratio_total_day)

plt.show()
plt.clf()
