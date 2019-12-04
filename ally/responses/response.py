import json

class Response():
    def __init__(self, response_format, data):
        self.response_format = response_format
        self.raw_data = data

    def parse_xml(self, data):
        pass

    def parse_json(self, data):
        self.json = json.loads(json.dumps(data["response"]))

    def get_raw_data(self):
        return self.raw_data
