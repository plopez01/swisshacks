from PIL import Image, ImageOps
import pytesseract
import string
from ConsistencyModel import ConsistencyModel

def read_passport(cm: ConsistencyModel, passport):
    # Load image
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

    bw.show()

    # OCR
    custom_config = r'--oem 1 --psm 6 -c tessedit_char_blacklist=$@&£'

    text_aux = pytesseract.image_to_string(bw, config=custom_config)
    print(text_aux)
    lines = text_aux.splitlines()
    non_empty = []
    for line in lines[:11]:
        if line.strip():  # skip empty or whitespace-only lines
            non_empty.append(line)
        else:
            print("hole                          l")

    # Take every other line from non-empty (even indices)
    text_list = non_empty[::2]

    text_list = text_list + lines[11:]



    passport_info = {}


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




    #cm.birth_date.check()
    print(passport_info)