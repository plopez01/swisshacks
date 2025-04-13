from ConsistencyFields import *

class ConsistencyModel:
    def __init__(self, external_handler):
        self.document = None
        self._external_handler = external_handler

        # Given name
        self.name = ConsistencyField("name", self)

        # Surname/s
        self.surname = ConsistencyField("surname", self)

        # M for male, F for female
        self.sex = ConsistencyField("sex", self)

        # This needed?, passport
        self.id_type = ConsistencyField("id_type", self)

        # Danish, Finish, Spanish...
        self.nationality = ConsistencyField("nationality", self)

        self.passport_num = ConsistencyField("passport_num", self)
        self.passport_code = ConsistencyField("passport_code", self)
        
        # Dates are a tuple following (year, month, day)
        self.passport_issue_date = DateField("passport_issue_date", self)
        self.passport_expiry_date = DateField("passport_expiry_date", self)

        # Check if this is actually needed
        self.passport_ocr = ConsistencyField("passport_ocr", self)

        self.birth_date = DateField("birth_date", self)

        # Country Portugal or Spain or Italy
        self.country_of_domicile = ConsistencyField("country_of_domicile", self)
        self.city = ConsistencyField("city", self)

        self.phone_num = ConsistencyField("phone_num", self)
        self.email = ConsistencyField("email", self)

        # thre letter currency name, eur for example
        self.currency = ConsistencyField("currency", self)
        self.building_num = ConsistencyField("building_num", self)
        self.street_name = ConsistencyField("street_name", self)
        self.postal_code = ConsistencyField("postal_code", self)

        # Personal info
        self.marital_status = ConsistencyField("marital_status", self)

        # Education
        # TODO: this should maybe be broken into separate fields
        self.education = ConsistencyField("education", self)

        # Employment
        # TODO: this should maybe be broken into separate fields
        self.employment = ConsistencyField("employment", self)

        self.wealth = ConsistencyField("wealth", self)

        # TODO: this should maybe be broken into separate fields
        self.bank_account_info = ConsistencyField("bank_account_info", self)

        self.signature = ConsistencyField("signature", self)

    def _handler(self, field: ConsistencyField, reason):
        self._external_handler(field, reason)
        
    def set_document(self, name: str):
        self.document = name
    
    def to_string(self):
        result = ""
        for field in vars(self):
            data = vars(self)[field]
            if isinstance(data, ConsistencyField):
                result += f"{data.name}: {data.postulate}\n"
        return result

    def print(self):
        print(self.to_string(), end='')

class InconsistencyCounterModel(ConsistencyModel):
    def __init__(self, external_handler):
        super().__init__(external_handler)
        self.inconsistencies = 0
        
    def _handler(self, field: ConsistencyField, reason):
        if field.discrepancy_level > 1:
            self.inconsistencies += 1
        self._external_handler(field, reason)
