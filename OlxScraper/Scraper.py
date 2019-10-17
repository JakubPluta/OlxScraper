from bs4 import BeautifulSoup as BS
import requests
import pandas as pd
import itertools
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import babel.dates
import datetime
from openpyxl.workbook import Workbook
import time

headers = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})


def olx_links(city='wroclaw',rooms='two'):
    links,dates,titles = [],[],[]
    rooms = 'two'
    city = 'wroclaw'
    for page in range(0,3):
        olx = f"https://www.olx.pl/nieruchomosci/mieszkania/wynajem/{city}/?search%5Bfilter_enum_rooms%5D%5B0%5D={rooms}&page={page}"
        res = requests.get(olx, headers=headers)
        soup = BS(res.text, 'html.parser')
        apartments_cont = soup.find_all('div', class_='space rel')
        for i in apartments_cont:
            try:
                link = i.find('a')['href']
                links.append(link)
            except:
                pass
            try:
                title = i.find('a').text.strip()
                titles.append(title)
            except:
                pass
            try:
                date = i.find_all('span')[1].text.strip().split()[0]
                dates.append(date)
            except:
                pass
    return links

#linklist = olx_links(city='wroclaw',rooms='two')

def save_pickle(data):
    pickle_out = open('olxlinks.pickle','wb')
    pickle.dump(data,pickle_out)
    pickle_out.close()

def load_pickle():
    pickle_in = open('olxlinks.pickle','rb')
    pickle_data = pickle.load(pickle_in)
    return pickle_data

#d = save_pickle(linklist)
df_links = load_pickle()





links, prices, titles, cities, vovos, districts, ids, days,months,years,descs, phones, froms, levels, furnitures, builds, areas, rooms, rents = [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
for link in df_links[:51]:
    if link.startswith('https://www.olx.pl'):
        links.append(link)
        res = requests.get(link, headers=headers)
        soup = BS(res.text, 'html.parser')
        try:
            price = soup.find('div', class_='price-label').text.strip()
            prices.append(price)
        except:
            None

        try:
            base = soup.find('div', class_='offer-titlebox')
            title = base.h1.text.strip()
            city, vovo, district = base.a.text.strip().split()
            day,month,year = base.em.text.strip().split()[3:6]
            id = base.em.text.strip().split()[-1]
            titles.append(title)
            cities.append(city)
            vovos.append(vovo)
            districts.append(district)
            days.append(day)
            months.append(month)
            years.append(year)
            ids.append(id)

        except:
            None

        try:
            tab =  soup.find('div', class_='clr descriptioncontent marginbott20')

            i_title = [i.text.strip() for i in tab.find_all('th')]
            i_info = [x.text.strip() for x in tab.find_all('strong')]
            info = dict(zip(i_title,i_info))
            #print(info)

            froms.append(i_info[0])
            #print(froms)
            levels.append(i_info[1])
            #print(levels)
            furnitures.append(i_info[2])
            builds.append(i_info[3])
            areas.append(i_info[4])
            rooms.append(i_info[5])
            rents.append(i_info[6])

        except:
            None
        try:
            desc =  soup.find('div', class_='clr lheight20 large').text.strip()
            descs.append(desc)
        except:
            None

        try:
            phone = soup.find('span', class_='spoilerHidden')['data-phone'].strip()
            phones.append(phone)
        except:
            None

    time.sleep(1)

my_dict ={'Id': ids, 'Title': titles, 'Price': prices,
                              'Oferta od': froms, 'Poziom': levels, 'Umeblowane': furnitures, 'Rodzaj zabudowy': builds,
                              'Powierzchnia': areas, 'Liczba pokoi': rooms, 'Czynsz (dodatkowo)': rents,
                              'City': cities, 'Voivodeship': vovos, 'District': districts,
                              'Day': days, 'Month': months, 'Year': years,
                              'Description': descs, 'Phone': phones, 'Link': links}


flats = pd.DataFrame.from_dict(my_dict,orient='index').T
flats.to_excel('flats.xlsx')



