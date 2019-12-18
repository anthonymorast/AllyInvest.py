class Quote():
    def __init__(self):
        pass

    def from_xml(self, xml):
        pass

    def from_json(self, json):
        if 'adp_100' in json:
        	self.adp_100 = json['adp_100']
        if 'adp_200' in json:
        	self.adp_200 = json['adp_200']
        if 'adp_50' in json:
        	self.adp_50 = json['adp_50']
        if 'adv_21' in json:
        	self.adv_21 = json['adv_21']
        if 'adv_30' in json:
        	self.adv_30 = json['adv_30']
        if 'adv_90' in json:
        	self.adv_90 = json['adv_90']
        if 'ask' in json:
        	self.ask = json['ask']
        if 'ask_time' in json:
        	self.ask_time = json['ask_time']
        if 'asksz' in json:
        	self.asksz = json['asksz']
        if 'basis' in json:
        	self.basis = json['basis']
        if 'beta' in json:
        	self.beta = json['beta']
        if 'bid' in json:
        	self.bid = json['bid']
        if 'bid_time' in json:
        	self.bid_time = json['bid_time']
        if 'bidsz' in json:
        	self.bidsz = json['bidsz']
        if 'bidtick' in json:
        	self.bidtick = json['bidtick']
        if 'chg' in json:
        	self.chg = json['chg']
        if 'chg_sign' in json:
        	self.chg_sign = json['chg_sign']
        if 'chg_t' in json:
        	self.chg_t = json['chg_t']
        if 'cl' in json:
        	self.cl = json['cl']
        if 'contract_size' in json:
        	self.contract_size = json['contract_size']
        if 'cusip' in json:
        	self.cusip = json['cusip']
        if 'date' in json:
        	self.date = json['date']
        if 'datetime' in json:
        	self.datetime = json['datetime']
        if 'days_to_expiration' in json:
        	self.days_to_expiration = json['days_to_expiration']
        if 'div' in json:
        	self.div = json['div']
        if 'divexdate' in json:
        	self.divexdate = json['divexdate']
        if 'divfreq' in json:
        	self.divfreq = json['divfreq']
        if 'divpaydt' in json:
        	self.divpaydt = json['divpaydt']
        if 'dollar_value' in json:
        	self.dollar_value = json['dollar_value']
        if 'eps' in json:
        	self.eps = json['eps']
        if 'exch' in json:
        	self.exch = json['exch']
        if 'exch_desc' in json:
        	self.exch_desc = json['exch_desc']
        if 'hi' in json:
        	self.hi = json['hi']
        if 'iad' in json:
        	self.iad = json['iad']
        if 'idelta' in json:
        	self.idelta = json['idelta']
        if 'igamma' in json:
        	self.igamma = json['igamma']
        if 'imp_volatility' in json:
        	self.imp_volatility = json['imp_volatility']
        if 'incr_vl' in json:
        	self.incr_vl = json['incr_vl']
        if 'irho' in json:
        	self.irho = json['irho']
        if 'issue_desc' in json:
        	self.issue_desc = json['issue_desc']
        if 'itheta' in json:
        	self.itheta = json['itheta']
        if 'ivega' in json:
        	self.ivega = json['ivega']
        if 'last' in json:
        	self.last = json['last']
        if 'lo' in json:
        	self.lo = json['lo']
        if 'name' in json:
        	self.name = json['name']
        if 'op_delivery' in json:
        	self.op_delivery = json['op_delivery']
        if 'op_flag' in json:
        	self.op_flag = json['op_flag']
        if 'op_style' in json:
        	self.op_style = json['op_style']
        if 'op_subclass' in json:
        	self.op_subclass = json['op_subclass']
        if 'openinterest' in json:
        	self.openinterest = json['openinterest']
        if 'opn' in json:
        	self.opn = json['opn']
        if 'opt_val' in json:
        	self.opt_val = json['opt_val']
        if 'pchg' in json:
        	self.pchg = json['pchg']
        if 'pchg_sign' in json:
        	self.pchg_sign = json['pchg_sign']
        if 'pcls' in json:
        	self.pcls = json['pcls']
        if 'pe' in json:
        	self.pe = json['pe']
        if 'phi' in json:
        	self.phi = json['phi']
        if 'plo' in json:
        	self.plo = json['plo']
        if 'popn' in json:
        	self.popn = json['popn']
        if 'pr_adp_100' in json:
        	self.pr_adp_100 = json['pr_adp_100']
        if 'pr_adp_200' in json:
        	self.pr_adp_200 = json['pr_adp_200']
        if 'pr_adp_50' in json:
        	self.pr_adp_50 = json['pr_adp_50']
        if 'pr_date' in json:
        	self.pr_date = json['pr_date']
        if 'pr_openinterest' in json:
        	self.pr_openinterest = json['pr_openinterest']
        if 'prbook' in json:
        	self.prbook = json['prbook']
        if 'prchg' in json:
        	self.prchg = json['prchg']
        if 'prem_mult' in json:
        	self.prem_mult = json['prem_mult']
        if 'put_call' in json:
        	self.put_call = json['put_call']
        if 'pvol' in json:
        	self.pvol = json['pvol']
        if 'qcond' in json:
        	self.qcond = json['qcond']
        if 'rootsymbol' in json:
        	self.rootsymbol = json['rootsymbol']
        if 'secclass' in json:
        	self.secclass = json['secclass']
        if 'sesn' in json:
        	self.sesn = json['sesn']
        if 'sho' in json:
        	self.sho = json['sho']
        if 'strikeprice' in json:
        	self.strikeprice = json['strikeprice']
        if 'symbol' in json:
        	self.symbol = json['symbol']
        if 'tcond' in json:
        	self.tcond = json['tcond']
        if 'timestamp' in json:
        	self.timestamp = json['timestamp']
        if 'tr_num' in json:
        	self.tr_num = json['tr_num']
        if 'tradetick' in json:
        	self.tradetick = json['tradetick']
        if 'trend' in json:
        	self.trend = json['trend']
        if 'under_cusip' in json:
        	self.under_cusip = json['under_cusip']
        if 'undersymbol' in json:
        	self.undersymbol = json['undersymbol']
        if 'vl' in json:
        	self.vl = json['vl']
        if 'volatility12' in json:
        	self.volatility12 = json['volatility12']
        if 'vwap' in json:
        	self.vwap = json['vwap']
        if 'wk52hi' in json:
        	self.wk52hi = json['wk52hi']
        if 'wk52hidate' in json:
        	self.wk52hidate = json['wk52hidate']
        if 'wk52lo' in json:
        	self.wk52lo = json['wk52lo']
        if 'wk52lodate' in json:
        	self.wk52lodate = json['wk52lodate']
        if 'xdate' in json:
        	self.xdate = json['xdate']
        if 'xday' in json:
        	self.xday = json['xday']
        if 'xmonth' in json:
        	self.xmonth = json['xmonth']
        if 'xyear' in json:
        	self.xyear = json['xyear']
        # if 'yield' in json:
        # 	self.yield = json['yield']
