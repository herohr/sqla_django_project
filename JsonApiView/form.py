from JsonApiView import ErrorResponse


class JsonForm:
    def __init__(self, json_dict, fields, **checker):
        self.json = json_dict
        self.fields = fields
        self.checker = checker
        self.not_valid_fields = []

    def check(self, field_name):
        none_obj = object()
        val = self.json.get(field_name, none_obj)
        if val is none_obj:
            return False
        if field_name in self.checker:
            try:
                if not self.checker[field_name](val):
                    return False
            except Exception:
                return False
        setattr(self, field_name, val)
        return True

    def is_valid(self):
        not_valid_fields = []
        for f in self.fields:
            r = self.check(f)
            if not r:
                not_valid_fields.append(f)
        if not_valid_fields:
            self.not_valid_fields = not_valid_fields
            return False
        return True

    def __bool__(self):
        r, _ = self.is_valid()
        return r

    def error_resp(self):
        return ErrorResponse(400, "fields: {} not valid or not given".format(self.not_valid_fields))
