# Functions used for the analysis of Josie17 simulation data
# 16/01/2019

import pandas as pd
import numpy as np
import re
import glob
import math
from math import log
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib.offsetbox import AnchoredText


def Calc_average_profile_pressure(dataframelist, xcolumn):
    nd = len(dataframelist)

    yref = [1000, 850, 700, 550, 400, 350, 300, 200, 150, 100, 75, 50, 35, 25, 20, 15,
            12, 10, 8, 6]

    # yref = [1000, 850, 750, 650,  550, 450, 350, 300, 200, 175, 150, 125, 100, 80, 60, 50, 40, 35, 30, 25, 20, 15,
    #         12, 10, 8, 6]
    # #
    # yref = [1000, 950, 900, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400, 350, 325, 300, 275, 250, 225, 200, 175,
    #         150, 135, 120, 105, 90, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40, 35, 30, 28, 26, 24, 22, 20, 18, 16, 14,
    #         12, 10, 8, 6]

    n = len(yref) - 1
    Ygrid = [-9999.0] * n

    Xgrid = [[-9999.0] * n for i in range(nd)]
    Xsigma = [[-9999.0] * n for i in range(nd)]

    Agrid = [[-9999.0] * n for i in range(nd)]
    Asigma = [[-9999.0] * n for i in range(nd)]

    for j in range(nd):
        dft = dataframelist[j]
        dft.PFcor = dft[xcolumn]

        for i in range(n):
            dftmp1 = pd.DataFrame()
            dfgrid = pd.DataFrame()


            grid_min = yref[i + 1]
            grid_max = yref[i]
            Ygrid[i] = (grid_min + grid_max) / 2.0

            filta = dft.Pair >= grid_min
            filtb = dft.Pair < grid_max
            filter1 = filta & filtb
            dftmp1['X'] = dft[filter1].PFcor
            dftmp1['PO3_OPM'] = dft[filter1]['PO3_OPM']

            filtnull = dftmp1.X > -9999.0
            dfgrid['X'] = dftmp1[filtnull].X
            dfgrid['PO3_OPM'] = dftmp1[filtnull].PO3_OPM

            Xgrid[j][i] = np.nanmean(dfgrid.X)
            Xsigma[j][i] = np.nanstd(dfgrid.X)

            Agrid[j][i] = np.nanmean(dfgrid.X - dfgrid['PO3_OPM'])
            Asigma[j][i] = np.nanstd(dfgrid.X - dfgrid['PO3_OPM'])

            # print('j', j, 'i',i, Xgrid[j][i])

    return Xgrid, Xsigma, Ygrid



def Calc_average_profile_time(dataframelist, dfref,  xcolumn, refcolumn, timecolumn, ybin, tmin, tmax, boolref ):

    nd = len(dataframelist)

    ybin0 = ybin
    ymax = tmax
    ymin = 0.0
    fac = 1.0
    n = math.floor(ymax / ybin0)
    ystart = tmin
    Ygrid = [-9999.0] * n

    Xgrid = [[-9999.0] * n for i in range(nd)]
    Xsigma = [[-9999.0] * n for i in range(nd)]
    Refgrid = [[-9999.0] * n for i in range(nd)]
    Refsigma = [[-9999.0] * n for i in range(nd)]

    for j in range(nd):
        dft = dataframelist[j]
        dftr = dfref[j]

        dft.PFcor = dft[xcolumn]

        for i in range(n):
            dftmp1 = pd.DataFrame()
            dfgrid = pd.DataFrame()
            dftmpr1 = pd.DataFrame()
            dfgridr = pd.DataFrame()

            grid_min = ystart + fac * float(ybin0) * float(i)
            grid_max = ystart + fac * float(ybin0) * float(i + 1)
            Ygrid[i] = (grid_min + grid_max) / 2.0

            filta = dft[timecolumn] >= grid_min
            filtb = dft[timecolumn] < grid_max
            filter1 = filta & filtb
            filtar = dftr[timecolumn] >= grid_min
            filtbr = dftr[timecolumn] < grid_max
            filterr1 = filtar & filtbr


            dftmp1['X'] = dft[filter1][xcolumn]
            dftmpr1['Ref'] = dftr[filterr1][refcolumn]

            filtnull = dftmp1.X > -9999.0
            filtnullr = dftmpr1.Ref > -9999.0

            dfgrid['X'] = dftmp1[filtnull].X
            dfgridr['Ref'] = dftmpr1[filtnullr].Ref

            Xgrid[j][i] = np.nanmean(dfgrid.X)
            Xsigma[j][i] = np.nanstd(dfgrid.X)

            Refgrid[j][i] = np.nanmean(dfgridr.Ref)
            Refsigma[j][i] = np.nanstd(dfgridr.Ref)

            # Agrid[j][i] = np.nanmean(dfgrid.X - dfgrid['PO3_OPM'])
            # Asigma[j][i] = np.nanstd(dfgrid.X - dfgrid['PO3_OPM'])

    if not boolref: return Xgrid, Xsigma, Ygrid
    if boolref: return Xgrid, Xsigma, Refgrid, Refsigma, Ygrid

####################
def Calc_average_profile_Pair(dataframelist, xcolumn):

    #
    yref = [1000, 950, 900, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400, 350, 325, 300, 275, 250, 225, 200, 175,
            150, 135, 120, 105, 90, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40, 35, 30, 28, 26, 24, 22, 20, 18, 16, 14,
            12, 10, 8, 6]


    # yref = [1000, 850, 700,  550, 400, 350, 300, 200, 150, 100, 75,  50, 35, 25, 20, 15,
    #         12, 10, 8, 6]

    nd = len(dataframelist)


    ymin = 0.0
    fac = 1.0
    n = len(yref) - 1
    Ygrid = [-9999.0] * n

    Xgrid = [[-9999.0] * n for i in range(nd)]
    Xsigma = [[-9999.0] * n for i in range(nd)]
    Agrid = [[-9999.0] * n for i in range(nd)]
    Asigma = [[-9999.0] * n for i in range(nd)]

    for j in range(nd):
        dft = dataframelist[j]
        dft.PFcor = dft[xcolumn]

        for i in range(n):
            dftmp1 = pd.DataFrame()
            dfgrid = pd.DataFrame()
            grid_min = yref[i + 1]
            grid_max = yref[i]
            Ygrid[i] = (grid_min + grid_max) / 2.0

            filta = dft.Tsim >= grid_min
            filtb = dft.Tsim < grid_max
            filter1 = filta & filtb
            dftmp1['X'] = dft[filter1].PFcor
            dftmp1['PO3_OPM'] = dft[filter1]['PO3_OPM']

            filtnull = dftmp1.X > -9999.0
            dfgrid['X'] = dftmp1[filtnull].X
            dfgrid['PO3_OPM'] = dftmp1[filtnull].PO3_OPM

            Xgrid[j][i] = np.nanmean(dfgrid.X)
            Xsigma[j][i] = np.nanstd(dfgrid.X)

            Agrid[j][i] = np.nanmean(dfgrid.X - dfgrid['PO3_OPM'])
            Asigma[j][i] = np.nanstd(dfgrid.X - dfgrid['PO3_OPM'])



    return Xgrid, Xsigma, Ygrid



def Calc_average_profileCurrent_pressure(dataframelist, xcolumn):
    nd = len(dataframelist)

    yref = [1000, 850, 700, 550, 400, 350, 300, 200, 150, 100, 75, 50, 35, 25, 20, 15,
            12, 10, 8, 6]

    # yref = [1000, 950, 900, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400, 350, 325, 300, 275, 250, 225, 200, 175,
    #         150, 135, 120, 105, 90, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40, 35, 30, 28, 26, 24, 22, 20, 18, 16, 14,
    #         12, 10, 8, 6]


    # yref = [1000]
    # for k in range(990, 500, -50):
    #     yref.append(k)
    # for l in range(500, 300, -25):
    #     yref.append(l)
    # for m in range(300, 100, -10):
    #     yref.append(m)
    # for n in range(100, 50, -5):
    #     yref.append(n)
    # for n in range(50, 6, -2):
    #     yref.append(n)
    #
    # print(len(yref))

    n = len(yref) - 1
    Ygrid = [-9999.0] * n

    Xgrid = [[-9999.0] * n for i in range(nd)]
    Xsigma = [[-9999.0] * n for i in range(nd)]

    Agrid = [[-9999.0] * n for i in range(nd)]
    Asigma = [[-9999.0] * n for i in range(nd)]

    for j in range(nd):
        dft = dataframelist[j]
        dft.PFcor = dft[xcolumn]

        for i in range(n):
            dftmp1 = pd.DataFrame()
            dfgrid = pd.DataFrame()

            grid_min = yref[i + 1]
            grid_max = yref[i]
            Ygrid[i] = (grid_min + grid_max) / 2.0

            filta = dft.Pair >= grid_min
            filtb = dft.Pair < grid_max
            filter1 = filta & filtb
            dftmp1['X'] = dft[filter1].PFcor
            dftmp1['I_OPM_jma'] = dft[filter1]['I_OPM_jma']

            filtnull = dftmp1.X > -9999.0
            dfgrid['X'] = dftmp1[filtnull].X
            dfgrid['I_OPM_jma'] = dftmp1[filtnull].I_OPM_jma

            Xgrid[j][i] = np.nanmean(dfgrid.X)
            Xsigma[j][i] = np.nanstd(dfgrid.X)

            Agrid[j][i] = np.nanmean(dfgrid.X - dfgrid['I_OPM_jma'])
            Asigma[j][i] = np.nanstd(dfgrid.X - dfgrid['I_OPM_jma'])

            # print('j', j, 'i',i, Xgrid[j][i])

    return Xgrid, Asigma, Ygrid



def Calc_average_profileCurrent_time(dataframelist, xcolumn, ybin, tmin, tmax ):

    nd = len(dataframelist)

    ybin0 = ybin
    ymax = tmax
    ymin = 0.0
    fac = 1.0
    n = math.floor(ymax / ybin0)
    ystart = tmin
    Ygrid = [-9999.0] * n

    Xgrid = [[-9999.0] * n for i in range(nd)]
    Xsigma = [[-9999.0] * n for i in range(nd)]
    Agrid = [[-9999.0] * n for i in range(nd)]
    Asigma = [[-9999.0] * n for i in range(nd)]

    for j in range(nd):
        dft = dataframelist[j]
        dft.PFcor = dft[xcolumn]

        for i in range(n):
            dftmp1 = pd.DataFrame()
            dfgrid = pd.DataFrame()
            grid_min = ystart + fac * float(ybin0) * float(i)
            grid_max = ystart + fac * float(ybin0) * float(i + 1)
            Ygrid[i] = (grid_min + grid_max) / 2.0

            filta = dft.Tsim >= grid_min
            filtb = dft.Tsim < grid_max
            filter1 = filta & filtb
            dftmp1['X'] = dft[filter1].PFcor
            dftmp1['I_OPM_jma'] = dft[filter1]['I_OPM_jma']

            filtnull = dftmp1.X > -9999.0
            dfgrid['X'] = dftmp1[filtnull].X
            dfgrid['I_OPM_jma'] = dftmp1[filtnull].I_OPM_jma

            Xgrid[j][i] = np.nanmean(dfgrid.X)
            Xsigma[j][i] = np.nanstd(dfgrid.X)

            Agrid[j][i] = np.nanmean(dfgrid.X - dfgrid['I_OPM_jma'])
            Asigma[j][i] = np.nanstd(dfgrid.X - dfgrid['I_OPM_jma'])

    return Xgrid, Asigma, Ygrid

########

def Calc_average_Dif(dataframelist, xcolumn, opmcolumn,  stringy):


    nd = len(dataframelist)
    yref = [1000, 850, 700, 550, 400, 350, 300, 200, 150, 100, 75, 50, 35, 25, 20, 15,
            12, 10, 8, 6]

    ybin = 400
    tmin = 200
    tmax = 8000
    ybin0 = ybin
    ymax = tmax
    fac = 1.0
    ystart = tmin

    if stringy =='pressure': n = len(yref) - 1
    if stringy == 'time':     n = math.floor(ymax / ybin0)


    Ygrid = [-9999.0] * n

    Xgrid = [[-9999.0] * n for i in range(nd)]
    OPMgrid = [[-9999.0] * n for i in range(nd)]
    Xsigma = [[-9999.0] * n for i in range(nd)]

    Agrid = [[-9999.0] * n for i in range(nd)]
    Asigma = [[-9999.0] * n for i in range(nd)]

    for j in range(nd):
        dft = dataframelist[j]
        dft.PFcor = dft[xcolumn]

        for i in range(n):
            dftmp1 = pd.DataFrame()
            dfgrid = pd.DataFrame()

            if stringy == 'pressure':
                grid_min = yref[i + 1]
                grid_max = yref[i]
                Ygrid[i] = (grid_min + grid_max) / 2.0
                filta = dft.Pair >= grid_min
                filtb = dft.Pair < grid_max

            if stringy == 'time':

                grid_min = ystart + fac * float(ybin0) * float(i)
                grid_max = ystart + fac * float(ybin0) * float(i + 1)
                Ygrid[i] = (grid_min + grid_max) / 2.0
                filta = dft.Tsim >= grid_min
                filtb = dft.Tsim < grid_max


            filter1 = filta & filtb
            dftmp1['X'] = dft[filter1].PFcor
            dftmp1[opmcolumn] = dft[filter1][opmcolumn]

            filtnull = dftmp1.X > -9999.0
            dfgrid['X'] = dftmp1[filtnull].X
            dfgrid[opmcolumn] = dftmp1[filtnull][opmcolumn]

            Xgrid[j][i] = np.nanmean(dfgrid.X)
            Xsigma[j][i] = np.nanstd(dfgrid.X)
            OPMgrid[j][i] = np.nanmean(dfgrid[opmcolumn])

            Agrid[j][i] = np.nanmean(dfgrid.X - dfgrid[opmcolumn])
            Asigma[j][i] = np.nanstd(dfgrid.X - dfgrid[opmcolumn])


    dimension = len(Ygrid)
    nol = len(Xgrid)

    A1verr = [[-9999.0] * dimension for i in range(nol)]
    A1v = [[-9999.0] * dimension for i in range(nol)]
    R1verr = [[-9999.0] * dimension for i in range(nol)]
    R1v = [[-9999.0] * dimension for i in range(nol)]

    for k in range(nol):
        profO3X = Xgrid[k]
        profOPMX = OPMgrid[k]
        profO3Xerr = Asigma[k]
        for ik in range(dimension):
            A1v[k][ik] = (profO3X[ik] - profOPMX[ik])
            A1verr[k][ik] = (profO3Xerr[ik])
            R1v[k][ik] = 100 * (profO3X[ik] - profOPMX[ik]) / profOPMX[ik]
            R1verr[k][ik] = 100 * (profO3Xerr[ik] / profOPMX[ik])

    return  A1v, A1verr, R1v, R1verr, Ygrid


def Calc_Dif(O3list, OPMlist, O3errlist, dimension):

    nd = len(O3list)

    A1verr = [[-9999.0] * dimension for i in range(nd)]
    A1v = [[-9999.0] * dimension for i in range(nd)]
    R1verr = [[-9999.0] * dimension for i in range(nd)]
    R1v = [[-9999.0] * dimension for i in range(nd)]

    for j in range(nd):
        profO3X = O3list[j]
        profOPMX = OPMlist[j]
        profO3Xerr = O3errlist[j]
        for i in range(dimension):
            A1v[j][i] = (profO3X[i] - profOPMX[i])
            A1verr[j][i] = (profO3Xerr[i])
            R1v[j][i] = 100 * (profO3X[i] - profOPMX[i]) / profOPMX[i]
            R1verr[j][i] = 100 * (profO3Xerr[i] / profOPMX[i])
            ## check error

            # print('j', j, 'i',i, A1v[j][i],  R1v[j][i], R1verr[j][i] )


    return A1v, A1verr, R1v, R1verr

# def Calc_ADif(profO3X, profOPMX, profO3Xerr, dimension):
#     A1verr = [-9999.9] * dimension
#     A1v = [-9999.9] * dimension
#
#     for i in range(dimension):
#         A1v[i] = (profO3X[i] - profOPMX[i])
#         A1verr[i] = (profO3Xerr[i])
#
#     # print(A1v)
#     return A1v, A1verr
#
# def Calc_RDif(profO3X, profOPMX, profO3Xerr, dimension):
#     R1v = [-9999.9] * dimension
#     R1verr = [-9999.9] * dimension
#     A1v = [-9999.9] * dimension
#
#     for i in range(dimension):
#         A1v[i] = (profO3X[i] - profOPMX[i])
#         R1v[i] = 100 * (profO3X[i] - profOPMX[i]) / profOPMX[i]
#         # R1v[i] = 100 * (profO3X[i] - profOPMX[i]) / profO3X[i]
#
#         R1verr[i] = 100 * (profO3Xerr[i] / profOPMX[i])
#
#     # print(A1v)
#     return R1v, R1verr

###################################3
####################################
########## the rest need to be organized #######################3

# function to calculate the mean of a column ignoring the -99 values
def meanfunction(dff, Xf):
    # dft = dff
    # dft.X = dff.
    tmp1 = dff.drop_duplicates(['Sim', 'Team'])
    tmp2 = tmp1[tmp1[Xf] != -99.99]
    fmean = tmp2[Xf].mean()
    fstd = tmp2[Xf].std()

    return (str(round(fmean, 2)) + ' ± ' + str(round(fstd, 2)))





def calculate_totO3OPM(df, filt1):
    # update this according to cco calculation, using sum and shift

    dfpair_tmp1 = df.loc[filt1].sort_values(by='Pair', ascending=False)
    dfpair1 = dfpair_tmp1[dfpair_tmp1.Pair >= 0]
    dfpair1 = dfpair_tmp1[dfpair_tmp1.PO3 > 0]


    O3_tot1 = (3.9449 * (dfpair1.PO3.shift() + dfpair1.PO3) *
                                              np.log(dfpair1.Pair.shift() / dfpair1.Pair)).sum()
    O3_tot_opm1 = (3.9449 * (dfpair1.PO3_OPM.shift() + dfpair1.PO3_OPM) *
               np.log(dfpair1.Pair.shift() / dfpair1.Pair)).sum()


    return O3_tot1, O3_tot_opm1


def calculate_O3frac(df, simlist):

    for ss in simlist:

        filt1 = (df.Sim == ss) & (df.Team == 1)
        filt2 = (df.Sim == ss) & (df.Team == 2)
        filt3 = (df.Sim == ss) & (df.Team == 3)
        filt4 = (df.Sim == ss) & (df.Team == 4)

        ## the for loop is very slow :/ ## not anymore :)
        O3_tot1, O3_tot_opm1 = calculate_totO3OPM(df, filt1)
        O3_tot2 , O3_tot_opm2 = calculate_totO3OPM(df, filt2)
        O3_tot3 , O3_tot_opm3 = calculate_totO3OPM(df, filt3)
        O3_tot4, O3_tot_opm4 = calculate_totO3OPM(df, filt4)
        # idx=where(pres ge 0 and oz gt 0)

        Adif1 = O3_tot1 - O3_tot_opm1
        Adif2 = O3_tot2 - O3_tot_opm2
        Adif3 = O3_tot3 - O3_tot_opm3
        Adif4 = O3_tot4 - O3_tot_opm4

        print(ss, '1', O3_tot1, O3_tot_opm1)
        print(ss, '2', O3_tot2, O3_tot_opm2)
        print(ss, '3', O3_tot3, O3_tot_opm3)

        try:
            Rdif1 = 100.0 * (O3_tot1 - O3_tot_opm1) / O3_tot_opm1
            frac1 = O3_tot1 / O3_tot_opm1
        except ZeroDivisionError:
            Rdif1 = np.nan
            frac1 = 0.0
        try:
            Rdif2 = 100.0 * (O3_tot2 - O3_tot_opm2) / O3_tot_opm2
            frac2 = O3_tot2 / O3_tot_opm2
        except ZeroDivisionError:
            Rdif2 = np.nan
            frac2 = 0.0
        try:
            Rdif3 = 100.0 * (O3_tot3 - O3_tot_opm3) / O3_tot_opm3
            frac3 = O3_tot3 / O3_tot_opm3
        except ZeroDivisionError:
            Rdif3 = np.nan
            frac3 = 0.0
        try:
            Rdif4 = 100.0 * (O3_tot4 - O3_tot_opm4) / O3_tot_opm4
            frac4 = O3_tot4 / O3_tot_opm4
        except ZeroDivisionError:
            Rdif4 = np.nan
            frac4 = 0.0

        df.at[filt1,'O3S'] = O3_tot1
        df.at[filt1,'OPM'] = O3_tot_opm1
        df.at[filt1,'ADif'] = Adif1
        df.at[filt1,'RDif'] = Rdif1
        df.at[filt1,'frac'] = frac1

        df.at[filt2,'O3S'] = O3_tot2
        df.at[filt2,'OPM'] = O3_tot_opm2
        df.at[filt2,'ADif'] = Adif2
        df.at[filt2,'RDif'] = Rdif2
        df.at[filt2,'frac'] = frac2

        df.at[filt3,'O3S'] = O3_tot3
        df.at[filt3,'OPM'] = O3_tot_opm3
        df.at[filt3,'ADif'] = Adif3
        df.at[filt3,'RDif'] = Rdif3
        df.at[filt3,'frac'] = frac3

        df.at[filt4,'O3S'] = O3_tot4
        df.at[filt4,'OPM'] = O3_tot_opm4
        df.at[filt4,'ADif'] = Adif4
        df.at[filt4,'RDif'] = Rdif4
        df.at[filt4,'frac'] = frac4

def calculate_O3frac17(df, simlist):

    for ss in simlist:

        filt1 = (df.Sim == ss) & (df.Team == 1)
        filt2 = (df.Sim == ss) & (df.Team == 2)
        filt3 = (df.Sim == ss) & (df.Team == 3)
        filt4 = (df.Sim == ss) & (df.Team == 4)
        filt5 = (df.Sim == ss) & (df.Team == 5)
        filt6 = (df.Sim == ss) & (df.Team == 6)
        filt7 = (df.Sim == ss) & (df.Team == 7)
        filt8 = (df.Sim == ss) & (df.Team == 8)


        ## the for loop is very slow :/
        O3_tot1, O3_tot_opm1 = calculate_totO3OPM(df, filt1)
        O3_tot2 , O3_tot_opm2 = calculate_totO3OPM(df, filt2)
        O3_tot3 , O3_tot_opm3 = calculate_totO3OPM(df, filt3)
        O3_tot4, O3_tot_opm4 = calculate_totO3OPM(df, filt4)
        O3_tot5, O3_tot_opm5 = calculate_totO3OPM(df, filt5)
        O3_tot6, O3_tot_opm6 = calculate_totO3OPM(df, filt6)
        O3_tot7, O3_tot_opm7 = calculate_totO3OPM(df, filt7)
        O3_tot8, O3_tot_opm8 = calculate_totO3OPM(df, filt8)

        # idx=where(pres ge 0 and oz gt 0)

        Adif1 = O3_tot1 - O3_tot_opm1
        Adif2 = O3_tot2 - O3_tot_opm2
        Adif3 = O3_tot3 - O3_tot_opm3
        Adif4 = O3_tot4 - O3_tot_opm4
        Adif5 = O3_tot5 - O3_tot_opm5
        Adif6 = O3_tot6 - O3_tot_opm6
        Adif7 = O3_tot7 - O3_tot_opm7
        Adif8 = O3_tot8 - O3_tot_opm8

        print(ss, '1', O3_tot1, O3_tot_opm1)
        print(ss, '2', O3_tot2, O3_tot_opm2)
        print(ss, '3', O3_tot3, O3_tot_opm3)

        try:
            Rdif1 = 100.0 * (O3_tot1 - O3_tot_opm1) / O3_tot_opm1
            frac1 = O3_tot1 / O3_tot_opm1
        except ZeroDivisionError:
            Rdif1 = np.nan
            frac1 = 0.0
        try:
            Rdif2 = 100.0 * (O3_tot2 - O3_tot_opm2) / O3_tot_opm2
            frac2 = O3_tot2 / O3_tot_opm2
        except ZeroDivisionError:
            Rdif2 = np.nan
            frac2 = 0.0
        try:
            Rdif3 = 100.0 * (O3_tot3 - O3_tot_opm3) / O3_tot_opm3
            frac3 = O3_tot3 / O3_tot_opm3
        except ZeroDivisionError:
            Rdif3 = np.nan
            frac3 = 0.0
        try:
            Rdif4 = 100.0 * (O3_tot4 - O3_tot_opm4) / O3_tot_opm4
            frac4 = O3_tot4 / O3_tot_opm4
        except ZeroDivisionError:
            Rdif4 = np.nan
            frac4 = 0.0
        try:
            Rdif5 = 100.0 * (O3_tot5 - O3_tot_opm5) / O3_tot_opm5
            frac5 = O3_tot5 / O3_tot_opm5
        except ZeroDivisionError:
            Rdif5 = np.nan
            frac5 = 0.0
        try:
            Rdif6 = 100.0 * (O3_tot6 - O3_tot_opm6) / O3_tot_opm6
            frac6 = O3_tot6 / O3_tot_opm6
        except ZeroDivisionError:
            Rdif6 = np.nan
            frac6 = 0.0
        try:
            Rdif7 = 100.0 * (O3_tot7 - O3_tot_opm7) / O3_tot_opm7
            frac7 = O3_tot7 / O3_tot_opm7
        except ZeroDivisionError:
            Rdif7 = np.nan
            frac7 = 0.0
        try:
            Rdif8 = 100.0 * (O3_tot8 - O3_tot_opm8) / O3_tot_opm8
            frac8 = O3_tot8 / O3_tot_opm8
        except ZeroDivisionError:
            Rdif8 = np.nan
            frac8 = 0.0




        df.loc[filt1,'O3S'] = O3_tot1
        df.loc[filt1,'OPM'] = O3_tot_opm1
        df.loc[filt1,'ADif'] = Adif1
        df.loc[filt1,'RDif'] = Rdif1
        df.loc[filt1,'frac'] = frac1

        df.loc[filt2,'O3S'] = O3_tot2
        df.loc[filt2,'OPM'] = O3_tot_opm2
        df.loc[filt2,'ADif'] = Adif2
        df.loc[filt2,'RDif'] = Rdif2
        df.loc[filt2,'frac'] = frac2

        df.loc[filt3,'O3S'] = O3_tot3
        df.loc[filt3,'OPM'] = O3_tot_opm3
        df.loc[filt3,'ADif'] = Adif3
        df.loc[filt3,'RDif'] = Rdif3
        df.loc[filt3,'frac'] = frac3

        df.loc[filt4,'O3S'] = O3_tot4
        df.loc[filt4,'OPM'] = O3_tot_opm4
        df.loc[filt4,'ADif'] = Adif4
        df.loc[filt4,'RDif'] = Rdif4
        df.loc[filt4,'frac'] = frac4

        df.loc[filt5,'O3S'] = O3_tot5
        df.loc[filt5,'OPM'] = O3_tot_opm5
        df.loc[filt5,'ADif'] = Adif5
        df.loc[filt5,'RDif'] = Rdif5
        df.loc[filt5,'frac'] = frac5

        df.loc[filt6, 'O3S'] = O3_tot6
        df.loc[filt6, 'OPM'] = O3_tot_opm6
        df.loc[filt6, 'ADif'] = Adif6
        df.loc[filt6, 'RDif'] = Rdif6
        df.loc[filt6, 'frac'] = frac6

        df.loc[filt7, 'O3S'] = O3_tot7
        df.loc[filt7, 'OPM'] = O3_tot_opm7
        df.loc[filt7, 'ADif'] = Adif7
        df.loc[filt7, 'RDif'] = Rdif7
        df.loc[filt7, 'frac'] = frac7

        df.loc[filt8, 'O3S'] = O3_tot8
        df.loc[filt8, 'OPM'] = O3_tot_opm8
        df.loc[filt8, 'ADif'] = Adif8
        df.loc[filt8, 'RDif'] = Rdif8
        df.loc[filt8, 'frac'] = frac8




def Calc_average_profile_pressureRDif(dataframelist, xcolumn, rbool ):

    nd = len(dataframelist)

    yref = [1000, 850, 700, 550, 400, 350, 300, 200, 150, 100, 75, 50, 35, 25, 20, 15,
            12, 10, 8, 6]

    # yref = [1000, 950, 900, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400, 350, 325, 300, 275, 250, 225, 200, 175,
    #         150, 135, 120, 105, 90, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40, 35, 30, 28, 26, 24, 22, 20, 18, 16, 14,
    #         12, 10, 8, 6]

    n = len(yref) - 1
    Ygrid = [-9999.0] * n

    Xgrid = [[-9999.0] * n for i in range(nd)]
    Xsigma = [[-9999.0] * n for i in range(nd)]

    Rgrid = [[-9999.0] * n for i in range(nd)]
    Rsigma = [[-9999.0] * n for i in range(nd)]

    for j in range(nd):
        dft = dataframelist[j]
        dft.PFcor = dft[xcolumn]

        for i in range(n):
            dftmp1 = pd.DataFrame()
            dfgrid = pd.DataFrame()

            grid_min = yref[i + 1]
            grid_max = yref[i]
            Ygrid[i] = (grid_min + grid_max) / 2.0

            filta = dft.Pair >= grid_min
            filtb = dft.Pair < grid_max
            filter1 = filta & filtb
            dftmp1['X'] = dft[filter1].PFcor

            filtnull = dftmp1.X > -9999.0
            dfgrid['X'] = dftmp1[filtnull].X
            Xgrid[j][i] = np.nanmean(dfgrid.X)
            Xsigma[j][i] = np.nanstd(dfgrid.X)

            dfgrid['R'] = 100 * (dft[filter1][xcolumn] - dft[filter1]['PO3_OPM'])/ dft[filter1]['PO3_OPM']
            # Rgrid[j][i] = np.nanmean(dfgrid.R)
            # Rsigma[j][i] = np.nanstd(dfgrid.R)

            Rgrid[j][i] = np.nanmean(dfgrid.R)
            Rsigma[j][i] = np.nanstd(dfgrid.R)

            # print('j', j, 'i',i, Xgrid[j][i])
    if rbool:
        return Xgrid, Xsigma, Rgrid, Rsigma, Ygrid

    if rbool==0:
        return Xgrid, Xsigma, Ygrid

def sst_filter(df):


    filtEN = df.ENSCI == 1
    filtSP = df.ENSCI == 0

    filtS10 = df.Sol == 1
    filtS05 = df.Sol == 0.5

    filtB10 = df.Buf == 1.0
    filtB05 = df.Buf == 0.5
    filtB01 = df.Buf == 0.1

    filterEN0505 = (filtEN & filtS05 & filtB05)
    filterEN1010 = (filtEN & filtS10 & filtB10)
    # filterEN1001 = (filtEN & filtS10 & filtB01)

    profEN0505 = df.loc[filterEN0505]
    profEN1010 = df.loc[filterEN1010]
    # profEN1010 = df.loc[filterEN1001]

    profEN0505_nodup = profEN0505.drop_duplicates(['Sim', 'Team'])
    profEN1010_nodup = profEN1010.drop_duplicates(['Sim', 'Team'])

    print(profEN0505_nodup[['Sim','Team']])

    totO3_EN0505 = profEN0505_nodup.frac.mean()
    totO3_EN1010 = profEN1010_nodup.frac.mean()

    filterSP1010 = (filtSP & filtS10 & filtB10)
    filterSP0505 = (filtSP & filtS05 & filtB05)
    filterSP1001 = (filtSP & filtS10 & filtB01)

    profSP1010 = df.loc[filterSP1010]
    profSP0505 = df.loc[filterSP0505]
    # profSP0505 = df.loc[filterSP1001]

    profSP1010_nodup = profSP1010.drop_duplicates(['Sim', 'Team'])
    profSP0505_nodup = profSP0505.drop_duplicates(['Sim', 'Team'])

    totO3_SP1010 = profSP1010_nodup.frac.mean()
    totO3_SP0505 = profSP0505_nodup.frac.mean()

    prof = [profEN0505, profEN1010, profSP0505, profSP1010]
    tot03 = [totO3_EN0505, totO3_EN1010, totO3_SP0505, totO3_SP1010]

    return prof, tot03

def sst_filter17(df):


    filtEN = df.ENSCI == 1
    filtSP = df.ENSCI == 0

    filtS10 = df.Sol == 1
    filtS05 = df.Sol == 0.5

    filtB10 = df.Buf == 1.0
    filtB05 = df.Buf == 0.5
    filtB01 = df.Buf == 0.1

    filterEN0505 = (filtEN & filtS05 & filtB05)
    # filterEN1010 = (filtEN & filtS10 & filtB10)
    filterEN1010 = (filtEN & filtS10 & filtB01)

    profEN0505 = df.loc[filterEN0505]
    profEN1010 = df.loc[filterEN1010]
    # profEN1010 = df.loc[filterEN1001]

    profEN0505_nodup = profEN0505.drop_duplicates(['Sim', 'Team'])
    profEN1010_nodup = profEN1010.drop_duplicates(['Sim', 'Team'])

    print(profEN0505_nodup[['Sim','Team']])

    totO3_EN0505 = profEN0505_nodup.frac.mean()
    totO3_EN1010 = profEN1010_nodup.frac.mean()

    filterSP1010 = (filtSP & filtS10 & filtB10)
    # filterSP0505 = (filtSP & filtS05 & filtB05)
    filterSP0505 = (filtSP & filtS10 & filtB01)

    profSP1010 = df.loc[filterSP1010]
    profSP0505 = df.loc[filterSP0505]
    # profSP0505 = df.loc[filterSP1001]

    profSP1010_nodup = profSP1010.drop_duplicates(['Sim', 'Team'])
    profSP0505_nodup = profSP0505.drop_duplicates(['Sim', 'Team'])

    totO3_SP1010 = profSP1010_nodup.frac.mean()
    totO3_SP0505 = profSP0505_nodup.frac.mean()

    prof = [profEN0505, profEN1010, profSP0505, profSP1010]
    tot03 = [totO3_EN0505, totO3_EN1010, totO3_SP0505, totO3_SP1010]

    return prof, tot03


def Calc_average_Dif_2df(dataframelist, dfref,  xcolumn, refcolumn,  stringy):

    nd = len(dataframelist)
    yref = [1000, 850, 700, 550, 400, 350, 300, 200, 150, 100, 75, 50, 35, 25, 20, 15,
            12, 10, 8, 6]

    ybin = 400
    tmin = 200
    tmax = 10000
    ybin0 = ybin
    ymax = tmax
    fac = 1.0
    ystart = tmin

    if stringy =='pressure': n = len(yref) - 1
    if stringy == 'time':     n = math.floor(ymax / ybin0)

    Ygrid = [-9999.0] * n
    Xgrid = [[-9999.0] * n for i in range(nd)]
    OPMgrid = [[-9999.0] * n for i in range(nd)]
    Xsigma = [[-9999.0] * n for i in range(nd)]
    Agrid = [[-9999.0] * n for i in range(nd)]
    Asigma = [[-9999.0] * n for i in range(nd)]

    for j in range(nd):
        dft = dataframelist[j]
        dftref = dfref[j]

        # dft.PFcor = dft[xcolumn]

        for i in range(n):
            dftmp1 = pd.DataFrame()
            dftmp1r = pd.DataFrame()

            dfgrid = pd.DataFrame()
            dfgridr = pd.DataFrame()

            if stringy == 'pressure':
                grid_min = yref[i + 1]
                grid_max = yref[i]
                Ygrid[i] = (grid_min + grid_max) / 2.0
                filta = dft.Pair >= grid_min
                filtb = dft.Pair < grid_max

            if stringy == 'time':

                grid_min = ystart + fac * float(ybin0) * float(i)
                grid_max = ystart + fac * float(ybin0) * float(i + 1)
                Ygrid[i] = (grid_min + grid_max) / 2.0
                filta = dft.Tsim_original >= grid_min
                filtb = dft.Tsim_original < grid_max
                filtar = dftref.Tsim_original >= grid_min
                filtbr = dftref.Tsim_original < grid_max


            filter1 = filta & filtb
            filter1r = filtar & filtbr

            dftmp1[xcolumn] = dft[filter1][xcolumn]
            dftmp1r[refcolumn] = dftref[filter1r][refcolumn]

            # if(len(dftmp1) != len(dftmp1r) ):
            # print(len(dftmp1), len(dftmp1r))
            #
            # filtnull = (dftmp1[xcolumn] > -9999.0) & (np.abs(dftmp1[xcolumn]) != np.inf)
            # filtnullr = (dftmp1r[refcolumn] > -9999.0) & (np.abs(dftmp1r[refcolumn]) != np.inf)

            filtnull = dftmp1[xcolumn] > -9999.0
            filtnullr = dftmp1r[refcolumn] > -9999.0

            dfgrid[xcolumn] = dftmp1[filtnull][xcolumn]
            dfgridr[refcolumn] = dftmp1r[filtnullr][refcolumn]

            # if(len(dfgrid[xcolumn]) != len(dfgridr[refcolumn]) ):
            #     print(len(dfgrid[xcolumn]), len(dfgridr[refcolumn]))


            Xgrid[j][i] = np.nanmean(dfgrid[xcolumn])
            Xsigma[j][i] = np.nanstd(dfgrid[xcolumn])
            OPMgrid[j][i] = np.nanmean(dfgridr[refcolumn])

            # Agrid[j][i] = np.nanmean(dfgrid[xcolumn] - dfgridr[refcolumn])
            if( len(np.array(dfgrid[xcolumn].tolist())) != len(np.array(dfgridr[refcolumn].tolist()))):
                one = len(np.array(dfgrid[xcolumn].tolist()))
                two = len(np.array(dfgridr[refcolumn].tolist()))
                d = two - one
                aone = np.array(dfgrid[xcolumn].tolist())
                atwo_t = np.array(dfgridr[refcolumn].tolist())
                atwo = atwo_t[0:-d]
                Asigma[j][i] = np.nanstd(aone- atwo)
            if( len(np.array(dfgrid[xcolumn].tolist())) == len(np.array(dfgridr[refcolumn].tolist()))):
                Asigma[j][i] = np.nanstd(np.array(dfgrid[xcolumn].tolist()) - np.array(dfgridr[refcolumn].tolist()))


            #     print(len(np.array(dfgrid[xcolumn].tolist())), len(np.array(dfgridr[refcolumn].tolist())))
            # Asigma[j][i] = np.nanstd(np.array(dfgrid[xcolumn].tolist()) - np.array(dfgridr[refcolumn].tolist()))
            # if(len(dfgrid[xcolumn]) == len(dfgridr[refcolumn]) ):
            #
            #     # Asigma[j][i] = np.nanstd(dfgrid[xcolumn] - dfgridr[refcolumn])
            #     Asigma[j][i] = np.nanstd(np.array(dfgrid[xcolumn].tolist()) - np.array(dfgridr[refcolumn].tolist()))
            #
            #     print('one', Asigma[j][i])



            # Asigma[j][i] = np.nanstd(dfgrid[xcolumn] - dfgridr[refcolumn])

    dimension = len(Ygrid)
    nol = len(Xgrid)

    print('function',dimension, nol)

    A1verr = [[-9999.0] * dimension for i in range(nol)]
    A1v = [[-9999.0] * dimension for i in range(nol)]
    R1verr = [[-9999.0] * dimension for i in range(nol)]
    R1v = [[-9999.0] * dimension for i in range(nol)]

    for k in range(nol):
        profO3X = Xgrid[k]
        profOPMX = OPMgrid[k]
        profO3Xerr = Asigma[k]
        for ik in range(dimension):
            A1v[k][ik] = (profO3X[ik] - profOPMX[ik])
            A1verr[k][ik] = (profO3Xerr[ik])
            R1v[k][ik] = 100 * (profO3X[ik] - profOPMX[ik]) / profOPMX[ik]
            R1verr[k][ik] = 100 * (profO3Xerr[ik] / profOPMX[ik])

    return  A1v, A1verr, R1v, R1verr, Ygrid
