## 2017 branch

#!/usr/bin/env python
# coding: utf-8
# Libraries
import pandas as pd
import matplotlib.pyplot as plt

from Josie_Functions import  Calc_average_profile_Pair, Calc_RDif, Calc_ADif, Calc_average_profile
from Josie_PlotFunctions import  errorPlot_ARDif_withtext, errorPlot_general

folderpath = 'Dif_2017'

# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv.csv", low_memory=False)
df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv.csv", low_memory=False)

df = df.drop(df[(df.PO3 < 0)].index)
df = df.drop(df[(df.PO3_OPM < 0)].index)


df = df.drop(df[((df.Sim == 171) | (df.Sim == 172) | (df.Sim == 180) | (df.Sim == 185))].index)
df = df.drop(df[(df.Sim == 179) & (df.Team == 4) & (df.Tsim > 4000)].index)
df = df.drop(df[(df.Sim == 172) & (df.Tsim < 500)].index)
df = df.drop(df[(df.Sim == 172) & (df.Team == 1) & (df.Tsim > 5000) & (df.Tsim < 5800)].index)
df = df.drop(df[(df.Sim == 178) & (df.Team == 3) & (df.Tsim > 1700) & (df.Tsim < 2100)].index)
df = df.drop(df[(df.Sim == 178) & (df.Team == 3) & (df.Tsim > 2500) & (df.Tsim < 3000)].index)

df = df.drop(df[((df.Sim == 175))].index)
df = df.drop(df[((df.Tsim > 7000))].index)

dfcleaned = df

resol = 200
# dimension for Rdif: ymax/resolution

ytitle = 'Pressure (hPa)'
ytitlet = 'Time (sec.)'

# attention for 17 and 2017



###############################################
# Filters for Sonde, Solution, Buff er selection
# 1, 0.1 ENSCI vs SPC
filtEN = dfcleaned.ENSCI == 1
filtSP = dfcleaned.ENSCI == 0

filtS10 = dfcleaned.Sol == 1
filtS05 = dfcleaned.Sol == 0.5

filtB10 = dfcleaned.Buf == 1.0
filtB05 = dfcleaned.Buf == 0.5
filtB01 = dfcleaned.Buf == 0.1


filterEN0505 = (filtEN & filtS05 & filtB05)
# & (dfcleaned.Sim == 184) & (dfcleaned.Team == 8))
filterEN1010 = (filtEN & filtS10 & filtB10)
filterEN1001 = (filtEN & filtS10 & filtB01)

profEN0505 = dfcleaned.loc[filterEN0505]
profEN1010 = dfcleaned.loc[filterEN1010]
profEN1001 = dfcleaned.loc[filterEN1001]

profEN0505_nodup = profEN0505.drop_duplicates(['Sim', 'Team'])
profEN1010_nodup = profEN1010.drop_duplicates(['Sim', 'Team'])
profEN1001_nodup = profEN1001.drop_duplicates(['Sim', 'Team'])

print(profEN0505_nodup[['Sim','Team']])

totO3_EN0505 = profEN0505_nodup.frac.mean()
totO3_EN1010 = profEN1010_nodup.frac.mean()
totO3_EN1001 = profEN1001_nodup.frac.mean()

filterSP1010 = (filtSP & filtS10 & filtB10)
filterSP0505 = (filtSP & filtS05 & filtB05)
filterSP1001 = (filtSP & filtS10 & filtB01)

profSP1010 = dfcleaned.loc[filterSP1010]
profSP0505 = dfcleaned.loc[filterSP0505]
profSP1001 = dfcleaned.loc[filterSP1001]

profSP1010_nodup = profSP1010.drop_duplicates(['Sim', 'Team'])
profSP0505_nodup = profSP0505.drop_duplicates(['Sim', 'Team'])
profSP1001_nodup = profSP1001.drop_duplicates(['Sim', 'Team'])

totO3_SP1010 = profSP1010_nodup.frac.mean()
totO3_SP0505 = profSP0505_nodup.frac.mean()
totO3_SP1001 = profSP1001_nodup.frac.mean()


avgprofEN0505_O3S_X, avgprofEN0505_O3S_Xerr, Y = Calc_average_profile_Pair(profEN0505, profEN0505.PO3)
avgprofEN1001_O3S_X, avgprofEN1001_O3S_Xerr, Y = Calc_average_profile_Pair(profEN1001, profEN0505.PO3)
avgprofSP1010_O3S_X, avgprofSP1010_O3S_Xerr, Y = Calc_average_profile_Pair(profSP1010, profEN0505.PO3)
avgprofSP1001_O3S_X, avgprofSP1001_O3S_Xerr, Y = Calc_average_profile_Pair(profSP1001, profEN0505.PO3)

PO3_deconvoluted = 'PO3_deconv_jma'

avgprofEN0505_O3S_X_dc, avgprofEN0505_O3S_Xerr_dc, Y = Calc_average_profile_Pair(profEN0505, profEN0505.PO3_deconv_jma)
avgprofEN1001_O3S_X_dc, avgprofEN1001_O3S_Xerr_dc, Y = Calc_average_profile_Pair(profEN1001, profEN1001.PO3_deconv_jma)
avgprofSP1010_O3S_X_dc, avgprofSP1010_O3S_Xerr_dc, Y = Calc_average_profile_Pair(profSP1010, profSP1010.PO3_deconv_jma)
avgprofSP1001_O3S_X_dc, avgprofSP1001_O3S_Xerr_dc, Y = Calc_average_profile_Pair(profSP1001, profSP1001.PO3_deconv_jma)

avgprofEN0505_O3S_X_dc_sm, avgprofEN0505_O3S_Xerr_dc_sm, Y = Calc_average_profile_Pair(profEN0505, profEN0505.PO3_deconv_sm6)
avgprofEN0505_O3S_X_dcjma, avgprofEN0505_O3S_Xerr_dcjma, Y = Calc_average_profile_Pair(profEN0505, profEN0505.PO3_deconv_jma)
avgprofEN0505_O3S_X_dcjma_sm6, avgprofEN0505_O3S_Xerr_dcjma_sm6, Y = Calc_average_profile_Pair(profEN0505, profEN0505.PO3_deconv_jma_sm6)


avgprofEN0505_OPM_X, avgprofEN0505_OPM_Xerr, Y = Calc_average_profile_Pair(profEN0505, profEN0505.PO3_OPM)
avgprofEN1001_OPM_X, avgprofEN1001_OPM_Xerr, Y = Calc_average_profile_Pair(profEN1001, profEN1001.PO3_OPM)
avgprofSP1010_OPM_X, avgprofSP1010_OPM_Xerr, Y = Calc_average_profile_Pair(profSP1010, profSP1010.PO3_OPM)
avgprofSP1001_OPM_X, avgprofSP1001_OPM_Xerr, Y = Calc_average_profile_Pair(profSP1001, profSP1001.PO3_OPM)

dimension = len(Y)

# Absolute difference calculation for standard PO3
aEN0505, aENerr0505 = Calc_ADif(avgprofEN0505_O3S_X, avgprofEN0505_OPM_X, avgprofEN0505_O3S_Xerr, dimension)
aEN1001, aENerr1001= Calc_ADif(avgprofEN1001_O3S_X, avgprofEN1001_OPM_X, avgprofEN1001_O3S_Xerr, dimension)
aSP1001, aSPerr1001 = Calc_ADif(avgprofSP1001_O3S_X, avgprofSP1001_OPM_X, avgprofSP1001_O3S_Xerr, dimension)
aSP1010, aSPerr1010 = Calc_ADif(avgprofSP1010_O3S_X, avgprofSP1010_OPM_X, avgprofSP1010_O3S_Xerr, dimension)
#  Relative difference calculation for standard PO3
rEN0505, rENerr0505 = Calc_RDif(avgprofEN0505_O3S_X, avgprofEN0505_OPM_X, avgprofEN0505_O3S_Xerr, dimension)
rEN1001, rENerr1001= Calc_RDif(avgprofEN1001_O3S_X, avgprofEN1001_OPM_X, avgprofEN1001_O3S_Xerr, dimension)
rSP1001, rSPerr1001 = Calc_RDif(avgprofSP1001_O3S_X, avgprofSP1001_OPM_X, avgprofSP1001_O3S_Xerr, dimension)
rSP1010, rSPerr1010 = Calc_RDif(avgprofSP1010_O3S_X, avgprofSP1010_OPM_X, avgprofSP1010_O3S_Xerr, dimension)

# Absolute difference calculation for deconvoluted PO3
aEN0505_dc, aENerr0505_dc = Calc_ADif(avgprofEN0505_O3S_X_dc, avgprofEN0505_OPM_X, avgprofEN0505_O3S_Xerr_dc, dimension)
aEN1001_dc, aENerr1001_dc = Calc_ADif(avgprofEN1001_O3S_X_dc, avgprofEN1001_OPM_X, avgprofEN1001_O3S_Xerr_dc, dimension)
aSP1001_dc, aSPerr1001_dc = Calc_ADif(avgprofSP1001_O3S_X_dc, avgprofSP1001_OPM_X, avgprofSP1001_O3S_Xerr_dc, dimension)
aSP1010_dc, aSPerr1010_dc = Calc_ADif(avgprofSP1010_O3S_X_dc, avgprofSP1010_OPM_X, avgprofSP1010_O3S_Xerr_dc, dimension)
#  Relative difference calculation for deconvoluted PO3
rEN0505_dc, rENerr0505_dc = Calc_RDif(avgprofEN0505_O3S_X_dc, avgprofEN0505_OPM_X, avgprofEN0505_O3S_Xerr_dc, dimension)
rEN1001_dc, rENerr1001_dc = Calc_RDif(avgprofEN1001_O3S_X_dc, avgprofEN1001_OPM_X, avgprofEN1001_O3S_Xerr_dc, dimension)
rSP1001_dc, rSPerr1001_dc = Calc_RDif(avgprofSP1001_O3S_X_dc, avgprofSP1001_OPM_X, avgprofSP1001_O3S_Xerr_dc, dimension)
rSP1010_dc, rSPerr1010_dc = Calc_RDif(avgprofSP1010_O3S_X_dc, avgprofSP1010_OPM_X, avgprofSP1010_O3S_Xerr_dc, dimension)

## a check for en0505
aEN0505_dc, aENerr0505_dc = Calc_ADif(avgprofEN0505_O3S_X_dc, avgprofEN0505_OPM_X, avgprofEN0505_O3S_Xerr_dc, dimension)
aEN0505_dc_sm, aENerr0505_dc_sm = Calc_ADif(avgprofEN0505_O3S_X_dc_sm, avgprofEN0505_OPM_X, avgprofEN0505_O3S_Xerr_dc_sm, dimension)
aEN0505_dcjma, aENerr0505_dcjma = Calc_ADif(avgprofEN0505_O3S_X_dcjma, avgprofEN0505_OPM_X, avgprofEN0505_O3S_Xerr_dcjma, dimension)
aEN0505_dcjma_sm6, aENerr0505_dcjma_sm6 = Calc_ADif(avgprofEN0505_O3S_X_dcjma_sm6, avgprofEN0505_OPM_X, avgprofEN0505_O3S_Xerr_dcjma_sm6, dimension)

rEN0505_dc, rENerr0505_dc = Calc_RDif(avgprofEN0505_O3S_X_dc, avgprofEN0505_OPM_X, avgprofEN0505_O3S_Xerr_dc, dimension)
rEN0505_dc_sm, rENerr0505_dc_sm = Calc_RDif(avgprofEN0505_O3S_X_dc_sm, avgprofEN0505_OPM_X, avgprofEN0505_O3S_Xerr_dc_sm, dimension)
rEN0505_dcjma, rENerr0505_dcjma = Calc_RDif(avgprofEN0505_O3S_X_dcjma, avgprofEN0505_OPM_X, avgprofEN0505_O3S_Xerr_dcjma, dimension)
rEN0505_dcjma_sm6, rENerr0505_dcjma_sm6 = Calc_RDif(avgprofEN0505_O3S_X_dcjma_sm6, avgprofEN0505_OPM_X, avgprofEN0505_O3S_Xerr_dcjma_sm6, dimension)


### standard plotting 4 sonde types ###
axlist = [aEN0505, aEN1001, aSP1010, aSP1001 ]
ax_errorlist = [aENerr0505, aENerr1001,  aSPerr1010, aSPerr1001 ]

axtitle = 'Sonde - OPM  Difference (mPa)'
alabellist = ['EN 0.5%-0.5B','EN 1.0%-0.1B', 'SP 1.0%-1.0B', 'SP 1.0%-0.1B']
o3list = [totO3_EN0505, totO3_EN1001, totO3_SP1010, totO3_SP1001]
dfnplist = [profEN0505.drop_duplicates(['Sim', 'Team']), profEN1001.drop_duplicates(['Sim', 'Team']), profSP1010_nodup,
    profSP1001_nodup]

rxlist = [rEN0505, rEN1001, rSP1010, rSP1001]
rxerrlist = [rENerr0505, rENerr1001, rSPerr1010, rSPerr1001 ]
rxtitle = 'Sonde - OPM  Difference (%)'

## now deconvoluted ones
axlist_dc = [aEN0505_dc, aEN1001_dc,  aSP1010_dc, aSP1001_dc ]
ax_errorlist_dc = [aENerr0505_dc, aENerr1001_dc,  aSPerr1010_dc, aSPerr1001_dc ]

rxlist_dc = [rEN0505_dc, rEN1001_dc, rSP1010_dc, rSP1001_dc]
rxerrlist_dc = [rENerr0505_dc, rENerr1001_dc, rSPerr1010_dc, rSPerr1001_dc ]


errorPlot_ARDif_withtext(axlist, ax_errorlist, Y, [-3, 3], [1000,5],  '2017 Data',  axtitle, ytitle, alabellist, o3list, dfnplist,
                           'Standard_ADif_Pair_CalibrationFunction_2017_withcut', folderpath ,  True, False)

errorPlot_ARDif_withtext(rxlist, rxerrlist, Y, [-40, 40], [1000,5],  '2017 Data',  rxtitle, ytitle, alabellist, o3list, dfnplist,
                           'Standard_RDif_Pair_CalibrationFunction_2017_withcut', folderpath, True, False)

###

errorPlot_ARDif_withtext(axlist_dc, ax_errorlist_dc, Y, [-3, 3], [1000,5],  '2017 Data Conv-Deconv (PO3 JMA corr.)',  axtitle, ytitle, alabellist, o3list, dfnplist,
                           'Convoluted_ADif_Pair_CalibrationFunction_2017_withcut_JMAcorrection', folderpath ,  True, False)

errorPlot_ARDif_withtext(rxlist_dc, rxerrlist_dc, Y, [-40, 40], [1000,5],  '2017 Data Conv-Deconv (PO3 JMA corr.)',  rxtitle, ytitle, alabellist, o3list, dfnplist,
                           'Convoluted_RDif_Pair_CalibrationFunction_2017_withcut_JMAcorrection', folderpath, True, False)

###  now make  a plot where you draw standard and dc ones in the same plot

plt.close('all')
fig, ax = plt.subplots()
plt.xlim([-20,20])
plt.ylim([1000, 5])
plt.title('2017 Data')
plt.xlabel(rxtitle)
plt.ylabel(ytitle)
plt.grid(True)

# plt.yticks(np.arange(0, 7001, 1000))

# reference line
ax.axvline(x=0, color='grey', linestyle='--')
ax.set_yscale('log')
colorl = ['black', 'red', 'blue', 'green']

labell = [' '] * 4
labell_dc = [' '] * 4

for i in range(4):
    n = len(dfnplist[i])
    labell[i] = alabellist[i] + ' ( n =' + str(n) + ')'

    ax.errorbar(rxlist[i], Y, xerr=rxerrlist[i], label=labell[i], color=colorl[i], linewidth=1, elinewidth=0.5,
                capsize=1, capthick=0.5)
    ax.errorbar(rxlist_dc[i], Y, xerr=rxerrlist_dc[i], color=colorl[i], linewidth=1, elinewidth=0.5,
                capsize=1, capthick=0.5, linestyle="--")

ax.legend(loc='lower right', frameon=True, fontsize='small')

plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/' + folderpath + '/' + 'Comparison' + '.png')
plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/' + folderpath + '/' + 'Comparison' + '.eps')

plt.close()

## check plot only for en0505 to see effcet of jms, sm etc
# new_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

# blue, orange, green, red, purple, brown, pinkish, greyish, yellowish, bluish
colorlist = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

achecklist = [aEN0505, aEN0505_dc, aEN0505_dc_sm, aEN0505_dcjma, aEN0505_dcjma_sm6]
achecklist_err = [aENerr0505, aENerr0505_dc, aENerr0505_dc_sm, aENerr0505_dcjma, aENerr0505_dcjma_sm6]

rchecklist = [rEN0505, rEN0505_dc, rEN0505_dc_sm, rEN0505_dcjma, rEN0505_dcjma_sm6]
rchecklist_err = [rENerr0505, rENerr0505_dc,rENerr0505_dc_sm,  rENerr0505_dcjma, rENerr0505_dcjma_sm6]

checklabel = ['PO3', 'PO3 deconv', 'PO3 deconv smoothed ', 'PO3 deconv jma', 'PO3 deconv jma smoothed']

# errorPlot_general(achecklist, achecklist_err, Y, [-3,3], [1000,5], '2017 data- ENSCI 0.5%-0.%B', axtitle, ytitle,
#                   checklabel, colorlist, 'ADif_Check_en0505_withcut', folderpath, 1)
#
# errorPlot_general(rchecklist, rchecklist_err, Y, [-40,40], [1000,5], '2017 data ENSCI 0.5%-0.%B', rxtitle, ytitle,
#                   checklabel, colorlist, 'RDif_Check_en0505_withcut', folderpath, 1)

