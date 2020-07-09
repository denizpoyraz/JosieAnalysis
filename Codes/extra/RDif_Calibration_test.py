## 2017 branch

#!/usr/bin/env python
# coding: utf-8
# Libraries
import pandas as pd
import matplotlib.pyplot as plt

from Josie_Functions import  Calc_average_profile_pressure, Calc_average_profile_time, Calc_Dif, Calc_average_profile_pressureRDif
from Josie_PlotFunctions import  errorPlot_ARDif_withtext, errorPlot_general

folderpath = 'test_rdif'

df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_Data_nocut.csv", low_memory=False)
# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv.csv", low_memory=False)

df = df.drop(df[(df.PO3 <= 0)].index)
df = df.drop(df[(df.PO3_OPM <= 0)].index)


# df = df.drop(df[((df.Sim == 171) | (df.Sim == 172) | (df.Sim == 180) | (df.Sim == 185))].index)

df = df.drop(df[(df.Sim == 179) & (df.Team == 4)].index)
df = df.drop(df[(df.Sim == 172) & (df.Team == 1)].index)
df = df.drop(df[(df.Sim == 178) & (df.Team == 3)].index)
df = df.drop(df[((df.Sim == 175))].index)


df = df.drop(df[(df.Sim == 179) & (df.Team == 4) & (df.Tsim > 4000)].index)
df = df.drop(df[(df.Sim == 172) & (df.Tsim < 500)].index)
df = df.drop(df[(df.Sim == 172) & (df.Team == 1) & (df.Tsim > 5000) & (df.Tsim < 5800)].index)
df = df.drop(df[(df.Sim == 178) & (df.Team == 3) & (df.Tsim > 1700) & (df.Tsim < 2100)].index)
df = df.drop(df[(df.Sim == 178) & (df.Team == 3) & (df.Tsim > 2500) & (df.Tsim < 3000)].index)

df = df.drop(df[((df.Sim == 186) &  (df.Tsim > 5000))].index)
df = df.drop(df[((df.Tsim > 7000))].index)

## new cuts 08/04
## not big effect
# df = df.drop(df[(df.Sim == 180) & (df.Team == 4)].index)
# df = df.drop(df[(df.Sim == 180) & (df.Team == 3)].index)
##

dfcleaned = df

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

##################################################################################
################     Pressure PO3 PLOTS        #################################
##################################################################################


## order of the lists [en0505, en1001, sp0505, sp1001]
print('o3')
avgprof_O3S_X, avgprof_O3S_Xerr, atest, atesterr, Y = Calc_average_profile_pressureRDif([profEN0505, profEN1001, profSP1010, profSP1001],
                                                                   'PO3',1)
print('avgprof_O3S_X', avgprof_O3S_X[0])
print('avgprof_O3S_Xerr', avgprof_O3S_Xerr[0] )
print('atest',atest[0])
print('atesterr', atesterr[0])

Aavgprof_O3S_X, Aavgprof_O3S_Xerr, Y = Calc_average_profile_pressure([profEN0505, profEN1001, profSP1010, profSP1001],
                                                                   'ADif_PO3S')
print('adif o3  ')

print('Aavgprof_O3S_X', Aavgprof_O3S_X[0])
print('Aavgprof_O3S_Xerr',  Aavgprof_O3S_Xerr[0] )


print('rdif ')

avgprof_O3S_X, avgprof_O3S_Xerr,rtest, rtesterr, Y = Calc_average_profile_pressureRDif([profEN0505, profEN1001, profSP1010, profSP1001],
                                                                   'PO3', 1)
print(rtest[0])
print(rtesterr[0])

# avgprof_O3S_X_dc, avgprof_O3S_Xerr_dc, Y = Calc_average_profile_pressure([profEN0505, profEN1001, profSP1010, profSP1001],
#                                                                          'PO3_deconv')
# avgprof_O3S_X_dc_sm6, avgprof_O3S_Xerr_dc_sm6, Y = Calc_average_profile_pressure([profEN0505, profEN1001, profSP1010, profSP1001],
#                                                                          'PO3_deconv_sm6')
# avgprof_O3S_X_dcjma, avgprof_O3S_Xerr_dcjma, Y = Calc_average_profile_pressure([profEN0505, profEN1001, profSP1010, profSP1001],
#                                                                                'PO3_deconv_jma')
# avgprof_O3S_X_dcjma_sm6, avgprof_O3S_Xerr_dcjma_sm6, Y = Calc_average_profile_pressure([profEN0505, profEN1001, profSP1010, profSP1001],
#                                                                                'PO3_deconv_jma_sm6')

avgprof_OPM_X, avgprof_OPM_Xerr, Y = Calc_average_profile_pressure([profEN0505, profEN1001, profSP1010, profSP1001],
                                                                   'PO3_OPM')

dimension = len(Y)

adif, adiferr, rdif, rdiferr = Calc_Dif(avgprof_O3S_X, avgprof_OPM_X, avgprof_O3S_Xerr, dimension)

adiftest, adiferrtest, rdiftest, rdiferrtest = Calc_Dif(avgprof_O3S_X, avgprof_OPM_X, Aavgprof_O3S_Xerr, dimension)


print(rdif[0])
print(rdiferr[0])


### Plotting
axtitle = 'Sonde - OPM  Difference (mPa)'
rxtitle = 'Sonde - OPM  Difference (%)'

labellist = ['EN 0.5%-0.5B','EN 1.0%-0.1B', 'SP 1.0%-1.0B', 'SP 1.0%-0.1B']
o3list = [totO3_EN0505, totO3_EN1001, totO3_SP1010,  totO3_SP1001]
dfnplist = [profEN0505.drop_duplicates(['Sim', 'Team']), profEN1001.drop_duplicates(['Sim', 'Team']),profSP1010_nodup, profSP1001_nodup]

errorPlot_ARDif_withtext(adif, adiferr, Y, [-3, 3], [1000,5],  '2017 Data',  axtitle, ytitle, labellist, o3list, dfnplist,
                           'ADif_Pair_2017_one', folderpath ,  True, False)

errorPlot_ARDif_withtext(Aavgprof_O3S_X, Aavgprof_O3S_Xerr, Y, [-3, 3], [1000,5],  '2017 Data',  axtitle, ytitle, labellist, o3list, dfnplist,
                           'ADif_Pair_2017_two', folderpath ,  True, False)

errorPlot_ARDif_withtext(rdif, rdiferr, Y, [-10, 10], [1000,5],  'rdif',  rxtitle, ytitle, labellist, o3list, dfnplist,
                           'RDif_Pair_2017_one', folderpath, True, False)


errorPlot_ARDif_withtext(rtest, rtesterr, Y, [-10, 10], [1000,5],  ' rtest two ',  rxtitle, ytitle, labellist, o3list, dfnplist,
                           'RDif_Pair_2017_two', folderpath, True, False)



errorPlot_ARDif_withtext(rdiftest, rdiferrtest, Y, [-10, 10], [1000,5],  'rdif a',  rxtitle, ytitle, labellist, o3list, dfnplist,
                           'RDif_Pair_2017_a', folderpath, True, False)