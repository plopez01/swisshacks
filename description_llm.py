from ConsistencyModel import ConsistencyModel
import google.generativeai as genai

def check_consistency(cm: ConsistencyModel, fields, description_text):
    """
    content = (
            "The year is 13/04/2025\n\n"
            "You will receive two inputs:\n\n"
            "1. A list of correct data in the format (field: value).\n"
            "2. A block of unstructured text that contains information to be analyzed.\n\n"
            "Your task is to:\n"
            "- Analyze the text and compare it against the reference information.\n"
            "- Identify **inconsistencies**, meaning contradictions, illogical statements, or conflicting data.\n\n"
            "Important notes:\n"
            "- The `employment` field refers **only to the subject's most recent or current job**, "
            "including position title, employer name, and starting year.\n"
            "- You must **ignore all previous or past jobs** when evaluating the `employment` field. "
            "Only compare the last job mentioned in the text against the reference information.\n"
            "- Field constraints:\n"
            "   - `sex` must be one of: Female, Male\n"
            "   - `marital_status` must be one of: Single, Married, Divorced, Widowed\n"
            "Do not check if sums of money match, for some fields of the description only partial information is given.\n"
            "Consider especially inconsistencies that are planely wrong\n"
            "Only mark something as inconsistent if you are extremely sure sure\n"
            "Not all reference data may be in the text, this is not considered inconsistent\n"
            "For each field where the information in the text is inconsistent with the reference data, "
            "return a JSON object with:\n"
            "- `field`: the name of the field\n"
            "- `reason`: a brief but clear explanation of the inconsistency (1–2 sentences max)\n\n"
            "Return a **list of JSON objects**, one per inconsistency.\n"
            "**Do not return any JSON for older jobs, inferred mismatches, or wording differences. "
            "Only return JSON for clear inconsistencies in the last job or other fields.**\n"
            "Do not include any explanations outside of the JSON list.\n\n"
            "Do not add markdown json annotations, only plain valid JSON\n"
            "Reference Information (correct values):\n"
            f"{fields}\n\n"
            "Text to Analyze:\n"
            f"{description_text}"
        )
    """
    #print(content)

    content = (
            "You will receive one text input:\n\n"
            "1. A block of unstructured text that contains information to be analyzed.\n\n"
            "Your task is to:\n"
            "- Analyze the text and extract information by filling out the following JSON schema:\n"
            "**Do not return any JSON for older jobs, inferred mismatches, or wording differences. "
            "Do not include any field not included in the JSON list.\n\n"
            "Text to Analyze:\n"
            f"{description_text}"
            "JSON Schema to be filled out:\n"
            "{  \n"
            "  \"name\": \"\",\n"
            "  \"surname\": \"\",\n"
            "  \"sex\": \"\",\n"
            "  \"id_type\": \"\",\n"
            "  \"nationality\": \"\",\n"
            "  \"passport_num\": \"\",\n"
            "  \"passport_code\": \"\",\n"
            "  \"passport_issue_date\": [\"\", \"\", \"\"],\n"
            "  \"passport_expiry_date\": [\"\", \"\", \"\"],\n"
            "  \"passport_ocr\": \"\",\n"
            "  \"birth_date\": [\"\", \"\", \"\"],\n"
            "  \"country_of_domicile\": \"\",\n"
            "  \"city\": \"\",\n"
            "  \"phone_num\": \"\",\n"
            "  \"email\": \"\",\n"
            "  \"currency\": \"\",\n"
            "  \"building_num\": \"\",\n"
            "  \"street_name\": \"\",\n"
            "  \"postal_code\": \"\",\n"
            "  \"marital_status\": \"\",\n"
            "  \"education\": \"\",\n"
            "  \"employment\": \"\",\n"
            "  \"wealth\": \"\",\n"
            "  \"bank_account_info\": \"\"\n"
            "}\n"
        )

    prompt = (
            content
    )

    # Configure the generative model API key.
    genai.configure(api_key="AIzaSyAwJD4w41itq27V9FvGHyPrHsr477z4tqI")
    model = genai.GenerativeModel("gemini-1.5-flash-latest")

    # Call the model with the properly constructed single prompt string.
    response = model.generate_content(prompt)

    text = response.text.split("```json")[1].rsplit("```")[0]
    print(text)

    return text
