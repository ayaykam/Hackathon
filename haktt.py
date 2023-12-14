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
    return response.text

def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    cars = soup.find_all('div', class_='name')

    for car in cars:
        try:
            title = car.find('div', class_='table-view clr label-viez').find('a').text
        except:
            title = ''

        try:
            price = car.find('div', class_='table-view clr label-view').find('strong').text
        except:
            price = ''

        try:
            desc = car.find('div', class_='block info-wrapper item-info-wrapper').find_all('p')
            desc = ' '.join(p.text for p in desc)
        except:
            desc = ''

        try:
            img = car.find('img').get('src')
        except:
            img = ''

        data = {
            'title': title,
            'price': price,
            'desc': desc,
            'img': img
        }

        write_to_csv(data)

def get_page(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('ul', class_='pagination').find_all('li')
    last_page = pages[-1].find('a').get('href').split('=')[-1]
    return last_page


def main():
    url = 'https://www.mashina.kg/search/all/'
    html= get_html(url)
    page = get_page(html)

    for page_num in range(1, int(page) + 1):
        page_url = f'{url}?page={page_num}'
        html = get_html(page_url)
        get_data(html)

with open('data.csv', 'w', newline='') as file:
    write = csv.writer(file)
    write.writerow(['title', 'price', 'image', 'description'])

main()