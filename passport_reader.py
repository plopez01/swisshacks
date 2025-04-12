from PIL import Image, ImageOps
import pytesseract
import base64
import io
import os
from ConsistencyModel import ConsistencyModel
import re
import utils
from utils import birthdate_to_num


def read_passport(cm: ConsistencyModel, passport):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    os.environ["TESSDATA_PREFIX"] = r"C:\Users\win10\Desktop\swisshacks\tessdata_best"

    # Load image
    # passport = io.BytesIO(base64.b64decode(passport, validate=True))
    passport = Image.open(passport)
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
    print(text_aux)
    lines = text_aux.splitlines()
    non_empty = []
    for line in lines[:11]:
        if line.strip():  # skip empty or whitespace-only lines
            non_empty.append(line)

    # Take every other line from non-empty (even indices)
    text_list = non_empty[::2]
    text_list = text_list + lines[11:]
    passport_info = {}

    print(signature)
    signature, _ = utils.cropImage(signature)

    passport_info['passport'] = ' '.join(text_list[1].split()[:-2])
    passport_info['code'] = text_list[1].split()[-2]
    passport_info['passport_no'] = text_list[1].split()[-1]
    passport_info['surname'] = text_list[2].split()[0]
    passport_info['firstname'] = ' '.join(text_list[2].split()[1:])
    passport_info['fullname'] = passport_info['firstname'] + ' ' + passport_info['surname']
    passport_info['birthdate'] = text_list[3].split()[0]
    passport_info['citizenship'] = ' '.join(text_list[3].split()[1:])
    passport_info['sex'] = text_list[4].split()[0][0]  # make sure it is the first letter F or M
    passport_info['issue_date'] = text_list[4].split()[1]
    passport_info['expiry_date'] = text_list[5].split()[0]
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
    #cm.birth_date.check()


