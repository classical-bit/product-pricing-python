from urllib.request import urlopen as ureq
from bs4 import BeautifulSoup as soup
import contextlib
import csv
product_list = list()
price_list = list()
url = 'https://www.amazon.in/s/?field-keywords='


def get_soup(url_string):
    with contextlib.closing(ureq(url_string)) as web_client:
        page_content = web_client.read()
    return soup(page_content, 'html5lib')


with open("input_csv.csv", 'r', encoding='utf8') as input_csv_file:
    file_reader = csv.reader(input_csv_file, delimiter=',')
    for row in file_reader:
        if row != "":
            row[1] = row[0]+" "+row[1]
        row[1] = str.replace(row[1], "+", "%2B")
        row[1] = str.replace(row[1], "-", " ")
        row[1] = str.replace(row[1], "_", " ")
        row[1] = str.replace(row[1], " ", "+")
        product_list.append(row[1])

input_csv_file.close()

for product in product_list:
    page_soup = get_soup(url+product)
    try:
        with open('output_csv.csv', 'a', encoding='utf8') as output_csv_file:
            writer = csv.writer(output_csv_file, delimiter=',', quotechar='"')
            price = page_soup.find('span', {'class': 'a-size-base a-color-price s-price a-text-bold'}).text
            if price < 1000:
                price = 'ERROR: LT1K'
            writer.writerows([[product, price]])
    except AttributeError:
        print('ERROR')
    # price_list.append(page_soup.find('span', {'class': 'a-size-base a-color-price s-price a-text-bold'}).text)

print(price_list)
