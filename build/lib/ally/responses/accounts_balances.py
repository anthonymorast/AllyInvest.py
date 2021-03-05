from .response import *

class AccountsBalancesResponse(Response):
    def __init__(self, response_format, data):
        super().__init__(response_format, data)
        self.account_data = {}      # a dictionary of dictionaries
        if response_format.lower() == 'xml':
            self.__parse_xml(data)
        elif response_format.lower() == 'json':
            self.__parse_json(data)

    def get_account_data_by_account(self, id):
        return self.account_data[str(id)]

    def get_all_account_data(self):
        return self.account_data

    def __parse_xml(self, data):
        pass

    def __parse_json(self, data):
        super().parse_json(data)
        for account in self.json["accountbalance"]:
            this_data = {}
            this_data["accountname"] = account["accountname"]
            this_data["accountvalue"] = account["accountvalue"]
            self.account_data[account["account"]] = this_data
