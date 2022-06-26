import json
from bs4 import BeautifulSoup as bs


def parse_price_location(price_location):
    price_location_json = json.loads(price_location)
    
    try:
        return price_location_json["price"]["USD"]["amount"]
    except:
        return 'No info'


def parse_programme_info(program_location):
    program_location_json = json.loads(program_location)
    
    try:
        return bs(program_location_json["text"], 'html.parser').text
    except: 
        return 'No info'
    

def parse_programme_location(region_location):
    region_location_json = json.loads(region_location)
    
    return f'{region_location_json[0]["city"]}, {region_location_json[0]["country"]}'


def parse_duration(duration_location):
    
    try:
        duration_location_json = json.loads(duration_location)
        return duration_location_json
    except:
        return 'No info'
