# 0. 패키지 로드
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 1. 데이터 파일 불러오기, 원본 데이터 복사하기
## header: 원본의 두 번째 행 데이터를 열의 이름으로 지정
## encoding: UnicodeDecodeError 발생으로 한글 표현 가능한 인코딩 방식인 EUC-KR 지정
df = pd.read_csv('crime.csv', header = 1, encoding = 'EUC-KR')
df.head()

# 2. 원본 데이터 복사하기
## deepcopy로 원본유지
crime = df.copy()

# 3. 열 이름, 원소 이름 변경
## 열 이름 변경
### 강력범죄는 s_, 폭력범죄는 g_, 지능범죄는 i_로 시작하도록 변경
crime.columns
crime.columns = ['year','day']\
                + [i.replace(i, "s_"+i) for i in crime.columns[2:10]]\
                + [i.replace(i, "g_"+i) for i in crime.columns[10:18]]\
                + [i.replace(i, "i_"+i) for i in crime.columns[18:27]]

## 원소 이름 변경
## replace(): 요일을 영어로 일괄 변경
crime = crime.replace({'월요일':'mon',
                       '화요일':'tue',
                       '수요일':'wed',
                       '목요일':'thu',
                       '금요일':'fri',
                       '토요일':'sat',
                       '일요일':'sun'})
crime.head(7)

## reindex(): 행의 순서 바꾸기(일>토에서 월>일로) > 추후 그래프 순서를 위해서 설정
len(crime)
crime = crime.reindex([1, 2, 3, 4, 5, 6, 0,
                       8, 9, 10, 11, 12, 13, 7,
                       15, 16, 17, 18, 19, 20, 14,
                       22, 23, 24, 25, 26, 27, 21,
                       29, 30, 31, 32, 33, 34, 28])
crime.head(7)

# 4. 파생변수 추가
## 범죄별 건수 합계 및 총 범죄 건수 합계 파생변수
crime = crime.assign(
    total_s = crime.iloc[:, 2:10].sum(axis = 1),
    total_g = crime.iloc[:, 10:18].sum(axis = 1),
    total_i = crime.iloc[:, 18:27].sum(axis = 1),
    total = crime.iloc[:, 2:27].sum(axis = 1))
crime.head()

## 평일/주말 구분 라벨 파생변수
### 평일: 월~금, 주말: 토~일
crime['day_label'] = np.where(crime['day'].isin(['mon', 'tue', 'wed', 'thu', 'fri']), \
                                                 'week', 'weekend')
crime.head(7)

# 5. (1)발생 건수 합계 기준 그래프
## 연도 기준 범죄별 건수 합계
### 그래프 설정
plt.rcParams.update({'font.family':'Malgun Gothic','font.size' : 10})
plt.figure(figsize = (8, 6))

### 집단별 합계표 생성
year_total = crime.groupby('year')\
                  .agg(강력범죄=('total_s','sum'),
                       폭력범죄=('total_g','sum'),
                       지능범죄=('total_i','sum'))

### 그래프 생성                       
year_total.plot.barh(stacked = True)
plt.xlabel("건수")
plt.ylabel("연도")
plt.title("각 범죄 발생 건수 비율 그래프")
plt.show()
plt.clf()

## 평일/주말 기준 건수 합계
### 평일/주말별 건수 합계표 생성
week_end = crime.groupby('day_label', as_index = False) \
                .agg(total=('total', 'sum'))

### 그래프 생성                
sns.barplot(data = week_end, x = 'day_label', y = 'total', hue = 'day_label')
plt.xlabel("평일/주말")
plt.ylabel("건수(백만)")
plt.title("평일/주말별 범죄 발생 건수 그래프")
plt.show()
plt.clf()

# 5. (2)연도별 범죄 발생 비율 파생변수 추가
## pd.options.display.float_format : 소수점 둘째 자리까지만 보이도록 설정
pd.options.display.float_format = '{:.2f}'.format

for i in ["_s", "_g" ,"_i" ,""]:
    for j in range(2018, 2023):
        crime.loc[crime['year'] == j, 'total'+ i +'_year'] = sum(crime.loc[crime['year'] == j,'total' + i])
    crime['ratio'+ i +'_day'] = crime['total' + i] / crime['total'+ i +'_year'] * 100
    
crime.head(7)

# 5. (3)연도/요일별 범죄 발생 비율 변화 그래프
## 연도/요일별 범죄 발생 비율표 생성
ratio_year_day = crime.iloc[:, [0, 1, -7, -5, -3, -1]]
ratio_year_day.head(7)

## 강력범죄 연도/요일별 범죄 발생 비율 변화 그래프
### plt.xticks() : x축의 범위를 2018~2022로 설정
sns.lineplot(data = ratio_year_day, x = 'day', y = 'ratio_s_day', hue = 'year')
plt.xlabel("요일")
plt.ylabel("비율(%)")
plt.title("강력범죄 요일별 범죄율 비교 그래프")
plt.show()
plt.clf()

## 폭력범죄 연도/요일별 범죄 발생 비율 변화 그래프
sns.lineplot(data = ratio_year_day, x = 'day', y = 'ratio_g_day', hue = 'year')
plt.xlabel("요일")
plt.ylabel("비율(%)")
plt.title("폭력범죄 요일별 범죄율 비교 그래프")
plt.show()
plt.clf()

## 지능범죄 연도/요일별 범죄 발생 비율 변화 그래프
sns.lineplot(data = ratio_year_day, x = 'day', y = 'ratio_i_day', hue = 'year')
plt.xlabel("요일")
plt.ylabel("비율(%)")
plt.title("지능범죄 요일별 범죄율 비교 그래프")
plt.show()
plt.clf()

## 전체 범죄 연도/요일별 범죄 발생 비율 변화 그래프
sns.lineplot(data = ratio_year_day, x = 'day', y = 'ratio_day', hue = 'year')
plt.xlabel("요일")
plt.ylabel("비율(%)")
plt.title("전체 범죄 요일별 범죄율 비교 그래프")
plt.show()
plt.clf()

# 6. 요일별 전체 범죄 발생 비율 그래프
## 요일별 전체 범죄 발생 비율표 생성
total_day = crime.groupby('day') \
                 .agg(total_s = ('total_s', 'sum'),
                      total_g = ('total_g', 'sum'),
                      total_i = ('total_i', 'sum'),
                      total = ('total', 'sum'))

total_day = total_day.assign(
    강력범죄 = lambda x: x['total_s'] / sum(x['total_s']) * 100,
    폭력범죄 = lambda x: x['total_g'] / sum(x['total_g']) * 100,
    지능범죄 = lambda x: x['total_i'] / sum(x['total_i']) * 100,
    총_범죄율 = lambda x: x['total'] / sum(x['total']) * 100)

total_day = total_day.reindex(index=['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'])

ratio_total_day = total_day.iloc[:, 4:]
ratio_total_day

## 요일별 전체 범죄 발생 비율 그래프 생성
sns.lineplot(data = ratio_total_day)
plt.xlabel("요일")
plt.ylabel("비율(%)")
plt.title("요일 기준 범죄율 비교 그래프")
plt.show()


