## 0910 branch

#!/usr/bin/env python
# coding: utf-8
# Libraries
import pandas as pd
import matplotlib.pyplot as plt

from Josie_Functions import  Calc_average_profile_pressure, Calc_average_profile_time, Calc_Dif, Calc_average_profileCurrent_pressure, Calc_average_profileCurrent_time
from Josie_PlotFunctions import  errorPlot_ARDif_withtext, errorPlot_general

folderpath = 'Dif_0910_err'

df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_deconv.csv", low_memory=False)
# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv.csv", low_memory=False)

df = df.drop(df[(df.PO3 < 0)].index)
df = df.drop(df[(df.PO3_OPM < 0)].index)

# df = df[df.ADX == 0]

test = df.drop_duplicates(['Sim', 'Team'])
print(len(test))

df = df[df.ADX == 0]

test = df.drop_duplicates(['Sim', 'Team'])
print(len(test))



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
## new cuts v4 08/04
# df = df.drop(df[(df.Sim == 160) & (df.Team == 4)].index)
# df = df.drop(df[(df.Sim == 166) & (df.Team == 1)].index)

# # ## v3 cuts 
### I think these cuts are not needed## checkcheck
df = df.drop(df[(df.Sim == 159) & (df.Team == 1)].index) ##??
df = df.drop(df[(df.Sim == 158) & (df.Team == 1)].index)
df = df.drop(df[(df.Sim == 163) & (df.Team == 4)].index)
df = df.drop(df[(df.Sim == 159) & (df.Team == 4)].index)
####

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

dfcleaned = df

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

##################################################################################
################     Pressure PO3 PLOTS        #################################
##################################################################################


## order of the lists [en0505, en1010, sp0505, sp1010]
avgprof_O3S_X, avgprof_O3S_Xerr, Y = Calc_average_profile_pressure([profEN0505, profEN1010, profSP0505, profSP1010],
                                                                   'PO3')
avgprof_O3S_X_dc, avgprof_O3S_Xerr_dc, Y = Calc_average_profile_pressure([profEN0505, profEN1010, profSP0505, profSP1010],
                                                                         'PO3_deconv')
avgprof_O3S_X_dc_sm10, avgprof_O3S_Xerr_dc_sm10, Y = Calc_average_profile_pressure([profEN0505, profEN1010, profSP0505, profSP1010],
                                                                         'PO3_deconv_sm10')
avgprof_O3S_X_dcjma, avgprof_O3S_Xerr_dcjma, Y = Calc_average_profile_pressure([profEN0505, profEN1010, profSP0505, profSP1010],
                                                                               'PO3_deconv_jma')
avgprof_O3S_X_dcjma_sm10, avgprof_O3S_Xerr_dcjma_sm10, Y = Calc_average_profile_pressure([profEN0505, profEN1010, profSP0505, profSP1010],
                                                                               'PO3_deconv_jma_sm10')
avgprof_OPM_X, avgprof_OPM_Xerr, Y = Calc_average_profile_pressure([profEN0505, profEN1010, profSP0505, profSP1010],
                                                                   'PO3_OPM')

dimension = len(Y)

adif, adiferr, rdif, rdiferr = Calc_Dif(avgprof_O3S_X, avgprof_OPM_X, avgprof_O3S_Xerr, dimension)
adif_dc, adiferr_dc, rdif_dc, rdiferr_dc = Calc_Dif(avgprof_O3S_X_dc, avgprof_OPM_X, avgprof_O3S_Xerr_dc, dimension)
adif_dc_sm10, adiferr_dc_sm10, rdif_dc_sm10, rdiferr_dc_sm10 = Calc_Dif(avgprof_O3S_X_dc_sm10, avgprof_OPM_X, avgprof_O3S_Xerr_dc_sm10, dimension)
adif_dcjma, adiferr_dcjma, rdif_dcjma, rdiferr_dcjma = Calc_Dif(avgprof_O3S_X_dcjma, avgprof_OPM_X, avgprof_O3S_Xerr_dcjma, dimension)
adif_dcjma_sm10, adiferr_dcjma_sm10, rdif_dcjma_sm10, rdiferr_dcjma_sm10 = Calc_Dif(avgprof_O3S_X_dcjma_sm10, avgprof_OPM_X,
                                                                                avgprof_O3S_Xerr_dcjma_sm10, dimension)

### Plotting
axtitle = 'Sonde - OPM  Difference (mPa)'
rxtitle = 'Sonde - OPM  Difference (%)'

labellist = ['EN 0.5%-0.5B','EN 1.0%-1.0B', 'SP 0.5%-0.5B', 'SP 1.0%-1.0B']
o3list = [totO3_EN0505, totO3_EN1010,  totO3_SP0505, totO3_SP1010]
dfnplist = [profEN0505.drop_duplicates(['Sim', 'Team']), profEN1010.drop_duplicates(['Sim', 'Team']), profSP0505_nodup,
            profSP1010_nodup]

errorPlot_ARDif_withtext(adif, adiferr, Y, [-3, 3], [1000,5],  '0910 Data',  axtitle, ytitle, labellist, o3list, dfnplist,
                           'ADif_Pair_0910', folderpath ,  True, False)

errorPlot_ARDif_withtext(rdif, rdiferr, Y, [-40, 40], [1000,5],  '0910 Data',  rxtitle, ytitle, labellist, o3list, dfnplist,
                           'RDif_Pair_0910', folderpath, True, False)

## convoluted ones

errorPlot_ARDif_withtext(adif_dc, adiferr_dc, Y, [-3, 3], [1000,5],  '0910 Data Conv-Deconv (PO3 JMA corr.)',  axtitle, ytitle, labellist, o3list, dfnplist,
                           'ADif_Pair_Convoluted_0910', folderpath ,  True, False)

errorPlot_ARDif_withtext(rdif_dc, rdiferr_dc, Y, [-40, 40], [1000,5],  '0910 Data Conv-Deconv (PO3 JMA corr.)',  rxtitle, ytitle, labellist, o3list, dfnplist,
                           'RDif_Pair_Convoluted_0910', folderpath, True, False)

# new_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
# blue, orange, green, red, purple, brown, pinkish, greyish, yellowish, bluish

colorlist = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

checklabel = ['PO3', 'PO3 deconv', 'PO3 deconv smoothed ', 'PO3 deconv jma', 'PO3 deconv jma smoothed']

errorPlot_general([adif[0], adif_dc[0], adif_dc_sm10[0], adif_dcjma[0], adif_dcjma_sm10[0]],
                  [adiferr[0], adiferr_dc[0], adiferr_dc_sm10[0], adiferr_dcjma[0], adiferr_dcjma_sm10[0]], Y, [-3,3], [1000,5],
                  '0910 data- ENSCI 0.5%-0.5%B', axtitle, ytitle,
                  checklabel, colorlist, 'ADif_Check_EN0505', folderpath, 1)

errorPlot_general([rdif[0], rdif_dc[0], rdif_dc_sm10[0], rdif_dcjma[0], rdif_dcjma_sm10[0]],
                  [rdiferr[0], rdiferr_dc[0], rdiferr_dc_sm10[0], rdiferr_dcjma[0], rdiferr_dcjma_sm10[0]], Y, [-20, 20], [1000,5],
                  '0910 data- ENSCI 0.5%-0.5%B', rxtitle, ytitle,
                  checklabel, colorlist, 'RDif_Check_EN0505', folderpath, 1)


errorPlot_general([adif[1], adif_dc[1], adif_dc_sm10[1], adif_dcjma[1], adif_dcjma_sm10[1]],
                  [adiferr[1], adiferr_dc[1], adiferr_dc_sm10[1], adiferr_dcjma[1], adiferr_dcjma_sm10[1]], Y, [-3,3], [1000,5],
                  '0910 data- ENSCI 1.0%-1.0%B', axtitle, ytitle,
                  checklabel, colorlist, 'ADif_Check_EN1010', folderpath, 1)

errorPlot_general([rdif[1], rdif_dc[1], rdif_dc_sm10[1], rdif_dcjma[1], rdif_dcjma_sm10[1]],
                  [rdiferr[1], rdiferr_dc[1], rdiferr_dc_sm10[1], rdiferr_dcjma[1], rdiferr_dcjma_sm10[1]], Y, [-20,20], [1000,5],
                  '0910 data- ENSCI 1.0%-1.0%B', rxtitle, ytitle,
                  checklabel, colorlist, 'RDif_Check_EN1010', folderpath, 1)

errorPlot_general([adif[2], adif_dc[2], adif_dc_sm10[2], adif_dcjma[2], adif_dcjma_sm10[2]],
                  [adiferr[2], adiferr_dc[2], adiferr_dc_sm10[2], adiferr_dcjma[2], adiferr_dcjma_sm10[2]], Y, [-3,3], [1000,5],
                  '0910 data- SP 0.5%-0.5%B', axtitle, ytitle,
                  checklabel, colorlist, 'ADif_Check_SP0505', folderpath, 1)

errorPlot_general([rdif[2], rdif_dc[2], rdif_dc_sm10[2], rdif_dcjma[2], rdif_dcjma_sm10[2]],
                  [rdiferr[2], rdiferr_dc[2], rdiferr_dc_sm10[2], rdiferr_dcjma[2], rdiferr_dcjma_sm10[2]], Y, [-20, 20], [1000,5],
                  '0910 data- SP 0.5%-0.5%B', rxtitle, ytitle,
                  checklabel, colorlist, 'RDif_Check_SP0505', folderpath, 1)

errorPlot_general([adif[3], adif_dc[3], adif_dc_sm10[3], adif_dcjma[3], adif_dcjma_sm10[3]],
                  [adiferr[3], adiferr_dc[3], adiferr_dc_sm10[3], adiferr_dcjma[3], adiferr_dcjma_sm10[3]], Y, [-3,3], [1000,5],
                  '0910 data- SP 1.0%-1.0%B', axtitle, ytitle,
                  checklabel, colorlist, 'ADif_Check_SP1010', folderpath, 1)

errorPlot_general([rdif[3], rdif_dc[3], rdif_dc_sm10[3], rdif_dcjma[3], rdif_dcjma_sm10[3]],
                  [rdiferr[3], rdiferr_dc[3], rdiferr_dc_sm10[3], rdiferr_dcjma[3], rdiferr_dcjma_sm10[3]], Y, [-20, 20], [1000,5],
                  '0910 data- SP 1.0%-1.0%B', rxtitle, ytitle,
                  checklabel, colorlist, 'RDif_Check_SP1010', folderpath, 1)

################################
## now do the same asaf of time
################################
resolution = 400
tmin = 200
tmax = 8000
## order of the lists [en0505, en1010, sp0505, sp1010]
avgprof_O3S_T, avgprof_O3S_Terr, Yt = Calc_average_profile_time([profEN0505, profEN1010, profSP0505, profSP1010],
                                                                   'PO3', resolution, tmin, tmax)
avgprof_O3S_T_dc, avgprof_O3S_Terr_dc, Yt = Calc_average_profile_time([profEN0505, profEN1010, profSP0505, profSP1010],
                                                                         'PO3_deconv', resolution, tmin, tmax)
avgprof_OPM_T, avgprof_OPM_Terr, Yt = Calc_average_profile_time([profEN0505, profEN1010, profSP0505, profSP1010],
                                                                   'PO3_OPM', resolution, tmin, tmax )

dimension = len(Yt)

adifT, adifTerr, rdifT, rdifTerr = Calc_Dif(avgprof_O3S_T, avgprof_OPM_T, avgprof_O3S_Terr, dimension)
adifT_dc, adifTerr_dc, rdifT_dc, rdifTerr_dc = Calc_Dif(avgprof_O3S_T_dc, avgprof_OPM_T, avgprof_O3S_Terr_dc, dimension)


### Plotting
axtitle = 'Sonde - OPM  Difference (mPa)'
rxtitle = 'Sonde - OPM  Difference (%)'

labellist = ['EN 0.5%-0.5B','EN 1.0%-1.0B', 'SP 0.5%-0.5B', 'SP 1.0%-1.0B']
# o3list = [totO3_EN0505, totO3_EN1010,  totO3_SP0505, totO3_SP1010]
# dfnplist = [profEN0505.drop_duplicates(['Sim', 'Team']), profEN1010.drop_duplicates(['Sim', 'Team']), profSP0505_nodup,
#             profSP1010_nodup]

errorPlot_ARDif_withtext(adifT, adifTerr, Yt, [-3, 3], [0, 9000],  '0910 Data',  axtitle, ytitlet, labellist, o3list, dfnplist,
                           'ADif_TSim_0910', folderpath ,  False, False)

errorPlot_ARDif_withtext(rdifT, rdifTerr, Yt, [-40, 40], [0, 9000],  '0910 Data',  rxtitle, ytitlet, labellist, o3list, dfnplist,
                           'RDif_TSim_0910', folderpath, False, False)

## convoluted ones

errorPlot_ARDif_withtext(adifT_dc, adifTerr_dc, Yt, [-3, 3], [0, 9000],  '0910 Data Conv-Deconv (PO3 JMA corr.)',  axtitle, ytitlet,
                         labellist, o3list, dfnplist,
                           'ADif_TSim_Convoluted_0910', folderpath ,  False, False)

errorPlot_ARDif_withtext(rdifT_dc, rdifTerr_dc, Yt, [-40, 40], [0, 9000],  '0910 Data Conv-Deconv (PO3 JMA corr.)',  rxtitle, ytitlet,
                         labellist, o3list, dfnplist,
                           'RDif_TSim_Convoluted_0910', folderpath, False, False)

##################################################################################
################      CURRENT IM PLOTS        #################################
##################################################################################


##  asaf pressure

avgprof_O3S_cur, avgprof_O3S_curerr, Ycur = Calc_average_profileCurrent_pressure([profEN0505, profEN1010, profSP0505, profSP1010],
                                                                   'IM')
avgprof_O3S_curSlow, avgprof_O3S_curSlowerr, Yslow = Calc_average_profileCurrent_pressure([profEN0505, profEN1010, profSP0505, profSP1010],
                                                                   'I_slow_conv')
avgprof_O3S_cur_dc, avgprof_O3S_curerr_dc, Y = Calc_average_profileCurrent_pressure([profEN0505, profEN1010, profSP0505, profSP1010],
                                                                         'I_fast_deconv')
avgprof_OPM_cur, avgprof_OPM_curerr, Y = Calc_average_profileCurrent_pressure([profEN0505, profEN1010, profSP0505, profSP1010],
                                                                   'I_OPM_jma')

dimension = len(Y)

adifcur, adifcurerr, rdifcur, rdifcurerr = Calc_Dif(avgprof_O3S_cur, avgprof_OPM_cur, avgprof_O3S_curerr, dimension)
adifcur_dc, adifcurerr_dc, rdifcur_dc, rdifcurerr_dc = Calc_Dif(avgprof_O3S_cur_dc, avgprof_OPM_cur, avgprof_O3S_curerr_dc, dimension)


### Plotting
axtitlecur = r'Sonde - OPM  Difference ($\mu$A)'
rxtitle = 'Sonde - OPM  Difference (%)'


errorPlot_ARDif_withtext(adifcur, adifcurerr, Y, [-3, 3], [1000,5],  '0910 Data (Current)',  axtitlecur, ytitle, labellist, o3list, dfnplist,
                           'Current_ADif_Pair_0910', folderpath ,  True, False)

errorPlot_ARDif_withtext(rdifcur, rdifcurerr, Y, [-40, 40], [1000,5],  '0910 Data (Current)',  rxtitle, ytitle, labellist, o3list, dfnplist,
                           'Current_RDif_Pair_0910', folderpath, True, False)

## convoluted ones

errorPlot_ARDif_withtext(adifcur_dc, adifcurerr_dc, Y, [-3, 3], [1000,5],  '0910 Data Conv-Deconv (Current)',  axtitlecur, ytitle,
                         labellist, o3list, dfnplist,
                           'Current_ADif_Pair_Convoluted_0910', folderpath ,  True, False)

errorPlot_ARDif_withtext(rdifcur_dc, rdifcurerr_dc, Y, [-40, 40], [1000,5],  '0910 Data Conv-Deconv (Current)',  rxtitle, ytitle,
                         labellist, o3list, dfnplist,
                           'Current_RDif_Pair_Convoluted_0910', folderpath, True, False)


##  asaf time

## order of the lists [en0505, en1010, sp0505, sp1010]
avgprof_O3S_curT, avgprof_O3S_curTerr, Yt = Calc_average_profileCurrent_time([profEN0505, profEN1010, profSP0505, profSP1010],
                                                                   'IM', resolution, tmin, tmax)
avgprof_O3S_curSlowT, avgprof_O3S_curSlowTerr, Yt = Calc_average_profileCurrent_time([profEN0505, profEN1010, profSP0505, profSP1010],
                                                                   'I_slow_conv', resolution, tmin, tmax)
avgprof_O3S_curT_dc, avgprof_O3S_curTerr_dc, Yt = Calc_average_profileCurrent_time([profEN0505, profEN1010, profSP0505, profSP1010],
                                                                         'I_fast_deconv', resolution, tmin, tmax)
avgprof_OPM_curT, avgprof_OPM_curTerr, Yt = Calc_average_profileCurrent_time([profEN0505, profEN1010, profSP0505, profSP1010],
                                                                   'I_OPM_jma', resolution, tmin, tmax )

dimension = len(Yt)

adifcurT, adifcurTerr, rdifcurT, rdifcurTerr = Calc_Dif(avgprof_O3S_curT, avgprof_OPM_curT, avgprof_O3S_curTerr, dimension)
adifcurT_dc, adifcurTerr_dc, rdifcurT_dc, rdifcurTerr_dc = Calc_Dif(avgprof_O3S_curT_dc, avgprof_OPM_curT, avgprof_O3S_curTerr_dc, dimension)


### Plotting
axtitle = 'Sonde - OPM  Difference (mPa)'
rxtitle = 'Sonde - OPM  Difference (%)'

errorPlot_ARDif_withtext(adifcurT, adifcurTerr, Yt, [-3, 3], [0, 9000],  '0910 Data (Current)',  axtitlecur, ytitlet, labellist, o3list, dfnplist,
                           'Current_ADif_TSim_0910_', folderpath ,  False, False)

errorPlot_ARDif_withtext(rdifcurT, rdifcurTerr, Yt, [-40, 40], [0, 9000],  '0910 Data (Current)',  rxtitle, ytitlet, labellist, o3list, dfnplist,
                           'Current_RDif_TSim_0910', folderpath, False, False)

## convoluted ones

errorPlot_ARDif_withtext(adifcurT_dc, adifcurTerr_dc, Yt, [-3, 3], [0, 9000],  '0910 Data Conv-Deconv (Current) ',  axtitlecur, ytitlet,
                         labellist, o3list, dfnplist,
                           'Current_ADif_TSim_Convoluted_0910', folderpath ,  False, False)

errorPlot_ARDif_withtext(rdifcurT_dc, rdifcurTerr_dc, Yt, [-40, 40], [0, 9000],  '0910 Data Conv-Deconv (Current)',  rxtitle, ytitlet,
                         labellist, o3list, dfnplist,
                           'Current_RDif_TSim_Convoluted_0910', folderpath, False, False)

#####  final plot for relative contribution of I_slow to the total current asaf of pressure

print('check', len(avgprof_O3S_curSlow[0]), len(avgprof_O3S_cur[0]))
print(len(Ycur), len(Yslow))
dimension = len(Yslow)

print('avgprof_O3S_curSlow', avgprof_O3S_curSlow[0])
print('avgprof_O3S_cur', avgprof_O3S_cur[0])

adifcurSlow = [ (i - j)/i for i in avgprof_O3S_cur[0] for j in avgprof_O3S_curSlow[0] ]

print('one adifcurSlow', adifcurSlow[0])

adifcurSlow, adifcurSlowerr, rdifcurSlow, rdifcurSlowerr = Calc_Dif(avgprof_O3S_curSlow, avgprof_O3S_cur, avgprof_O3S_curSlowerr, dimension)

print('adifcurSlow', adifcurSlow[0])
print('rdifcurSlow', rdifcurSlow[0])

for k in range(4):
    for s in range(len(rdifcurSlow[k])):
        rdifcurSlow[k][s] = avgprof_O3S_curSlow[k][s]/ avgprof_O3S_cur[k][s] * 100

print('rdifcurSlow two', rdifcurSlow[0])

errorPlot_ARDif_withtext(adifcurSlow, adifcurSlowerr, Yslow, [-3, 3], [1000,5],  '0910 Data',  axtitle, ytitle, labellist, o3list, dfnplist,
                           'I_Slow_Contribution_ADif_Pair_0910', folderpath ,  True, False)

errorPlot_ARDif_withtext(rdifcurSlow, rdifcurSlowerr, Yslow, [-20, 20], [1000,5],  '0910 Data',  r'I$_{slow}$conv./I$_{ECC}$ (%)', ytitle, labellist, o3list, dfnplist,
                           'I_Slow_Contribution_RDif_Pair_0910', folderpath, True, False)

#####  final plot for relative contribution of I_slow to the total current asaf of time
dimension = len(Yt)


adifcurSlowT, adifcurSlowTerr, rdifcurSlowT, rdifcurSlowTerr = Calc_Dif(avgprof_O3S_curSlowT, avgprof_O3S_curT, avgprof_O3S_curSlowTerr, dimension)

for kk in range(4):
    for ss in range(len(rdifcurSlow[kk])):
        rdifcurSlowT[kk][ss] = avgprof_O3S_curSlowT[kk][ss]/ avgprof_O3S_curT[kk][ss] * 100

errorPlot_ARDif_withtext(adifcurSlowT, adifcurSlowTerr, Yt, [-3, 3], [0, 9000],  '0910 Data',  axtitle, ytitlet, labellist, o3list, dfnplist,
                           'I_Slow_Contribution_ADif_TSim_0910', folderpath ,  False, False)

errorPlot_ARDif_withtext(rdifcurSlowT, rdifcurSlowTerr, Yt, [-20, 20], [0, 9000],  '0910 Data',    r'I$_{slow}$conv./I$_{ECC}$ (%)', ytitlet, labellist, o3list, dfnplist,
                           'I_Slow_Contribution_RDif_TSim_0910', folderpath, False, False)