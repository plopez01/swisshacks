import os
import base64
import fitz  # Asegúrate de tener instalada la biblioteca PyMuPDF
import json
from api import game_starter

# Obtiene la ruta del directorio actual
directorio_actual = os.getcwd()

# 1. Obtener base64 del PDF
request_result = game_starter()
if request_result is None:
    print("Error al obtener el resultado de la solicitud")
    exit()

base64_pdf = request_result["client_data"]["account"]

# 2. Guardar como archivo PDF
pdf_filename = os.path.join(directorio_actual, "client_account.pdf")
with open(pdf_filename, "wb") as f:
    f.write(base64.b64decode(base64_pdf))

# 3. Usar PyPDF2 para leer el PDF
import json
from PyPDF2 import PdfReader

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

def extract_form_values(path):
    with open(path, 'rb') as file:
        reader = PdfReader(file)
        fields = reader.get_fields()

        if not fields:
            return {}

        form_data = {}

        # Campos de texto
        for field_name in KNOWN_FIELDS["text_fields"]:
            value = fields.get(field_name, {}).get('/V', None)  # Get value or None if not found
            form_data[field_name] = value

        # Checkboxes (Moneda)
        selected_currency = None
        for field_name in KNOWN_FIELDS["checkbox_fields"]:
            value = fields.get(field_name, {}).get('/V', None)  # Get value or None if not found
            if value == '/Yes':  # Solo el campo con '/Yes' será seleccionado
                selected_currency = field_name
                break  # Salimos del ciclo al encontrar el valor True

        # Si no hay una moneda seleccionada, comprobamos 'other_ccy'
        if not selected_currency:
            other_ccy_value = form_data.get("other_ccy", "").strip()  # El valor de 'other_ccy'
            if other_ccy_value:  # Si tiene algún valor
                selected_currency = "other_ccy"

        # Agregar la moneda seleccionada (si hay)
        form_data["currency"] = selected_currency if selected_currency else None

        """
        # Extraer la firma como imagen y guardar en el directorio
        signature_image = extract_signature_as_image(path)
        if signature_image:
            form_data["signature"] = signature_image  # Guardamos la ruta de la imagen
        """
        
        return form_data

# Uso
form_values = extract_form_values(pdf_filename)

# Mostrar resultado en consola
for field, value in form_values.items():
    print(f"Field Name: {field}, Value: {value}")

# Convertir a JSON
pdf_content_json = json.dumps(form_values, indent=4)

"""
# 4. Comparar con los campos de client_data
client_data = game_starter["result"]["client_data"]
missing_fields = {}

for key, value in client_data.items():
    # Evitar comparar el PDF en sí
    if key == "description":
        continue
    if isinstance(value, str) and value not in pdf_text:
        missing_fields[key] = value

# 5. Mostrar resultados
print("\nTexto extraído del PDF:\n")
print(pdf_text)
print("\nCampos del JSON que no están en el PDF:\n")
print(missing_fields)
"""