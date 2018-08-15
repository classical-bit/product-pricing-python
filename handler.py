from urllib.request import urlopen as ureq
from bs4 import BeautifulSoup as soup
import contextlib
import csv

product_list = list()
price_list = list()

beginFrom_tag = 0

url = 'https://www.amazon.in/s/?field-keywords='


def get_soup(url_string):
    web_client = ureq(url_string)
    page_content = web_client.read()
    web_client.close()
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

print(product_list)

# page_soup = get_soup(url+"oneplus+6")
# print(page_soup.find('span', {'class': 'a-size-base a-color-price s-price a-text-bold'}).text)

try:
    with open('log_file.csv', 'r', encoding='utf8') as log_file_in:
        reader = csv.reader(log_file_in, delimiter=',')
        for row in reader:
            beginFrom_tag = int(row[0])
            print("FOUND LOG: Starting from product index-", beginFrom_tag + 1)
except IndexError:
    print("ERROR: IndexError")
except FileNotFoundError:
    print("Log doesn't exist! Starting from scratch")
finally:
    log_file_in.close()

for product_number in range(beginFrom_tag, len(product_list)):
    page_soup = get_soup(url+product_list[product_number])
    try:
        with open('output_csv.csv', 'a', encoding="utf8") as output_csv_file:
            writer = csv.writer(output_csv_file, delimiter=',', quotechar='"')
            price = page_soup.find('span', {'class': 'a-size-base a-color-price s-price a-text-bold'}).text
            if int(str.replace(price, ',', '')) < 1000:
                price = 'ERROR: LT1K'
            price = str.replace(price, ' ', '')
            writer.writerows([[str.replace(product_list[product_number], '+', ' '), price]])

        with open('log_file.csv', 'w', encoding='utf8') as log_file_out:
            writer = csv.writer(log_file_out, delimiter=',')
            writer.writerows([[product_number+1, len(product_list)]])
        print('DONE: ', product_number + 1, '/', len(product_list))

    except AttributeError:
        print('ERROR')

output_csv_file.close()
log_file_out.close()