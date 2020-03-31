## 0910 branch

## updated version of Rdif plots. Now I take the difference of sonde - opm and take the average of the differences afterwards


#!/usr/bin/env python
# coding: utf-8
# Libraries
import pandas as pd
import matplotlib.pyplot as plt

from Josie_Functions import  Calc_average_profile_Pair, Calc_RDif, Calc_average_profile,  Calc_ADif
from Josie_PlotFunctions import  Plot_compare_4profile_plots_pair, Plot_compare_4profile_plots_time

# df = pd.read_csv("/home/poyraden/Josie17/Files/Josie1718_Data.csv")
df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_Data_v2_pair.csv", low_memory=False)

df = df.drop(df[(df.PO3 < 0)].index)
df = df.drop(df[(df.PO3_OPM < 0)].index)

df = df.drop(df[df.Pair > 999].index)
df = df.drop(df[df.PO3_OPM > 999].index)


resol = 200
# dimension for Rdif: ymax/resolution

ytitle = 'Pressure (hPa)'
ytitlet = 'Time (sec.)'

# attention for 17 and 0910
# dfcleaned = df = df[df.ADX == 0]
# dfcleaned = df
dfcleaned = df = df[df.ADX == 0]




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
filterEN1010 = (filtEN & filtS10 & filtB10)

profEN0505 = dfcleaned.loc[filterEN0505]
profEN1010 = dfcleaned.loc[filterEN1010]

profEN0505_nodup = profEN0505.drop_duplicates(['Sim', 'Team'])
profEN1010_nodup = profEN1010.drop_duplicates(['Sim', 'Team'])

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


## take the difference of PO3 and OPM
# yref = [1000, 950, 900, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400, 350, 325, 300, 275, 250, 225, 200, 175,
#         150, 135, 120, 105, 90, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40, 35, 30, 28, 26, 24, 22, 20, 18, 16, 14,
#         12, 10, 8, 6]


profEN0505['adif'] = profEN0505['PO3'] - profEN0505['PO3_OPM']
profEN0505['rdif'] = 100 * (profEN0505['PO3'] - profEN0505['PO3_OPM']) / profEN0505['PO3_OPM']

profSP1010['adif'] = profSP1010['PO3'] - profSP1010['PO3_OPM']
profSP1010['rdif'] = 100 * (profSP1010['PO3'] - profSP1010['PO3_OPM']) / profSP1010['PO3_OPM']


adifEN0505_X, adifEN0505_Xerr, Y1 = Calc_average_profile_Pair(profEN0505, 'adif')
#
adifSP1010_X, adifSP1010_Xerr, Y1 = Calc_average_profile_Pair(profSP1010, 'adif')

rdifEN0505_X, rdifEN0505_Xerr, Y1 = Calc_average_profile_Pair(profEN0505, 'rdif')
#
rdifSP1010_X, rdifSP1010_Xerr, Y1 = Calc_average_profile_Pair(profSP1010, 'rdif')

print(adifEN0505_X)

avgprofEN0505_X, avgprofEN0505_Xerr, Y1 = Calc_average_profile_Pair(profEN0505, 'ADif_PO3S')
avgprofEN1010_X, avgprofEN1010_Xerr, Y1 = Calc_average_profile_Pair(profEN1010, 'ADif_PO3S')

avgprofSP1010_X, avgprofSP1010_Xerr, Y1 = Calc_average_profile_Pair(profSP1010, 'ADif_PO3S')
avgprofSP0505_X, avgprofSP0505_Xerr, Y1 = Calc_average_profile_Pair(profSP0505, 'ADif_PO3S')


avgprofEN0505_O3S_X, avgprofEN0505_O3S_Xerr, Y = Calc_average_profile_Pair(profEN0505, 'PO3')
avgprofEN1010_O3S_X, avgprofEN1010_O3S_Xerr, Y = Calc_average_profile_Pair(profEN1010, 'PO3')

avgprofSP1010_O3S_X, avgprofSP1010_O3S_Xerr, Y = Calc_average_profile_Pair(profSP1010, 'PO3')
avgprofSP0505_O3S_X, avgprofSP0505_O3S_Xerr, Y = Calc_average_profile_Pair(profSP0505, 'PO3')

avgprofEN0505_OPM_X, avgprofEN0505_OPM_Xerr, Y = Calc_average_profile_Pair(profEN0505, 'PO3_OPM')
avgprofEN1010_OPM_X, avgprofEN1010_OPM_Xerr, Y = Calc_average_profile_Pair(profEN1010, 'PO3_OPM')

avgprofSP1010_OPM_X, avgprofSP1010_OPM_Xerr, Y = Calc_average_profile_Pair(profSP1010, 'PO3_OPM')
avgprofSP0505_OPM_X, avgprofSP0505_OPM_Xerr, Y = Calc_average_profile_Pair(profSP0505, 'PO3_OPM')

dimension = len(Y)

print(adifEN0505_X)
print(avgprofEN0505_X)



# piece of code special for Relative difference calculation
rEN0505, rENerr0505 = Calc_RDif(avgprofEN0505_O3S_X, avgprofEN0505_OPM_X, avgprofEN0505_Xerr, dimension)
rEN1010, rENerr1010 = Calc_RDif(avgprofEN1010_O3S_X, avgprofEN1010_OPM_X, avgprofEN1010_Xerr, dimension)

rSP1010, rSPerr1010 = Calc_RDif(avgprofSP1010_O3S_X, avgprofSP1010_OPM_X, avgprofSP1010_Xerr, dimension)
rSP0505, rSPerr0505 = Calc_RDif(avgprofSP0505_O3S_X, avgprofSP0505_OPM_X, avgprofSP0505_Xerr, dimension)

aEN0505, aENerr0505 = Calc_ADif(avgprofEN0505_O3S_X, avgprofEN0505_OPM_X, avgprofEN0505_Xerr, dimension)

print(rdifEN0505_X)
print(rEN0505)

print('adif')
print(adifEN0505_X)
print(avgprofEN0505_X)
print(aEN0505)

#
Plot_compare_4profile_plots_pair(
    avgprofEN0505_X, avgprofEN0505_Xerr, adifEN0505_X, adifEN0505_Xerr, avgprofSP1010_X, avgprofSP1010_Xerr,
    adifSP1010_X, adifSP1010_Xerr, Y, [-3, 3], ' ', 'Sonde - OPM  Difference (mPa)', ytitle, 'EN 0.5%-0.5B',
    'EN 0.5%-0.5B new', 'SP 1.0%-1.0B', 'SP 1.0%-1.0B new', totO3_EN0505, totO3_EN0505, totO3_SP1010, totO3_SP1010,
    profEN0505.drop_duplicates(['Sim', 'Team']), profEN0505.drop_duplicates(['Sim', 'Team']), profSP1010_nodup,
    profSP1010_nodup, 'ADif_0910v2_difmethods')

Plot_compare_4profile_plots_pair(
    rEN0505, rENerr0505, rdifEN0505_X, rdifEN0505_Xerr, rSP1010, rSPerr1010, rdifSP1010_X, rdifSP1010_Xerr, Y, [-40, 40], ' ',
    'Sonde - OPM  Difference (%)',
    ytitle, 'EN 0.5%-0.5B', 'EN 0.5%-0.5B new', 'SP 1.0%-1.0B', 'SP 1.0%-1.0B new', totO3_EN0505, totO3_EN0505, totO3_SP1010,
    totO3_SP1010,
    profEN0505.drop_duplicates(['Sim', 'Team']), profEN0505.drop_duplicates(['Sim', 'Team']), profSP1010_nodup,
    profSP1010_nodup, 'RDif_0910v2_difmethods')
#
#
#
# now the same asaf time

avgprofEN0505_X_time, avgprofEN0505_Xerr_time, Y1_time = Calc_average_profile(profEN0505, 200, 'ADif_PO3S')
# avgprofEN1010_X_time, avgprofEN1010_Xerr_time, Y_time = Calc_average_profile(profEN1010, 200,'ADif_PO3S')

avgprofSP1010_X_time, avgprofSP1010_Xerr_time, Y_time = Calc_average_profile(profSP1010, 200, 'ADif_PO3S')
# avgprofSP0505_X_time, avgprofSP0505_Xerr_time, Y_time = Calc_average_profile(profSP0505, 200, 'ADif_PO3S')


avgprofEN0505_O3S_X_time, avgprofEN0505_O3S_Xerr_time, Y_time = Calc_average_profile(profEN0505,200, 'PO3')
# avgprofEN1010_O3S_X_time, avgprofEN1010_O3S_Xerr_time, Y_time = Calc_average_profile(profEN1010, 200, 'PO3')

avgprofSP1010_O3S_X_time, avgprofSP1010_O3S_Xerr_time, Y_time = Calc_average_profile(profSP1010,200, 'PO3')
# avgprofSP0505_O3S_X_time, avgprofSP0505_O3S_Xerr_time, Y_time = Calc_average_profile(profSP0505, 200, 'PO3')

avgprofEN0505_OPM_X_time, avgprofEN0505_OPM_Xerr_time, Y_time = Calc_average_profile(profEN0505, 200,'PO3_OPM')
# avgprofEN1010_OPM_X_time, avgprofEN1010_OPM_Xerr_time, Y_time = Calc_average_profile(profEN1010, 200,'PO3_OPM')

avgprofSP1010_OPM_X_time, avgprofSP1010_OPM_Xerr_time, Y_time = Calc_average_profile(profSP1010,200, 'PO3_OPM')
# avgprofSP0505_OPM_X_time, avgprofSP0505_OPM_Xerr_time, Y_time = Calc_average_profile(profSP0505, 200,'PO3_OPM')

dimension = len(Y_time)

# piece of code special for Relative difference calculation
rEN0505_time, rENerr0505_time = Calc_RDif(avgprofEN0505_O3S_X_time, avgprofEN0505_OPM_X_time, avgprofEN0505_Xerr_time, dimension)
# rEN1010_time, rENerr1010_time = Calc_RDif(avgprofEN1010_O3S_X_time, avgprofEN1010_OPM_X_time, avgprofEN1010_Xerr_time, dimension)

rSP1010_time, rSPerr1010_time = Calc_RDif(avgprofSP1010_O3S_X_time, avgprofSP1010_OPM_X_time, avgprofSP1010_Xerr_time, dimension)
# rSP0505_time, rSPerr0505_time = Calc_RDif(avgprofSP0505_O3S_X_time, avgprofSP0505_OPM_X_time, avgprofSP0505_Xerr_time, dimension)


adifEN0505_X_time, adifEN0505_Xerr_time, Y_time = Calc_average_profile(profEN0505, 200, 'adif')
#
adifSP1010_X_time, adifSP1010_Xerr_time, Y_time = Calc_average_profile(profSP1010, 200, 'adif')

rdifEN0505_X_time, rdifEN0505_Xerr_time, Y_time = Calc_average_profile(profEN0505, 200, 'rdif')
#
rdifSP1010_X_time, rdifSP1010_Xerr_time, Y_time = Calc_average_profile(profSP1010, 200, 'rdif')


Plot_compare_4profile_plots_time(
    avgprofEN0505_X_time, avgprofEN0505_Xerr_time, adifEN0505_X_time, adifEN0505_Xerr_time, avgprofSP1010_X_time,
    avgprofSP1010_Xerr_time, adifSP1010_X_time, adifSP1010_Xerr_time, Y_time, [-3, 3], ' ',
    'Sonde - OPM  Difference (mPa)', ytitlet, 'EN 0.5%-0.5B',
   'EN 0.5%-0.5B new', 'SP 1.0%-1.0B', 'SP 1.0%-1.0B new', totO3_EN0505, totO3_EN1010, totO3_SP1010, totO3_SP0505,
    profEN0505.drop_duplicates(['Sim', 'Team']), profEN0505.drop_duplicates(['Sim', 'Team']), profSP1010_nodup,
    profSP1010_nodup, 'ADif_Time_0910v2_difmethods')

Plot_compare_4profile_plots_time(
    rEN0505_time, rENerr0505_time, rdifEN0505_X_time, rdifEN0505_Xerr_time, rSP1010_time, rSPerr1010_time, rdifSP1010_X_time,
    rdifSP1010_Xerr_time, Y_time, [-40, 40], ' ', 'Sonde - OPM  Difference (%)',
    ytitlet,  'EN 0.5%-0.5B',
   'EN 0.5%-0.5B new', 'SP 1.0%-1.0B', 'SP 1.0%-1.0B new', totO3_EN0505, totO3_EN1010, totO3_SP1010,
    totO3_SP0505,
    profEN0505.drop_duplicates(['Sim', 'Team']), profEN0505.drop_duplicates(['Sim', 'Team']), profSP1010_nodup,
    profSP1010_nodup, 'RDif_Time_0910v2_difmethods')