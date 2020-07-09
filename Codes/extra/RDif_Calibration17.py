## 2017 branch

#!/usr/bin/env python
# coding: utf-8
# Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from Josie_Functions import  Calc_average_profile_pressure, Calc_average_profile_time, Calc_Dif, Calc_average_profileCurrent_pressure, Calc_average_profileCurrent_time
from Josie_PlotFunctions import  errorPlot_ARDif_withtext, errorPlot_general

folderpath = 'Dif_2017_HV'

df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconvHV.csv", low_memory=False)
# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_test.csv", low_memory=False)

df = df.drop(df[(df.PO3 < 0)].index)
df = df.drop(df[(df.PO3_OPM < 0)].index)

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


df['CurMinBkg'] = df['IM'] - df['Header_IB1']
df['I_fast_deconvMinBkg'] = df['I_fast_deconv'] - df['Header_IB1']

ytitle = 'Pressure (hPa)'
ytitlet = 'Time (sec.)'


###############################################


filtEN = df.ENSCI == 1
filtSP = df.ENSCI == 0

filtS10 = df.Sol == 1
filtS05 = df.Sol == 0.5

filtB10 = df.Buf == 1.0
filtB05 = df.Buf == 0.5
filtB01 = df.Buf == 0.1

filterEN0505 = (filtEN & filtS05 & filtB05)
# & (df.Sim == 184) & (df.Team == 8))
filterEN1010 = (filtEN & filtS10 & filtB10)
filterEN1001 = (filtEN & filtS10 & filtB01)

profEN0505 = df.loc[filterEN0505]
profEN1010 = df.loc[filterEN1010]
profEN1001 = df.loc[filterEN1001]

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

profSP1010 = df.loc[filterSP1010]
profSP0505 = df.loc[filterSP0505]
profSP1001 = df.loc[filterSP1001]

profSP1010_nodup = profSP1010.drop_duplicates(['Sim', 'Team'])
profSP0505_nodup = profSP0505.drop_duplicates(['Sim', 'Team'])
profSP1001_nodup = profSP1001.drop_duplicates(['Sim', 'Team'])

totO3_SP1010 = profSP1010_nodup.frac.mean()
totO3_SP0505 = profSP0505_nodup.frac.mean()
totO3_SP1001 = profSP1001_nodup.frac.mean()


labellist = ['EN 0.5%-0.5B','EN 1.0%-0.1B', 'SP 1.0%-0.1B', 'SP 1.0%-1.0B' ]

# labellist = ['EN 0.5%-0.5B','EN 1.0%-1.0B', 'SP 0.5%-0.5B', 'SP 1.0%-1.0B'] 2017
o3list = [totO3_EN0505, totO3_EN1001,  totO3_SP1001, totO3_SP1010]
dfnplist = [profEN0505.drop_duplicates(['Sim', 'Team']), profEN1001.drop_duplicates(['Sim', 'Team']), profSP1001_nodup,
            profSP1010_nodup]


# ##################################################################################
# ################      All profiles CURRENT IM PLOTS        #################################
# ##################################################################################

avgprofAll_O3S_cur, avgprofAll_O3S_curerr, Ycur = Calc_average_profileCurrent_pressure([df],
                                                                   'IM')
avgprofAll_O3S_cur_dcsm12, avgprofAll_O3S_curerr_dcsm12, Y = Calc_average_profileCurrent_pressure([df],
                                                                         'I_fast_deconv_sm12')
avgprofAll_OPM_cur, avgprofAll_OPM_curerr, Y = Calc_average_profileCurrent_pressure([df],
                                                                   'I_OPM_jma')
avgprofAll_O3S_cur_dcmib0sm12, avgprofAll_O3S_curerr_dcmib0sm12, Y = Calc_average_profileCurrent_pressure([df],
                                                                         'Ifast_minib0_deconv_sm12')

dimension = len(Y)

# adifcurAll, adifcurAllerr, rdifcurAll, rdifcurAllerr = Calc_Dif(avgprofAll_O3S_cur, avgprofAll_OPM_cur, avgprofAll_O3S_curerr, dimension)
# adifcurAll_dcsm12, adifcurAllerr_dcsm12, rdifcurAll_dcsm12, rdifcurAllerr_dc_sm12 = \
#     Calc_Dif(avgprofAll_O3S_cur_dcsm12, avgprofAll_OPM_cur, avgprofAll_O3S_curerr_dcsm12, dimension)
# adifcurAll_dcmib0sm12, adifcurAllerr_dcmib0sm12, rdifcurAll_dcmib0sm12, rdifcurAllerr_dcmib0sm12 = \
#     Calc_Dif(avgprofAll_O3S_cur_dcmib0sm12, avgprofAll_OPM_cur, avgprofAll_O3S_curerr_dcmib0sm12, dimension)

adifcurAll, adifcurAllerr, rdifcurAll, rdifcurAllerr = Calc_Dif(avgprofAll_O3S_cur, avgprofAll_OPM_cur, avgprofAll_O3S_curerr, dimension)
adifcurAll_dcsm12, adifcurAllerr_dcsm12, rdifcurAll_dcsm12, rdifcurAllerr_dc_sm12 = \
    Calc_Dif(avgprofAll_O3S_cur_dcsm12, avgprofAll_OPM_cur, avgprofAll_O3S_curerr_dcsm12, dimension)
adifcurAll_dcmib0sm12, adifcurAllerr_dcmib0sm12, rdifcurAll_dcmib0sm12, rdifcurAllerr_dcmib0sm12 = \
    Calc_Dif(avgprofAll_O3S_cur_dcmib0sm12, avgprofAll_OPM_cur, avgprofAll_O3S_curerr_dcmib0sm12, dimension)

rdif = np.concatenate([rdifcurAll, rdifcurAll_dcsm12, rdifcurAll_dcmib0sm12])
rdif_err = np.concatenate([rdifcurAllerr, rdifcurAllerr_dc_sm12, rdifcurAllerr_dcmib0sm12])

labellistAll = ['Standard', 'Deconvoluted', 'Deconvoluted min iB0']

axtitlecur = r'Sonde - OPM[JMA]  Difference ($\mu$A)'
rxtitle = 'Sonde - OPM[JMA]  Difference (%)'

ndlist = [df.drop_duplicates(['Sim', 'Team']), df.drop_duplicates(['Sim', 'Team']), df.drop_duplicates(['Sim', 'Team'])]

errorPlot_ARDif_withtext(rdif, rdif_err, Y, [-40, 40], [1000,5],  '2017 Data ',  rxtitle,
                         ytitle, labellistAll, o3list, ndlist, 'AllRDif_Pair_2017_Convoluted ', folderpath, True, False)

# ##################################################################################
# ################      CURRENT IM PLOTS        #################################
# ##################################################################################
#
# # df['CurMinBkg'] = df['IM'] - df['Header_IB1']
# # df['I_fast_deconvMinBkg'] = df['I_fast_deconv'] - df['Header_IB1']
# ##  asaf pressure
#
avgprof_O3S_cur, avgprof_O3S_curerr, Ycur = Calc_average_profileCurrent_pressure([profEN0505, profEN1001, profSP1001, profSP1010],
                                                                   'IM')
# avgprof_O3S_curSlow, avgprof_O3S_curSlowerr, Yslow = Calc_average_profileCurrent_pressure([profEN0505, profEN1001, profSP1001, profSP1010],
#                                                                    'I_slow_conv')
# avgprof_O3S_cur_dc, avgprof_O3S_curerr_dc, Y = Calc_average_profileCurrent_pressure([profEN0505, profEN1001, profSP1001, profSP1010],
#                                                                          'I_fast_deconv')

# avgprof_O3S_cur_fast, avgprof_O3S_curerr_fast, Y = Calc_average_profileCurrent_pressure([profEN0505, profEN1001, profSP1001, profSP1010],
#                                                                          'I_fast')
#
# avgprof_O3S_cur_dc_sm6, avgprof_O3S_curerr_dc_sm6, Y = Calc_average_profileCurrent_pressure([profEN0505, profEN1001, profSP1001, profSP1010],
#                                                                          'I_fast_deconv_sm6')
avgprof_O3S_cur_dc_sm12, avgprof_O3S_curerr_dc_sm12, Y = Calc_average_profileCurrent_pressure([profEN0505, profEN1001, profSP1001, profSP1010],
                                                                         'I_fast_deconv_sm12')
# avgprof_O3S_cur_dc_sm18, avgprof_O3S_curerr_dc_sm18, Y = Calc_average_profileCurrent_pressure([profEN0505, profEN1001, profSP1001, profSP1010],
#                                                                          'I_fast_deconv_sm18')
avgprof_OPM_cur, avgprof_OPM_curerr, Y = Calc_average_profileCurrent_pressure([profEN0505, profEN1001, profSP1001, profSP1010],
                                                                   'I_OPM_jma')

## fast minus ib0 plots
# avgprof_O3S_cur_mib0, avgprof_O3S_curerr_mib0, Y = Calc_average_profileCurrent_pressure([profEN0505, profEN1001, profSP1001, profSP1010],
#                                                                          'Ifast_minib0')
# avgprof_O3S_cur_dcmib0, avgprof_O3S_curerr_dcmib0, Y = Calc_average_profileCurrent_pressure([profEN0505, profEN1001, profSP1001, profSP1010],
#                                                                          'Ifast_minib0_deconv')
# avgprof_O3S_cur_dcmib0_sm6, avgprof_O3S_curerr_dcmib0_sm6, Y = Calc_average_profileCurrent_pressure([profEN0505, profEN1001, profSP1001, profSP1010],
#                                                                          'Ifast_minib0_deconv_sm6')
avgprof_O3S_cur_dcmib0_sm12, avgprof_O3S_curerr_dcmib0_sm12, Y = Calc_average_profileCurrent_pressure([profEN0505, profEN1001, profSP1001, profSP1010],
                                                                         'Ifast_minib0_deconv_sm12')
# avgprof_O3S_cur_dcmib0_sm18, avgprof_O3S_curerr_dcmib0_sm18, Y = Calc_average_profileCurrent_pressure([profEN0505, profEN1001, profSP1001, profSP1010],
#                                                                          'Ifast_minib0_deconv_sm18')


# dimension = len(Y)
#
adifcur, adifcurerr, rdifcur, rdifcurerr = Calc_Dif(avgprof_O3S_cur, avgprof_OPM_cur, avgprof_O3S_curerr, dimension)
# adifcur_dc, adifcurerr_dc, rdifcur_dc, rdifcurerr_dc = Calc_Dif(avgprof_O3S_cur_dc, avgprof_OPM_cur, avgprof_O3S_curerr_dc, dimension)
# adifcur_dc_sm6, adifcurerr_dc_sm6, rdifcur_dc_sm6, rdifcurerr_dc_sm6 = Calc_Dif(avgprof_O3S_cur_dc_sm6, avgprof_OPM_cur, avgprof_O3S_curerr_dc_sm6, dimension)
adifcur_dc_sm12, adifcurerr_dc_sm12, rdifcur_dc_sm12, rdifcurerr_dc_sm12 = Calc_Dif(avgprof_O3S_cur_dc_sm12, avgprof_OPM_cur, avgprof_O3S_curerr_dc_sm12, dimension)
# adifcur_dc_sm18, adifcurerr_dc_sm18, rdifcur_dc_sm18, rdifcurerr_dc_sm18 = Calc_Dif(avgprof_O3S_cur_dc_sm18, avgprof_OPM_cur, avgprof_O3S_curerr_dc_sm18, dimension)

# adifcur_mib0, adifcurerr_mib0, rdifcur_mib0, rdifcurerr_mib0 = Calc_Dif(avgprof_O3S_cur_mib0, avgprof_OPM_cur, avgprof_O3S_curerr_mib0, dimension)
# adifcur_dcmib0, adifcurerr_dcmib0, rdifcur_dcmib0, rdifcurerr_dcmib0 = Calc_Dif(avgprof_O3S_cur_dcmib0, avgprof_OPM_cur, avgprof_O3S_curerr_dcmib0, dimension)
# adifcur_dcmib0_sm6, adifcurerr_dcmib0_sm6, rdifcur_dcmib0_sm6, rdifcurerr_dcmib0_sm6 = Calc_Dif(avgprof_O3S_cur_dcmib0_sm6, avgprof_OPM_cur, avgprof_O3S_curerr_dcmib0_sm6, dimension)
adifcur_dcmib0_sm12, adifcurerr_dcmib0_sm12, rdifcur_dcmib0_sm12, rdifcurerr_dcmib0_sm12 = Calc_Dif(avgprof_O3S_cur_dcmib0_sm12, avgprof_OPM_cur, avgprof_O3S_curerr_dcmib0_sm12, dimension)
# adifcur_dcmib0_sm18, adifcurerr_dcmib0_sm18, rdifcur_dcmib0_sm18, rdifcurerr_dcmib0_sm18 = Calc_Dif(avgprof_O3S_cur_dcmib0_sm18, avgprof_OPM_cur, avgprof_O3S_curerr_dcmib0_sm18, dimension)
#
# adifcurf, adifcurerrf, rdifcurf, rdifcurerrf = Calc_Dif(avgprof_O3S_cur_fast, avgprof_OPM_cur, avgprof_O3S_curerr_fast, dimension)

#
# ### Plotting

axtitlecur = r'Sonde - OPM[JMA]  Difference ($\mu$A)'
rxtitle = 'Sonde - OPM[JMA]  Difference (%)'

# ## plotting fast component only
# errorPlot_ARDif_withtext(adifcurf, adifcurerrf, Y, [-3, 3], [1000,5],  '2017 Data (Current, I fast)',  axtitlecur, ytitle, labellist, o3list, dfnplist,
#                            'Currentmib0_fast_ADif_Pair_2017', folderpath ,  True, False)
# errorPlot_ARDif_withtext(rdifcurf, rdifcurerrf, Y, [-40, 40], [1000,5],  '2017 Data (Current, I fast)',  rxtitle, ytitle, labellist, o3list, dfnplist,
#                            'Currentmib0_fast_RDif_Pair_2017', folderpath, True, False)

## min ob0 plots
#
# errorPlot_ARDif_withtext(adifcur_mib0, adifcurerr_mib0, Y, [-3, 3], [1000,5],  '2017 Data (Current, I fast minus iB0)',  axtitlecur, ytitle, labellist, o3list, dfnplist,
#                            'Currentmib0_ADif_Pair_2017', folderpath ,  True, False)
# errorPlot_ARDif_withtext(rdifcur_mib0, rdifcurerr_mib0, Y, [-40, 40], [1000,5],  '2017 Data (Current, I fast minus iB0)',  rxtitle, ytitle, labellist, o3list, dfnplist,
#                            'Currentmib0_RDif_Pair_2017', folderpath, True, False)

# errorPlot_ARDif_withtext(adifcur_dcmib0, adifcurerr_dcmib0, Y, [-3, 3], [1000,5],  '2017 Data  Conv-Deconv (Current, minus iB0)',  axtitlecur, ytitle, labellist, o3list, dfnplist,
#                            'Currentmib0_ADif_Pair_2017_Convoluted', folderpath ,  True, False)
# errorPlot_ARDif_withtext(rdifcur_dcmib0, rdifcurerr_dcmib0, Y, [-40, 40], [1000,5],  '2017 Data  Conv-Deconv (Current, minus iB0)',  rxtitle, ytitle, labellist, o3list, dfnplist,
#                            'Currentmib0_RDif_Pair_2017_Convoluted', folderpath, True, False)

# errorPlot_ARDif_withtext(adifcur_dcmib0_sm6, adifcurerr_dcmib0_sm6, Y, [-3, 3], [1000,5],  '2017 Data  Conv-Deconv (Current, minus iB0 smoothed 6 secs)',  axtitlecur, ytitle, labellist, o3list, dfnplist,
#                            'Currentmib0_ADif_Pair_2017_Convoluted_smoothed6', folderpath ,  True, False)
# errorPlot_ARDif_withtext(rdifcur_dcmib0_sm6, rdifcurerr_dcmib0_sm6, Y, [-40, 40], [1000,5],  '2017 Data  Conv-Deconv (Current, minus iB0 smoothed 6 secs)',  rxtitle, ytitle, labellist, o3list, dfnplist,
#                            'Currentmib0_RDif_Pair_2017_Convoluted_smoothed6', folderpath, True, False)
#
# errorPlot_ARDif_withtext(adifcur_dcmib0_sm12, adifcurerr_dcmib0_sm12, Y, [-3, 3], [1000,5],  '2017 Data  Conv-Deconv (Current, minus iB0 smoothed 12 secs)',  axtitlecur, ytitle, labellist, o3list, dfnplist,
#                            'Currentmib0_ADif_Pair_2017_Convoluted_smoothed12', folderpath ,  True, False)
errorPlot_ARDif_withtext(rdifcur_dcmib0_sm12, rdifcurerr_dcmib0_sm12, Y, [-40, 40], [1000,5],  '2017 Data  Conv-Deconv (Current, minus iB0 smoothed 12 secs)',  rxtitle, ytitle, labellist, o3list, dfnplist,
                           'Currentmib0_RDif_Pair_2017_Convoluted_smoothed12', folderpath, True, False)
#
# errorPlot_ARDif_withtext(adifcur_dcmib0_sm18, adifcurerr_dcmib0_sm18, Y, [-3, 3], [1000,5],  '2017 Data  Conv-Deconv (Current, minus iB0 smoothed 18 secs)',  axtitlecur, ytitle, labellist, o3list, dfnplist,
#                            'Currentmib0_ADif_Pair_2017_Convoluted_smoothed18', folderpath ,  True, False)
# errorPlot_ARDif_withtext(rdifcur_dcmib0_sm18, rdifcurerr_dcmib0_sm18, Y, [-40, 40], [1000,5],  '2017 Data  Conv-Deconv (Current, minus iB0 smoothed 18 secs)',  rxtitle, ytitle, labellist, o3list, dfnplist,
#                            'Currentmib0_RDif_Pair_2017_Convoluted_smoothed18', folderpath, True, False)


# errorPlot_ARDif_withtext(adifcur, adifcurerr, Y, [-3, 3], [1000,5],  '2017 Data (Current)',  axtitlecur, ytitle, labellist, o3list, dfnplist,
#                            'Current_ADif_Pair_2017', folderpath ,  True, False)
#
# errorPlot_ARDif_withtext(rdifcur, rdifcurerr, Y, [-40, 40], [1000,5],  '2017 Data (Current)',  rxtitle, ytitle, labellist, o3list, dfnplist,
#                            'Current_RDif_Pair_2017', folderpath, True, False)

## convoluted ones

# errorPlot_ARDif_withtext(adifcur_dc, adifcurerr_dc, Y, [-3, 3], [1000,5],  '2017 Data Conv-Deconv (Current )',  axtitlecur, ytitle,
#                          labellist, o3list, dfnplist,
#                            'Current_ADif_Pair_Convoluted_2017', folderpath ,  True, False)
#
# errorPlot_ARDif_withtext(rdifcur_dc, rdifcurerr_dc, Y, [-40, 40], [1000,5],  '2017 Data Conv-Deconv (Current)',  rxtitle, ytitle,
#                          labellist, o3list, dfnplist,
#                            'Current_RDif_Pair_Convoluted_2017', folderpath, True, False)

# ## convoluted ones sm6
# errorPlot_ARDif_withtext(adifcur_dc_sm6, adifcurerr_dc_sm6, Y, [-3, 3], [1000,5],  '2017 Data Conv-Deconv (Current Smoothed 6 secs)',  axtitlecur, ytitle,
#                          labellist, o3list, dfnplist,
#                            'Current_ADif_Pair_Convoluted_2017_smoothed6', folderpath ,  True, False)
# errorPlot_ARDif_withtext(rdifcur_dc_sm6, rdifcurerr_dc_sm6, Y, [-40, 40], [1000,5],  '2017 Data Conv-Deconv (Current Smoothed 6 secs)',  rxtitle, ytitle,
#                          labellist, o3list, dfnplist,
#                            'Current_RDif_Pair_Convoluted_2017_smoothed6', folderpath, True, False)
#
# ## convoluted ones sm12
# errorPlot_ARDif_withtext(adifcur_dc_sm12, adifcurerr_dc_sm12, Y, [-3, 3], [1000,5],  '2017 Data Conv-Deconv (Current Smoothed 12 secs)',  axtitlecur, ytitle,
#                          labellist, o3list, dfnplist,
#                            'Current_ADif_Pair_Convoluted_2017_smoothed12', folderpath ,  True, False)
errorPlot_ARDif_withtext(rdifcur_dc_sm12, rdifcurerr_dc_sm12, Y, [-40, 40], [1000,5],  '2017 Data Conv-Deconv (Current Smoothed 12 secs)',  rxtitle, ytitle,
                         labellist, o3list, dfnplist,
                           'Current_RDif_Pair_Convoluted_2017_smoothed12', folderpath, True, False)

# ## convoluted ones sm18
# errorPlot_ARDif_withtext(adifcur_dc_sm18, adifcurerr_dc_sm18, Y, [-3, 3], [1000,5],  '2017 Data Conv-Deconv (Current Smoothed 18 secs)',  axtitlecur, ytitle,
#                          labellist, o3list, dfnplist,
#                            'Current_ADif_Pair_Convoluted_2017_smoothed18', folderpath ,  True, False)
# errorPlot_ARDif_withtext(rdifcur_dc_sm18, rdifcurerr_dc_sm18, Y, [-40, 40], [1000,5],  '2017 Data Conv-Deconv (Current Smoothed 18 secs)',  rxtitle, ytitle,
#                          labellist, o3list, dfnplist,
#                            'Current_RDif_Pair_Convoluted_2017_smoothed18', folderpath, True, False)
# #
# #
# # ##  asaf time
# #
# # ## order of the lists [en0505, en1010, sp0505, sp1010]
# avgprof_O3S_curT, avgprof_O3S_curTerr, Yt = Calc_average_profileCurrent_time([profEN0505, profEN1001, profSP1001, profSP1010],
#                                                                    'IM', resolution, tmin, tmax)
# avgprof_O3S_curSlowT, avgprof_O3S_curSlowTerr, Yt = Calc_average_profileCurrent_time([profEN0505, profEN1001, profSP1001, profSP1010],
#                                                                    'I_slow_conv', resolution, tmin, tmax)
# avgprof_O3S_curT_dc, avgprof_O3S_curTerr_dc, Yt = Calc_average_profileCurrent_time([profEN0505, profEN1001, profSP1001, profSP1010],
#                                                                          'I_fast_deconv', resolution, tmin, tmax)
# avgprof_O3S_curT_dc_sm6, avgprof_O3S_curTerr_dc_sm6, Yt = Calc_average_profileCurrent_time([profEN0505, profEN1001, profSP1001, profSP1010],
#                                                                          'I_fast_deconv_sm6', resolution, tmin, tmax)
# avgprof_O3S_curT_dc_sm12, avgprof_O3S_curTerr_dc_sm12, Yt = Calc_average_profileCurrent_time([profEN0505, profEN1001, profSP1001, profSP1010],
#                                                                          'I_fast_deconv_sm12', resolution, tmin, tmax)
# avgprof_O3S_curT_dc_sm18, avgprof_O3S_curTerr_dc_sm18, Yt = Calc_average_profileCurrent_time([profEN0505, profEN1001, profSP1001, profSP1010],
#                                                                          'I_fast_deconv_sm18', resolution, tmin, tmax)
# avgprof_OPM_curT, avgprof_OPM_curTerr, Yt = Calc_average_profileCurrent_time([profEN0505, profEN1001, profSP1001, profSP1010],
#                                                                    'I_OPM_jma', resolution, tmin, tmax )
# #
# dimension = len(Yt)
#
# adifcurT, adifcurTerr, rdifcurT, rdifcurTerr = Calc_Dif(avgprof_O3S_curT, avgprof_OPM_curT, avgprof_O3S_curTerr, dimension)
# adifcurT_dc, adifcurTerr_dc, rdifcurT_dc, rdifcurTerr_dc = Calc_Dif(avgprof_O3S_curT_dc, avgprof_OPM_curT, avgprof_O3S_curTerr_dc, dimension)
# adifcurT_dc_sm6, adifcurTerr_dc_sm6, rdifcurT_dc_sm6, rdifcurTerr_dc_sm6 = Calc_Dif(avgprof_O3S_curT_dc_sm6, avgprof_OPM_curT, avgprof_O3S_curTerr_dc_sm6, dimension)
# adifcurT_dc_sm12, adifcurTerr_dc_sm12, rdifcurT_dc_sm12, rdifcurTerr_dc_sm12 = Calc_Dif(avgprof_O3S_curT_dc_sm12, avgprof_OPM_curT, avgprof_O3S_curTerr_dc_sm12, dimension)
# adifcurT_dc_sm18, adifcurTerr_dc_sm18, rdifcurT_dc_sm18, rdifcurTerr_dc_sm18 = Calc_Dif(avgprof_O3S_curT_dc_sm18, avgprof_OPM_curT, avgprof_O3S_curTerr_dc_sm18, dimension)
#
# #
# # ### Plotting
# axtitle = 'Sonde - OPM  Difference (mPa)'
# rxtitle = 'Sonde - OPM  Difference (%)'
#
# errorPlot_ARDif_withtext(adifcurT, adifcurTerr, Yt, [-3, 3], [0, 9000],  '2017 Data (Current)',  axtitlecur, ytitlet, labellist, o3list, dfnplist,
#                            'Current_ADif_TSim_2017_', folderpath ,  False, False)
# errorPlot_ARDif_withtext(rdifcurT, rdifcurTerr, Yt, [-40, 40], [0, 9000],  '2017 Data (Current)',  rxtitle, ytitlet, labellist, o3list, dfnplist,
#                            'Current_RDif_TSim_2017', folderpath, False, False)
# #
# # ## convoluted ones
# errorPlot_ARDif_withtext(adifcurT_dc, adifcurTerr_dc, Yt, [-3, 3], [0, 9000],  '2017 Data Conv-Deconv (Current) ',  axtitlecur, ytitlet,
#                          labellist, o3list, dfnplist,
#                            'Current_ADif_TSim_Convoluted_2017', folderpath ,  False, False)
# errorPlot_ARDif_withtext(rdifcurT_dc, rdifcurTerr_dc, Yt, [-40, 40], [0, 9000],  '2017 Data Conv-Deconv (Current)',  rxtitle, ytitlet,
#                          labellist, o3list, dfnplist,
#                            'Current_RDif_TSim_Convoluted_2017', folderpath, False, False)
# # ## convoluted ones sm6
# errorPlot_ARDif_withtext(adifcurT_dc_sm6, adifcurTerr_dc_sm6, Yt, [-3, 3], [0, 9000],  '2017 Data Conv-Deconv (Current Smoothed 6 secs) ',  axtitlecur, ytitlet,
#                          labellist, o3list, dfnplist,
#                            'Current_ADif_TSim_Convoluted_2017_smoothed6', folderpath ,  False, False)
# errorPlot_ARDif_withtext(rdifcurT_dc_sm6, rdifcurTerr_dc_sm6, Yt, [-40, 40], [0, 9000],  '2017 Data Conv-Deconv (Current Smoothed 6 secs)',  rxtitle, ytitlet,
#                          labellist, o3list, dfnplist,
#                            'Current_RDif_TSim_Convoluted_2017_smoothed6', folderpath, False, False)
# # ## convoluted ones sm12
# errorPlot_ARDif_withtext(adifcurT_dc_sm12, adifcurTerr_dc_sm12, Yt, [-3, 3], [0, 9000],  '2017 Data Conv-Deconv (Current Smoothed 12 secs) ',  axtitlecur, ytitlet,
#                          labellist, o3list, dfnplist,
#                            'Current_ADif_TSim_Convoluted_2017_smoothed12', folderpath ,  False, False)
# errorPlot_ARDif_withtext(rdifcurT_dc_sm12, rdifcurTerr_dc_sm12, Yt, [-40, 40], [0, 9000],  '2017 Data Conv-Deconv (Current Smoothed 12 secs)',  rxtitle, ytitlet,
#                          labellist, o3list, dfnplist,
#                            'Current_RDif_TSim_Convoluted_2017_smoothed12', folderpath, False, False)
# # ## convoluted ones sm18
# errorPlot_ARDif_withtext(adifcurT_dc_sm18, adifcurTerr_dc_sm18, Yt, [-3, 3], [0, 9000],  '2017 Data Conv-Deconv (Current Smoothed 18 secs) ',  axtitlecur, ytitlet,
#                          labellist, o3list, dfnplist,
#                            'Current_ADif_TSim_Convoluted_2017_smoothed18', folderpath ,  False, False)
# errorPlot_ARDif_withtext(rdifcurT_dc_sm18, rdifcurTerr_dc_sm18, Yt, [-40, 40], [0, 9000],  '2017 Data Conv-Deconv (Current Smoothed 18 secs)',  rxtitle, ytitlet,
#                          labellist, o3list, dfnplist,
#                            'Current_RDif_TSim_Convoluted_2017_smoothed18', folderpath, False, False)

#####  final plot for relative contribution of I_slow to the total current asaf of pressure
#
# print('check', len(avgprof_O3S_curSlow[0]), len(avgprof_O3S_cur[0]))
# print(len(Ycur), len(Yslow))
# dimension = len(Yslow)
#
# print('avgprof_O3S_curSlow', avgprof_O3S_curSlow[0])
# print('avgprof_O3S_cur', avgprof_O3S_cur[0])
#
# adifcurSlow = [ (i - j)/i for i in avgprof_O3S_cur[0] for j in avgprof_O3S_curSlow[0] ]
#
# print('one adifcurSlow', adifcurSlow[0])
#
# adifcurSlow, adifcurSlowerr, rdifcurSlow, rdifcurSlowerr = Calc_Dif(avgprof_O3S_curSlow, avgprof_O3S_cur, avgprof_O3S_curSlowerr, dimension)
#
# print('adifcurSlow', adifcurSlow[0])
# print('rdifcurSlow', rdifcurSlow[0])
#
# for k in range(4):
#     for s in range(len(rdifcurSlow[k])):
#         rdifcurSlow[k][s] = avgprof_O3S_curSlow[k][s]/ avgprof_O3S_cur[k][s] * 100
#
# print('rdifcurSlow two', rdifcurSlow[0])
#
# errorPlot_ARDif_withtext(adifcurSlow, adifcurSlowerr, Yslow, [-3, 3], [1000,5],  '2017 Data',  axtitle, ytitle, labellist, o3list, dfnplist,
#                            'I_Slow_Contribution_ADif_Pair_2017', folderpath ,  True, False)
#
# errorPlot_ARDif_withtext(rdifcurSlow, rdifcurSlowerr, Yslow, [-20, 20], [1000,5],  '2017 Data',  r'I$_{slow}$conv./I$_{ECC}$ (%)', ytitle, labellist, o3list, dfnplist,
#                            'I_Slow_Contribution_RDif_Pair_2017', folderpath, True, False)
#
# #####  final plot for relative contribution of I_slow to the total current asaf of time
# dimension = len(Yt)
#
#
# adifcurSlowT, adifcurSlowTerr, rdifcurSlowT, rdifcurSlowTerr = Calc_Dif(avgprof_O3S_curSlowT, avgprof_O3S_curT, avgprof_O3S_curSlowTerr, dimension)
#
# for kk in range(4):
#     for ss in range(len(rdifcurSlow[kk])):
#         rdifcurSlowT[kk][ss] = avgprof_O3S_curSlowT[kk][ss]/ avgprof_O3S_curT[kk][ss] * 100
#
# errorPlot_ARDif_withtext(adifcurSlowT, adifcurSlowTerr, Yt, [-3, 3], [0, 9000],  '2017 Data',  axtitle, ytitlet, labellist, o3list, dfnplist,
#                            'I_Slow_Contribution_ADif_TSim_2017', folderpath ,  False, False)
#
# errorPlot_ARDif_withtext(rdifcurSlowT, rdifcurSlowTerr, Yt, [-20, 20], [0, 9000],  '2017 Data',    r'I$_{slow}$conv./I$_{ECC}$ (%)', ytitlet, labellist, o3list, dfnplist,
#                            'I_Slow_Contribution_RDif_TSim_2017', folderpath, False, False)


##################################################################################
################     Pressure PO3 PLOTS        #################################
##################################################################################

#
# ## order of the lists [en0505, en1010, sp0505, sp1010]
# avgprof_O3S_X, avgprof_O3S_Xerr, Y = Calc_average_profile_pressure([profEN0505, profEN1001, profSP1001, profSP1010],
#                                                                    'PO3')
# avgprof_O3S_X_dc, avgprof_O3S_Xerr_dc, Y = Calc_average_profile_pressure([profEN0505, profEN1001, profSP1001, profSP1010],
#                                                                          'PO3_deconv')
# avgprof_O3S_X_dc_sm6, avgprof_O3S_Xerr_dc_sm6, Y = Calc_average_profile_pressure([profEN0505, profEN1001, profSP1001, profSP1010],
#                                                                          'PO3_deconv_sm6')
# avgprof_O3S_X_dc_sm12, avgprof_O3S_Xerr_dc_sm12, Y = Calc_average_profile_pressure([profEN0505, profEN1001, profSP1001, profSP1010],
#                                                                          'PO3_deconv_sm12')
# avgprof_O3S_X_dcjma, avgprof_O3S_Xerr_dcjma, Y = Calc_average_profile_pressure([profEN0505, profEN1001, profSP1001, profSP1010],
#                                                                                'PO3_deconv_jma')
# avgprof_O3S_X_dcjma_sm6, avgprof_O3S_Xerr_dcjma_sm6, Y = Calc_average_profile_pressure([profEN0505, profEN1001, profSP1001, profSP1010],
#                                                                                'PO3_deconv_jma_sm6')
# avgprof_O3S_X_dcjma_sm12, avgprof_O3S_Xerr_dcjma_sm12, Y = Calc_average_profile_pressure([profEN0505, profEN1001, profSP1001, profSP1010],
#                                                                                'PO3_deconv_jma_sm12')
#
# avgprof_O3S_X_dcjma_sm18, avgprof_O3S_Xerr_dcjma_sm18, Y = Calc_average_profile_pressure([profEN0505, profEN1001, profSP1001, profSP1010],
#                                                                                'PO3_deconv_jma_sm18')
#
# avgprof_O3S_X_dcjma_smb6, avgprof_O3S_Xerr_dcjma_smb6, Y = Calc_average_profile_pressure([profEN0505, profEN1001, profSP1001, profSP1010],
#                                                                                'PO3_deconv_smb6_jma')
#
# avgprof_O3S_X_dcjma_smb12, avgprof_O3S_Xerr_dcjma_smb12, Y = Calc_average_profile_pressure([profEN0505, profEN1001, profSP1001, profSP1010],
#                                                                                'PO3_deconv_smb12_jma')
#
#
#
# avgprof_OPM_X, avgprof_OPM_Xerr, Y = Calc_average_profile_pressure([profEN0505, profEN1001, profSP1001, profSP1010],
#                                                                    'PO3_OPM')
#
# dimension = len(Y)
# # standard
# adif, adiferr, rdif, rdiferr = Calc_Dif(avgprof_O3S_X, avgprof_OPM_X, avgprof_O3S_Xerr, dimension)
# # deconvoluted
# adif_dc, adiferr_dc, rdif_dc, rdiferr_dc = Calc_Dif(avgprof_O3S_X_dc, avgprof_OPM_X, avgprof_O3S_Xerr_dc, dimension)
# #deconvoluted smoothed
# adif_dc_sm6, adiferr_dc_sm6, rdif_dc_sm6, rdiferr_dc_sm6 = Calc_Dif(avgprof_O3S_X_dc_sm6, avgprof_OPM_X, avgprof_O3S_Xerr_dc_sm6, dimension)
# adif_dc_sm12, adiferr_dc_sm12, rdif_dc_sm12, rdiferr_dc_sm12 = Calc_Dif(avgprof_O3S_X_dc_sm12, avgprof_OPM_X, avgprof_O3S_Xerr_dc_sm12, dimension)
# #deconvoluted jma corrected
# adif_dcjma, adiferr_dcjma, rdif_dcjma, rdiferr_dcjma = Calc_Dif(avgprof_O3S_X_dcjma, avgprof_OPM_X, avgprof_O3S_Xerr_dcjma, dimension)
# #deconvoluted jma corrected smoothed
# adif_dcjma_sm6, adiferr_dcjma_sm6, rdif_dcjma_sm6, rdiferr_dcjma_sm6 = Calc_Dif(avgprof_O3S_X_dcjma_sm6, avgprof_OPM_X,
#                                                                                 avgprof_O3S_Xerr_dcjma_sm6, dimension)
# adif_dcjma_sm12, adiferr_dcjma_sm12, rdif_dcjma_sm12, rdiferr_dcjma_sm12 = Calc_Dif(avgprof_O3S_X_dcjma_sm12, avgprof_OPM_X,
#                                                                                 avgprof_O3S_Xerr_dcjma_sm12, dimension)
# adif_dcjma_sm18, adiferr_dcjma_sm18, rdif_dcjma_sm18, rdiferr_dcjma_sm18 = Calc_Dif(avgprof_O3S_X_dcjma_sm18, avgprof_OPM_X,
#                                                                                 avgprof_O3S_Xerr_dcjma_sm18, dimension)
# #smoothed and then deconvoluted jma corrected
# adif_dcjma_smb6, adiferr_dcjma_smb6, rdif_dcjma_smb6, rdiferr_dcjma_smb6 = Calc_Dif(avgprof_O3S_X_dcjma_smb6, avgprof_OPM_X,
#                                                                                 avgprof_O3S_Xerr_dcjma_smb6, dimension)
# adif_dcjma_smb12, adiferr_dcjma_smb12, rdif_dcjma_smb12, rdiferr_dcjma_smb12 = Calc_Dif(avgprof_O3S_X_dcjma_smb12, avgprof_OPM_X,
#                                                                                 avgprof_O3S_Xerr_dcjma_smb12, dimension)
#
# ### Plotting
# axtitle_nojma = 'Sonde - OPM  Difference (mPa)'
# axtitle = 'Sonde[JMA] - OPM  Difference (mPa)'
#
# rxtitle_nojma = 'Sonde - OPM  Difference (%)'
# rxtitle = 'Sonde[JMA] - OPM  Difference (%)'
#
#
# #
# #standard
# errorPlot_ARDif_withtext(adif, adiferr, Y, [-3, 3], [1000,5],  '2017 Data',  axtitle_nojma, ytitle, labellist, o3list, dfnplist,
#                            'ADif_Pair_2017', folderpath ,  True, False)
#
# errorPlot_ARDif_withtext(rdif, rdiferr, Y, [-40, 40], [1000,5],  '2017 Data',  rxtitle_nojma, ytitle, labellist, o3list, dfnplist,
#                            'RDif_Pair_2017', folderpath, True, False)
#
# ## convoluted ones
#
# errorPlot_ARDif_withtext(adif_dc, adiferr_dc, Y, [-3, 3], [1000,5],  '2017 Data Conv-Deconv ',  axtitle_nojma, ytitle, labellist, o3list, dfnplist,
#                            'ADif_Pair_Convoluted_2017', folderpath ,  True, False)
#
# errorPlot_ARDif_withtext(rdif_dc, rdiferr_dc, Y, [-40, 40], [1000,5],  '2017 Data Conv-Deconv ',  rxtitle_nojma, ytitle, labellist, o3list, dfnplist,
#                            'RDif_Pair_Convoluted_2017', folderpath, True, False)
# ## convoluted jma
# errorPlot_ARDif_withtext(adif_dcjma, adiferr_dcjma, Y, [-3, 3], [1000,5],  '2017 Data Conv-Deconv (PO3 JMA corr.)',  axtitle, ytitle, labellist, o3list, dfnplist,
#                            'ADif_Pair_Convoluted_2017_jma', folderpath ,  True, False)
#
# errorPlot_ARDif_withtext(rdif_dcjma, rdiferr_dcjma, Y, [-40, 40], [1000,5],  '2017 Data Conv-Deconv (PO3 JMA corr.)',  rxtitle, ytitle, labellist, o3list, dfnplist,
#                            'RDif_Pair_Convoluted_2017_jma', folderpath, True, False)
# ## convoluted jma smmothed
# errorPlot_ARDif_withtext(adif_dcjma_sm6, adiferr_dcjma_sm6, Y, [-3, 3], [1000,5],  '2017 Data Conv-Deconv (PO3 JMA Smoothed 6sec.)',  axtitle, ytitle, labellist, o3list, dfnplist,
#                            'ADif_Pair_Convoluted_2017_jmasmoothed6', folderpath ,  True, False)
#
# errorPlot_ARDif_withtext(rdif_dcjma_sm6, rdiferr_dcjma_sm6, Y, [-40, 40], [1000,5],  '2017 Data Conv-Deconv (PO3 JMA Smoothed 6sec.)',  rxtitle, ytitle, labellist, o3list, dfnplist,
#                            'RDif_Pair_Convoluted_2017_jmasmoothed6', folderpath, True, False)
#
# ## convoluted jma smmothed
# errorPlot_ARDif_withtext(adif_dcjma_sm12, adiferr_dcjma_sm12, Y, [-3, 3], [1000,5],  '2017 Data Conv-Deconv (PO3 JMA Smoothed 12sec.)',  axtitle, ytitle, labellist, o3list, dfnplist,
#                            'ADif_Pair_Convoluted_2017_jmasmoothed12', folderpath ,  True, False)
#
# errorPlot_ARDif_withtext(rdif_dcjma_sm12, rdiferr_dcjma_sm12, Y, [-40, 40], [1000,5],  '2017 Data Conv-Deconv (PO3 JMA Smoothed 12sec.)',  rxtitle, ytitle, labellist, o3list, dfnplist,
#                            'RDif_Pair_Convoluted_2017_jmasmoothed12', folderpath, True, False)
#
# errorPlot_ARDif_withtext(adif_dcjma_sm18, adiferr_dcjma_sm18, Y, [-3, 3], [1000,5],  '2017 Data Conv-Deconv (PO3 JMA Smoothed 18sec.)',  axtitle, ytitle, labellist, o3list, dfnplist,
#                            'ADif_Pair_Convoluted_2017_jmasmoothed18', folderpath ,  True, False)
#
# errorPlot_ARDif_withtext(rdif_dcjma_sm18, rdiferr_dcjma_sm18, Y, [-40, 40], [1000,5],  '2017 Data Conv-Deconv (PO3 JMA Smoothed 18sec.)',  rxtitle, ytitle, labellist, o3list, dfnplist,
#                            'RDif_Pair_Convoluted_2017_jmasmoothed18', folderpath, True, False)
#
# ## smoothed then  convoluted jma
# errorPlot_ARDif_withtext(adif_dcjma_smb6, adiferr_dcjma_smb6, Y, [-3, 3], [1000,5],  '2017 Data Conv-Deconv (PO3 JMA Smoothed 6sec.)',  axtitle, ytitle, labellist, o3list, dfnplist,
#                            'ADif_Pair_SmmothedConvoluted_2017_jma6', folderpath ,  True, False)
#
# errorPlot_ARDif_withtext(rdif_dcjma_smb6, rdiferr_dcjma_smb6, Y, [-40, 40], [1000,5],  '2017 Data Conv-Deconv (PO3 JMA Smoothed 6sec.)',  rxtitle, ytitle, labellist, o3list, dfnplist,
#                            'RDif_Pair_SmoothedConvoluted_2017_jma6', folderpath, True, False)
#
# errorPlot_ARDif_withtext(adif_dcjma_smb12, adiferr_dcjma_smb12, Y, [-3, 3], [1000,5],  '2017 Data Conv-Deconv (PO3 JMA Smoothed 12sec.)',  axtitle, ytitle, labellist, o3list, dfnplist,
#                            'ADif_Pair_SmmothedConvoluted_2017_jma12', folderpath ,  True, False)
#
# errorPlot_ARDif_withtext(rdif_dcjma_smb12, rdiferr_dcjma_smb12, Y, [-40, 40], [1000,5],  '2017 Data Conv-Deconv (PO3 JMA Smoothed 12sec.)',  rxtitle, ytitle, labellist, o3list, dfnplist,
#                            'RDif_Pair_SmoothedConvoluted_2017_jma12', folderpath, True, False)


#
# # new_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
# # blue, orange, green, red, purple, brown, pinkish, greyish, yellowish, bluish
#
# colorlist = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
#
# checklabel = ['PO3', 'PO3 deconv', 'PO3 deconv smoothed ', 'PO3 deconv jma', 'PO3 deconv jma smoothed']
#
# errorPlot_general([adif[0], adif_dc[0], adif_dc_sm6[0], adif_dcjma[0], adif_dcjma_sm6[0]],
#                   [adiferr[0], adiferr_dc[0], adiferr_dc_sm6[0], adiferr_dcjma[0], adiferr_dcjma_sm6[0]], Y, [-3,3], [1000,5],
#                   '2017 data- ENSCI 0.5%-0.5%B', axtitle, ytitle,
#                   checklabel, colorlist, 'ADif_Check_EN0505', folderpath, 1)
#
# errorPlot_general([rdif[0], rdif_dc[0], rdif_dc_sm6[0], rdif_dcjma[0], rdif_dcjma_sm6[0]],
#                   [rdiferr[0], rdiferr_dc[0], rdiferr_dc_sm6[0], rdiferr_dcjma[0], rdiferr_dcjma_sm6[0]], Y, [-20, 20], [1000,5],
#                   '2017 data- ENSCI 0.5%-0.5%B', rxtitle, ytitle,
#                   checklabel, colorlist, 'RDif_Check_EN0505', folderpath, 1)
#
#
# errorPlot_general([adif[1], adif_dc[1], adif_dc_sm6[1], adif_dcjma[1], adif_dcjma_sm6[1]],
#                   [adiferr[1], adiferr_dc[1], adiferr_dc_sm6[1], adiferr_dcjma[1], adiferr_dcjma_sm6[1]], Y, [-3,3], [1000,5],
#                   '2017 data- ENSCI 1.0%-1.0%B', axtitle, ytitle,
#                   checklabel, colorlist, 'ADif_Check_EN1001', folderpath, 1)
#
# errorPlot_general([rdif[1], rdif_dc[1], rdif_dc_sm6[1], rdif_dcjma[1], rdif_dcjma_sm6[1]],
#                   [rdiferr[1], rdiferr_dc[1], rdiferr_dc_sm6[1], rdiferr_dcjma[1], rdiferr_dcjma_sm6[1]], Y, [-20,20], [1000,5],
#                   '2017 data- ENSCI 1.0%-1.0%B', rxtitle, ytitle,
#                   checklabel, colorlist, 'RDif_Check_EN1001', folderpath, 1)
#
# errorPlot_general([adif[2], adif_dc[2], adif_dc_sm6[2], adif_dcjma[2], adif_dcjma_sm6[2]],
#                   [adiferr[2], adiferr_dc[2], adiferr_dc_sm6[2], adiferr_dcjma[2], adiferr_dcjma_sm6[2]], Y, [-3,3], [1000,5],
#                   '2017 data- SP 0.5%-0.5%B', axtitle, ytitle,
#                   checklabel, colorlist, 'ADif_Check_SP1001', folderpath, 1)
#
# errorPlot_general([rdif[2], rdif_dc[2], rdif_dc_sm6[2], rdif_dcjma[2], rdif_dcjma_sm6[2]],
#                   [rdiferr[2], rdiferr_dc[2], rdiferr_dc_sm6[2], rdiferr_dcjma[2], rdiferr_dcjma_sm6[2]], Y, [-20, 20], [1000,5],
#                   '2017 data- SP 0.5%-0.5%B', rxtitle, ytitle,
#                   checklabel, colorlist, 'RDif_Check_SP1001', folderpath, 1)
#
# errorPlot_general([adif[3], adif_dc[3], adif_dc_sm6[3], adif_dcjma[3], adif_dcjma_sm6[3]],
#                   [adiferr[3], adiferr_dc[3], adiferr_dc_sm6[3], adiferr_dcjma[3], adiferr_dcjma_sm6[3]], Y, [-3,3], [1000,5],
#                   '2017 data- SP 1.0%-1.0%B', axtitle, ytitle,
#                   checklabel, colorlist, 'ADif_Check_SP1010', folderpath, 1)
#
# errorPlot_general([rdif[3], rdif_dc[3], rdif_dc_sm6[3], rdif_dcjma[3], rdif_dcjma_sm6[3]],
#                   [rdiferr[3], rdiferr_dc[3], rdiferr_dc_sm6[3], rdiferr_dcjma[3], rdiferr_dcjma_sm6[3]], Y, [-20, 20], [1000,5],
#                   '2017 data- SP 1.0%-1.0%B', rxtitle, ytitle,
#                   checklabel, colorlist, 'RDif_Check_SP1010', folderpath, 1)
#
# ################################
# ## now do the same asaf of time
# ################################
# resolution = 400
# tmin = 200
# tmax = 8000
# # ## order of the lists [en0505, en1010, sp0505, sp1010]
# avgprof_O3S_T, avgprof_O3S_Terr, Yt = Calc_average_profile_time([profEN0505, profEN1001, profSP1001, profSP1010],
#                                                                    'PO3', resolution, tmin, tmax)
# avgprof_O3S_T_dc, avgprof_O3S_Terr_dc, Yt = Calc_average_profile_time([profEN0505, profEN1001, profSP1001, profSP1010],
#                                                                          'PO3_deconv', resolution, tmin, tmax)
# avgprof_O3S_T_dc_sm6, avgprof_O3S_Terr_dc_sm6, Yt = Calc_average_profile_time([profEN0505, profEN1001, profSP1001, profSP1010],
#                                                                          'PO3_deconv_sm6', resolution, tmin, tmax)
# avgprof_O3S_T_dc_sm12, avgprof_O3S_Terr_dc_sm12, Yt = Calc_average_profile_time([profEN0505, profEN1001, profSP1001, profSP1010],
#                                                                          'PO3_deconv_sm12', resolution, tmin, tmax)
# avgprof_O3S_T_dcjma, avgprof_O3S_Terr_dcjma, Yt = Calc_average_profile_time([profEN0505, profEN1001, profSP1001, profSP1010],
#                                                                          'PO3_deconv_jma', resolution, tmin, tmax)
#
# avgprof_O3S_T_dcjma_sm6, avgprof_O3S_Terr_dcjma_sm6, Yt = Calc_average_profile_time([profEN0505, profEN1001, profSP1001, profSP1010],
#                                                                          'PO3_deconv_jma_sm6', resolution, tmin, tmax)
# avgprof_O3S_T_dcjma_sm12, avgprof_O3S_Terr_dcjma_sm12, Yt = Calc_average_profile_time([profEN0505, profEN1001, profSP1001, profSP1010],
#                                                                          'PO3_deconv_jma_sm12', resolution, tmin, tmax)
# avgprof_O3S_T_dcjma_sm18, avgprof_O3S_Terr_dcjma_sm18, Yt = Calc_average_profile_time([profEN0505, profEN1001, profSP1001, profSP1010],
#                                                                          'PO3_deconv_jma_sm18', resolution, tmin, tmax)
# #
# avgprof_OPM_T, avgprof_OPM_Terr, Yt = Calc_average_profile_time([profEN0505, profEN1001, profSP1001, profSP1010],
#                                                                    'PO3_OPM', resolution, tmin, tmax )
# #
# #
#
# dimension = len(Yt)
# #
# #
# #standard
# adifT, adifTerr, rdifT, rdifTerr = Calc_Dif(avgprof_O3S_T, avgprof_OPM_T, avgprof_O3S_Terr, dimension)
# #deconvoluted
# adifT_dc, adifTerr_dc, rdifT_dc, rdifTerr_dc = Calc_Dif(avgprof_O3S_T_dc, avgprof_OPM_T, avgprof_O3S_Terr_dc, dimension)
# #deconvoluted smoothed
# adifT_dc_sm6, adifTerr_dc_sm6, rdifT_dc_sm6, rdifTerr_dc_sm6 = Calc_Dif(avgprof_O3S_T_dc_sm6, avgprof_OPM_T, avgprof_O3S_Terr_dc_sm6, dimension)
# adifT_dc_sm12, adifTerr_dc_sm12, rdifT_dc_sm12, rdifTerr_dc_sm12 = Calc_Dif(avgprof_O3S_T_dc_sm12, avgprof_OPM_T, avgprof_O3S_Terr_dc_sm12, dimension)
# #deconvoluted jma corrected
# adifT_dcjma, adifTerr_dcjma, rdifT_dcjma, rdifTerr_dcjma = Calc_Dif(avgprof_O3S_T_dcjma, avgprof_OPM_T, avgprof_O3S_Terr_dcjma, dimension)
# #deconvoluted jma corrected smoothed
# adifT_dcjma_sm6, adifTerr_dcjma_sm6, rdifT_dcjma_sm6, rdifTerr_dcjma_sm6 = Calc_Dif(avgprof_O3S_T_dcjma_sm6, avgprof_OPM_T,
#                                                                                 avgprof_O3S_Terr_dcjma_sm6, dimension)
# adifT_dcjma_sm12, adifTerr_dcjma_sm12, rdifT_dcjma_sm12, rdifTerr_dcjma_sm12 = Calc_Dif(avgprof_O3S_T_dcjma_sm12, avgprof_OPM_T,
#                                                                                 avgprof_O3S_Terr_dcjma_sm12, dimension)
#
# adifT_dcjma_sm18, adifTerr_dcjma_sm18, rdifT_dcjma_sm18, rdifTerr_dcjma_sm18 = Calc_Dif(avgprof_O3S_T_dcjma_sm18, avgprof_OPM_T,
#                                                                                 avgprof_O3S_Terr_dcjma_sm18, dimension)
# #
# #
# # ### Plotting
#
# #
# # labellist = ['EN 0.5%-0.5B','EN 1.0%-1.0B', 'SP 0.5%-0.5B', 'SP 1.0%-1.0B']
# # # o3list = [totO3_EN0505, totO3_EN1001,  totO3_SP1001, totO3_SP1010]
# # # dfnplist = [profEN0505.drop_duplicates(['Sim', 'Team']), profEN1001.drop_duplicates(['Sim', 'Team']), profSP1001_nodup,
# # #             profSP1010_nodup]
# # print('test error', len(adifT), len(adifTerr))
# #
# #
# errorPlot_ARDif_withtext(adifT, adifTerr, Yt, [-3, 3], [0, 9000],  '2017 Data',  axtitle_nojma, ytitlet, labellist, o3list, dfnplist,
#                            'ADif_TSim_2017', folderpath ,  False, False)
#
# errorPlot_ARDif_withtext(rdifT, rdifTerr, Yt, [-40, 40], [0, 9000],  '2017 Data',  rxtitle_nojma, ytitlet, labellist, o3list, dfnplist,
#                            'RDif_TSim_2017', folderpath, False, False)
#
# ## convoluted ones
#
# errorPlot_ARDif_withtext(adifT_dc, adifTerr_dc, Yt, [-3, 3], [0, 9000],  '2017 Data Conv-Deconv ',  axtitle_nojma, ytitlet,
#                          labellist, o3list, dfnplist,
#                            'ADif_TSim_Convoluted_2017', folderpath ,  False, False)
#
# errorPlot_ARDif_withtext(rdifT_dc, rdifTerr_dc, Yt, [-40, 40], [0, 9000],  '2017 Data Conv-Deconv ',  rxtitle_nojma, ytitlet,
#                          labellist, o3list, dfnplist,
#                            'RDif_TSim_Convoluted_2017', folderpath, False, False)
# ## convoluted corrected jma
# errorPlot_ARDif_withtext(adifT_dcjma, adifTerr_dcjma, Yt, [-3, 3], [0, 9000],  '2017 Data Conv-Deconv (PO3 JMA corr.)',  axtitle, ytitlet,
#                          labellist, o3list, dfnplist,
#                            'ADif_TSim_Convoluted_2017_jma', folderpath ,  False, False)
#
# errorPlot_ARDif_withtext(rdifT_dcjma, rdifTerr_dcjma, Yt, [-40, 40], [0, 9000],  '2017 Data Conv-Deconv (PO3 JMA corr.)',  rxtitle, ytitlet,
#                          labellist, o3list, dfnplist,
#                            'RDif_TSim_Convoluted_2017_jma', folderpath, False, False)
#
# ## convoluted smmmothed corrected jma 6 seconds
# errorPlot_ARDif_withtext(adifT_dcjma_sm6, adifTerr_dcjma_sm6, Yt, [-3, 3], [0, 9000],  '2017 Data Conv-Deconv (PPO3 JMA Smoothed 6sec.)',  axtitle, ytitlet,
#                          labellist, o3list, dfnplist,
#                            'ADif_TSim_Convoluted_2017_jma_smoothed6', folderpath ,  False, False)
#
# errorPlot_ARDif_withtext(rdifT_dcjma_sm6, rdifTerr_dcjma_sm6, Yt, [-40, 40], [0, 9000],  '2017 Data Conv-Deconv (PO3 JMA Smoothed 6sec.)',  rxtitle, ytitlet,
#                          labellist, o3list, dfnplist,
#                            'RDif_TSim_Convoluted_2017_jma_smoothed6', folderpath, False, False)
# ## convoluted smmmothed corrected jma 12 seconds
# errorPlot_ARDif_withtext(adifT_dcjma_sm12, adifTerr_dcjma_sm12, Yt, [-3, 3], [0, 9000],  '2017 Data Conv-Deconv (PPO3 JMA Smoothed 12sec.)',  axtitle, ytitlet,
#                          labellist, o3list, dfnplist,
#                            'ADif_TSim_Convoluted_2017_jma_smoothed12', folderpath ,  False, False)
#
# errorPlot_ARDif_withtext(rdifT_dcjma_sm12, rdifTerr_dcjma_sm12, Yt, [-40, 40], [0, 9000],  '2017 Data Conv-Deconv (PO3 JMA Smoothed 12sec.)',  rxtitle, ytitlet,
#                          labellist, o3list, dfnplist,
#                            'RDif_TSim_Convoluted_2017_jma_smoothed12', folderpath, False, False)
#
# ## convoluted smmmothed corrected jma 12 seconds
# errorPlot_ARDif_withtext(adifT_dcjma_sm18, adifTerr_dcjma_sm18, Yt, [-3, 3], [0, 9000],  '2017 Data Conv-Deconv (PPO3 JMA Smoothed 18sec.)',  axtitle, ytitlet,
#                          labellist, o3list, dfnplist,
#                            'ADif_TSim_Convoluted_2017_jma_smoothed18', folderpath ,  False, False)
#
# errorPlot_ARDif_withtext(rdifT_dcjma_sm18, rdifTerr_dcjma_sm18, Yt, [-40, 40], [0, 9000],  '2017 Data Conv-Deconv (PO3 JMA Smoothed 18sec.)',  rxtitle, ytitlet,
#                          labellist, o3list, dfnplist,
#                            'RDif_TSim_Convoluted_2017_jma_smoothed18', folderpath, False, False)

#
#
