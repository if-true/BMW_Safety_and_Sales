import pandas as pd


df = pd.read_csv(
  'Motor_Vehicle_Collisions_-_Crashes.csv',
  low_memory=False).drop_duplicates()


for column in df.columns:
  try: df[column] = df[column].apply(lambda value: str(value).lower())
  except: continue

list_numericcolumns = [
  'NUMBER OF PERSONS INJURED',
  'NUMBER OF PERSONS KILLED ', 'NUMBER OF PEDESTRIANS INJURED',
  'NUMBER OF PEDESTRIANS KILLED', 'NUMBER OF CYCLIST INJURED',
  'NUMBER OF CYCLIST KILLED ', 'NUMBER OF MOTORIST INJURED',
  'NUMBER OF MOTORIST KILLED', 'LATITUDE', 'LONGITUDE',]
for column in list_numericcolumns: 
  try: 
    df[column] = df[column].astype('float')
    print(column)
  except: continue
print()

    
list_timecolumns = [
    'CRASH DATE',
    'CRASH TIME']
for column in list_timecolumns:
  df[column] = pd.to_datetime(df[column])
print()


for column in df.columns:
  if column in list_numericcolumns: continue
  if column in list_timecolumns: continue
  print(column)    
  try: df[column] = df[column].astype('category')
  except: continue
print()

for column in df.columns:
  df = df.rename(columns={
    column: column.lower().replace(' ','_')\
    .replace('number_of','num')})


print(df.columns)
print(df.dtypes)
df.to_csv('NYC_Collisions_Normalized.csv',index=False)
