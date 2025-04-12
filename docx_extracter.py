import requests
import os
import re
import io
from pathlib import Path
import base64, binascii
import zipfile
from lxml import etree


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

def find_value(label, lines, offset=1):
        try:
            idx = lines.index(label)
            return lines[idx + offset].strip()
        except (ValueError, IndexError):
            return ""

def extract_gender(text_lines):
    for line in text_lines:
        line_lower = line.lower()
        if "female" in line_lower and "male" in line_lower:
            if "☒ female" in line_lower:
                return "Female"
            elif "☒ male" in line_lower:
                return "Male"
    return None

def extract_fields(text_lines):
    data = {}
    joined = "\n".join(text_lines)

    # Line-by-line lookup
    full_name = find_value("First/ Middle Name (s)", text_lines)
    name_parts = full_name.split()
    data["name"] = name_parts[0]
    data["surname1"] = name_parts[1]
    data["surname2"] = find_value("Last Name", text_lines)

    data["sex"] = extract_gender(text_lines)
    data["id_type"] = find_value("ID Type", text_lines)


    data["passport_num"] = find_value("Passport No/ Unique ID", text_lines)
    data["ID Type"] = find_value("Passport No/ Unique ID", text_lines)

    data["country"] = find_value("Country of Domicile", text_lines)
    data["email"] = next((line for line in text_lines if "@" in line), "")
    data["phone_number"] = next((line for line in text_lines if re.search(r"\d{2,} \d{3} \d{4}", line)), "")
    return data





