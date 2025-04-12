from ConsistencyFields import *

class ConsistencyModel:
    def __init__(self, external_handler):
        self._external_handler = external_handler

        # Given name
        self.name = ConsistencyField("name", self._handler)

        # Surname/s
        self.surname = ConsistencyField("surname", self._handler)

        # M for male, F for female
        self.sex = ConsistencyField("sex", self._handler)

        # This needed?, passport
        self.id_type = ConsistencyField("id_type", self._handler)

        self.passport_num = ConsistencyField("passport_num", self._handler)
        self.passport_code = ConsistencyField("passport_code", self._handler)
        
        # Dates are a tuple following (year, month, day)
        self.passport_issue_date = DateField("passport_issue_date", self._handler)
        self.passport_expiry_date = DateField("passport_expiry_date", self._handler)

        # Check if this is actually needed
        self.passport_ocr = ConsistencyField("passport_ocr", self._handler)

        self.birth_date = DateField("birth_date", self._handler)

        # Country is the name, like Portugal, or Spain
        self.country = ConsistencyField("country", self._handler)
        self.city = ConsistencyField("city", self._handler)

        self.phone_num = ConsistencyField("phone_num", self._handler)
        self.email = ConsistencyField("email", self._handler)

        # thre letter currency name, eur for example
        self.currency = ConsistencyField("currency", self._handler)
        self.building_num = ConsistencyField("building_num", self._handler)
        self.street_name = ConsistencyField("street_name", self._handler)
        self.postal_code = ConsistencyField("postal_code", self._handler)

        # Personal info
        self.marital_status = ConsistencyField("marital_status", self._handler)

        # Education
        # TODO: this should maybe be broken into separate fields
        self.education = ConsistencyField("education", self._handler)

        # Employment
        # TODO: this should maybe be broken into separate fields
        self.employment = ConsistencyField("employment", self._handler)

        self.wealth = ConsistencyField("wealth", self._handler)

        # TODO: this should maybe be broken into separate fields
        self.bank_account_info = ConsistencyField("bank_account_info", self._handler)

        self.signature = ConsistencyField("signature", self._handler)

    def _handler(self, field, reason):
        self._external_handler(field, reason)

class InconsistencyCounterModel(ConsistencyModel):
    def __init__(self, external_handler):
        super().__init__(external_handler)
        self.inconsistencies = 0
         
    def _handler(self, field, value, reason):
        self.inconsistencies += 1
        self._external_handler(field, value, reason)