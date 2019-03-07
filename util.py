import json

class JsonSerializable():
    def to_json(self):
        jsondict = self._to_dict()
        return json.dumps(jsondict, ensure_ascii=False)

    def _to_dict(self):
        def _to_dict_re(value):
            if isinstance(value, JsonSerializable):
                return value._to_dict()
            else:
                return value

        jsondict = {}
        for key in self.__dict__.keys():
            value = getattr(self, key)
            if type(value) is list:
                li = []
                for item in value:
                    li.append(_to_dict_re(item))
                jsondict[key] = li
            else:
                jsondict[key] = _to_dict_re(value)

        return jsondict

