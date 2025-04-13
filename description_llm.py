from ConsistencyModel import ConsistencyModel
import google.generativeai as genai

def check_consistency(cm: ConsistencyModel, fields, description_text):
    content = (
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
            "   - `wealth` must match one of the following options:\n"
            "       • '< EUR 1.5m' — Total net worth is below 1.5 million euros.\n"
            "       • 'EUR 1.5m-5m' — Net worth is between 1.5 and 5 million euros.\n"
            "       • 'EUR 5m-10m' — Net worth is between 5 and 10 million euros.\n"
            "       • 'EUR 10m-20m' — Net worth is between 10 and 20 million euros.\n"
            "       • 'EUR 20m-50m' — Net worth is between 20 and 50 million euros.\n"
            "       • '> EUR 50m' — Net worth exceeds 50 million euros.\n\n"
            "Compare the wealth information in the text to these categories when checking for inconsistencies.\n\n"
            "Do not check if sums of money match, for some fields of the description only partial information is given.\n"
            "Consider especially inconsistencies that are planely wrong\n"
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

    #print(content)

    prompt = (
            content
    )

    # Configure the generative model API key.
    genai.configure(api_key="AIzaSyAwJD4w41itq27V9FvGHyPrHsr477z4tqI")
    model = genai.GenerativeModel("gemini-1.5-flash-latest")

    # Call the model with the properly constructed single prompt string.
    response = model.generate_content(prompt)
    print(response.text)
