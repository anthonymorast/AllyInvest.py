class Holding():
    def __init__(self):
        pass

    def from_xml(self, xml):
        pass

    def from_json(self, json):
        # Feeling thankful for Notepad++ macros...
        if 'accounttype' in json:
        	self.accounttype = json['accounttype']
        if 'assetclass' in json:
        	self.assetclass = json['assetclass']
        if 'cfi' in json:
        	self.cfi = json['cfi']
        if 'change' in json['quote']:
        	self.change = json['quote']['change']
        if 'costbasis' in json:
        	self.costbasis = json['costbasis']
        if 'cusip' in json['instrument']:
        	self.cusip = json['instrument']['cusip']
        if 'desc' in json:
        	self.desc = json['desc']
        if 'factor' in json['instrument']:
        	self.factor = json['instrument']['factor']
        if 'gainloss' in json:
        	self.gainloss = json['gainloss']
        if 'lastprice' in json['quote']:
        	self.lastprice = json['quote']['lastprice']
        if 'marketvalue' in json:
        	self.marketvalue = json['marketvalue']
        if 'marketvaluechange' in json:
        	self.marketvaluechange = json['marketvaluechange']
        if 'matdt' in json:
        	self.matdt = json['matdt']
        if 'mmy' in json:
        	self.mmy = json['mmy']
        if 'mult' in json:
        	self.mult = json['mult']
        if 'price' in json:
        	self.price = json['price']
        if 'purchaseprice' in json:
        	self.purchaseprice = json['purchaseprice']
        if 'putcall' in json:
        	self.putcall = json['putcall']
        if 'qty' in json:
        	self.qty = json['qty']
        if 'sectyp' in json['instrument']:
        	self.sectyp = json['instrument']['sectyp']
        if 'strkpx' in json:
        	self.strkpx = json['strkpx']
        if 'sym' in json['instrument']:
        	self.sym = json['instrument']['sym']
        if 'totalsecurities' in json:
        	self.totalsecurities = json['totalsecurities']
