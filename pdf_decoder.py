import os
import base64
import fitz  # Asegúrate de tener instalada la biblioteca PyMuPDF
from api import start_game
from PyPDF2 import PdfReader
from ConsistencyModel import ConsistencyModel
import fitz  # PyMuPDF para capturar la región de la imagen

# Dictionary of known fields in the PDF form
# Separated into text fields and checkbox fields for currency selection
KNOWN_FIELDS = {
    "text_fields": [
        "account_name",
        "account_holder_name",
        "account_holder_surname",
        "passport_number",
        "building_number",
        "street_name",
        "postal_code",
        "city",
        "country",
        "name",
        "phone_number",
        "email",
        "other_ccy",
    ],
    "checkbox_fields": [
        "chf",
        "eur",
        "usd"
    ]
}

def extract_signature(path):
    with open(path, 'rb') as file:
        reader = PdfReader(file)
        fields = reader.get_fields()
        
        page = reader.pages[0]
        signature_base64 = None

        """
        if '/Resources' in page and '/XObject' in page['/Resources']:
            xobjects = page['/Resources']['/XObject']
            if '/fzImg0' in xobjects:
                signature_obj = xobjects['/fzImg0'].get_object()
                
                # Calcular centro y dimensiones
                center_x = float(page.mediabox.width) * 0.2639
                center_y = float(page.mediabox.height) * 0.716
                width = float(page.mediabox.width) * 0.254
                height = float(page.mediabox.height) * 0.047
        
                # Calcular coordenadas del rectángulo a partir del centro y dimensiones
                x0 = center_x - width/2
                y0 = center_y - height/2
                x1 = center_x + width/2
                y1 = center_y + height/2
                
                # Capturar la región de la firma en el PDF
                doc = fitz.open(path)
                page_pdf = doc[0]
                rect = fitz.Rect(x0, y0, x1, y1)
                pix = page_pdf.get_pixmap(clip=rect)
                pix.save("signature_region.png")
                doc.close()
                return "signature_region.png"
            
        else:
        """
        return None

def extract_form_values(path):
    with open(path, 'rb') as file:
        reader = PdfReader(file)
        fields = reader.get_fields()

        if not fields:
            return {}

        form_data = {}

        for field_name in KNOWN_FIELDS["text_fields"]:
            value = fields.get(field_name, {}).get('/V', None)
            form_data[field_name] = value

        selected_currency = None
        for field_name in KNOWN_FIELDS["checkbox_fields"]:
            value = fields.get(field_name, {}).get('/V', None)
            if value == '/Yes':
                selected_currency = field_name
                break

        if not selected_currency:
            other_ccy_value = form_data.get("other_ccy", "").strip()
            if other_ccy_value:
                selected_currency = "other_ccy"

        form_data["currency"] = selected_currency if selected_currency else None
        form_data["signature"] = None #Cambiar para producción

        return form_data

def decode(cm: ConsistencyModel, base64_pdf):
    directorio_actual = os.getcwd()

    pdf_filename = os.path.join(directorio_actual, "client_account.pdf")
    with open(pdf_filename, "wb") as f:
        f.write(base64.b64decode(base64_pdf))

    form_values = extract_form_values(pdf_filename)

    if form_values.get("account_name"):
        full_name = form_values["account_name"].strip()
        name_parts = full_name.split()
        
        form_values["client_name"] = None
        form_values["surname_1"] = None
        form_values["surname_2"] = None

        for (i, name_part) in enumerate(name_parts):
            if i == 0:
                form_values["client_name"] = name_part
            elif i == 1:
                form_values["surname_1"] = name_part
            elif i == 2:
                form_values["surname_2"] = name_part
            else:
                break
    
    if (form_values["surname_1"]):
        cm.name.check(form_values["client_name"] + " " + form_values["surname_1"])
    else:
        cm.name.check(form_values["client_name"])

    cm.surname.check(form_values["surname_2"])
    cm.passport_num.check(form_values["passport_number"])
    cm.building_num.check(form_values["building_number"])
    cm.street_name.check(form_values["street_name"])
    cm.postal_code.check(form_values["postal_code"])
    cm.city.check(form_values["city"])
    cm.country.check(form_values["country"])
    cm.phone_num.check(form_values["phone_number"])
    cm.email.check(form_values["email"])


if __name__ == "__main__":
    cm = ConsistencyModel()
    decode(cm)
