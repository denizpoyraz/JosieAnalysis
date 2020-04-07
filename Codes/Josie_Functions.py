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
def Calc_average_profile_pressure(dataframelist, xcolumn ):

    nd = len(dataframelist)

    yref = [1000, 850, 700, 550, 400, 350, 300, 200, 150, 100, 75, 50, 35, 25, 20, 15,
            12, 10, 8, 6]

    n = len(yref) - 1
    Ygrid = [-9999.0] * n

    Xgrid = [[-9999.0] * n for i in range(nd)]
    Xsigma = [[-9999.0] * n for i in range(nd)]

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

    return Xgrid, Xsigma, Ygrid

def Calc_average_profile_time(dataframelist, xcolumn, ybin, tmin, tmax ):

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
            # print(i, 'len of dftmp1 ', len(dftmp1))

            filtnull = dftmp1.X > -9999.0
            dfgrid['X'] = dftmp1[filtnull].X

            Xgrid[j][i] = np.nanmean(dfgrid.X)
            Xsigma[j][i] = np.nanstd(dfgrid.X)

    return Xgrid, Xsigma, Ygrid

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

    return A1v, A1verr, R1v, R1verr

def Calc_ADif(profO3X, profOPMX, profO3Xerr, dimension):
    A1verr = [-9999.9] * dimension
    A1v = [-9999.9] * dimension

    for i in range(dimension):
        A1v[i] = (profO3X[i] - profOPMX[i])
        A1verr[i] = (profO3Xerr[i])

    # print(A1v)
    return A1v, A1verr

def Calc_RDif(profO3X, profOPMX, profO3Xerr, dimension):
    R1v = [-9999.9] * dimension
    R1verr = [-9999.9] * dimension
    A1v = [-9999.9] * dimension

    for i in range(dimension):
        A1v[i] = (profO3X[i] - profOPMX[i])
        R1v[i] = 100 * (profO3X[i] - profOPMX[i]) / profOPMX[i]
        # R1v[i] = 100 * (profO3X[i] - profOPMX[i]) / profO3X[i]

        R1verr[i] = 100 * (profO3Xerr[i] / profOPMX[i])

    # print(A1v)
    return R1v, R1verr

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


def Calc_average_profile_Pair(dataframe, xcolumn):

    dft = dataframe
    dft.PFcor = dft[xcolumn]

    #
    # yref = [1000, 950, 900, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400, 350, 325, 300, 275, 250, 225, 200, 175,
    #         150, 135, 120, 105, 90, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40, 35, 30, 28, 26, 24, 22, 20, 18, 16, 14,
    #         12, 10, 8, 6]


    yref = [1000, 850, 700,  550, 400, 350, 300, 200, 150, 100, 75,  50, 35, 25, 20, 15,
            12, 10, 8, 6]

    n = len(yref) - 1
    Xgrid = [-9999.0] * n
    Xsigma = [-9999.0] * n
    Ygrid = [-9999.0] * n

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
        # filtfin = np.isnan(dftmp1.X)
        # filtfin = not(filtfin)
        # filterall = filtnull & filtfin
        filterall = filtnull
        dfgrid['X'] = dftmp1[filterall].X
        tmp = np.array(dfgrid.X.tolist())
        # dfgrid = dfgrid.dropna()  ## problems with nan
        Xgrid[i] = np.nanmean(dfgrid.X)
        Xsigma[i] = np.nanstd(dfgrid.X)

    # print('Xgrid', Xgrid)
    return Xgrid, Xsigma, Ygrid