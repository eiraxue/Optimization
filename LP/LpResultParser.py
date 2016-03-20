import re

from LpSolverHelper import calNumberOfVariablesConstraints

import datamodel.RepoAllocModel as allocModel


def parseLpSolverResult(result, inventory, deals, borrowRates):
    res = result["x"]
    N_deal = len(deals)
    N_prod = len(inventory)
    N_bRate = len(borrowRates)

    N_variables, N_constraints = calNumberOfVariablesConstraints(inventory, deals, borrowRates)

    collAlloc = []
    for p in inventory:
        p_index = int(re.search(r'\d+', p).group())
        for d in deals:
            d_index = int(re.search(r'\d+', d).group())
            alloc_qty = res[(p_index - 1) * N_prod + d_index - 1]
            alloc = allocModel.CollateralAllocation(p, d, float(alloc_qty))
            collAlloc.append(alloc)

    borrowAlloc = []
    creditDict = {"AAA": 1, "AA": 2, "A": 3, "BBB": 4, "BB": 5, "B": 6}
    assetDict = {"Sovereign": 1, "Corporate": 2, "Municipal": 3}
    assetSize = len(assetDict)
    creditSize = len(creditDict)

    base_index = N_prod * N_deal
    for d in deals:
        d_index = int(re.search(r'\d+', d).group())

        for asset in assetDict:
            for credit in creditDict:
                index_borrow = (assetDict[asset] - 1) * creditSize + (creditDict[credit] - 1)
                bAlloc = allocModel.BorrowAllocation(d, credit, asset, float(
                        res[base_index + (d_index - 1) * N_bRate + index_borrow]))
                borrowAlloc.append(bAlloc)

    return collAlloc, borrowAlloc
