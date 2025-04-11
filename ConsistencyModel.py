class ConsistencyField:
    def __init__(self, inconsistent_handler):
        self.truth = None
        self._inconsistent_handler = inconsistent_handler

    def check(self, val):
        if self._check_impl(val):
            return True
        else:
            self._inconsistent_handler(self)
            return False

    def _check_impl(self, val):
        if self.truth == None:
            self.truth = val
            return True
        
        return self.truth == val

class ConsistencyModel:
    def __init__(self, handler):
        self.name = ConsistencyField(handler)
        self.surname_1 = ConsistencyField(handler)
        self.surname_2 = ConsistencyField(handler)

        self.sex = ConsistencyField(handler)

        # This needed?
        self.id_type = ConsistencyField(handler)

        self.passport_num = ConsistencyField(handler)
        self.passport_issue_date = ConsistencyField(handler)
        self.passport_expiry_date = ConsistencyField(handler)

        # Check if this is actually needed
        self.passport_ocr = ConsistencyField(handler)

        self.birth_date = ConsistencyField(handler)

        self.country = ConsistencyField(handler)
        self.city = ConsistencyField(handler)

        self.phone_num = ConsistencyField(handler)
        self.email = ConsistencyField(handler)

        self.currency = ConsistencyField(handler)
        self.building_num = ConsistencyField(handler)
        self.street_name = ConsistencyField(handler)
        self.postal_code = ConsistencyField(handler)

        # Personal info
        self.marital_status = ConsistencyField(handler)

        # Education
        # TODO: this should maybe be broken into separate fields
        self.education = ConsistencyField(handler)

        # Employment
        # TODO: this should maybe be broken into separate fields
        self.employment = ConsistencyField(handler)

        self.wealth = ConsistencyField(handler)

        # TODO: this should maybe be broken into separate fields
        self.bank_account_info = ConsistencyField(handler)

        self.signature = ConsistencyField(handler)

        



    

   