import pandas as pd
import numpy as np

# encoding에 대해 찾아보기
df = pd.read_csv('crime.csv', encoding='EUC-KR')
crime=df.copy()
crime.columns
crime = crime.rename(columns=crime.iloc[0])
crime = crime.drop([0])
crime = crime.rename(columns={'시점':'year','범죄발생요일별(1)':'day'})
crime.head()


crime.loc[crime['day'] == '월요일', 'day'] = 'mon'
crime.loc[crime['day'] == '화요일', 'day'] = 'tue'
crime.loc[crime['day'] == '수요일', 'day'] = 'wed'
crime.loc[crime['day'] == '목요일', 'day'] = 'thu'
crime.loc[crime['day'] == '금요일', 'day'] = 'fri'
crime.loc[crime['day'] == '토요일', 'day'] = 'sat'
crime.loc[crime['day'] == '일요일', 'day'] = 'sun'

crime.head()

len(crime.columns)

strong = crime.iloc[:,0:10]
gang = crime.iloc[:,[0,1,10,11,12,13,14,15,16,17]]
intel = crime.iloc[:,[0,1,18,19,20,21,22,23,24,25,26]]
crime.head()

strong.head()
gang .head()
intel.head()

#crime_new = crime[crime.apply(pd.to_numeric, errors='coerce')

df = crime
df.loc[:, df.columns != 'day'] = df.loc[:, df.columns != 'day'].apply(pd.to_numeric)
crime_new = df

crime_new.columns
crime_new.describe()
crime_new.info()
for x in crime_new["day"]:
    print(type(x))
# axis 쓰고 안쓰고
# crime_new = crime.assign(
#     total = crime_new.iloc[:,2:26].sum(axis=1),
#     mean = (crime_new.iloc[:,2:26].sum(axis=1))/24
# )

crime_new = crime.assign(
    total = lambda x : x.iloc[:,2:26].sum(axis=1),
    mean = lambda x : x['total'] /24
)

# crime_new = crime.assign(
#     total = crime_new.iloc[:,2:26].sum(axis=1),
#     mean = lambda x : x['total'] /24
# )
print(crime_new.dtypes)
crime_new.head()
# crime_new = crime_new.assign(
#     total = lambda x : x[x.columns[2:26]].sum(axis=1)
# )
# crime_new.head()


crime.head()
crime_new.groupby('day').mean()

