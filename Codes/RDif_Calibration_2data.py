## 0910 branch

#!/usr/bin/env python
# coding: utf-8
# Libraries
import pandas as pd
import matplotlib.pyplot as plt

from Josie_Functions import  Calc_average_profile_Pair, Calc_RDif, Calc_average_profile
from Josie_PlotFunctions import  Plot_compare_4profile_plots_pair, Plot_compare_4profile_plots_time

df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie17_data_timecut_pairfixed.csv", low_memory=False)

# attention for 17 and 0910
# dfcleaned = df = df[df.ADX == 0]
dfcleaned = df

## previous version of 17 cuts
# df = df.drop(df[((df.Sim == 171) | (df.Sim == 172) |  (df.Sim == 180) | (df.Sim == 185) )].index)
# df = df.drop(df[(df.Sim == 179) & (df.Team == 4)].index)
# df = df.drop(df[(df.Sim == 172) & (df.Team == 1)].index)
# df = df.drop(df[(df.Sim == 178) & (df.Team == 3)].index)
# df = df.drop(df[((df.Sim == 175))].index)
#
# ## new version of 17 cuts
# df = df.drop(df[((df.Sim == 171) | (df.Sim == 172) |  (df.Sim == 180) | (df.Sim == 185) )].index)
# df = df.drop(df[(df.Sim == 179) & (df.Team == 4) & (df.Tsim > 4000)].index)
# df = df.drop(df[(df.Sim == 172) &  (df.Tsim < 500)].index)
# df = df.drop(df[(df.Sim == 172) & (df.Team == 1) & (df.Tsim > 5000) & (df.Tsim < 5800)].index)
# df = df.drop(df[(df.Sim == 178) & (df.Team == 3) & (df.Tsim > 1700) & (df.Tsim < 2100)].index)
# df = df.drop(df[(df.Sim == 178) & (df.Team == 3) & (df.Tsim > 2500) & (df.Tsim < 3000)].index)
# df = df.drop(df[((df.Sim == 175))].index)
# df = df.drop(df[((df.Tsim > 7000))].index)


# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_Data_withtimecut_v2.csv", low_memory=False)


resol = 300
# dimension for Rdif: ymax/resolution

ytitle = 'Pressure (hPa)'
ytitlet = 'Time (sec.)'

############################################### Filters for Sonde, Solution, Buff er selection
# 1, 0.1 ENSCI vs SPC
filtEN = dfcleaned.ENSCI == 1
filtSP = dfcleaned.ENSCI == 0

filtS10 = dfcleaned.Sol == 1
filtS05 = dfcleaned.Sol == 0.5

filtB10 = dfcleaned.Buf == 1.0
filtB05 = dfcleaned.Buf == 0.5

filterEN0505 = (filtEN & filtS05 & filtB05)
profEN0505 = dfcleaned.loc[filterEN0505]

profEN0505_nodup = profEN0505.drop_duplicates(['Sim', 'Team'])
totO3_EN0505 = profEN0505_nodup.frac.mean()

filterSP1010 = (filtSP & filtS10 & filtB10)
profSP1010 = dfcleaned.loc[filterSP1010]

profSP1010_nodup = profSP1010.drop_duplicates(['Sim', 'Team'])
totO3_SP1010 = profSP1010_nodup.frac.mean()

avgprofEN0505_X, avgprofEN0505_Xerr, Y1 = Calc_average_profile_Pair(profEN0505, 'ADif_PO3S')
avgprofSP1010_X, avgprofSP1010_Xerr, Y1 = Calc_average_profile_Pair(profSP1010, 'ADif_PO3S')
avgprofEN0505_O3S_X, avgprofEN0505_O3S_Xerr, Y = Calc_average_profile_Pair(profEN0505, 'PO3')
avgprofSP1010_O3S_X, avgprofSP1010_O3S_Xerr, Y = Calc_average_profile_Pair(profSP1010, 'PO3')
avgprofEN0505_OPM_X, avgprofEN0505_OPM_Xerr, Y = Calc_average_profile_Pair(profEN0505, 'PO3_OPM')
avgprofSP1010_OPM_X, avgprofSP1010_OPM_Xerr, Y = Calc_average_profile_Pair(profSP1010, 'PO3_OPM')

dimension = len(Y)

# piece of code special for Relative difference calculation
rEN0505, rENerr0505 = Calc_RDif(avgprofEN0505_O3S_X, avgprofEN0505_OPM_X, avgprofEN0505_Xerr, dimension)
rSP1010, rSPerr1010 = Calc_RDif(avgprofSP1010_O3S_X, avgprofSP1010_OPM_X, avgprofSP1010_Xerr, dimension)

## the same for time binning

avgprofEN0505_X_time, avgprofEN0505_Xerr_time, Y_time = Calc_average_profile(profEN0505,resol,  'ADif_PO3S')
avgprofSP1010_X_time, avgprofSP1010_Xerr_time, Y_time = Calc_average_profile(profSP1010,resol,  'ADif_PO3S')
avgprofEN0505_O3S_X_time, avgprofEN0505_O3S_Xerr_time, Y_time = Calc_average_profile(profEN0505,resol,  'PO3')
avgprofSP1010_O3S_X_time, avgprofSP1010_O3S_Xerr_time, Y_time = Calc_average_profile(profSP1010,resol,  'PO3')
avgprofEN0505_OPM_X_time, avgprofEN0505_OPM_Xerr_time, Y_time = Calc_average_profile(profEN0505,resol,  'PO3_OPM')
avgprofSP1010_OPM_X_time, avgprofSP1010_OPM_Xerr_time, Y_time = Calc_average_profile(profSP1010,resol,  'PO3_OPM')

dimension = len(Y_time)

# piece of code special for Relative difference calculation
rEN0505_time, rENerr0505_time = Calc_RDif(avgprofEN0505_O3S_X_time, avgprofEN0505_OPM_X_time, avgprofEN0505_Xerr_time, dimension)
rSP1010_time, rSPerr1010_time = Calc_RDif(avgprofSP1010_O3S_X_time, avgprofSP1010_OPM_X_time, avgprofSP1010_Xerr_time, dimension)

#additional cuts aplied on 0910 v1 data

df0910 = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_Data_withtimecut_v2_pair.csv", low_memory=False)

# ## v3 cuts

df0910 = df0910.drop(df0910[(df0910.Sim == 159) & (df0910.Team == 1)].index)
df0910 = df0910.drop(df0910[(df0910.Sim == 158) & (df0910.Team == 1)].index)
df0910 = df0910.drop(df0910[(df0910.Sim == 163) & (df0910.Team == 4)].index)
df0910 = df0910.drop(df0910[(df0910.Sim == 159) & (df0910.Team == 4)].index)


# attention for 17 and 0910
df0910 = df0910[df0910.ADX == 0]



filtEN_0910 = df0910.ENSCI == 1
filtSP_0910 = df0910.ENSCI == 0

filtS10_0910 = df0910.Sol == 1
filtS05_0910 = df0910.Sol == 0.5

filtB10_0910 = df0910.Buf == 1.0
filtB05_0910 = df0910.Buf == 0.5

filterEN0505_0910 = (filtEN_0910 & filtS05_0910 & filtB05_0910)
profEN0505_0910 = df0910.loc[filterEN0505_0910]
profEN0505_0910_nodup = profEN0505_0910.drop_duplicates(['Sim', 'Team'])
totO3_EN0505_0910 = profEN0505_0910_nodup.frac.mean()


filterSP1010_0910 = (filtSP_0910 & filtS10_0910 & filtB10_0910)
profSP1010_0910 = df0910.loc[filterSP1010_0910]
profSP1010_0910_nodup = profSP1010_0910.drop_duplicates(['Sim', 'Team'])
totO3_SP1010_0910 = profSP1010_0910_nodup.frac.mean()

avgprofEN0505_0910_X, avgprofEN0505_0910_Xerr, Y1 = Calc_average_profile_Pair(profEN0505_0910, 'ADif_PO3S')
avgprofSP1010_0910_X, avgprofSP1010_0910_Xerr, Y1 = Calc_average_profile_Pair(profSP1010_0910, 'ADif_PO3S')
avgprofEN0505_0910_O3S_X, avgprofEN0505_0910_O3S_Xerr, Y = Calc_average_profile_Pair(profEN0505_0910, 'PO3')
avgprofSP1010_0910_O3S_X, avgprofSP1010_0910_O3S_Xerr, Y = Calc_average_profile_Pair(profSP1010_0910, 'PO3')
avgprofEN0505_0910_OPM_X, avgprofEN0505_0910_OPM_Xerr, Y = Calc_average_profile_Pair(profEN0505_0910, 'PO3_OPM')
avgprofSP1010_0910_OPM_X, avgprofSP1010_0910_OPM_Xerr, Y = Calc_average_profile_Pair(profSP1010_0910, 'PO3_OPM')

dimension = len(Y)
# piece of code special for Relative difference calculation
rEN0505_0910, rENerr0505_0910 = Calc_RDif(avgprofEN0505_0910_O3S_X, avgprofEN0505_0910_OPM_X, avgprofEN0505_0910_Xerr, dimension)
rSP1010_0910, rSPerr1010_0910 = Calc_RDif(avgprofSP1010_0910_O3S_X, avgprofSP1010_0910_OPM_X, avgprofSP1010_0910_Xerr, dimension)


## the same asaf time

avgprofEN0505_0910_X_time, avgprofEN0505_0910_Xerr_time, Y_time =  Calc_average_profile(profEN0505_0910,resol,  'ADif_PO3S')
avgprofSP1010_0910_X_time, avgprofSP1010_0910_Xerr_time, Y_time =  Calc_average_profile(profSP1010_0910,resol,  'ADif_PO3S')
avgprofEN0505_0910_O3S_X_time, avgprofEN0505_0910_O3S_Xerr_time, Y_time =  Calc_average_profile(profEN0505_0910,resol,  'PO3')
avgprofSP1010_0910_O3S_X_time, avgprofSP1010_0910_O3S_Xerr_time, Y_time =  Calc_average_profile(profSP1010_0910,resol,  'PO3')
avgprofEN0505_0910_OPM_X_time, avgprofEN0505_0910_OPM_Xerr_time, Y_time =  Calc_average_profile(profEN0505_0910,resol,  'PO3_OPM')
avgprofSP1010_0910_OPM_X_time, avgprofSP1010_0910_OPM_Xerr_time, Y_time =  Calc_average_profile(profSP1010_0910,resol,  'PO3_OPM')

dimension = len(Y_time)
# piece of code special for Relative difference calculation
rEN0505_0910_time, rENerr0505_0910_time = Calc_RDif(avgprofEN0505_0910_O3S_X_time, avgprofEN0505_0910_OPM_X_time, avgprofEN0505_0910_Xerr_time, dimension)
rSP1010_0910_time, rSPerr1010_0910_time = Calc_RDif(avgprofSP1010_0910_O3S_X_time, avgprofSP1010_0910_OPM_X_time, avgprofSP1010_0910_Xerr_time, dimension)


Plot_compare_4profile_plots_pair(
    avgprofEN0505_X, avgprofEN0505_Xerr, avgprofEN0505_0910_X, avgprofEN0505_0910_Xerr, avgprofSP1010_X, avgprofSP1010_Xerr,
    avgprofSP1010_0910_X, avgprofSP1010_0910_Xerr, Y, [-3, 3], ' ', 'Sonde - OPM  Difference (mPa)', ytitle, 'EN 0.5%-0.5B - 17',
    'EN 0.5%-0.5B - 0910 ', 'SP 1.0%-1.0B - 17', 'SP 1.0%-1.0B 0910', totO3_EN0505, totO3_EN0505_0910, totO3_SP1010, totO3_SP1010_0910,
    profEN0505.drop_duplicates(['Sim', 'Team']), profEN0505_0910.drop_duplicates(['Sim', 'Team']), profSP1010_nodup,
    profSP1010_0910_nodup, 'ADif_Pair_CalibrationFunction_0910v3_vs17_nm')

Plot_compare_4profile_plots_pair(
    rEN0505, rENerr0505, rEN0505_0910, rENerr0505_0910, rSP1010, rSPerr1010, rSP1010_0910, rSPerr1010_0910, Y, [-40, 40], ' ',
    'Sonde - OPM  Difference (%)',
    ytitle, 'EN 0.5%-0.5B - 17',  'EN 0.5%-0.5B - 0910 ', 'SP 1.0%-1.0B - 17', 'SP 1.0%-1.0B 0910 - 0910', totO3_EN0505, totO3_EN0505_0910, totO3_SP1010,
    totO3_SP1010_0910,
    profEN0505.drop_duplicates(['Sim', 'Team']), profEN0505_0910.drop_duplicates(['Sim', 'Team']), profSP1010_nodup,
    profSP1010_0910_nodup, 'RDif_Pair_CalibrationFunction_0910v3_vs17_nm')


Plot_compare_4profile_plots_time(
    avgprofEN0505_X_time, avgprofEN0505_Xerr_time, avgprofEN0505_0910_X_time, avgprofEN0505_0910_Xerr_time,
    avgprofSP1010_X_time, avgprofSP1010_Xerr_time, avgprofSP1010_0910_X_time, avgprofSP1010_0910_Xerr_time, Y_time,
    [-3, 3], ' ', 'Sonde - OPM  Difference (mPa)', 'Time (sec.)', 'EN 0.5%-0.5B - 17', 'EN 0.5%-0.5B - 0910 ',
    'SP 1.0%-1.0B - 17', 'SP 1.0%-1.0B 0910', totO3_EN0505, totO3_EN0505_0910, totO3_SP1010, totO3_SP1010_0910,
    profEN0505.drop_duplicates(['Sim', 'Team']), profEN0505_0910.drop_duplicates(['Sim', 'Team']), profSP1010_nodup,
    profSP1010_0910_nodup, 'ADif_Time_CalibrationFunction_0910v3_vs17_nm')

Plot_compare_4profile_plots_time(
    rEN0505_time, rENerr0505_time, rEN0505_0910_time, rENerr0505_0910_time, rSP1010_time, rSPerr1010_time, rSP1010_0910_time, rSPerr1010_0910_time, Y_time, [-40, 40], ' ',
    'Sonde - OPM  Difference (%)',  'Time (sec.)', 'EN 0.5%-0.5B - 17',  'EN 0.5%-0.5B - 0910 ', 'SP 1.0%-1.0B - 17',
    'SP 1.0%-1.0B 0910 - 0910', totO3_EN0505, totO3_EN0505_0910, totO3_SP1010, totO3_SP1010_0910,
    profEN0505.drop_duplicates(['Sim', 'Team']), profEN0505_0910.drop_duplicates(['Sim', 'Team']), profSP1010_nodup,
    profSP1010_0910_nodup, 'RDif_Time_CalibrationFunction_0910v3_vs17_nm')

########################################################################################################################


# ## v3 cuts
# df0910 = df0910.drop(df0910[(df0910.Sim == 166) & (df0910.Team == 1)].index)
# df0910 = df0910.drop(df0910[(df0910.Sim == 164) & (df0910.Tsim > 4500) ].index)
# df0910 = df0910.drop(df0910[(df0910.Sim == 163) & (df0910.Tsim > 7000) ].index)
# df0910 = df0910.drop(df0910[(df0910.Sim == 162)].index)
# df0910 = df0910.drop(df0910[(df0910.Sim == 148)].index)
# df0910 = df0910.drop(df0910[(df0910.Sim == 145)].index)
# df0910 = df0910.drop(df0910[(df0910.Sim == 140)].index)
# df0910 = df0910.drop(df0910[(df0910.Sim == 160) & (df0910.Tsim > 6000) ].index)
