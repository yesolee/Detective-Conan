import pandas as pd
import numpy as np

# raw data 불러오기##
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
    
intel = gang.assign(
    total_intel = lambda x : x.iloc[:, 2:11].sum(axis = 1),
    mean_intel = lambda x : x['total_intel'] / 9)


crime.head()
strong.head()
gang .head()
intel.head()


############################
# 각 범죄 대분류별 범죄 발생 건수 차이 - 그래프

import matplotlib.pyplot as plt

data = {
    'Category': ['강력범죄', '폭력범죄', '지능범죄'],
    'Total Incidents': [125025, 1319239, 1917085] # 체크해야함
}

df_plot = pd.DataFrame(data)

#구글링한 내용
plt.rcParams['font.family'] = 'Malgun Gothic'  # 시스템에 설치된 한글 폰트로 변경
plt.rcParams['axes.unicode_minus'] = False  # 음수 부호를 제대로 표시하도록 설정

# 그래프 생성
plt.figure(figsize=(10, 6))
plt.bar(df_plot['Category'], df_plot['Total Incidents'], color=['blue', 'green', 'red'])
plt.xlabel('범죄 대분류')
plt.ylabel('총 발생 건수')
plt.title('범죄 대분류별 총 발생 건수')
plt.tight_layout() #레이아웃 조정하는 함수
plt.show()

# 연도별 강력범죄의 총 발생 건수를 계산

#strong 연도별
strong_crime_yearly = strong.groupby('year')['total_strong'].sum()

#gang 연도별
gang_crime_yearly = gang.groupby('year')['total_gang'].sum()

#intel 연도별
intel_crime_yearly = intel.groupby('year')['total_intel'].sum()

# 각 범죄별 평일/주말 범죄 발생 건수 추이(월~금/토~일) - 그래프

# 평일(월요일부터 금요일) 강력범죄 발생 건수
strong_weekday = strong[(strong['day'] == 'mon') | (strong['day'] == 'tue') | (strong['day'] == 'wed') | (strong['day'] == 'thu') | (strong['day'] == 'fri')]
strong_weekday_count = strong_weekday.groupby('year')['total_strong'].sum().reset_index()
strong_weekday_count = strong_weekday_count.rename(columns={'total_strong': 'weekday_total_strong'})

# 주말(토요일과 일요일) 강력범죄 발생 건수
strong_weekend = strong[(strong['day'] == 'sat') | (strong['day'] == 'sun')]
strong_weekend_count = strong_weekend.groupby('year')['total_strong'].sum().reset_index()
strong_weekend_count = strong_weekend_count.rename(columns={'total_strong': 'weekend_total_strong'})

print("강력범죄 평일 발생 건수:")
print(strong_weekday_count)

print("\n강력범죄 주말 발생 건수:")
print(strong_weekend_count)


# 각 연도별 특정 요일의 범죄 발생 건수 추세

## {연도별 특정 이벤트도 반영해서 분석 (ex. 팬데믹)}

### 요일별 범죄 발생 : 분석 결과, 토요일과 일요일(주말)에 총 범죄 발생 건수와 
#평균 발생 건수가 평일에 비해 높은 것으로 나타났습니다. 특히,토요일에는 0건으로
#가장 많았으며, 일요일은 0건으로 그 뒤를 이었습니다. 
#이 결과는 주말에 사람들이 야외활동이 많아지면서 범죄 발생 가능성이 증가할것
#으로 보여지고, 주말에는 더 많은 사람들이 야외에서 시간을 보내고, 음주를 하거나
#늦게까지 외출을 하는 등의 경우가 많아지면서 범죄 발생률이 증가할 수 있습니다.
#따라서 주말에는 경찰의 순찰을 강화하고, 범죄 예방 캠페인을 집중적으로 실시하는 등
#의 대처(대응)이 필요할 것으로 보입니다.

import seaborn as sns
import matplotlib.pyplot as plt

# 데이터 그래프 생성




import matplotlib
print (matplotlib.get_cachedir())



from matplotlib import
font_manager
font_manager._rebuild()


