from ConsistencyFields import *

class ConsistencyModel:
    def __init__(self, handler):
        self.name = ConsistencyField("name", handler)
        self.surname_1 = ConsistencyField("surname_1", handler)
        self.surname_2 = ConsistencyField("surname_2", handler)

        self.sex = ConsistencyField("sex", handler)

        # This needed?
        self.id_type = ConsistencyField("id_type", handler)

        self.passport_num = ConsistencyField("passport_num", handler)
        self.passport_issue_date = DateField("passport_issue_date", handler)
        self.passport_expiry_date = DateField("passport_expiry_date", handler)

        # Check if this is actually needed
        self.passport_ocr = ConsistencyField("passport_ocr", handler)

        self.birth_date = DateField("birth_date", handler)

        self.country = ConsistencyField("country", handler)
        self.city = ConsistencyField("city", handler)

        self.phone_num = ConsistencyField("phone_num", handler)
        self.email = ConsistencyField("email", handler)

        self.currency = ConsistencyField("currency", handler)
        self.building_num = ConsistencyField("building_num", handler)
        self.street_name = ConsistencyField("street_name", handler)
        self.postal_code = ConsistencyField("postal_code", handler)

        # Personal info
        self.marital_status = ConsistencyField("marital_status", handler)

        # Education
        # TODO: this should maybe be broken into separate fields
        self.education = ConsistencyField("education", handler)

        # Employment
        # TODO: this should maybe be broken into separate fields
        self.employment = ConsistencyField("employment", handler)

        self.wealth = ConsistencyField("wealth", handler)

        # TODO: this should maybe be broken into separate fields
        self.bank_account_info = ConsistencyField("bank_account_info", handler)

        self.signature = ConsistencyField("signature", handler)


   