import base64
import io

from PIL import Image, ImageOps
import pytesseract
import os

import mappings
from ConsistencyModel import ConsistencyModel
import re
import utils
from utils import birthdate_to_num
import io, base64

def decode_passport(passport):
    passport = io.BytesIO(base64.b64decode(passport, validate=True))
    passport = Image.open(passport)
    return passport

def read_passport(cm: ConsistencyModel, passport):

    script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of current script
    tessdata_path = os.path.join(script_dir, 'testdata')

    # Set the TESSDATA_PREFIX environment variable
    os.environ["TESSDATA_PREFIX"] = tessdata_path

    # Load image
    passport = decode_passport(passport)
    whitecover = Image.open("whitecover.png")
    whitecover = whitecover.resize((75, 75))
    # Convert to grayscale
    gray = ImageOps.grayscale(passport)
    bbox = (265, 210, 350, 250)  # Define the area to extract (left, top, right, bottom)

    signature = gray.crop(bbox)
    position = (300, 100)  # (x, y) coordinates

    # Paste overlay image onto the base image with transparency
    gray.paste(whitecover, position, whitecover)

    scale1 = 3
    resized = gray.resize((int(scale1 * gray.width), int(scale1 * gray.height)), Image.LANCZOS)

    # Enhance contrast
    def change_contrast(img, level):
        factor = (259 * (level + 255)) / (255 * (259 - level))
        def contrast(c):
            return 128 + factor * (c - 128)
        return img.point(contrast)

    high_contrast = change_contrast(resized, 50)

    bw = high_contrast.point(lambda x: 0 if x < 155 else (160 if x < 200 else 255), '1')

    custom_config = r'--oem 1 --psm 6 -c tessedit_char_blacklist=$@&£'

    text_aux = pytesseract.image_to_string(bw, config=custom_config)

    lines = text_aux.splitlines()

    print(text_aux)
    print(lines)
    non_empty = []
    for line in lines:
        if line.strip():  # skip empty or whitespace-only lines
            non_empty.append(line)

    # Take every other line from non-empty (even indices)
    text_list = non_empty[::2]
    passport_info = {}

    signature, _ = utils.cropImage(signature)

    passport_info['passport_code'] = text_list[1].split()[-2]
    passport_info['passport_num'] = text_list[1].split()[-1]
    passport_info['surname'] = text_list[2].split()[0]
    passport_info['firstname'] = ' '.join(text_list[2].split()[1:])
    passport_info['birthdate'] = text_list[3].split()[0]
    passport_info['nationality'] = ''.join(text_list[3].split()[1].split("/")[0])
    passport_info['sex'] = text_list[4].split()[0][0]  # make sure it is the first letter F or M
    passport_info['passport_issue_date'] = text_list[4].split()[1]
    passport_info['passport_expiry_date'] = text_list[5].split()[0]
    passport_info['signature'] = signature

    print(passport_info)

    """
    This is overall just not working might need to use llm
    
    text1_list = [s for s in re.sub(r'\s+', ' ', text_list[-2]).strip().split('<') if s]
    text2_list = [s for s in re.sub(r'\s+', ' ', text_list[-1]).replace(" ", '').split('<') if s]
    print(text1_list)
    print(text2_list)


    if (text1_list[1] == passport_info['code']+passport_info['surname'] and
        passport_info['firstname'] == text1_list[2] + " " + text1_list[3]):
        print("correct1")

    print(passport_info['passport_no']+passport_info['code']+birthdate_to_num(passport_info['birthdate']))
    print(text2_list[0])
    if (passport_info['passport_no']+passport_info['code'])+birthdate_to_num(passport_info['birthdate']) == text2_list[0]:
        print("correct2")
    # internal passport bottom info check with rest of info
    """

    cm.passport_code.check(passport_info['passport_code'])
    cm.passport_num.check(passport_info['passport_num'])
    cm.surname.check(passport_info['surname'])
    cm.name.check(passport_info['firstname'])
    cm.birth_date.check(utils.birthdate_to_num_list(passport_info['birthdate']))
    cm.city.check(mappings.nationality_to_country(passport_info["nationality"]))
    cm.sex.check(passport_info['sex'])
    cm.passport_issue_date.check(passport_info['passport_issue_date'])
    cm.passport_expiry_date.check(passport_info['passport_expiry_date'])

    





