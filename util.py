import json

class JsonSerializable():
    def to_json(self):
        jsondict = self._to_dict()
        return json.dumps(jsondict, ensure_ascii=False)

    def _to_dict(self):
        def re_to_dict(value):
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
                    li.append(re_to_dict(item))
                jsondict[key] = li
            else:
                jsondict[key] = re_to_dict(value)

        return jsondict
