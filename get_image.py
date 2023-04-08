from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import datetime
import re
from dateutil.relativedelta import relativedelta
import ast

def call_dataset(str):
    filename = str
    data = {}
    
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            key, values_str = line.strip().split(": ")
            try:
                values = ast.literal_eval(values_str)
                data[key] = values
            except ValueError:
                print(f"Skipping line: {line}")
        
    return data

def get_image(date, data):
    
    from datetime import datetime
    input_date = date
    input_date_obj = datetime.strptime(input_date, '%Y/%m/%d')
    month_int = input_date_obj.month
    year_int = input_date_obj.year
    day_int = input_date_obj.day
    url = str()
    
    for key, value in data.items():
        match_search = re.search(r'(\d+)月(\d+)日', key)
        if match_search:
            key_month, key_day = map(int, match_search.groups())
            key_year = value[0]
            if month_int == key_month and day_int == key_day and year_int == key_year:
                print(f"{'Found the match: '} {'month: '}{key_month, key_day, key_year}")
                url = value[1]
    
    if url.strip():
        response_date = requests.get(url)
        print(response_date)
        # Use BeautifulSoup to parse the HTML content of the webpage
        soup_date = BeautifulSoup(response_date.content, 'html.parser', from_encoding='UTF-8')

        dd_tag_temp = soup_date.find('dd', class_='contents')

        link_tag = dd_tag_temp.find('a', href=True)
        if link_tag:
            link_schedule = link_tag['href']
            print(link_schedule)
        else:
            print('No link found')
            
        # Find the image on the url page

        url_schedule = link_schedule
        soup_schedule = BeautifulSoup(requests.get(url_schedule).content, 'html.parser', from_encoding='UTF-8')
        meta_tag = soup_schedule.find('meta', {'property': 'og:image'})
        if meta_tag:
            image_url = meta_tag['content']
            print(f"{'The image link: '}{image_url}")
            return image_url
        else:
            print("No image URL found.")
    else:
        print('Empty URL. No Day was found')

def print_dict(data):
    for title, href in data.items():
        print(f'{title}: {href}')

def main():
    data = call_dataset('D:\python-project\Badminton_scheduling\data-washing-minatoku\schedule.txt')
    # print_dict(data)
    date = input("Which date you would like to search for: ")
    get_image(date, data)
    
if __name__ == '__main__':
    main()


        