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

def convert_data(data):
    converted_data = []
    for key, value in data.items():
        converted_data.append(
            {"title": key, "year": value[0], "url": value[1], "id": int(value[2])}
        )
        
    return converted_data

def write_dict_to_file(data):
    with open('D:\python-project\Badminton_scheduling\data-washing-minatoku\schedule_sql.txt', 'w', encoding= "UTF-8") as file:
        for item in data:
            line = f"{item['title']}, {item['year']}, {item['url']}, {item['id']}\n"
            file.write(line)

def remove_id_in_title(data):
    
    for item in data:
        last_space_index = item['title'].rfind(' ')
        item['title'] = item['title'][:last_space_index]
    
    return data

def print_dict(data):
    for title, href in data.items():
        print(f'{title}: {href}')
            
def main():
    data = call_dataset('D:\python-project\Badminton_scheduling\data-washing-minatoku\schedule.txt')
    new_data = convert_data(data)
    
    write_dict_to_file(remove_id_in_title(new_data))

    
    
if __name__ == "__main__": 
    main()
    