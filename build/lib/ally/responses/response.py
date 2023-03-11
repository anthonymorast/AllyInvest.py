import json

class Response():
    def __init__(self, response_format, data):
        self.response_format = response_format
        self.raw_data = data
        self.error = ''

    def parse_xml(self, data):
        self.xml = data
        self.error = data.find('error').text

    def parse_json(self, data):
        self.json = json.loads(json.dumps(data["response"]))
        self.error = self.json['error']

    def get_raw_data(self):
        return self.raw_data
