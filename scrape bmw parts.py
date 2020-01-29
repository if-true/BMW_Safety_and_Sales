!pip install -U -q PyDrive
!pip install -U -q ebaysdk

# importing our dependencies
import time
import folium
import datetime
import traceback
import pandas as pd
import numpy as np
import seaborn as sns
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from google.colab import files
from ebaysdk.finding import Connection as finding

# Code to read csv file int
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

# Authenticate and create the PyDrive client.
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)
link = 'https://drive.google.com/open?id=1eGadPmwcM0OdkJ4rD1WN6-DCPRuhtCSc'
myid = link.split('=')[1]
downloaded = drive.CreateFile({'id': myid}) 
downloaded.GetContentFile('dataframe.csv')
sns.set()

# READING IN THE ORIGINAL DATAFRAME
df_original = pd.read_csv('dataframe.csv', low_memory=False).drop_duplicates()
df = df_original.copy()
df.dropna(subset=['on_street_name'],inplace=True,axis=0)
df_inj = df[df['num_persons_injured']>0]
df_kx = df[df['num_persons_killed']>0]



# In this cell, we collect a large number of details about the sales history
# of BMW Replacement parts
list_output = []
incrementor = 10
maxpages = 101
api = finding(
    appid='enntmepf-anblgife-PRD-9f8fe58ca-5a1431ef', 
    config_file=None)

for pricelow in range(0, 1000, incrementor):
  pricehigh = pricelow + incrementor
  for page in range(1, 101): 
    if page > maxpages: continue    
      
    if page % 10 == 0:
      if pricelow % 10 == 0:
        print()
        print('Pricelow: ' + str(pricelow))
        print('Pricehigh: ' + str(pricehigh))
        print('Page: ' + str(page)) 
        print('Maxpages: ' + str(maxpages))
        print('Entries: ' + str(soup.totalentries.text))
        print('Added:' + str(added))   
        print('Newtotal: ' + str(len(list_output)))

    Dictionary_ApiRequest = { 
      'keywords': '(2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018) bmw',
      'paginationInput': {'pageNumber': page},
      'categoryId': '6030',
      'sortOrder': 'EndTimeSoonest',
      'itemFilter': [
          {'name': 'MinPrice', 'paramName': 'USD', 'value': pricelow},
          {'name': 'MaxPrice', 'paramName': 'USD', 'value': pricehigh},
          {'name': 'LocatedIn', 'value': 'US'},
          {'name': 'SoldItemsOnly', 'value': True}]}
    try: response = api.execute('findCompletedItems', Dictionary_ApiRequest)
    except: traceback.print_exc(); continue

    added = 0
    soup = BeautifulSoup(response.text,'lxml')
    maxpages = int(soup.totalpages.text)
    for item in soup.find_all('item'):
      title = soup.item.title.text.lower()
      catname = soup.categoryname.text.lower()
      catcode = soup.categoryid.text.lower()
      itemid = soup.itemid.text
      list_output.append('\t'.join([title, catname, catcode, itemid]))
      added += 1

    
df_ebay = pd.DataFrame(
    list_output, columns=[
        'title','catcode','catname','itemid']).drop_duplicates()
print('df_ebay shape: ' + str(df_ebay.shape))
df_ebay.to_csv('output.csv',index='ignore')
files.download('output.csv') 
