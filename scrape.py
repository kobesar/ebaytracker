from bs4 import BeautifulSoup
import pandas as pd
import requests as re

def get_recent_sales(url, product):
  df_former = pd.read_csv('data/' + product + '.csv', names=['title', 'price', 'date'], header=None)

  resp = re.get(url)
  soup = BeautifulSoup(resp.text, 'html.parser')
  items = soup.find_all('li', {'class': 's-item'})

  df = []

  for item in items:
    id = None
    title = None
    price = None
    date = None
    try:
      title = item.find('div', {'class': 's-item__title'}).contents[0].text
      price = item.find('span', {'class': 's-item__price'}).find('span', recursive=False).contents[0]
      date = item.find('div', {'class': 's-item__title--tagblock'}).find('span', recursive=False).contents[0].replace('Sold ', '')
    except:
      print('error')

    df.append({'title': title, 'price': price, 'date': date})
  
  df_former = df_former.append(pd.DataFrame(df), ignore_index = True)
  df_former.drop_duplicates()
  df_former.to_csv('data/' + product + '.csv')

get_recent_sales('https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=Nikkor+10-24mm+f%2F3.5-4.5G+ED&_sacat=0&LH_TitleDesc=0&_odkw=Nikon+AF-S+DX+Zoom-Nikkor+10-24mm+f%2F3.5-4.5G+ED&_osacat=0&LH_Complete=1&LH_Sold=1', 'nikkor1024')

get_recent_sales('https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=nikon+d7200&_sacat=0&LH_TitleDesc=0&_odkw=Nikkor+10-24mm+f%2F3.5-4.5G+ED&_osacat=0&LH_Complete=1&LH_Sold=1', 'd7200')

get_recent_sales('https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=tamron+24-70+nikon+g1&_sacat=0&LH_TitleDesc=0&_odkw=nikon+d7200&_osacat=0&LH_Complete=1&LH_Sold=1', 'tamron2470')

d7200 = pd.read_csv('data/d7200.csv')
nikkor1024 = pd.read_csv('data/nikkor1024.csv')
tamron2470 = pd.read_csv('data/tamron2470.csv')

d7200['product'] = 'd7200'
nikkor1024['product'] = 'nikkor1024'
tamron2470['product'] = 'tamron2470'

full_dat = pd.concat([d7200, nikkor1024, tamron2470], ignore_index=True)
full_dat.to_csv('data/full_data.csv')