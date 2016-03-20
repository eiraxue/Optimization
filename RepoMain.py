import csv

from datamodel.RepoDataModel import Deal
from datamodel.RepoDataModel import Product
from datamodel.RepoDataModel import ProductAttribute

from datamodel.RepoAllocModel import BorrowAllocation
from datamodel.RepoAllocModel import CollateralAllocation



def initialize_inventory(fileName):
    f = open(fileName)
    csv_f = csv.reader(f)
    i = 0
    inventory = {}
    for row in csv_f:
        inventory[row[0]]=Product(row[0], float(row[1]), row[2], row[3], float(row[4]))
    return inventory

def initialize_deals(dealsFile, dealAssetReq, dealCreditRq):
    f1 = open(dealsFile)
    deals_data = csv.reader(f1)
    i = 0
    deals = {}
    for row in deals_data:
        deals[row[0]] = Deal(row[0], float(row[1]))

    f2 = open(dealAssetReq)
    assetReqs = csv.reader(f2)
    for row in assetReqs:
        deals[row[0]].addAssetReq(row[1], float(row[2]))

    f3 = open(dealCreditRq)
    creditReqs = csv.reader(f3)
    for row in creditReqs:
        deals[row[0]].addCreditReq(row[1], float(row[2]))
    return deals

def createBorrowMarket(borrowFile):
    f = open(borrowFile)
    csv_f = csv.reader(f)
    borrowRates = {}
    for row in csv_f:
        attr = ProductAttribute(row[0], row[1])
        borrowRates[attr] =  float(row[2])/100
    return borrowRates

def writeInventoryAlloc(fileName, inventoryAlloc):
    f= open(fileName,'wt')
    writer = csv.writer(f)
    for ele in inventoryAlloc:
        writer.writerow((ele.getProduct(),  ele.getDeal(),   ele.getQty()))


def print_List(aList):
    for ele in aList:
        print ele

def print_dict(aDict):
    for ele in aDict:
        print ele, aDict[ele]

# parse the input data files
baseDir = "C:/Users/Ron/workspace_eclipse/Optimization/input/"

inventoryFile = baseDir+ 'InventoryPositions.csv'
inventory = initialize_inventory(inventoryFile)
print_dict(inventory)

dealsFile =  baseDir+ 'RepoDeals.csv'
dealAssetReq =  baseDir+ 'RepoDealAssetClassRequirements.csv'
dealCreditRq =  baseDir+ 'RepoDealCreditRatingRequirements.csv'
deals = initialize_deals(dealsFile, dealAssetReq, dealCreditRq)
print_dict(deals)

borrowsFile = baseDir+ 'ExternalBorrowRates.csv'
borrowRates = createBorrowMarket(borrowsFile)
print_dict(borrowRates)

from LP import LpResultParser, LPsolver, LpSolverHelper

# calculate the number of variables and constraints
print LpSolverHelper.calNumberOfVariablesConstraints(inventory, deals, borrowRates)

# generate constraints and objective function
obj, A, b = LpSolverHelper.generateConstraintsObjF(inventory, deals, borrowRates)

print A
print b[0]
print obj[0]



result = LPsolver.RepoLPsolver(obj[0], A, b[0])
print result
collAlloc , borrowAlloc = LpResultParser.parseLpSolverResult(result, inventory, deals, borrowRates)
print_List(collAlloc)
print_List(borrowAlloc)

CollAllocName = baseDir +"CollAlloc.csv"
writeInventoryAlloc(CollAllocName, collAlloc)


creditDict = {"AAA":1, "AA": 2, "A": 3, "BBB": 4, "BB": 5, "B": 6}
assetDict = {"Sovereign": 1, "Corporate": 2, "Municipal": 3 }
print_dict(creditDict)
print_dict(assetDict)

