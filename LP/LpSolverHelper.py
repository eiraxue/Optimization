import re

import numpy as np

from datamodel.RepoDataModel import ProductAttribute


def generateConstraintsObjF(inventory, deals, borrowRates):
    N_deal = len(deals)
    N_prod = len(inventory)
    N_bRate = len(borrowRates)
    #
    # # dimension of the variables
    # N = N_deal * N_prod + N_bRate
    # a = np.zeros(shape=(1, N))
    #
    # # total number of constraints
    # N_C = N_deal + N_prod
    # for ele in deals:
    #     d = deals[ele]
    #     N_C += d.getConstraintsN()
    # print N_C

    N_variables, N_constraints = calNumberOfVariablesConstraints(inventory, deals, borrowRates)
    print N_variables, N_constraints

    # generate constraints for deal MKV
    A = np.zeros(shape=(N_constraints, N_variables))
    c = np.zeros(shape=(1, N_constraints))
    i_constraints = 0
    for d in deals:
        d_index = int(re.search(r'\d+', d).group())
        a0 = np.zeros(shape=(1, N_deal * N_prod))
        a1 = -np.ones(shape=(1, N_bRate))
        for p in inventory:
            p_index = int(re.search(r'\d+', p).group())
            a0[0][(p_index - 1) * N_prod + d_index - 1] = -inventory[p].getPrice()
        A[i_constraints][0:N_deal * N_prod] = a0

        A[i_constraints][(N_deal * N_prod + (d_index-1)*N_bRate):(N_deal * N_prod+d_index*N_bRate)] = a1
        c[0][i_constraints] = -deals[d].getMKV()
        i_constraints += 1

    print "Total %f constraints generated !" % (i_constraints)

    # generate constraints for product qty
    for p in inventory:
        p_index = int(re.search(r'\d+', p).group())
        a0 = np.zeros(shape=(1, N_deal * N_prod))
        for d in deals:
            d_index = int(re.search(r'\d+', d).group())
            a0[0][(p_index - 1) * N_prod + d_index - 1] = 1.0
        A[i_constraints][0:N_deal * N_prod] = a0
        c[0][i_constraints] = inventory[p].getQty()
        i_constraints += 1

    print "Total %f constraints generated !" % (i_constraints)

    # index the credit and asset to pupulate matrix A
    creditDict = {"AAA": 1, "AA": 2, "A": 3, "BBB": 4, "BB": 5, "B": 6}
    assetDict = {"Sovereign": 1, "Corporate": 2, "Municipal": 3}
    assetSize = len(assetDict)
    creditSize = len(creditDict)

    # generate constraints for requirements in the deals
    for d in deals:
        d_index = int(re.search(r'\d+', d).group())
        assetReqs = deals[d].getAssetReqs()
        creditReqs = deals[d].getCreditReqs()

        # asset requirements
        for assetR in assetReqs:
            a0 = np.zeros(shape=(1, N_deal * N_prod))
            a1 = np.zeros(shape=(1, N_bRate))
            for p in inventory:
                p_index = int(re.search(r'\d+', p).group())
                assetProduct = inventory[p].getAsset()
                if assetProduct == assetR:
                    a0[0][(p_index - 1) * N_prod + d_index - 1] = -inventory[p].getPrice()

            index_a1 = assetDict[assetR]
            for i in range(creditSize):
                a1[0][(index_a1 - 1) * creditSize + i] = -1.0

            A[i_constraints][0:N_deal * N_prod] = a0
            A[i_constraints][(N_deal * N_prod + (d_index-1)*N_bRate):(N_deal * N_prod+d_index*N_bRate)] = a1

            c[0][i_constraints] = -assetReqs[assetR]
            i_constraints += 1

        for creditR in creditReqs:
            a0 = np.zeros(shape=(1, N_deal * N_prod))
            a1 = np.zeros(shape=(1, N_bRate))
            for p in inventory:
                p_index = int(re.search(r'\d+', p).group())
                creditProduct = inventory[p].getCredit()
                if creditProduct == creditR:
                    a0[0][(p_index - 1) * N_prod + d_index - 1] = -inventory[p].getPrice()

            index_a1 = creditDict[creditR]
            for i in range(assetSize):
                a1[0][i * creditSize + index_a1 - 1] = -1.0

            A[i_constraints][0:N_deal * N_prod] = a0
            A[i_constraints][N_deal * N_prod + (d_index-1)*N_bRate:N_deal * N_prod+d_index*N_bRate] = a1
            c[0][i_constraints] = -creditReqs[creditR]
            i_constraints += 1
    print "Total %f constraints generated !" % (i_constraints)

    # generate objective function
    objF = np.zeros(shape = (1, N_variables))

    for d in deals:
        d_index = int(re.search(r'\d+', d).group())

        for assetR in assetDict:
            for creditR in creditDict:
                index_a1 = (assetDict[assetR] - 1) * creditSize + creditDict[creditR] - 1
                prodAttr = ProductAttribute(creditR, assetR)
                objF[0][N_deal*N_prod + (d_index-1)*N_bRate+index_a1]=borrowRates[prodAttr]

    return objF, A, c


def calNumberOfVariablesConstraints(inventory, deals, borrowRates):
    N_deal = len(deals)
    N_prod = len(inventory)
    N_bRate = len(borrowRates)

    # dimension of the variables
    N = N_deal * N_prod + N_bRate*N_deal

    # total number of constraints
    N_C = N_deal + N_prod
    for ele in deals:
        d = deals[ele]
        N_C += d.getConstraintsN()

    return N, N_C
