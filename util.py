import json

class JsonSerializable():
    def to_json(self):
        jsondict = self._to_dict()
        return json.dumps(jsondict, ensure_ascii=False)

    def _to_dict(self):
        jsondict = {}
        for key in self.__dict__.keys():
            v = getattr(self, key)
            if isinstance(v, JsonSerializable):
                jsondict[key] = v._to_dict()
            else:
                jsondict[key] = v
        return jsondict