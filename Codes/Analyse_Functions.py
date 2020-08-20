import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from numpy.polynomial import polynomial as P
import matplotlib.gridspec as gridspec

from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt

from Josie_Functions import Calc_average_profileCurrent_pressure, Calc_average_profile_time, Calc_average_profile_Pair, Calc_average_profile_pressure


def cuts2017(dfm):

    dfm = dfm.drop(dfm[(dfm.PO3 < 0)].index)
    dfm = dfm.drop(dfm[(dfm.PO3_OPM < 0)].index)

    dfm = dfm.drop(dfm[(dfm.Sim == 179) & (dfm.Team == 4)].index)
    dfm = dfm.drop(dfm[(dfm.Sim == 172) & (dfm.Team == 1)].index)
    dfm = dfm.drop(dfm[(dfm.Sim == 178) & (dfm.Team == 3)].index)
    dfm = dfm.drop(dfm[((dfm.Sim == 175))].index)

    dfm = dfm.drop(dfm[(dfm.Sim == 179) & (dfm.Team == 4) & (dfm.Tsim > 4000)].index)
    dfm = dfm.drop(dfm[(dfm.Sim == 172) & (dfm.Tsim < 500)].index)
    dfm = dfm.drop(dfm[(dfm.Sim == 172) & (dfm.Team == 1) & (dfm.Tsim > 5000) & (dfm.Tsim < 5800)].index)
    dfm = dfm.drop(dfm[(dfm.Sim == 178) & (dfm.Team == 3) & (dfm.Tsim > 1700) & (dfm.Tsim < 2100)].index)
    dfm = dfm.drop(dfm[(dfm.Sim == 178) & (dfm.Team == 3) & (dfm.Tsim > 2500) & (dfm.Tsim < 3000)].index)

    dfm = dfm.drop(dfm[((dfm.Sim == 186) & (dfm.Tsim > 5000))].index)
    dfm = dfm.drop(dfm[((dfm.Tsim > 7000))].index)

    return dfm

def cuts0910(dfm):

    dfm = dfm.drop(dfm[(dfm.PO3 < 0)].index)
    dfm = dfm.drop(dfm[(dfm.PO3_OPM < 0)].index)

    dfm = dfm[dfm.ADX == 0]
    # # v2 cuts, use this and v3 standard more conservative cuts not valid for 140, 1122, 163, 166  v2
    dfm=dfm[dfm.Tsim > 900]
    dfm=dfm[dfm.Tsim <= 8100]
    dfm = dfm.drop(dfm[(dfm.Sim == 141) & (dfm.Team == 3)].index)
    # dfm = dfm.drop(dfm[(dfm.Sim == 143) & (dfm.Team == 2) & (dfm.Tsim > 7950) & (dfm.Tsim < 8100)].index)
    dfm = dfm.drop(dfm[(dfm.Sim == 147) & (dfm.Team == 3)].index)
    dfm = dfm.drop(dfm[(dfm.Sim == 158) & (dfm.Team == 2)].index)
    dfm = dfm.drop(dfm[(dfm.Sim == 167) & (dfm.Team == 4)].index)
    # ## new cuts v2 20/05
    # dfm = dfm.drop(dfm[(dfm.Sim == 160) & (dfm.Team == 4)].index)
    # dfm = dfm.drop(dfm[(dfm.Sim == 165) & (dfm.Team == 4)].index)

    # # ## v3 cuts
    ### I think these cuts are not needed## checkcheck
    dfm = dfm.drop(dfm[(dfm.Sim == 159) & (dfm.Team == 1)].index)
    dfm = dfm.drop(dfm[(dfm.Sim == 158) & (dfm.Team == 1)].index)
    dfm = dfm.drop(dfm[(dfm.Sim == 163) & (dfm.Team == 4)].index)
    dfm = dfm.drop(dfm[(dfm.Sim == 159) & (dfm.Team == 4)].index)

    return dfm

def polyfit(dfp):

    dfp = cuts2017(dfp)

    dfp['TPintC'] = dfp['TPext'] - 273
    dfp['TPextC'] = dfp['TPint'] - 273
    # dfp['TPintK'] = dfp['TPext']
    # dfp['TPextK'] = dfp['TPint']

    dfp = dfp[dfp.Sim > 185]

    dfen = dfp[dfp.ENSCI == 1]
    dfsp = dfp[dfp.ENSCI == 0]

    avgprof_tpint_en, avgprof_tpint_en_err, Y = Calc_average_profile_pressure([dfen], 'TPintC')
    avgprof_tpext_en, avgprof_tpext_en_err, Y = Calc_average_profile_pressure([dfen], 'TPextC')

    avgprof_tpint_sp, avgprof_tpint_sp_err, Y = Calc_average_profile_pressure([dfsp], 'TPintC')
    avgprof_tpext_sp, avgprof_tpext_sp_err, Y = Calc_average_profile_pressure([dfsp], 'TPextC')

    adifall_en = [i - j for i, j in zip(avgprof_tpint_en[0], avgprof_tpext_en[0])]
    adifall_en_err = [np.sqrt(i * i + j * j) for i, j in zip(avgprof_tpint_en_err[0], avgprof_tpext_en_err[0])]

    adifall_sp = [i - j for i, j in zip(avgprof_tpint_sp[0], avgprof_tpext_sp[0])]
    adifall_sp_err = [np.sqrt(i * i + j * j) for i, j in zip(avgprof_tpint_sp_err[0], avgprof_tpext_sp_err[0])]

    p_en = np.poly1d(np.polyfit(Y, adifall_en, 15))
    p_sp = np.poly1d(np.polyfit(Y, adifall_sp, 15))

    # print('Y', Y)
    print('p_en', p_en)

    return p_en, p_sp