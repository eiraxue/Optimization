class CollateralAllocation:
    def __init__(self, prod, deal, qty):
        self.prod = prod
        self.deal = deal
        self.qty = qty

    def __str__(self):
        return "%s, %s, %f" % (self.prod, self.deal, self.qty)

    def getProduct(self):
        return self.prod

    def getDeal(self):
        return self.deal

    def getQty(self):
        return self.qty



class BorrowAllocation:
    def __init__(self, deal, credit, asset, mkv):
        self.deal = deal
        self.credit =credit
        self.asset = asset
        self.mkv = mkv

    def __str__(self):
        return "%s %s, %s, %f" % (self.deal, self.credit, self.asset, self.mkv)

    def getCredit(self):
        return self.credit

    def getDeal(self):
        return self.deal

    def getMkv(self):
        return self.mkv

    def getAsset(self):
        return self.asset
