 ## 0910 branch

#!/usr/bin/env python
# coding: utf-8
# Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from Josie_Functions import  Calc_average_profile_pressure, Calc_average_profile_time, Calc_Dif, Calc_average_profileCurrent_pressure, Calc_average_Dif
from Josie_PlotFunctions import  errorPlot_ARDif_withtext, errorPlot_general

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

def filter0910(dfm):

    filtEN = dfm.ENSCI == 1
    filtSP = dfm.ENSCI == 0

    filtS10 = dfm.Sol == 1
    filtS05 = dfm.Sol == 0.5

    filtB10 = dfm.Buf == 1.0
    filtB05 = dfm.Buf == 0.5

    filterEN0505 = (filtEN & filtS05 & filtB05)
    filterEN1010 = (filtEN & filtS10 & filtB10)

    profEN0505 = dfm.loc[filterEN0505]
    profEN1010 = dfm.loc[filterEN1010]

    profEN0505_nodup = profEN0505.drop_duplicates(['Sim', 'Team'])
    profEN1010_nodup = profEN1010.drop_duplicates(['Sim', 'Team'])

    totO3_EN0505 = profEN0505_nodup.frac.mean()
    totO3_EN1010 = profEN1010_nodup.frac.mean()

    filterSP1010 = (filtSP & filtS10 & filtB10)
    filterSP0505 = (filtSP & filtS05 & filtB05)

    profSP1010 = dfm.loc[filterSP1010]
    profSP0505 = dfm.loc[filterSP0505]

    profSP1010_nodup = profSP1010.drop_duplicates(['Sim', 'Team'])
    profSP0505_nodup = profSP0505.drop_duplicates(['Sim', 'Team'])

    totO3_SP1010 = profSP1010_nodup.frac.mean()
    totO3_SP0505 = profSP0505_nodup.frac.mean()

    prof = [profEN0505, profEN1010, profSP0505, profSP1010]

    o3list = [totO3_EN0505, totO3_EN1010, totO3_SP0505, totO3_SP1010]
    dfnplist = [profEN0505.drop_duplicates(['Sim', 'Team']), profEN1010.drop_duplicates(['Sim', 'Team']), profSP0505_nodup,profSP1010_nodup]

    return prof, o3list, dfnplist

###################################################


def filter2017(dfm):

     filtEN = dfm.ENSCI == 1
     filtSP = dfm.ENSCI == 0

     filtS10 = dfm.Sol == 1
     filtS05 = dfm.Sol == 0.5

     filtB10 = dfm.Buf == 1.0
     filtB05 = dfm.Buf == 0.5
     filtB01 = dfm.Buf == 0.1

     filterEN0505 = (filtEN & filtS05 & filtB05)
     filterEN1001 = (filtEN & filtS10 & filtB01)

     profEN0505 = dfm.loc[filterEN0505]
     profEN1001 = dfm.loc[filterEN1001]

     profEN0505_nodup = profEN0505.drop_duplicates(['Sim', 'Team'])
     profEN1001_nodup = profEN1001.drop_duplicates(['Sim', 'Team'])

     totO3_EN0505 = profEN0505_nodup.frac.mean()
     totO3_EN1001 = profEN1001_nodup.frac.mean()

     filterSP1010 = (filtSP & filtS10 & filtB10)
     filterSP1001 = (filtSP & filtS10 & filtB01)

     profSP1010 = dfm.loc[filterSP1010]
     profSP1001 = dfm.loc[filterSP1001]

     profSP1010_nodup = profSP1010.drop_duplicates(['Sim', 'Team'])
     profSP1001_nodup = profSP1001.drop_duplicates(['Sim', 'Team'])

     totO3_SP1010 = profSP1010_nodup.frac.mean()
     totO3_SP1001 = profSP1001_nodup.frac.mean()

     prof = [profEN0505, profEN1001, profSP1001, profSP1010]

     o3list = [totO3_EN0505, totO3_EN1001, totO3_SP1001, totO3_SP1010]
     dfnplist = [profEN0505.drop_duplicates(['Sim', 'Team']), profEN1001.drop_duplicates(['Sim', 'Team']),
                 profSP1001_nodup, profSP1010_nodup]

     return prof, o3list, dfnplist


 ###################################################


folderpath = 'Dif_2017_beta0error'

# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv_beta0.csv", low_memory=False)
# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv_beta0_fixedvalue.csv", low_memory=False)

df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv_beta0.csv", low_memory=False)
dfp = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv_beta0plus1sigma.csv", low_memory=False)
dfm = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv_beta0minus1sigma.csv", low_memory=False)

df = cuts2017(df)
dfp = cuts2017(dfp)
dfm = cuts2017(dfm)

prof17, o3list17, dfnplist17 = filter2017(df)
prof17p, o3list17p, dfnplist17p = filter2017(dfp)
prof17m, o3list17m, dfnplist17m = filter2017(dfm)


ytitle = 'Pressure (hPa)'
ytitlet = 'Time (sec.)'

# ### Plotting

axtitlecur = r'Sonde - OPM[JMA]  Difference ($\mu$A)'
rxtitlecur = 'Sonde - OPM[JMA]  Difference (%)'

### Plotting
axtitle_nojma = 'Sonde - OPM  Difference (mPa)'
axtitle = 'Sonde[JMA] - OPM  Difference (mPa)'

rxtitle_nojma = 'Sonde - OPM  Difference (%)'
rxtitle = 'Sonde[JMA] - OPM  Difference (%)'


labellist0910 = ['EN 0.5%-0.5B','EN 1.0%-1.0B', 'SP 0.5%-0.5B', 'SP 1.0%-1.0B']
labellist17 = ['EN 0.5%-0.5B','EN 1.0%-0.1B', 'SP 1.0%-0.1B', 'SP 1.0%-1.0B']

adif_PO3_deconvjma, adif_PO3_deconvjma_err, rdif_PO3_deconvjma, rdif_PO3_deconvjma_err, Yp = Calc_average_Dif(prof17, 'PO3_deconv_jma', 'PO3_OPM',  'pressure')
adif_PO3_deconvjmap, adif_PO3_deconvjmap_err, rdif_PO3_deconvjmap, rdif_PO3_deconvjmap_err, Yp = Calc_average_Dif(prof17p, 'PO3_deconv_jma', 'PO3_OPM',  'pressure')
adif_PO3_deconvjmam, adif_PO3_deconvjmam_err, rdif_PO3_deconvjmam, rdif_PO3_deconvjmam_err, Yp = Calc_average_Dif(prof17m, 'PO3_deconv_jma', 'PO3_OPM',  'pressure')

adif_IM_deconv82, adif_IM_deconv82_err, rdif_IM_deconv82, rdif_IM_deconv82_err, Yp = Calc_average_Dif(prof17, 'Ifast_minib0_deconv_sm8_gf2', 'I_OPM_jma',  'pressure')
adif_IM_deconv82p, adif_IM_deconv82p_err, rdif_IM_deconv82p, rdif_IM_deconv82p_err, Yp = Calc_average_Dif(prof17p, 'Ifast_minib0_deconv_sm8_gf2', 'I_OPM_jma',  'pressure')
adif_IM_deconv82m, adif_IM_deconv82m_err, rdif_IM_deconv82m, rdif_IM_deconv82m_err, Yp = Calc_average_Dif(prof17m, 'Ifast_minib0_deconv_sm8_gf2', 'I_OPM_jma',  'pressure')


# ## convoluted jma
errorPlot_ARDif_withtext(adif_PO3_deconvjma, adif_PO3_deconvjma_err, Yp, [-3, 3], [1000,5],'2017 Data Conv-Deconv (PO3 JMA corr.)',  axtitle, ytitle, labellist17, o3list17, dfnplist17,
                       'ADif_Pair_2017_PO3Deconv', folderpath ,  True, False)
errorPlot_ARDif_withtext(rdif_PO3_deconvjma, rdif_PO3_deconvjma_err, Yp, [-40, 40], [1000,5], '2017 Data Conv-Deconv (PO3 JMA corr.)',  rxtitle, ytitle, labellist17, o3list17, dfnplist17,
                       'RDif_Pair_2017_PO3Deconv', folderpath, True, False)

errorPlot_ARDif_withtext(rdif_PO3_deconvjmap, rdif_PO3_deconvjmap_err, Yp, [-40, 40], [1000,5], '2017 Data Conv-Deconv (PO3 JMA corr.)',  rxtitle, ytitle, labellist17, o3list17p, dfnplist17p,
                       'RDif_Pair_2017_PO3DeconvPlus', folderpath, True, False)


errorPlot_general([rdif_PO3_deconvjma[0], rdif_PO3_deconvjmap[0], rdif_PO3_deconvjmam[0]] , [rdif_PO3_deconvjma_err[0], rdif_PO3_deconvjmap_err[0], rdif_PO3_deconvjmam_err[0]] ,
                  Yp, [-40, 40], [1000,5], '2017 Data Conv-Deconv (PO3 JMA corr.)', rxtitle, ytitle,
                  [r'EN 0.5%-0.5B beta0', 'EN 0.5%-0.5B beta0+$1\sigma$', 'EN 0.5%-0.5B beta0-$1\sigma$' ], ['black','red', 'blue'], 'Betaerror_en0505', folderpath, True, False, True)


### current
errorPlot_general([rdif_IM_deconv82[0], rdif_IM_deconv82p[0], rdif_IM_deconv82m[0]] , [rdif_IM_deconv82_err[0], rdif_IM_deconv82p_err[0], rdif_IM_deconv82m_err[0]] ,
                  Yp, [-40, 40], [1000,5], 'EN 0.5%-0.5B 2017 Data Conv-Deconv (Current - iB0)'
                  , rxtitlecur, ytitle, [r'EN 0.5%-0.5B beta0', 'EN 0.5%-0.5B beta0+$1\sigma$', 'EN 0.5%-0.5B beta0-$1\sigma$' ], ['black','red', 'blue'],
                  'Current_Betaerror_EN0505', folderpath, True, False, True)

errorPlot_general([rdif_IM_deconv82[1], rdif_IM_deconv82p[1], rdif_IM_deconv82m[1]] , [rdif_IM_deconv82_err[1], rdif_IM_deconv82p_err[1], rdif_IM_deconv82m_err[1]] ,
                  Yp, [-40, 40], [1000,5], 'EN 1.0%-0.1B 2017 Data Conv-Deconv (Current - iB0)'
                  , rxtitlecur, ytitle, [r'EN 1.0%-0.1B beta0', 'EN 1.0%-0.1B beta0+$1\sigma$', 'EN 1.0%-0.1B beta0-$1\sigma$' ], ['black','red', 'blue'],
                  'Current_Betaerror_EN1001', folderpath, True, False, True)

errorPlot_general([rdif_IM_deconv82[2], rdif_IM_deconv82p[2], rdif_IM_deconv82m[2]] , [rdif_IM_deconv82_err[2], rdif_IM_deconv82p_err[2], rdif_IM_deconv82m_err[2]] ,
                  Yp, [-40, 40], [1000,5], 'SP 1.0%-0.1B 2017 Data Conv-Deconv (Current - iB0)'
                  , rxtitlecur, ytitle, [r'SP 1.0%-0.1B beta0', 'SP 1.0%-0.1B beta0+$1\sigma$', 'SP 1.0%-0.1B beta0-$1\sigma$' ], ['black','red', 'blue'],
                  'Current_Betaerror_SP1001', folderpath, True, False, True)

errorPlot_general([rdif_IM_deconv82[3], rdif_IM_deconv82p[3], rdif_IM_deconv82m[3]] , [rdif_IM_deconv82_err[3], rdif_IM_deconv82p_err[3], rdif_IM_deconv82m_err[3]] ,
                  Yp, [-40, 40], [1000,5], 'SP 1.0%-1.0B 2017 Data Conv-Deconv (Current - iB0)'
                  , rxtitlecur, ytitle, [r'SP 1.0%-1.0B beta0', 'SP 1.0%-1.0B beta0+$1\sigma$', 'SP 1.0%-1.0B beta0-$1\sigma$' ], ['black','red', 'blue'],
                  'Current_Betaerror_SP1010', folderpath, True, False, True)



## current


print('en 0505', rdif_PO3_deconvjma_err[0])
print('en 0505 plus', rdif_PO3_deconvjmap_err[0])
print('en 0505 minus', rdif_PO3_deconvjmam_err[0])

dimension = len(adif_PO3_deconvjma[0])
ones = [0] * dimension

errorPlot_general([ones, ones, ones] , [rdif_PO3_deconvjma_err[0], rdif_PO3_deconvjmap_err[0], rdif_PO3_deconvjmam_err[0]] ,
                  Yp, [-40, 40], [1000,5], '0910 Data Conv-Deconv (PO3 JMA corr.) Errors only'
                  , rxtitle, ytitle, [r'EN 0.5%-0.5B beta0', 'EN 0.5%-0.5B beta0+$1\sigma$', 'EN 0.5%-0.5B beta0-$1\sigma$' ],
                  ['black','red', 'blue'], 'Betaerroronly_en0505', folderpath, True, False, False)

#

# dimension = len(adif_PO3_deconvjma[0])
# len = len(adif_PO3_deconvjma)
#
# rdif_relative = [[0] * dimension for i in range(len)]
# rdif_relativep = [[0] * dimension for i in range(len)]
# mainp =  [[0] * dimension for i in range(len)]
# mainm =  [[0] * dimension for i in range(len)]
# plusp =  [[0] * dimension for i in range(len)]
# plusm =  [[0] * dimension for i in range(len)]
# minusp =  [[0] * dimension for i in range(len)]
# minusm =  [[0] * dimension for i in range(len)]
#
#
# for j in range(len):
#     rdif_relative[j] = [rdif_PO3_deconvjma[j][i]  /rdif_PO3_deconvjma_err[j][i] for i in range(dimension)]
#     rdif_relativep[j] = [rdif_PO3_deconvjmap[j][i]  /rdif_PO3_deconvjmap_err[j][i] for i in range(dimension)]
#     # mainp[j] = [rdif_PO3_deconvjma[j][i]  + rdif_PO3_deconvjma_err[j][i] for i in range(dimension)]
#     # mainm[j] = [rdif_PO3_deconvjma[j][i]  - rdif_PO3_deconvjma_err[j][i] for i in range(dimension)]
#     # plusp[j] = [rdif_PO3_deconvjmap[j][i]  + rdif_PO3_deconvjmap_err[j][i] for i in range(dimension)]
#     # plusm[j] = [rdif_PO3_deconvjmap[j][i]  - rdif_PO3_deconvjmap_err[j][i] for i in range(dimension)]
#     # minusp[j] = [rdif_PO3_deconvjmam[j][i]  + rdif_PO3_deconvjmam_err[j][i] for i in range(dimension)]
#     # minusm[j] = [rdif_PO3_deconvjmam[j][i]  - rdif_PO3_deconvjmam_err[j][i] for i in range(dimension)]
#
#     mainp[j] = [0 + rdif_PO3_deconvjma_err[j][i] for i in range(dimension)]
#     mainm[j] = [0 - rdif_PO3_deconvjma_err[j][i] for i in range(dimension)]
#     plusp[j] = [0 + rdif_PO3_deconvjmap_err[j][i] for i in range(dimension)]
#     plusm[j] = [0 - rdif_PO3_deconvjmap_err[j][i] for i in range(dimension)]
#     minusp[j] = [0 + rdif_PO3_deconvjmam_err[j][i] for i in range(dimension)]
#     minusm[j] = [0 - rdif_PO3_deconvjmam_err[j][i] for i in range(dimension)]
#
#
#
#
# print('error', rdif_PO3_deconvjma_err[0])
# print('rdif', rdif_PO3_deconvjma[0])
# print('reltive', rdif_relative[0])
# print('reltive plus', rdif_relativep[0])

# fig, ax = plt.subplots()
# plt.xlim([-40, 40])
# plt.ylim([1000,5])
# plt.title('Betaerroronly_en0505')
# plt.xlabel(rxtitle)
# plt.ylabel(ytitle)
# plt.grid(True)
# ax.set_yscale('log')
#
# ax.fill_betweenx(Yp, mainm[0], mainp[0], alpha=0.1, facecolor='k', edgecolor= 'black')
# ax.fill_betweenx(Yp, plusm[0], plusp[0], alpha=0.1, facecolor='red', edgecolor = 'red')
# ax.fill_betweenx(Yp, minusm[0], minusp[0], alpha=0.1, facecolor='blue', edgecolor = 'blue')
#
#
# ax.errorbar(ones, Yp, xerr=rdif_PO3_deconvjma_err[0], label='EN 0.5%-0.5B beta0', color='black', linewidth=1, elinewidth=0.5, capsize=1, capthick=0.5, linestyle='--')
# ax.errorbar(ones, Yp, xerr=rdif_PO3_deconvjmap_err[0], label=r'EN 0.5%-0.5B beta0$+1\sigma', color='red', linewidth=1, elinewidth=0.5, capsize=1, capthick=0.5, linestyle=':')
# ax.errorbar(ones, Yp, xerr=rdif_PO3_deconvjmam_err[0], label=r'EN 0.5%-0.5B beta0$-1\sigma', color='blue', linewidth=1, elinewidth=0.5, capsize=1, capthick=0.5, linestyle='-.')
# ax.legend(loc='lower right', frameon=True, fontsize='x-small')
#
# plt.show()
#
