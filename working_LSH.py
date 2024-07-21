import pandas as pd
import numpy as np

# raw data 불러오기
df = pd.read_csv('crime.csv', encoding = 'EUC-KR') # encoding에 대해 찾아보기

# 데이터 복제
crime = df.copy()

# 데이터 정보 타입 확인
crime.describe()
crime.info()

# 0번 행을 열로 변경
crime = crime.rename(columns = crime.iloc[0])

# 중복되는 0번 행 삭제
crime = crime.drop([0])

# 변수명 변경
crime = crime.rename(columns = {'시점':'year','범죄발생요일별(1)':'day'})

crime.loc[crime['day'] == '월요일', 'day'] = 'mon'
crime.loc[crime['day'] == '화요일', 'day'] = 'tue'
crime.loc[crime['day'] == '수요일', 'day'] = 'wed'
crime.loc[crime['day'] == '목요일', 'day'] = 'thu'
crime.loc[crime['day'] == '금요일', 'day'] = 'fri'
crime.loc[crime['day'] == '토요일', 'day'] = 'sat'
crime.loc[crime['day'] == '일요일', 'day'] = 'sun'

# object 타입을 int로 변경
df = crime
df.loc[:, df.columns != 'day'] = df.loc[:, df.columns != 'day'].apply(pd.to_numeric) # to_numeric 어떻게 작동하는지 확인하기 
crime = df

# 범죄 대분류 별로 데이터 분리 (강력/폭력/지능)
strong = crime.iloc[:, 0:10]
gang = crime.iloc[:, [0, 1, 10, 11, 12, 13, 14, 15, 16, 17]]
intel = crime.iloc[:, [0, 1, 18, 19, 20, 21, 22, 23, 24, 25, 26]]

strong.head()
gang .head()
intel.head()

# 파생변수 추가
crime = crime.assign(
    total = lambda x : x.iloc[:, 2:26].sum(axis = 1),
    mean = lambda x : x['total'] / 24)

strong = strong.assign(
    total_strong = lambda x : x.iloc[:, 2:10].sum(axis = 1),
    mean_strong = lambda x : x['total_strong'] / 8)
    
gang = gang.assign(
    total_gang = lambda x : x.iloc[:, 2:10].sum(axis = 1),
    mean_gang = lambda x : x['total_gang'] / 8)
    
intel = intel.assign(
    total_intel = lambda x : x.iloc[:, 2:11].sum(axis = 1),
    mean_intel = lambda x : x['total_intel'] / 9)

crime.head()
strong.head()
gang .head()
intel.head()

# 각 범죄 대분류별 범죄 발생 건수 차이 - 그래프


# 각 범죄별 평일/주말 범죄 발생 건수 추이 - 그래프
## 평일(월 ~ 금), 주말(토~ 일)


# 각 연도별 특정 요일의 범죄 발생 건수 추세
# 산점도 199, 막대 그래프 272, 274

import seaborn as sns


