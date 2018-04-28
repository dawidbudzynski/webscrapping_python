import pandas
import requests
from bs4 import BeautifulSoup

base_url = 'https://www.pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s={}.html'
first_page = 'https://www.pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/'
r = requests.get(first_page)
c = r.content
soup = BeautifulSoup(c, 'html.parser')
last_page_no = soup.find_all('a', {'class': 'Page'})[-1].text
list_all_info = []
for page in range(0, int(last_page_no) * 10, 10):
    r = requests.get(base_url.format(page))
    c = r.content
    soup = BeautifulSoup(c, 'html.parser')

    all_info = soup.find_all('div', {'class': 'propertyRow'})
    for item in all_info:
        dict_single_property_info = {}
        price = item.find('h4', {'class': 'propPrice'}).text.replace('\n', '').replace(' ', '')
        address = item.find_all('span', {'class': 'propAddressCollapse'})
        full_address = address[0].text + ' ' + address[1].text
        try:
            beds = item.find('span', {'class', 'infoBed'}).find('b').text
        except AttributeError:
            beds = None
        try:
            baths = item.find('span', {'class', 'infoValueFullBath'}).find('b').text
        except AttributeError:
            baths = None
        try:
            half_baths = item.find('span', {'class', 'infoValueHalfBath'}).find('b').text
        except AttributeError:
            half_baths = None
        try:
            area = item.find('span', {'class', 'infoSqFt'}).find('b').text
        except AttributeError:
            area = None

        lot_size = None
        for column_group in item.find_all('div', {'class': 'columnGroup'}):
            for feature_group, feature_name in zip(column_group.find_all('span', {'class': 'featureGroup'}),
                                                   column_group.find_all('span', {'class': 'featureName'})):
                if 'Lot Size' in feature_group.text:
                    lot_size = feature_name.text

        dict_single_property_info['Price'] = price
        dict_single_property_info['Address'] = full_address
        dict_single_property_info['Beds'] = beds
        dict_single_property_info['Full baths'] = baths
        dict_single_property_info['Half baths'] = half_baths
        dict_single_property_info['Area'] = area
        dict_single_property_info['Lot size'] = lot_size
        list_all_info.append(dict_single_property_info)

df = pandas.DataFrame(list_all_info)
df.to_csv('result.csv')

