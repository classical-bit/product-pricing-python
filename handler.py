from urllib.request import urlopen as ureq
import urllib.error
from bs4 import BeautifulSoup as soup
import csv

product_list = list()
price_list = list()
minimum_price = 1000

beginFrom_tag = 0

url = 'https://www.amazon.in/s/?field-keywords='


def get_soup(url_string):
    web_client = ureq(url_string)
    page_content = web_client.read()
    web_client.close()
    return soup(page_content, 'html5lib')


try:
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
except FileNotFoundError:
    print('FILE NOT FOUND: "input_csv.csv"')


# print(product_list)
# page_soup = get_soup(url+"oneplus+6")
# print(page_soup.find('span', {'class': 'a-size-base a-color-price s-price a-text-bold'}).text)

try:
    with open('log_file.csv', 'r', encoding='utf8') as log_file_in:
        reader = csv.reader(log_file_in, delimiter=',')
        for row in reader:
            beginFrom_tag = int(row[0])
            print("FOUND LOG: Starting from product index [", beginFrom_tag + 1, ']')
except IndexError:
    # print("ERROR: IndexError")
    pass
except FileNotFoundError:
    print("LOG NOT FOUND: Starting from scratch")
finally:
    try:
        log_file_in.close()
    except NameError:
        pass

for product_number in range(beginFrom_tag, len(product_list)):
    try:
        page_soup = get_soup(url + product_list[product_number])
        with open('output_csv.csv', 'a', encoding="utf8", newline='') as output_csv_file:
            writer = csv.writer(output_csv_file, delimiter=',', quotechar='"')
            price = page_soup.find('span', {'class': 'a-size-base a-color-price s-price a-text-bold'}).text
            if int(str.replace(price, ',', '')) < minimum_price:
                price = ''
            price = str.replace(price, ' ', '')
            writer.writerows([[str.replace(product_list[product_number], '+', ' '), price]])

        with open('log_file.csv', 'w', encoding='utf8') as log_file_out:
            writer = csv.writer(log_file_out, delimiter=',')
            writer.writerow([product_number+1, len(product_list)])
        print('DONE: ', product_number + 1, '/', len(product_list))

    except AttributeError:
        print('ERROR: Invalid Name [', product_number + 1, '/', len(product_list), ']')
    except urllib.error.HTTPError:
        print('ERROR: AmazonServer is denying, Try again after an appropriate time ')
        exit(0)
    finally:
        try:
            output_csv_file.close()
        except NameError:
            pass
        try:
            log_file_out.close()
        except NameError:
            pass
