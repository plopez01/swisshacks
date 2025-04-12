import io
import base64, binascii
import zipfile
from lxml import etree

from ConsistencyModel import ConsistencyModel


def docx_extracter(cm:ConsistencyModel, profile_value):
    try:
        docx = base64.b64decode(profile_value, validate=True)
        docx_stream = io.BytesIO(docx)
        text_data = extract_text_from_docx(docx_stream)

        with open('docx.txt', 'w') as f:
            f.write(str(text_data))

        extract_fields(cm, text_data)

        #print("DOCDSFDSAFADSF")

        fields = [
            'name', 'surname',
            'marital_status',
            'id_type',
            'passport_num', 'passport_issue_date', 'passport_expiry_date',
            'passport_ocr', 'birth_date',
            'country', 'city',
            'phone_num', 'email',
            'currency', 'building_num', 'street_name', 'postal_code',
            'education', 'employment',
            'wealth', 'bank_account_info',
            'signature'
        ]

        #for field_name in fields:
            #field = getattr(cm, field_name)
            #print(f"{field_name}: {field.value if hasattr(field, 'value') else field}")

        #print("DOCDSFDSAFADSF")









    except binascii.Error as e:
        print(e)

def extract_text_from_docx(docx_path):
    # Word XML namespace
    namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    # Open and parse the document.xml file inside the docx (zip) file
    with zipfile.ZipFile(docx_path) as docx_zip:
        with docx_zip.open("word/document.xml") as document_xml:
            xml_content = document_xml.read()
            tree = etree.fromstring(xml_content)

    # Extract all text from <w:t> elements
    text_nodes = tree.xpath(".//w:t", namespaces=namespaces)
    all_text = [node.text for node in text_nodes if node.text]

    return all_text

def find_value(label, lines, offset):
        try:
            idx = lines.index(label)
            return lines[idx + offset].strip()
        except (ValueError, IndexError):
            return ""

def extract_gender(text_lines):
    for line in text_lines:
        line_lower = line.lower()
        if "☒ female" in line_lower:
            return "Female"
        elif "☒ male" in line_lower:
            return "Male"
    return None

def extract_maritalState(text_lines):
    for line in text_lines:
        line_lower = line.lower()
        if "☒ divorced" in line_lower:
            return "Divorced"
        elif "☒ married" in line_lower:
            return "Married"
        elif "☒ single" in line_lower:
            return "Single"
        elif "☒ widowed" in line_lower:
            return "Widowed"
    return None

def extract_employment(label, lines):
    idx = lines.index(label)
    result = lines[idx+1:idx+5]
    result = " ".join(result)
    return result[2:]


def extract_fields(cm:ConsistencyModel, text_lines):

    # Line-by-line lookup
    full_name = find_value("First/ Middle Name (s)", text_lines,1)
    cm.name.check(full_name)
    cm.surname.check(find_value("Last Name", text_lines,1))

    #cm.name.check(name_parts[0])
    #cm.surname1.check(name_parts[1])
    #cm.surname2.check(find_value("Last Name", text_lines,1))


    cm.sex.check(extract_gender(text_lines)[0])
    cm.id_type.check(find_value("ID Type", text_lines,1))
    cm.passport_num.check(find_value("Passport No/ Unique ID", text_lines,1))
    cm.passport_issue_date.check(tuple(find_value("ID Issue Date", text_lines,1).split('-')))
    cm.passport_expiry_date.check(tuple(find_value("ID Expiry Date", text_lines,1).split('-')))
    cm.birth_date.check(tuple(find_value("Date of birth ", text_lines,1).split('-')))
    cm.country.check(find_value("Country of Domicile", text_lines,1))

    address = find_value("Address", text_lines,1)
    #cm.address.check(address)
    address = address.split(",")

    address[1] = address[1].split()
    address[0] = address[0].split()

    cm.city.check(address[1][-1])
    cm.building_num.check(address[0][-1])
    cm.street_name.check(" ".join(address[0][:-1]))
    cm.postal_code.check(address[1][0] + "-" + address[1][1])


    cm.phone_num.check(find_value("Telephone", text_lines,1))
    cm.email.check(next((line for line in text_lines if "@" in line), ""))
    cm.marital_status.check(extract_maritalState(text_lines))
    cm.education.check(find_value("Education History", text_lines,1))
    cm.employment.check(extract_employment("Current employment and function",text_lines))






