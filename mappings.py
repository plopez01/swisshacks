import json

with open('country_map.json') as f:
    global country_map
    country_map = json.load(f)


def month_name_to_num(month_name: str):
    month_map = {
        'jan': '01',
        'feb': '02',
        'mar': '03',
        'apr': '04',
        'may': '05',
        'jun': '06',
        'jul': '07',
        'aug': '08',
        'sep': '09',
        'oct': '10',
        'nov': '11',
        'dec': '12'
    }
    return month_map[month_name]


def nationality_to_country(country: str):
    return country_map[country]

