import requests
import os
import re
import io
from pathlib import Path
import base64, binascii
import zipfile
from lxml import etree
from plum import add_promotion_rule


def docx_extracter(profile_value):
    try:
        docx = base64.b64decode(profile_value, validate=True)
        docx_stream = io.BytesIO(docx)
        text_data = extract_text_from_docx(docx_stream)

        data = {}
        data = extract_fields(text_data)
        print(data)

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


def extract_fields(text_lines):
    data = {}
    joined = "\n".join(text_lines)

    # Line-by-line lookup
    full_name = find_value("First/ Middle Name (s)", text_lines,1)
    name_parts = full_name.split()
    data["name"] = name_parts[0]
    data["surname1"] = name_parts[1]
    data["surname2"] = find_value("Last Name", text_lines,1)

    data["sex"] = extract_gender(text_lines)
    data["id_type"] = find_value("ID Type", text_lines,1)


    data["passport_num"] = find_value("Passport No/ Unique ID", text_lines,1)
    data["passport_issue_date"] = find_value("ID Issue Date", text_lines,1)
    data["passport_expiry_date"] = find_value("ID Expiry Date", text_lines,1)

    data["birth_date"] = find_value("Date of birth ", text_lines,1)


    data["country"] = find_value("Country of Domicile", text_lines,1)

    address = find_value("Address", text_lines,1)
    data["address"] = address

    address = address.split(",")

    address[1] = address[1].split()
    address[0] = address[0].split()
    data["city"] = address[1][-1]
    data["building number"] = address[0][-1]
    data["street name"] = " ".join(address[0][:-1])
    data["postal code"] = address[1][0] + "-" + address[1][1]









    data["phone_num"] = next((line for line in text_lines if re.search(r"\d{2,} \d{3} \d{4}", line)), "")
    data["email"] = next((line for line in text_lines if "@" in line), "")

    data["marital_status"] = extract_maritalState(text_lines)

    data["education"] = find_value("Education History", text_lines,1)

    #data["employment"] = find_value("Current employment and function", text_lines,1)
    data["employment"] = extract_employment("Current employment and function",text_lines)

    return data





