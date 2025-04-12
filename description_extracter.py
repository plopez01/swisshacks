import base64
import zipfile
import io
from xml.etree import ElementTree as ET

def extract_docx_text_from_base64(description_value, output_file="description.txt"):
    try:
        # Step 1: Decode the Base64 string
        description_bytes = base64.b64decode(description_value, validate=True)

        # Step 2: Open the bytes as a ZIP file (because .docx is really a ZIP)
        zip_buffer = io.BytesIO(description_bytes)
        with zipfile.ZipFile(zip_buffer, "r") as zip_file:
            # Step 3: Read the main document XML from the Word file
            xml_content = zip_file.read("word/document.xml")
            tree = ET.fromstring(xml_content)

            # Step 4: Extract all text elements
            text = ""
            for elem in tree.iter():
                if elem.tag.endswith("}t"):  # 't' tag holds the text
                    text += elem.text or ""

        # Step 5: Save extracted text to a file (optional)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"✅ Text extracted and saved to '{output_file}'")
        return text

    except Exception as e:
        print(f"❌ Error: {e}")
        return None
