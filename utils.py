import string

error_mapping = {"2": "Z",
                 "6": "G",
                 "0": "O",
                 "": ""}

def birthdate_to_num(birthdate: string):
    month_map = {
        'Jan': '01',
        'Feb': '02',
        'Mar': '03',
        'Apr': '04',
        'May': '05',
        'Jun': '06',
        'Jul': '07',
        'Aug': '08',
        'Sep': '09',
        'Oct': '10',
        'Nov': '11',
        'Dec': '12'
    }

    day, month_abbr, year = birthdate.split('-')
    return year[-2:] + month_map[month_abbr] + day.zfill(2)
