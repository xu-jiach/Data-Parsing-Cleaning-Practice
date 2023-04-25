from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import datetime
import re
from dateutil.relativedelta import relativedelta

# get the main webpage
def get_main_webpage():
    # Step 1: Send a GET request to the webpage you want to scrape
    url = 'https://www.minatoku-sports.com/private/index.php'
    response = requests.get(url)

    # Step 2: Use BeautifulSoup to parse the HTML content of the webpage
    soup = BeautifulSoup(response.content, 'html.parser', from_encoding='UTF-8')
    return soup

# write the data from the soup to a dictionary
def create_dict(soup):
    
    data = {}

    for dd_element in soup.find_all('dd', class_='title'):
        a_element = dd_element.find('a')
        if a_element is not None:
            title = a_element.text.strip().translate(str.maketrans('０１２３４５６７８９()', '0123456789（）'))
            dt_element = dd_element.previous_element
            while dt_element is not None and dt_element.name != 'dt':
                dt_element = dt_element.previous_element
            if dt_element is not None:
                published_date = dt_element.text.strip()
                published_year = datetime.datetime.strptime(published_date, '%Y年%m月%d日').year
                if a_element is not None:
                # find the url and make it a full url
                    href = a_element['href']
                    temp = href.replace('./','')
                    href = 'https://www.minatoku-sports.com/private/' + temp
                    # add an temp id to the title to prevent duplication
                    id_param = href.split('=')[1]
                    # concatenate the id to the title
                    title= f"{title} {id_param}"
                    data[title] = (published_year, href, id_param)
    return data

# print the data to the console
def print_dict(data):
    for title, href in data.items():
        print(f'{title}: {href}')

# write the data to a file
def write_dict_to_file(data):
    with open('D:\python-project\Badminton_scheduling\data-washing-minatoku\schedule.txt', 'w', encoding= "UTF-8") as file:
        for key, value in data.items():
            file.write(f'{key}: {value}\n')

# Clear Duplication
# if the same day appear twice in a year. 
# Then the later one shall be catergorized to the next year
def clear_duplication(data):
    from datetime import datetime, timedelta

    # define start and end dates
    start_date_str = '2015/1/15' # set start_date to current date and time
    start_date = datetime.strptime(start_date_str, '%Y/%m/%d')
    end_date = datetime.now() # set end_date to current date and time

    # loop through each day
    current_date = start_date
    while current_date <= end_date:
        year_int = current_date.year
        month_int = current_date.month
        day_int = current_date.day

        if month_int == 1: # only search for matches in January
            # search for matches for the current date
            matches = [] # initialize an empty list to store matches
            for key, value in data.items():
                if "1月" not in key: # skip keys that don't contain "1月" in the title
                    continue
                
                # extract the month and day from the key
                match_search = re.search(r'(\d+)月(\d+)日', key)
                # print("find a match")
                if match_search:
                    key_month, key_day = map(int, match_search.groups())
                    item_year = value[0]
                    if month_int == key_month and day_int == key_day and year_int == item_year:
                        matches.append((key, value))
                        

            if len(matches) == 2:
                first_match_key, first_match_value = matches[0]
                first_match_value = (first_match_value[0]+1, first_match_value[1], first_match_value[2])
                data.update({first_match_key: first_match_value})
                print(f'Updated first match: {first_match_key}: {first_match_value}')

        # advance to the next day
        current_date += timedelta(days=1)
        
    print("duplication has been cleared. If duplication happend again, then there must be an exception")

# Change the year of the data
# the actual year is different from the published year
def change_year(data):
    from datetime import datetime, timedelta
    
    dates_list = []
    for year in range(2016, 2024):
        for day in range(4, 6):
            date_str = f"{year}/1/{day}"
            date_obj = datetime.strptime(date_str, '%Y/%m/%d')
            dates_list.append(date_obj)
    
    for date in dates_list:
        flag = True
        month_int = date.month
        year_int = date.year
        day_int = date.day
        print(year_int, month_int, day_int)
        for key, value in data.items():
            match_search = re.search(r'(\d+)月(\d+)日', key)
            if match_search:
                key_month, key_day = map(int, match_search.groups())
                item_year = value[0]
                if month_int == key_month and day_int == key_day and year_int == item_year:
                    # find the nearest item that have the same year
                    current_key = key  # Create a new variable to hold the current key
                    while flag == True:
                        temp_key = current_key  # Use the current key to start the search
                        print(f"'The temp_key is:'{temp_key}")
                        next_key = list(data.keys())[list(data.keys()).index(temp_key) + 1]
                        print(f"'The next key is:'{next_key}")
                        match_next_key = re.search(r'(\d+)月(\d+)日', next_key)
                        if match_next_key:
                            print("Found a match next key")
                            next_key_month, next_key_day = map(int, match_next_key.groups())
                            print(f"next key month and day: {next_key_month, next_key_day}")
                            next_key_year = data[next_key][0]
                            if next_key_month != 1:
                                if next_key_year == item_year:
                                    print(f"'The next key is {next_key} and it is in year {next_key_year}'")
                                    print(f"'The year of {key} should not be {item_year}'")
                                    print(f"'Modify the year of {key} to {item_year+1}'")
                                    new_value = (item_year+1, data[key][1], data[key][2])
                                    data.update({key: new_value})
                                else:
                                    print(f"'The next key is {next_key} and it is in year {next_key_year}'")
                                    print(f"'The year of {key} is {item_year}. It is correct.'")
                                flag = False
                            else:
                                current_key = next_key  # Update the current key for the next iteration
                        else:
                            print("The key is in special format. Skip to the next one")
                            current_key = next_key # Update the current key for the next iteration

def main():
    soup = get_main_webpage()
    data = create_dict(soup)
    clear_duplication(data)
    change_year(data)
    write_dict_to_file(data)
    return data

if __name__ == '__main__':
    main()