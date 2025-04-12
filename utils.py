import string
from PIL import Image, ImageChops

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


def birthdate_to_num_list(birthdate: string):
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
    return day, month_map[month_abbr], year


def cropImage(image, registrationPoint=(0, 0), threshold=225):
    """
    Crops a grayscale image by removing borders whiter than the given threshold.
    Pixels with values >= threshold are treated as white (ignored).
    """
    im = image.convert("L")  # Ensure grayscale

    # Create a mask of pixels darker than threshold
    mask = im.point(lambda x: 0 if x >= threshold else 255, mode='1')

    # Get bounding box of non-white (i.e., below threshold) content
    bbox = mask.getbbox()

    if bbox is None:
        print("Image is completely white or above threshold!")
        return None, None

    # Crop the original image using this bbox
    cropped = im.crop(bbox)

    # Adjust registration point
    left, upper, _, _ = bbox
    newRegistrationPoint = (
        registrationPoint[0] - left,
        registrationPoint[1] - upper
    )

    return cropped, newRegistrationPoint


