## 0910 branch

#!/usr/bin/env python
# coding: utf-8
# Libraries
import pandas as pd
import matplotlib.pyplot as plt

from Josie_Functions import  Calc_average_profile_Pair, Calc_RDif, Calc_ADif, Calc_average_profile
from Josie_PlotFunctions import  errorPlot_withtext


df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_Data_withcut.csv", low_memory=False)

df = df.drop(df[(df.PO3 < 0)].index)
df = df.drop(df[(df.PO3_OPM < 0)].index)

dfcleaned = df = df[df.ADX == 0]
# dfcleaned = df

resol = 200
# dimension for Rdif: ymax/resolution

ytitle = 'Pressure (hPa)'
ytitlet = 'Time (sec.)'

# attention for 17 and 0910



###############################################
# Filters for Sonde, Solution, Buff er selection
# 1, 0.1 ENSCI vs SPC
filtEN = dfcleaned.ENSCI == 1
filtSP = dfcleaned.ENSCI == 0

filtS10 = dfcleaned.Sol == 1
filtS05 = dfcleaned.Sol == 0.5

filtB10 = dfcleaned.Buf == 1.0
filtB05 = dfcleaned.Buf == 0.5

filterEN0505 = (filtEN & filtS05 & filtB05)
# & (dfcleaned.Sim == 184) & (dfcleaned.Team == 8))
filterEN1010 = (filtEN & filtS10 & filtB10)

profEN0505 = dfcleaned.loc[filterEN0505]
profEN1010 = dfcleaned.loc[filterEN1010]

profEN0505_nodup = profEN0505.drop_duplicates(['Sim', 'Team'])
profEN1010_nodup = profEN1010.drop_duplicates(['Sim', 'Team'])

print(profEN0505_nodup[['Sim','Team']])

totO3_EN0505 = profEN0505_nodup.frac.mean()
totO3_EN1010 = profEN1010_nodup.frac.mean()


filterSP1010 = (filtSP & filtS10 & filtB10)
filterSP0505 = (filtSP & filtS05 & filtB05)

profSP1010 = dfcleaned.loc[filterSP1010]
profSP0505 = dfcleaned.loc[filterSP0505]

profSP1010_nodup = profSP1010.drop_duplicates(['Sim', 'Team'])
profSP0505_nodup = profSP0505.drop_duplicates(['Sim', 'Team'])

totO3_SP1010 = profSP1010_nodup.frac.mean()
totO3_SP0505 = profSP0505_nodup.frac.mean()


avgprofEN0505_X, avgprofEN0505_Xerr, Y1 = Calc_average_profile_Pair(profEN0505, 'ADif_PO3S')
avgprofEN1010_X, avgprofEN1010_Xerr, Y1 = Calc_average_profile_Pair(profEN1010, 'ADif_PO3S')

avgprofSP1010_X, avgprofSP1010_Xerr, Y1 = Calc_average_profile_Pair(profSP1010, 'ADif_PO3S')
avgprofSP0505_X, avgprofSP0505_Xerr, Y1 = Calc_average_profile_Pair(profSP0505, 'ADif_PO3S')


avgprofEN0505_O3S_X, avgprofEN0505_O3S_Xerr, Y = Calc_average_profile_Pair(profEN0505, 'PO3')
avgprofEN1010_O3S_X, avgprofEN1010_O3S_Xerr, Y = Calc_average_profile_Pair(profEN1010, 'PO3')

print('po3')
avgprofSP1010_O3S_X, avgprofSP1010_O3S_Xerr, Y = Calc_average_profile_Pair(profSP1010, 'PO3')
avgprofSP0505_O3S_X, avgprofSP0505_O3S_Xerr, Y = Calc_average_profile_Pair(profSP0505, 'PO3')

avgprofEN0505_OPM_X, avgprofEN0505_OPM_Xerr, Y = Calc_average_profile_Pair(profEN0505, 'PO3_OPM')
avgprofEN1010_OPM_X, avgprofEN1010_OPM_Xerr, Y = Calc_average_profile_Pair(profEN1010, 'PO3_OPM')
print('opm')
avgprofSP1010_OPM_X, avgprofSP1010_OPM_Xerr, Y = Calc_average_profile_Pair(profSP1010, 'PO3_OPM')
avgprofSP0505_OPM_X, avgprofSP0505_OPM_Xerr, Y = Calc_average_profile_Pair(profSP0505, 'PO3_OPM')

dimension = len(Y)

# piece of code special for Relative difference calculation
rEN0505, rENerr0505 = Calc_RDif(avgprofEN0505_O3S_X, avgprofEN0505_OPM_X, avgprofEN0505_Xerr, dimension)
rEN1010, rENerr1010 = Calc_RDif(avgprofEN1010_O3S_X, avgprofEN1010_OPM_X, avgprofEN1010_Xerr, dimension)

aEN0505, aENerr0505 = Calc_ADif(avgprofEN0505_O3S_X, avgprofEN0505_OPM_X, avgprofEN0505_Xerr, dimension)


rSP1010, rSPerr1010 = Calc_RDif(avgprofSP1010_O3S_X, avgprofSP1010_OPM_X, avgprofSP1010_Xerr, dimension)
rSP0505, rSPerr0505 = Calc_RDif(avgprofSP0505_O3S_X, avgprofSP0505_OPM_X, avgprofSP0505_Xerr, dimension)


axlist = [avgprofEN0505_X, avgprofEN1010_X, avgprofSP1010_X, avgprofSP0505_X ]
ax_errorlist = [avgprofEN0505_Xerr, avgprofEN1010_Xerr, avgprofSP1010_Xerr, avgprofSP0505_Xerr ]

axtitle = 'Sonde - OPM  Difference (mPa)'
alabellist = ['EN 0.5%-0.5B','EN 1.0%-1.0B', 'SP 1.0%-1.0B', 'SP 0.5%-0.5B']
o3list = [totO3_EN0505, totO3_EN1010, totO3_SP1010, totO3_SP0505]
dfnplist = [profEN0505.drop_duplicates(['Sim', 'Team']), profEN1010.drop_duplicates(['Sim', 'Team']), profSP1010_nodup,
    profSP0505_nodup]



errorPlot_withtext(axlist, ax_errorlist, Y, [-3, 3], [1000,5],  '',  axtitle, ytitle, alabellist, o3list, dfnplist,
                           'TESTtest_ADif_Pair_CalibrationFunction_0910_withcut', True)

rxlist = [rEN0505, rEN1010, rSP1010, rSP0505]
rxerrlist = [rENerr0505, rENerr1010, rSPerr1010, rSPerr0505 ]
rxtitle = 'Sonde - OPM  Difference (%)'
errorPlot_withtext(rxlist, rxerrlist, Y, [-40, 40], [1000,5],  '',  rxtitle, ytitle, alabellist, o3list, dfnplist,
                           'TESTtest_RDif_Pair_CalibrationFunction_0910_withcut', True)





# # now the same asaf time
#
# avgprofEN0505_X_time, avgprofEN0505_Xerr_time, Y1_time = Calc_average_profile(profEN0505, 200, 'ADif_PO3S')
# avgprofEN1010_X_time, avgprofEN1010_Xerr_time, Y_time = Calc_average_profile(profEN1010, 200,'ADif_PO3S')
#
# avgprofSP1010_X_time, avgprofSP1010_Xerr_time, Y_time = Calc_average_profile(profSP1010, 200, 'ADif_PO3S')
# avgprofSP0505_X_time, avgprofSP0505_Xerr_time, Y_time = Calc_average_profile(profSP0505, 200, 'ADif_PO3S')
#
#
# avgprofEN0505_O3S_X_time, avgprofEN0505_O3S_Xerr_time, Y_time = Calc_average_profile(profEN0505,200, 'PO3')
# avgprofEN1010_O3S_X_time, avgprofEN1010_O3S_Xerr_time, Y_time = Calc_average_profile(profEN1010, 200, 'PO3')
#
# avgprofSP1010_O3S_X_time, avgprofSP1010_O3S_Xerr_time, Y_time = Calc_average_profile(profSP1010,200, 'PO3')
# avgprofSP0505_O3S_X_time, avgprofSP0505_O3S_Xerr_time, Y_time = Calc_average_profile(profSP0505, 200, 'PO3')
#
# avgprofEN0505_OPM_X_time, avgprofEN0505_OPM_Xerr_time, Y_time = Calc_average_profile(profEN0505, 200,'PO3_OPM')
# avgprofEN1010_OPM_X_time, avgprofEN1010_OPM_Xerr_time, Y_time = Calc_average_profile(profEN1010, 200,'PO3_OPM')
#
# avgprofSP1010_OPM_X_time, avgprofSP1010_OPM_Xerr_time, Y_time = Calc_average_profile(profSP1010,200, 'PO3_OPM')
# avgprofSP0505_OPM_X_time, avgprofSP0505_OPM_Xerr_time, Y_time = Calc_average_profile(profSP0505, 200,'PO3_OPM')
#
# dimension = len(Y_time)
#
# # piece of code special for Relative difference calculation
# rEN0505_time, rENerr0505_time = Calc_RDif(avgprofEN0505_O3S_X_time, avgprofEN0505_OPM_X_time, avgprofEN0505_Xerr_time, dimension)
# rEN1010_time, rENerr1010_time = Calc_RDif(avgprofEN1010_O3S_X_time, avgprofEN1010_OPM_X_time, avgprofEN1010_Xerr_time, dimension)
#
# rSP1010_time, rSPerr1010_time = Calc_RDif(avgprofSP1010_O3S_X_time, avgprofSP1010_OPM_X_time, avgprofSP1010_Xerr_time, dimension)
# rSP0505_time, rSPerr0505_time = Calc_RDif(avgprofSP0505_O3S_X_time, avgprofSP0505_OPM_X_time, avgprofSP0505_Xerr_time, dimension)
