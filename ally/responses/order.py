from xml.etree import ElementTree

def get_class_vars(class_type):
    return [v for k, v in vars(class_type).items() if \
            not k.startswith('_')]

class Order():
    def __init__(self, **data):
        # From Request Object.
        self.acct = data.get('acct')
        # Stock Symbol.
        self.sym = data.get('sym')
        # Number of Shares.
        self.qty = str(int(data.get('qty')))
        # use class SECURITY_TYPE
        self.sec_typ = str(data.get('sec_typ', ''))
        # use class SIDE
        self.side = str(data.get('side', ''))
        # use class ORDER_TYPE
        self.typ = str(data.get('typ', ''))

        # For Changes and Cancels
        self.ord_id = data.get('ord_id')

        # For Buying to Cover a Short Position.
        self.acct_typ = data.get('acct_typ')

        # For Limit Orders
        # Limit Price.
        self.px = f"{data.get('px', 0.0):.2f}"
        # use class TIME_IN_FORCE
        self.tm_in_force = str(data.get('tm_in_force', ''))

        # For Options
        # use class OPTION_POSITION
        self.pos_efct = str(data.get('pos_efct', ''))
        # Strike Price.
        self.strk_px = f"{data.get('strk_px', 0.0):.2f}"
        # use class OPTION_CLASS
        self.cfi = str(data.get('cfi', ''))
        # Date of Maturity.
        self.mat_dt = data.get('mat_dt')
        # Option Expiration.
        self.mmy = data.get('mmy')

    def validate(self):
        """Verify all required information is in the order.
        """
        # Account must exist.
        assert self.acct
        # Symbol must exist.
        assert self.sym
        # Quantity must exist and be an integer greater than zero.
        # Partials are sold when # shares held is less than one.
        assert int(self.qty) > 0
        # Order type must exist and be in ORDER_TYPE.
        assert self.typ
        assert self.typ in get_class_vars(ORDER_TYPE)
        # Side must exist and be in SIDE.
        assert self.side
        assert self.side in get_class_vars(SIDE)
        # Security type must exist and be in SECURITY_TYPE.
        assert self.sec_typ
        assert self.sec_typ in get_class_vars(SECURITY_TYPE)

        # If Account Type is used, it must be in ACCOUNT_TYPE.
        if self.acct_typ:
            assert self.acct_type in get_class_vars(ACCOUNT_TYPE)

        if self.typ != ORDER_TYPE.MARKET:
            # Time in Force must exist and be in TIME_IN_FORCE.
            assert self.tm_in_force
            assert self.tm_in_force in get_class_vars(TIME_IN_FORCE)
        if self.typ in [ORDER_TYPE.LIMIT, ORDER_TYPE.STOP_LIMIT]:
            # Price must exist and be a float greater than zero.
            assert self.px
            assert float(self.px) > 0.0

        if self.sec_typ == SECURITY_TYPE.OPTION:
            # Position must exist and be in OPTION_POSITION.
            assert self.pos_efct
            assert self.pos_efct in get_class_vars(OPTION_POSITION)
            # Strike Price must exist & be a float greater than zero.
            assert self.strk_px
            assert float(self.strk_px) > 0.0
            # CFI must exist and be in OPTION_CLASS.
            assert self.cfi
            assert self.cfi in get_class_vars(OPTION_CLASS)
            # Date of Maturity must exist.
            assert self.mat_dt
            # Option Expiration must exist.
            assert self.mmy

        return True

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

    def to_fixml(self, cancel=False):
        """Convert the contents of the order to FIXML.
           This is only for common stock and single-leg options.
            @param self - the object pointer
            @param cancel - should this order be cancelled only?
        """
        nsp = {'xmlns': 'http://www.fixprotocol.org/FIXML-5-0-SP2'}
        order_tag = "Order"
        if self.ord_id and cancel:
            order_tag = "OrdCxlReq"
        elif self.ord_id:
            order_tag = "OrdCxlRplcReq"

        # Now Build the FIXML.
        # First get the attributes always required.
        base_xml = ElementTree.Element("FIXML", nsp)
        order = ElementTree.SubElement(base_xml, order_tag)
        order.set('Acct', self.acct)
        order.set('Typ', self.typ)
        order.set('Side', self.side)
        instrmt = ElementTree.SubElement(order, 'Instrmt')
        instrmt.set('SecTyp', self.sec_typ)
        instrmt.set('Sym', self.sym)
        ordqty = ElementTree.SubElement(order, 'OrdQty')
        ordqty.set('Qty', self.qty)

        # Add field-dependent attributes.
        if self.ord_id:
            order.set('OrigID', self.ord_id)
        if self.side == SIDE.BUY and \
           self.acct_typ == ACCOUNT_TYPE.SHORT:
            order.set('AcctTyp', self.acct_typ)
        if self.typ != ORDER_TYPE.MARKET:
            order.set('TmInForce', self.tm_in_force)
            if self.typ != ORDER_TYPE.STOP:
                order.set('Px', self.px)
        if self.sec_typ == SECURITY_TYPE.OPTION:
            order.set('PosEfct', self.pos_efct)
            instrmt.set('CFI', self.cfi)
            instrmt.set('StrkPx', self.strk_px)
            instrmt.set('MMY', self.mmy)
            instrmt.set('MatDt', self.mat_dt.isoformat())

        return base_xml

def get_multileg_fixml(orders, cancel=False):
    """Create FIXML for a multi-leg option chain using multiple orders.
        @param orders - A list of the orders.
        @param cancel - should this order be cancelled only?
    """
    if not orders:
        return None
    # Validate all the orders have the same basic info.
    orders[0].validate()
    chk_dict = dict(ord_id=orders[0].ord_id,
                    typ=orders[0].typ,
                    tm_in_force=orders[0].tm_in_force,
                    px=orders[0].px,
                    acct=orders[0].acct,
                    sym=orders[0].sym,
                   )
    for order in orders[1:]:
        # Along with validation, all basic data must match.
        order.validate()
        assert order.ord_id == chk_dict['ord_id']
        assert order.typ == chk_dict['typ']
        assert order.tm_in_force == chk_dict['tm_in_force']
        assert order.px == chk_dict['px']
        assert order.acct == chk_dict['acct']
        assert order.sym == chk_dict['sym']

    # Set the Namespace and base tag name.
    nsp = {'xmlns': 'http://www.fixprotocol.org/FIXML-5-0-SP2'}
    order_tag = "NewOrdMLeg"
    if chk_dict['ord_id'] and cancel:
        order_tag = "OrdCxlReq"
    elif chk_dict['ord_id']:
        order_tag = "MLegOrdCxlRplc"

    # Now Build the FIXML.
    # First get the attributes always required.
    base_xml = ElementTree.Element("FIXML", nsp)
    mleg = ElementTree.SubElement(base_xml, order_tag)
    mleg.set('Acct', chk_dict['acct'])
    if chk_dict['ord_id']:
        # For a replace or cancel, the original ID is needed.
        mleg.set('OrigCIOrdID', chk_dict['ord_id'])
    if chk_dict['ord_id'] and cancel:
        # For a cancel, the FIXML is much simpler.
        instrmt = ElementTree.SubElement(mleg, 'Instrmt')
        instrmt.set('SecTyp', SECURITY_TYPE.MLEG)
        instrmt.set('Sym', chk_dict['sym'])
    else:
        # For all others, fill in the rest of the info for each leg.
        mleg.set('OrdTyp', chk_dict['typ'])
        if chk_dict['typ'] == ORDER_TYPE.LIMIT:
            mleg.set('TmInForce', chk_dict['tm_in_force'])
            mleg.set('Px', chk_dict['px'])
        for order in orders:
            # Cycle through each order and add it.
            ord_el = ElementTree.SubElement(mleg, 'Ord')
            ord_el.set('OrdQty', order.qty)
            ord_el.set('PosEfct', order.pos_efct)
            leg = ElementTree.SubElement(ord_el, 'Leg')
            leg.set('Side', order.side)
            leg.set('Strk', order.strk_px)
            leg.set('Mat', order.mat_dt.isoformat())
            leg.set('MMY', order.mmy)
            leg.set('SecTyp', order.sec_typ)
            leg.set('CFI', order.cfi)
            leg.set('Sym', order.sym)

    return base_xml

class TIME_IN_FORCE:
    DAY = "0"
    GTC = "1"
    MARKET_ON_CLOSE = "7"

class ACCOUNT_TYPE:
    SHORT = "5"

class ORDER_TYPE:
    MARKET = "1"
    LIMIT = "2"
    STOP = "3"
    STOP_LIMIT = "4"

class SIDE:
    BUY = "1"
    SELL = "2"
    SELL_SHORT = "5"

class SECURITY_TYPE:
    COMMON_STOCK = "CS"
    OPTION = "OPT"
    MULTI_LEG = "MLEG"

class OPTION_POSITION:
    OPEN = "O"
    CLOSE = "C"

class OPTION_CLASS:
    CALL = "OC"
    PUT = "OP"
