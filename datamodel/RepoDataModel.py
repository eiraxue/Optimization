class Product:
    def __init__(self, id, price, assetClass, creditClass, qty):
        self.id = id
        self.price = price
        self.assetClass = assetClass
        self.creditClass = creditClass
        self.qty = qty

    def __str__(self):
        return "Product %s: price [%f], asset [%s], credit [%s], qty [%f]" % (self.id, self.price, self.assetClass, self.creditClass, self.qty)

    def getAsset(self):
        return self.assetClass

    def getCredit(self):
        return self.creditClass

    def getPrice(self):
        return self.price

    def setQty(self, qty):
        self.qty = qty

    def getQty(self):
        return self.qty

    def subtractQty(self, qty):
        self.qty -= qty


class Deal:
    def __init__(self, id, mkv):
        self.id = id
        self.mkv = mkv
        self.assetReqs = {}
        self.creditReqs = {}
        self.filledMKV = 0.0
        self.constraintsN = 0

    def __str__(self):
        str = "Deal %s: mkv [%f], " % (self.id, self.mkv)

        str += "AssetReqs ["
        for ele in self.assetReqs:
            str += " %s, minMKV %f; " % (ele, self.assetReqs[ele])
        str += "], CreditReqs ["

        for ele in self.creditReqs:
            str += " %s, minMKV %f; " % (ele, self.creditReqs[ele])
        str += " ]"
        return str

    def getId(self):
        return self.id

    def getMKV(self):
        return self.mkv

    def addAssetReq(self, asset, pct):
        self.assetReqs[asset] = pct*self.mkv/100.0
        self.constraintsN += 1

    def addCreditReq(self, credit, pct):
        self.creditReqs[credit] = pct*self.mkv/100.0
        self.constraintsN += 1

    def getConstraintsN(self):
        return self.constraintsN

    def reduceAssetReq(self, asset, mkv):
        self.assetReqs[asset] -= mkv

    def reduceCreditReq(self, credit, mkv):
        self.assetReqs[credit] -= mkv

    def fillMKV(self, mkv):
        self.filledMKV += mkv

    def getAssetReqs(self):
        return self.assetReqs

    def getCreditReqs(self):
        return self.creditReqs

    def getAssetReqsN(self):
        return len(self.assetReqs)

    def getCreditReqsN(self):
        return len(self.creditReqs)


class ProductAttribute:
    def __init__(self, credit, asset):
        self.credit = credit
        self.asset = asset


    def __hash__(self):
        return hash((self.asset, self.credit))

    def __eq__(self, other):
        return (self.asset, self.credit) == (other.asset, other.credit)

    def __str__(self):
        return "Asset [%s], Credit [%s]" % (self.asset, self.credit)

