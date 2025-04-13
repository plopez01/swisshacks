import base64



def extract_docx_text_from_base64(description_value):
    try:
        # Step 1: Decode the Base64 string
        description_bytes = base64.b64decode(description_value, validate=True)

        # Step 2: Write the bytes to a .txt file
        with open("description.txt", "wb") as f:
            f.write(description_bytes)

        print("✅ File written successfully to description.txt")
        return str(description_bytes)

    except Exception as e:
        print(f"❌ Error: {e}")
        return None

