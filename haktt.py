from bs4 import BeautifulSoup
import requests
import csv
import lxml

def write_to_csv(data: dict):
    with open('data.csv', 'a', newline='') as file:
        write = csv.writer(file) 
        write.writerow([data['title'], data['price'], data['img'], data['desc']])

def get_html(url):
    response = requests.get(url)
    # print(response.status_code)
    return response.text

def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    cars = soup.find_all('div', class_='table-view-list')

    for car in cars:
        try:
            title = car.find('div', class_='title').find('h2').text.strip()
        except:
            title = ''

        try:
            price = car.find('div', class_='price').find('p').find('strong').text.split()
            price = ' '.join(price)
        except:
            price = ''

        try:
            desc = car.find('div', class_='block info-wrapper item-info-wrapper').text.split()
            desc = ' '.join(desc)
        except:
            desc = ''

        try:
            img = car.find('div', class_='thumb-item-carousel').find('img').attrs.get('src')
        except:
            img = 'none image'

        data = {
            'title': title,
            'price': price,
            'desc': desc,
            'img': img
        }

        write_to_csv(data)

def get_page(html):
    soup = BeautifulSoup(html, 'lxml')
    page_list = soup.find('ul', class_='pagination').find_all('a')[-1].attrs.get('data-page')
    if page_list is not None:
        # print(page_list)
        return int(page_list)
    return 0


def main():
    url = 'https://www.mashina.kg/search/all/'
    html= get_html(url)
    num = get_page(html)
    for i in range(1, num+1):
        # print(i)
        url_page = url + '?page=' + str(i)
        print(url_page)
        html = get_html(url_page)
        get_data(html)
        print(f'sparsing {i} - машина')


with open('data.csv', 'w') as file:
    write = csv.writer(file)
    write.writerow(['title', 'price', 'image', 'description'])

main()
