class Order():
    def __init__(self):
        pass

    def from_xml(self, xml):
        nsp = {'': 'http://www.fixprotocol.org/FIXML-5-0-SP2'}
        exec_rpt = xml.find('FIXML', nsp).find('ExecRpt', nsp)
        if not exec_rpt:
          return
        self.ord_id = exec_rpt.attrib.get('OrdID')
        self.id = exec_rpt.attrib.get('ID')
        self.stat = exec_rpt.attrib.get('Stat')
        self.acct = exec_rpt.attrib.get('Acct')
        self.acct_typ = exec_rpt.attrib.get('AcctTyp')
        self.side = exec_rpt.attrib.get('Side')
        self.typ = exec_rpt.attrib.get('Typ')
        self.px = exec_rpt.attrib.get('Px')
        self.tm_in_force = exec_rpt.attrib.get('TmInForce')
        self.leaves_qty = exec_rpt.attrib.get('LeavesQty')
        self.trd_dt = exec_rpt.attrib.get('TrdDt')
        self.txn_tm = exec_rpt.attrib.get('TxnTm')
        instrmt = exec_rpt.find('Instrmt', nsp)
        if instrmt:
            self.sym = instrmt.attrib.get('Sym')
            self.sec_typ = instrmt.attrib.get('SecTyp')
            self.desc = instrmt.attrib.get('Desc')
        ordqty = exec_rpt.find('OrdQty', nsp)
        if ordqty:
            self.qty = ordqty.attrib.get('Qty')
        comm = exec_rpt.find('Comm', nsp)
        if comm:
            self.comm = comm.attrib.get('Comm')

    def from_json(self, json):
        exec_rpt = json.get('FIXML', {}).get('ExecRpt')
        if not exec_rpt:
          return
        self.ord_id = exec_rpt.get('@OrdID')
        self.id = exec_rpt.get('@ID')
        self.stat = exec_rpt.get('@Stat')
        self.acct = exec_rpt.get('@Acct')
        self.acct_typ = exec_rpt.get('@AcctTyp')
        self.side = exec_rpt.get('@Side')
        self.typ = exec_rpt.get('@Typ')
        self.px = exec_rpt.get('@Px')
        self.tm_in_force = exec_rpt.get('@TmInForce')
        self.leaves_qty = exec_rpt.get('@LeavesQty')
        self.trd_dt = exec_rpt.get('@TrdDt')
        self.txn_tm = exec_rpt.get('@TxnTm')
        instrmt = exec_rpt.get('Instrmt')
        if instrmt:
            self.sym = instrmt.get('@Sym')
            self.sec_typ = instrmt.get('@SecTyp')
            self.desc = instrmt.get('@Desc')
        ordqty = exec_rpt.get('OrdQty')
        if ordqty:
            self.qty = ordqty.get('@Qty')
        comm = exec_rpt.get('Comm')
        if comm:
            self.comm = comm.get('@Comm')
