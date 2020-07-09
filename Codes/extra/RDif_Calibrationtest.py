## 0910 branch

#!/usr/bin/env python
# coding: utf-8
# Libraries
import pandas as pd
import matplotlib.pyplot as plt

from Josie_Functions import  Calc_average_profile_Pair, Calc_RDif, Calc_ADif, Calc_average_profile_pressure,Calc_average_profile_time, Calc_Dif
from Josie_PlotFunctions import  errorPlot_ARDif_withtext, errorPlot_general

folderpath = 'Dif_0910'

df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_deconv.csv", low_memory=False)
# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv.csv", low_memory=False)

df = df.drop(df[(df.PO3 < 0)].index)
df = df.drop(df[(df.PO3_OPM < 0)].index)

# dfcleaned = df = df[df.ADX == 0]

## cuts for Josie0910 data
# # v2 cuts, use this and v3 standard more conservative cuts not valid for 140, 162, 163, 166  v2
df=df[df.Tsim > 900]
df=df[df.Tsim <= 8100]
df = df.drop(df[(2000 < df.Tsim) & (df.Tsim < 2500) & (df.Sim != 140) & (df.Sim != 162) & (df.Sim != 163) & (
                df.Sim != 166)].index)
df = df.drop(df[(df.Tsim > 4000) & (df.Tsim < 4500) & (df.Sim != 140) & (df.Sim != 162) & (df.Sim != 163) & (
                df.Sim != 166)].index)
df = df.drop(df[(df.Tsim > 6000) & (df.Tsim < 6500) & (df.Sim != 140) & (df.Sim != 162) & (df.Sim != 163) & (
                df.Sim != 166)].index)

df = df.drop(df[(df.Sim == 141) & (df.Team == 3)].index)
df = df.drop(df[(df.Sim == 143) & (df.Team == 2) & (df.Tsim > 7950) & (df.Tsim < 8100)].index)
df = df.drop(df[(df.Sim == 147) & (df.Team == 3)].index)
df = df.drop(df[(df.Sim == 158) & (df.Team == 2)].index)
df = df.drop(df[(df.Sim == 167) & (df.Team == 4)].index)

df = df.drop(df[(df.Sim == 158) & (df.Tsim > 7300) & (df.Tsim < 7700)].index)
df = df.drop(df[(df.Sim == 159) & (df.Tsim > 7800) & (df.Tsim < 8000)].index)
df = df.drop(df[(df.Sim == 161) & (df.Tsim > 6800) & (df.Tsim < 7200)].index)

    # # additional cuts for specific simulations  v3
df = df.drop(df[(df.Sim == 140) & (df.Tsim < 1000)].index)
df = df.drop(df[(df.Sim == 140) & (df.Tsim > 2450) & (df.Tsim < 2800)].index)
df = df.drop(df[(df.Sim == 140) & (df.Tsim > 4400) & (df.Tsim < 4800)].index)
df = df.drop(df[(df.Sim == 140) & (df.Tsim > 6400) & (df.Tsim < 6800)].index)

df = df.drop(df[(df.Sim == 162) & (df.Tsim > 2100) & (df.Tsim < 2550)].index)
df = df.drop(df[(df.Sim == 162) & (df.Tsim > 4100) & (df.Tsim < 4600)].index)
df = df.drop(df[(df.Sim == 162) & (df.Tsim > 5450) & (df.Tsim < 5800)].index)
df = df.drop(df[(df.Sim == 162) & (df.Tsim > 6100) & (df.Tsim < 6550)].index)

df = df.drop(df[(df.Sim == 163) & (df.Tsim > 2100) & (df.Tsim < 2550)].index)
df = df.drop(df[(df.Sim == 163) & (df.Tsim > 4100) & (df.Tsim < 4600)].index)
df = df.drop(df[(df.Sim == 163) & (df.Tsim > 5450) & (df.Tsim < 5800)].index)
df = df.drop(df[(df.Sim == 163) & (df.Tsim > 6100) & (df.Tsim < 6550)].index)

df = df.drop(df[(df.Sim == 166) & (df.Tsim > 2200) & (df.Tsim < 2650)].index)
df = df.drop(df[(df.Sim == 166) & (df.Tsim > 4200) & (df.Tsim < 4700)].index)
df = df.drop(df[(df.Sim == 166) & (df.Tsim > 6200) & (df.Tsim < 6650)].index)
df = df.drop(df[(df.Sim == 166) & (df.Tsim > 7550) & (df.Tsim < 7750)].index)
df = df.drop(df[(df.Sim == 166) & (df.Team == 1) & (df.Tsim > 4400) & (df.Tsim < 5400)].index)

# # ## v3 cuts
#
df = df.drop(df[(df.Sim == 159) & (df.Team == 1)].index)
df = df.drop(df[(df.Sim == 158) & (df.Team == 1)].index)
df = df.drop(df[(df.Sim == 163) & (df.Team == 4)].index)
df = df.drop(df[(df.Sim == 159) & (df.Team == 4)].index)

dfcleaned = df

resol = 200
# dimension for Rdif: ymax/resolution

ytitle = 'Pressure (hPa)'
ytitlet = 'Time (sec.)'


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

## variables and plotting asaf Pair and PO3

avgprofEN0505_O3S_X, avgprofEN0505_O3S_Xerr, Y = Calc_average_profile_Pair(profEN0505, 'PO3')
avgprofEN1010_O3S_X, avgprofEN1010_O3S_Xerr, Y = Calc_average_profile_Pair(profEN1010, 'PO3')

print('avgprofEN0505_O3S_X', avgprofEN0505_O3S_X)
print('avgprofEN1010_O3S_X', avgprofEN1010_O3S_X)


avgprof_O3S_X, avgprof_O3S_Xerr, Y = Calc_average_profile_pressure([profEN0505,profEN1010], 'PO3')

print('avgprof_O3S_X[0]', avgprof_O3S_X[0])
print('avgprof_O3S_X[1]', avgprof_O3S_X[1])


avgprofEN0505_OPM_X, avgprofEN0505_OPM_Xerr, Y = Calc_average_profile_Pair(profEN0505, 'PO3_OPM')
avgprofEN1010_OPM_X, avgprofEN1010_OPM_Xerr, Y = Calc_average_profile_Pair(profEN1010, 'PO3_OPM')


dimension = len(Y)

# Absolute difference calculation for standard PO3
aEN0505, aENerr0505 = Calc_ADif(avgprofEN0505_O3S_X, avgprofEN0505_OPM_X, avgprofEN0505_O3S_Xerr, dimension)
aEN1010, aENerr1010 = Calc_ADif(avgprofEN1010_O3S_X, avgprofEN1010_OPM_X, avgprofEN1010_O3S_Xerr, dimension)

#  Relative difference calculation for standard PO3
rEN0505, rENerr0505 = Calc_RDif(avgprofEN0505_O3S_X, avgprofEN0505_OPM_X, avgprofEN0505_O3S_Xerr, dimension)
rEN1010, rENerr1010 = Calc_RDif(avgprofEN1010_O3S_X, avgprofEN1010_OPM_X, avgprofEN1010_O3S_Xerr, dimension)


print('aEN0505', aEN0505)
print('rEN0505', rEN0505)
print('aEN1010', aEN1010)
print('rEN1010', rEN1010)

adif, adiferr, rdif, rdiferr = Calc_Dif([avgprofEN0505_O3S_X, avgprofEN1010_O3S_X], [avgprofEN0505_OPM_X, avgprofEN1010_OPM_X],
                                        [avgprofEN0505_O3S_Xerr, avgprofEN1010_O3S_Xerr], dimension)

print(' new adif[0]', adif[0])
print(' new rdif[0]', rdif[0])
print(' new adif[1]', adif[1])
print(' new rdif[1]', rdif[1])


