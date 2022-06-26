import os
import requests 
from bs4 import BeautifulSoup as bs 
import pandas as pd 
import parse_funcs as pf 

# CONSTANTS 
URL_BASE = 'https://www.bachelorstudies.com/Computer-Science/?page='
N_PAGES = 20
__DIR__ = os.getcwd()
HTML_DIR = os.path.join(__DIR__, 'html')


# STATUS 
FILES_LOADED = bool(all(f'page_{n}.html' in os.listdir(
    HTML_DIR) for n in range(1, N_PAGES + 1)))


# OUTPUT 

OUTPUT_DF = pd.DataFrame()


def generate_programme_df(_dict):
    return pd.DataFrame({
            k:[v]
            for k,v in _dict.items()
        })


def update_df(_dict):
    global OUTPUT_DF
    OUTPUT_DF = pd.concat([OUTPUT_DF, generate_programme_df(_dict)])


def load_page(n_page):

    '''
        Loads source html of page
    '''

    page_url = URL_BASE + str(n_page)

    page_request = requests.get(page_url)
    page_html = page_request.text

    with open(os.path.join(HTML_DIR, f'page_{n_page}.html'), 'w', encoding='utf-8') as html_file:
        html_file.write(page_html)
    print(f'[LOG] -> Parsed Page №{n_page}')


def parse_programme_page(programme_url):

    page = requests.get(programme_url)
    soup = bs(page.text, 'html.parser')
    section = soup.find("section", {"id": "general"})    
    
    locations =  section.find('locations')
    
    #print(locations)
    
    return {
        "school_name": eval(locations[":school"]),
        "location": pf.parse_programme_location(locations[":program-locations"]),
        "price_usd": pf.parse_price_location(locations[":price"]),
        "duration": pf.parse_duration(locations[":duration"]),
        "languages": str(eval(locations[":teaching-languages"])),
        "pace": str(eval(locations[":pace"])),
        "programme_info": pf.parse_programme_info(locations[":program"])
    }


def parse_page(page_number):

    page_file = f'page_{page_number}.html'

    dir_files = os.listdir(HTML_DIR)

    if page_file not in dir_files:
        print(f'[ERROR] -> Could not find file {page_file}')
        return 

    full_filepath = os.path.join(HTML_DIR, page_file)
    
    soup = bs(open(full_filepath, encoding='utf-8').read(), 'html.parser')
    print(f'[LOG] -> Soup generated {page_file}')
    
    study_programmes = soup.find_all(class_="program-listitem relative")
    print(f'[PARSE] -> {len(study_programmes)} study programmes found for {page_file}')

    for programme_div in study_programmes:
        programme_title_div = programme_div.find(class_="program_title")
        
        programme_title = programme_title_div.find('h4').text
        programme_url = programme_div.find('h4').find('a')['href']
        
        programme_details = {}
        
        if programme_url != "":
            programme_details = parse_programme_page(programme_url)

        #print(f'[PARSE] -> {programme_title} \n {programme_url} \n {proramme_details}')

        output_dict = {
            'programme_title': programme_title,
            'programme_url': programme_url
        }
        
        output_dict.update(programme_details)

        update_df(output_dict)


def main():
    if not FILES_LOADED:
        for n_page in range(1, N_PAGES + 1):
            load_page(n_page)

    for n_page in range(1, N_PAGES + 1):
        parse_page(n_page)

    OUTPUT_DF.to_excel('universities.xlsx')


# mainloop
if __name__ == '__main__':
    main()