## 0910 branch

#!/usr/bin/env python
# coding: utf-8
# Libraries
import pandas as pd
import matplotlib.pyplot as plt

from Josie_Functions import  Calc_average_profile_pressure, Calc_average_profile_time, Calc_Dif, Calc_average_profileCurrent_pressure, Calc_average_Dif
from Josie_PlotFunctions import  errorPlot_ARDif_withtext, errorPlot_general

folderpath = 'Dif_2017_beta0'

df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv_beta0.csv", low_memory=False)
# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv_beta0_fixedvalue.csv", low_memory=False)

# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_deconv.csv", low_memory=False)

df = df.drop(df[(df.PO3 < 0)].index)
df = df.drop(df[(df.PO3_OPM < 0)].index)

# df = df[df.ADX == 0]

test = df.drop_duplicates(['Sim', 'Team'])
print(len(test))


test = df.drop_duplicates(['Sim', 'Team'])
print(len(test))

########################################################################################################################
# ## cuts for Josie2017 data


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


########################################################################################################################
# ## cuts for Josie0910 data
# df = df[df.ADX == 0]
# # # v2 cuts, use this and v3 standard more conservative cuts not valid for 140, 1122, 163, 166  v2
# df=df[df.Tsim > 900]
# df=df[df.Tsim <= 8100]
# df = df.drop(df[(df.Sim == 141) & (df.Team == 3)].index)
# # df = df.drop(df[(df.Sim == 143) & (df.Team == 2) & (df.Tsim > 7950) & (df.Tsim < 8100)].index)
# df = df.drop(df[(df.Sim == 147) & (df.Team == 3)].index)
# df = df.drop(df[(df.Sim == 158) & (df.Team == 2)].index)
# df = df.drop(df[(df.Sim == 167) & (df.Team == 4)].index)
# # ## new cuts v2 20/05
# # df = df.drop(df[(df.Sim == 160) & (df.Team == 4)].index)
# # df = df.drop(df[(df.Sim == 165) & (df.Team == 4)].index)
#
# # # ## v3 cuts
# ### I think these cuts are not needed## checkcheck
# df = df.drop(df[(df.Sim == 159) & (df.Team == 1)].index) ##??
# df = df.drop(df[(df.Sim == 158) & (df.Team == 1)].index)
# df = df.drop(df[(df.Sim == 163) & (df.Team == 4)].index)
# df = df.drop(df[(df.Sim == 159) & (df.Team == 4)].index)
########################################################################################################################


#### try HV's gaussian filerting range
# dft[j]['Ifast_minib0_deconv_sm10'] = dft[j].Ifast_minib0_deconv.rolling(window=5).mean()

df['Ifast_minib0_deconv_sm4_gf15'] = df['Ifast_minib0_deconv'].rolling(window=2, win_type='gaussian', center=True).mean(std=15)

# #### time cuts
#
# df = df.drop(df[(2000 < df.Tsim) & (df.Tsim < 2500) & (df.Sim != 140) & (df.Sim != 162) & (df.Sim != 163) & (
#                 df.Sim != 166)].index)
# df = df.drop(df[(df.Tsim > 4000) & (df.Tsim < 4500) & (df.Sim != 140) & (df.Sim != 162) & (df.Sim != 163) & (
#                 df.Sim != 166)].index)
# df = df.drop(df[(df.Tsim > 6000) & (df.Tsim < 6500) & (df.Sim != 140) & (df.Sim != 162) & (df.Sim != 163) & (
#                 df.Sim != 166)].index)
#
# df = df.drop(df[(df.Sim == 158) & (df.Tsim > 7300) & (df.Tsim < 7700)].index)
# df = df.drop(df[(df.Sim == 159) & (df.Tsim > 7800) & (df.Tsim < 8000)].index)
# df = df.drop(df[(df.Sim == 161) & (df.Tsim > 6800) & (df.Tsim < 7200)].index)
#
#     # # additional cuts for specific simulations  v3
# df = df.drop(df[(df.Sim == 140) & (df.Tsim < 1000)].index)
# df = df.drop(df[(df.Sim == 140) & (df.Tsim > 2450) & (df.Tsim < 2800)].index)
# df = df.drop(df[(df.Sim == 140) & (df.Tsim > 4400) & (df.Tsim < 4800)].index)
# df = df.drop(df[(df.Sim == 140) & (df.Tsim > 6400) & (df.Tsim < 6800)].index)
#
# df = df.drop(df[(df.Sim == 162) & (df.Tsim > 2100) & (df.Tsim < 2550)].index)
# df = df.drop(df[(df.Sim == 162) & (df.Tsim > 4100) & (df.Tsim < 4600)].index)
# df = df.drop(df[(df.Sim == 162) & (df.Tsim > 5450) & (df.Tsim < 5800)].index)
# df = df.drop(df[(df.Sim == 162) & (df.Tsim > 6100) & (df.Tsim < 6550)].index)
#
# df = df.drop(df[(df.Sim == 163) & (df.Tsim > 2100) & (df.Tsim < 2550)].index)
# df = df.drop(df[(df.Sim == 163) & (df.Tsim > 4100) & (df.Tsim < 4600)].index)
# df = df.drop(df[(df.Sim == 163) & (df.Tsim > 5450) & (df.Tsim < 5800)].index)
# df = df.drop(df[(df.Sim == 163) & (df.Tsim > 6100) & (df.Tsim < 6550)].index)
#
# df = df.drop(df[(df.Sim == 166) & (df.Tsim > 2200) & (df.Tsim < 2650)].index)
# df = df.drop(df[(df.Sim == 166) & (df.Tsim > 4200) & (df.Tsim < 4700)].index)
# df = df.drop(df[(df.Sim == 166) & (df.Tsim > 6200) & (df.Tsim < 6650)].index)
# df = df.drop(df[(df.Sim == 166) & (df.Tsim > 7550) & (df.Tsim < 7750)].index)
# df = df.drop(df[(df.Sim == 166) & (df.Team == 1) & (df.Tsim > 4400) & (df.Tsim < 5400)].index)

###############################################
# Filters for Sonde, Solution, Buff er selection
# 1, 0.1 ENSCI vs SPC
filtEN = df.ENSCI == 1
filtSP = df.ENSCI == 0

filtS10 = df.Sol == 1
filtS05 = df.Sol == 0.5

filtB10 = df.Buf == 1.0
filtB05 = df.Buf == 0.5
filtB01 = df.Buf == 0.1

filterEN0505 = (filtEN & filtS05 & filtB05)
filterEN1010 = (filtEN & filtS10 & filtB10)
filterEN1001 = (filtEN & filtS10 & filtB01)

profEN0505 = df.loc[filterEN0505]
# profEN1010 = df.loc[filterEN1010]
profEN1010 = df.loc[filterEN1001]


profEN0505_nodup = profEN0505.drop_duplicates(['Sim', 'Team'])
profEN1010_nodup = profEN1010.drop_duplicates(['Sim', 'Team'])

print(profEN0505_nodup[['Sim','Team']])

totO3_EN0505 = profEN0505_nodup.frac.mean()
totO3_EN1010 = profEN1010_nodup.frac.mean()


filterSP1010 = (filtSP & filtS10 & filtB10)
filterSP0505 = (filtSP & filtS05 & filtB05)
filterSP1001 = (filtSP & filtS10 & filtB01)

profSP1010 = df.loc[filterSP1010]
# profSP0505 = df.loc[filterSP0505]
profSP0505 = df.loc[filterSP1001]


profSP1010_nodup = profSP1010.drop_duplicates(['Sim', 'Team'])
profSP0505_nodup = profSP0505.drop_duplicates(['Sim', 'Team'])

totO3_SP1010 = profSP1010_nodup.frac.mean()
totO3_SP0505 = profSP0505_nodup.frac.mean()

prof = [profEN0505, profEN1010, profSP0505, profSP1010]

print(list(df))

# ##################################################################################
# ################     Pressure PO3 PLOTS        #################################
# ##################################################################################

adif_PO3, adif_PO3_err, rdif_PO3, rdif_PO3_err, Yp = Calc_average_Dif(prof, 'PO3', 'PO3_OPM',  'pressure')
adif_PO3_deconvjma, adif_PO3_deconvjma_err, rdif_PO3_deconvjma, rdif_PO3_deconvjma_err, Yp = Calc_average_Dif(prof, 'PO3_deconv_jma', 'PO3_OPM',  'pressure')
# adif_PO3_deconvjma_sm6, adif_PO3_deconvjma_sm6_err, rdif_PO3_deconvjma_sm6, rdif_PO3_deconvjma_sm6_err, Yp = Calc_average_Dif(prof, 'PO3_deconv_jma_sm6', 'PO3_OPM',  'pressure')
# adif_PO3_deconvjma_sm8_gf1, adif_PO3_deconvjma_sm8_gf1_err, rdif_PO3_deconvjma_sm8_gf1, rdif_PO3_deconvjma_sm8_gf1_err, Yp = \
# Calc_average_Dif(prof, 'PO3_deconv_jma_sm8_gf1', 'PO3_OPM',  'pressure')
# adif_PO3_deconvjma_sm8_gf2, adif_PO3_deconvjma_sm8_gf2_err, rdif_PO3_deconvjma_sm8_gf2, rdif_PO3_deconvjma_sm8_gf2_err, Yp = \
# Calc_average_Dif(prof, 'PO3_deconv_jma_sm8_gf2', 'PO3_OPM',  'pressure')
# adif_PO3_deconvjma_sm8_gf4, adif_PO3_deconvjma_sm8_gf4_err, rdif_PO3_deconvjma_sm8_gf4, rdif_PO3_deconvjma_sm8_gf4_err, Yp = \
# Calc_average_Dif(prof, 'PO3_deconv_jma_sm8_gf4', 'PO3_OPM',  'pressure')


ytitle = 'Pressure (hPa)'
ytitlet = 'Time (sec.)'

# ### Plotting

axtitlecur = r'Sonde - OPM[JMA]  Difference ($\mu$A)'
rxtitle = 'Sonde - OPM[JMA]  Difference (%)'

### Plotting
axtitle_nojma = 'Sonde - OPM  Difference (mPa)'
axtitle = 'Sonde[JMA] - OPM  Difference (mPa)'

rxtitle_nojma = 'Sonde - OPM  Difference (%)'
rxtitle = 'Sonde[JMA] - OPM  Difference (%)'


# labellist = ['EN 0.5%-0.5B','EN 1.0%-1.0B', 'SP 0.5%-0.5B', 'SP 1.0%-1.0B']
labellist = ['EN 0.5%-0.5B','EN 1.0%-0.1B', 'SP 1.0%-0.1B', 'SP 1.0%-1.0B']

o3list = [totO3_EN0505, totO3_EN1010,  totO3_SP0505, totO3_SP1010]
dfnplist = [profEN0505.drop_duplicates(['Sim', 'Team']), profEN1010.drop_duplicates(['Sim', 'Team']), profSP0505_nodup,
        profSP1010_nodup]

# #standard
errorPlot_ARDif_withtext(adif_PO3, adif_PO3_err, Yp, [-3, 3], [1000,5],  '2017 Data',  axtitle_nojma, ytitle, labellist, o3list, dfnplist,
                       'ADif_Pair_2017', folderpath ,  True, False)
errorPlot_ARDif_withtext(rdif_PO3, rdif_PO3_err, Yp, [-40, 40], [1000,5],  '2017 Data',  rxtitle_nojma, ytitle, labellist, o3list, dfnplist,
                       'RDif_Pair_2017', folderpath, True, False)
#
# ## convoluted jma
errorPlot_ARDif_withtext(adif_PO3_deconvjma, adif_PO3_deconvjma_err, Yp, [-3, 3], [1000,5],'2017 Data Conv-Deconv (PO3 JMA corr.)',  axtitle, ytitle, labellist, o3list, dfnplist,
                       'ADif_Pair_2017_PO3Deconv', folderpath ,  True, False)
errorPlot_ARDif_withtext(rdif_PO3_deconvjma, rdif_PO3_deconvjma_err, Yp, [-40, 40], [1000,5], '2017 Data Conv-Deconv (PO3 JMA corr.)',  rxtitle, ytitle, labellist, o3list, dfnplist,
                       'RDif_Pair_2017_PO3Deconv', folderpath, True, False)

#

##################################################################################
# ################      CURRENT IM PLOTS        #################################
# ##################################################################################
#
# # df['CurMinBkg'] = df['IM'] - df['Header_IB1']
# # df['Ifast_deconvMinBkg'] = df['Ifast_deconv'] - df['Header_IB1']

adif_IM, adif_IM_err, rdif_IM, rdif_IM_err, Yp = Calc_average_Dif(prof, 'IM', 'I_OPM_jma',  'pressure')
errorPlot_ARDif_withtext(adif_IM, adif_IM_err, Yp, [-3, 3], [1000,5],  '2017 Data (Current)',  axtitlecur, ytitle, labellist, o3list, dfnplist,
                       'Current_ADif_Pair_2017', folderpath ,  True, False)
errorPlot_ARDif_withtext(rdif_IM, rdif_IM_err, Yp, [-40, 40], [1000,5],  '2017 Data (Current)',  rxtitle, ytitle, labellist, o3list, dfnplist,
                       'Current_RDif_Pair_2017', folderpath, True, False)

adif_Ifastdeconv, adif_Ifastdeconv_err, rdif_Ifastdeconv, rdif_Ifastdeconv_err, Yp = Calc_average_Dif(prof, 'Ifast_deconv', 'I_OPM_jma',  'pressure')
errorPlot_ARDif_withtext(rdif_Ifastdeconv, rdif_Ifastdeconv_err, Yp, [-40, 40], [1000,5],  '2017 Data Conv-Deconv (Current)',  rxtitle, ytitle,
                     labellist, o3list, dfnplist,
                       'Current_RDif_Pair_Convoluted_2017', folderpath, True, False)

adif_Ifastdeconv_sm6, adif_Ifastdeconv_sm6_err, rdif_Ifastdeconv_sm6, rdif_Ifastdeconv_sm6_err, Yp = Calc_average_Dif(prof, 'Ifast_deconv_sm6', 'I_OPM_jma',  'pressure')
errorPlot_ARDif_withtext(rdif_Ifastdeconv_sm6, rdif_Ifastdeconv_sm6_err, Yp, [-40, 40], [1000,5],  '2017 Data Conv-Deconv (Current Smoothed 6 secs)',
                         rxtitle, ytitle,labellist, o3list, dfnplist,'Current_RDif_Pair_Convoluted_2017_smoothed6', folderpath, True, False)

adif_Ifastdeconv_sm8, adif_Ifastdeconv_sm8_err, rdif_Ifastdeconv_sm8, rdif_Ifastdeconv_sm8_err, Yp = Calc_average_Dif(prof, 'Ifast_deconv_sm8', 'I_OPM_jma',  'pressure')
errorPlot_ARDif_withtext(rdif_Ifastdeconv_sm8, rdif_Ifastdeconv_sm8_err, Yp, [-40, 40], [1000,5],  '2017 Data Conv-Deconv (Current Smoothed 8 secs)',
                         rxtitle, ytitle,labellist, o3list, dfnplist,'Current_RDif_Pair_Convoluted_2017_smoothed8', folderpath, True, False)

adif_Ifastdeconv_sm8, adif_Ifastdeconv_sm10_err, rdif_Ifastdeconv_sm10, rdif_Ifastdeconv_sm10_err, Yp = Calc_average_Dif(prof, 'Ifast_deconv_sm10', 'I_OPM_jma',  'pressure')
errorPlot_ARDif_withtext(rdif_Ifastdeconv_sm10, rdif_Ifastdeconv_sm10_err, Yp, [-40, 40], [1000,5],  '2017 Data Conv-Deconv (Current Smoothed 10 secs)',
                         rxtitle, ytitle,labellist, o3list, dfnplist,'Current_RDif_Pair_Convoluted_2017_smoothed10', folderpath, True, False)

adif_Ifastminib0deconv, adif_Ifastminib0deconv_err, rdif_Ifastminib0deconv, rdif_Ifastminib0deconv_err, Yp = \
    Calc_average_Dif(prof, 'Ifast_minib0_deconv', 'I_OPM_jma',  'pressure')
errorPlot_ARDif_withtext(rdif_Ifastminib0deconv, rdif_Ifastminib0deconv_err, Yp, [-40, 40], [1000,5],  '2017 Data  Conv-Deconv (Current, minus iB0 )',
                         rxtitle, ytitle, labellist, o3list, dfnplist,'Currentmib0_RDif_Pair_2017_Convoluted2', folderpath, True, False)


adif_Ifastminib0deconv_sm6, adif_Ifastminib0deconv_sm6_err, rdif_Ifastminib0deconv_sm6, rdif_Ifastminib0deconv_sm6_err, Yp = \
    Calc_average_Dif(prof, 'Ifast_minib0_deconv_sm6', 'I_OPM_jma',  'pressure')
errorPlot_ARDif_withtext(rdif_Ifastminib0deconv_sm6, rdif_Ifastminib0deconv_sm6_err, Yp, [-40, 40], [1000,5],  '2017 Data  Conv-Deconv (Current, minus iB0 smoothed 6 secs)',
                         rxtitle, ytitle, labellist, o3list, dfnplist,'Currentmib0_RDif_Pair_2017_Convoluted_smoothed6', folderpath, True, False)

adif_Ifastminib0deconv_sm6_gf1, adif_Ifastminib0deconv_sm6_gf1_err, rdif_Ifastminib0deconv_sm6_gf1, rdif_Ifastminib0deconv_sm6_gf1_err, Yp = \
    Calc_average_Dif(prof, 'Ifast_minib0_deconv_sm6_gf1', 'I_OPM_jma',  'pressure')
errorPlot_ARDif_withtext(rdif_Ifastminib0deconv_sm6_gf1, rdif_Ifastminib0deconv_sm6_gf1_err, Yp, [-40, 40], [1000,5],  '2017 Data  Conv-Deconv (Current, minus iB0 smoothed 6 secs gf1)',
                         rxtitle, ytitle, labellist, o3list, dfnplist,'Currentmib0_RDif_Pair_2017_Convoluted_smoothed6_gf1', folderpath, True, False)

adif_Ifastminib0deconv_sm6_gf2, adif_Ifastminib0deconv_sm6_gf2_err, rdif_Ifastminib0deconv_sm6_gf2, rdif_Ifastminib0deconv_sm6_gf2_err, Yp = \
    Calc_average_Dif(prof, 'Ifast_minib0_deconv_sm6_gf2', 'I_OPM_jma',  'pressure')
errorPlot_ARDif_withtext(rdif_Ifastminib0deconv_sm6_gf2, rdif_Ifastminib0deconv_sm6_gf2_err, Yp, [-40, 40], [1000,5],  '2017 Data  Conv-Deconv (Current, minus iB0 smoothed 6 secs gf2)',
                         rxtitle, ytitle, labellist, o3list, dfnplist,'Currentmib0_RDif_Pair_2017_Convoluted_smoothed6_gf2', folderpath, True, False)

adif_Ifastminib0deconv_sm6_gf4, adif_Ifastminib0deconv_sm6_gf4err, rdif_Ifastminib0deconv_sm6_gf4, rdif_Ifastminib0deconv_sm6_gf4_err, Yp = \
    Calc_average_Dif(prof, 'Ifast_minib0_deconv_sm6_gf4', 'I_OPM_jma',  'pressure')
errorPlot_ARDif_withtext(rdif_Ifastminib0deconv_sm6_gf4, rdif_Ifastminib0deconv_sm6_gf4_err, Yp, [-40, 40], [1000,5],  '2017 Data  Conv-Deconv (Current, minus iB0 smoothed 6 secs gf4)',
                         rxtitle, ytitle, labellist, o3list, dfnplist,'Currentmib0_RDif_Pair_2017_Convoluted_smoothed6_gf4', folderpath, True, False)

adif_Ifastminib0deconv_sm8, adif_Ifastminib0deconv_sm8_err, rdif_Ifastminib0deconv_sm8, rdif_Ifastminib0deconv_sm8_err, Yp = \
    Calc_average_Dif(prof, 'Ifast_minib0_deconv_sm8', 'I_OPM_jma',  'pressure')
adif_Ifastminib0deconv_sm8_gf1, adif_Ifastminib0deconv_sm8_gf1_err, rdif_Ifastminib0deconv_sm8_gf1, rdif_Ifastminib0deconv_sm8_gf1_err, Yp = \
    Calc_average_Dif(prof, 'Ifast_minib0_deconv_sm8_gf1', 'I_OPM_jma',  'pressure')
adif_Ifastminib0deconv_sm8_gf2, adif_Ifastminib0deconv_sm8_gf2_err, rdif_Ifastminib0deconv_sm8_gf2, rdif_Ifastminib0deconv_sm8_gf2_err, Yp = \
    Calc_average_Dif(prof, 'Ifast_minib0_deconv_sm8_gf2', 'I_OPM_jma',  'pressure')
adif_Ifastminib0deconv_sm8_gf4, adif_Ifastminib0deconv_sm8_gf4_err, rdif_Ifastminib0deconv_sm8_gf4, rdif_Ifastminib0deconv_sm8_gf4_err, Yp = \
    Calc_average_Dif(prof, 'Ifast_minib0_deconv_sm8_gf4', 'I_OPM_jma',  'pressure')

errorPlot_ARDif_withtext(adif_Ifastminib0deconv_sm8, adif_Ifastminib0deconv_sm8_err, Yp, [-3, 3], [1000,5],  '2017 Data  Conv-Deconv (Current, minus iB0 smoothed 8 secs)',  axtitlecur, ytitle, labellist, o3list, dfnplist,
                       'Currentmib0_ADif_Pair_2017_Convoluted_smoothed8', folderpath ,  True, False)
errorPlot_ARDif_withtext(rdif_Ifastminib0deconv_sm8, rdif_Ifastminib0deconv_sm8_err, Yp, [-40, 40], [1000,5],  '2017 Data  Conv-Deconv (Current, minus iB0 smoothed 8 secs)',  rxtitle, ytitle, labellist, o3list, dfnplist,
                       'Currentmib0_RDif_Pair_2017_Convoluted_smoothed8', folderpath, True, False)
errorPlot_ARDif_withtext(rdif_Ifastminib0deconv_sm8_gf1, rdif_Ifastminib0deconv_sm8_gf1_err, Yp, [-40, 40], [1000,5],  '2017 Data  Conv-Deconv (Current, minus iB0 smoothed 8 secs gf1)',  rxtitle, ytitle, labellist, o3list, dfnplist,
                       'Currentmib0_RDif_Pair_2017_Convoluted_smoothed8_gf1', folderpath, True, False)
errorPlot_ARDif_withtext(rdif_Ifastminib0deconv_sm8_gf2, rdif_Ifastminib0deconv_sm8_gf2_err, Yp, [-40, 40], [1000,5],  '2017 Data  Conv-Deconv (Current, minus iB0 smoothed 8 secs gf2)',  rxtitle, ytitle, labellist, o3list, dfnplist,
                       'Currentmib0_RDif_Pair_2017_Convoluted_smoothed8_gf2', folderpath, True, False)
errorPlot_ARDif_withtext(rdif_Ifastminib0deconv_sm8_gf2, rdif_Ifastminib0deconv_sm8_gf2_err, Yp, [-40, 40], [1000,5],  '2017 Data  Conv-Deconv (Current, minus iB0 smoothed 8 secs gf2)',  rxtitle, ytitle, labellist, o3list, dfnplist,
                       'Currentmib0_RDif_Pair_2017_Convoluted_smoothed8_gf2', folderpath, True, False)
errorPlot_ARDif_withtext(rdif_Ifastminib0deconv_sm8_gf4, rdif_Ifastminib0deconv_sm8_gf4_err, Yp, [-40, 40], [1000,5],  '2017 Data  Conv-Deconv (Current, minus iB0 smoothed 8 secs gf4)',  rxtitle, ytitle, labellist, o3list, dfnplist,
                       'Currentmib0_RDif_Pair_2017_Convoluted_smoothed8_gf4', folderpath, True, False)

adif_Ifastminib0deconv_sm10, adif_Ifastminib0deconv_sm10_err, rdif_Ifastminib0deconv_sm10, rdif_Ifastminib0deconv_sm10_err, Yp = \
    Calc_average_Dif(prof, 'Ifast_minib0_deconv_sm10', 'I_OPM_jma',  'pressure')
adif_Ifastminib0deconv_sm10_gf1, adif_Ifastminib0deconv_sm10_gf1_err, rdif_Ifastminib0deconv_sm10_gf1, rdif_Ifastminib0deconv_sm10_gf1_err, Yp = \
    Calc_average_Dif(prof, 'Ifast_minib0_deconv_sm10_gf1', 'I_OPM_jma',  'pressure')
adif_Ifastminib0deconv_sm10_gf2, adif_Ifastminib0deconv_sm10_gf2_err, rdif_Ifastminib0deconv_sm10_gf2, rdif_Ifastminib0deconv_sm10_gf2_err, Yp = \
    Calc_average_Dif(prof, 'Ifast_minib0_deconv_sm10_gf2', 'I_OPM_jma',  'pressure')
adif_Ifastminib0deconv_sm10_gf4, adif_Ifastminib0deconv_sm10_gf4_err, rdif_Ifastminib0deconv_sm10_gf4, rdif_Ifastminib0deconv_sm10_gf4_err, Yp = \
    Calc_average_Dif(prof, 'Ifast_minib0_deconv_sm10_gf4', 'I_OPM_jma',  'pressure')

errorPlot_ARDif_withtext(adif_Ifastminib0deconv_sm10, adif_Ifastminib0deconv_sm10_err, Yp, [-3, 3], [1000,5],  '2017 Data  Conv-Deconv (Current, minus iB0 smoothed 10 secs)',  axtitlecur, ytitle, labellist, o3list, dfnplist,
                       'Currentmib0_ADif_Pair_2017_Convoluted_smoothed10', folderpath ,  True, False)
errorPlot_ARDif_withtext(rdif_Ifastminib0deconv_sm10, rdif_Ifastminib0deconv_sm10_err, Yp, [-40, 40], [1000,5],  '2017 Data  Conv-Deconv (Current, minus iB0 smoothed 10 secs)',  rxtitle, ytitle, labellist, o3list, dfnplist,
                       'Currentmib0_RDif_Pair_2017_Convoluted_smoothed10', folderpath, True, False)
errorPlot_ARDif_withtext(rdif_Ifastminib0deconv_sm10_gf1, rdif_Ifastminib0deconv_sm10_gf1_err, Yp, [-40, 40], [1000,5],  '2017 Data  Conv-Deconv (Current, minus iB0 smoothed 10 secs gf1)',  rxtitle, ytitle, labellist, o3list, dfnplist,
                       'Currentmib0_RDif_Pair_2017_Convoluted_smoothed10_gf1', folderpath, True, False)
errorPlot_ARDif_withtext(rdif_Ifastminib0deconv_sm10_gf2, rdif_Ifastminib0deconv_sm10_gf2_err, Yp, [-40, 40], [1000,5],  '2017 Data  Conv-Deconv (Current, minus iB0 smoothed 10 secs gf2)',  rxtitle, ytitle, labellist, o3list, dfnplist,
                       'Currentmib0_RDif_Pair_2017_Convoluted_smoothed10_gf2', folderpath, True, False)
errorPlot_ARDif_withtext(rdif_Ifastminib0deconv_sm10_gf2, rdif_Ifastminib0deconv_sm10_gf2_err, Yp, [-40, 40], [1000,5],  '2017 Data  Conv-Deconv (Current, minus iB0 smoothed 10 secs gf2)',  rxtitle, ytitle, labellist, o3list, dfnplist,
                       'Currentmib0_RDif_Pair_2017_Convoluted_smoothed10_gf2', folderpath, True, False)
errorPlot_ARDif_withtext(rdif_Ifastminib0deconv_sm10_gf4, rdif_Ifastminib0deconv_sm10_gf4_err, Yp, [-40, 40], [1000,5],  '2017 Data  Conv-Deconv (Current, minus iB0 smoothed 10 secs gf4)',  rxtitle, ytitle, labellist, o3list, dfnplist,
                       'Currentmib0_RDif_Pair_2017_Convoluted_smoothed10_gf4', folderpath, True, False)

adif_Ifastminib0deconv_sm10, adif_Ifastminib0deconv_sm10_err, rdif_Ifastminib0deconv_sm10, rdif_Ifastminib0deconv_sm10_err, Yp = \
    Calc_average_Dif(prof, 'Ifast_minib0_deconv_sm10', 'I_OPM_jma',  'pressure')

adif_Ifastminib0deconv_smb6, adif_Ifastminib0deconv_smb6_err, rdif_Ifastminib0deconv_smb6, rdif_Ifastminib0deconv_smb6_err, Yp = \
    Calc_average_Dif(prof, 'Ifast_minib0_deconv_smb6', 'I_OPM_jma',  'pressure')
adif_Ifastminib0deconv_smb6_gf1, adif_Ifastminib0deconv_smb6_gf1_err, rdif_Ifastminib0deconv_smb6_gf1, rdif_Ifastminib0deconv_smb6_gf1_err, Yp = \
    Calc_average_Dif(prof, 'Ifast_minib0_deconv_smb6_gf1', 'I_OPM_jma',  'pressure')
adif_Ifastminib0deconv_smb6_gf2, adif_Ifastminib0deconv_smb6_gf2_err, rdif_Ifastminib0deconv_smb6_gf2, rdif_Ifastminib0deconv_smb6_gf2_err, Yp = \
    Calc_average_Dif(prof, 'Ifast_minib0_deconv_smb6_gf2', 'I_OPM_jma',  'pressure')
adif_Ifastminib0deconv_smb6_gf4, adif_Ifastminib0deconv_smb6_gf4_err, rdif_Ifastminib0deconv_smb6_gf4, rdif_Ifastminib0deconv_smb6_gf4_err, Yp = \
    Calc_average_Dif(prof, 'Ifast_minib0_deconv_smb6_gf4', 'I_OPM_jma',  'pressure')

errorPlot_ARDif_withtext(adif_Ifastminib0deconv_smb6, adif_Ifastminib0deconv_smb6_err, Yp, [-3, 3], [1000,5],  '2017 Data  Conv-Deconv (Current, minus iB0 first smoothed 6 secs)',  axtitlecur, ytitle, labellist, o3list, dfnplist,
                       'Currentmib0_ADif_Pair_2017_Convoluted_firstsmoothed6', folderpath ,  True, False)
errorPlot_ARDif_withtext(rdif_Ifastminib0deconv_smb6, rdif_Ifastminib0deconv_smb6_err, Yp, [-40, 40], [1000,5],  '2017 Data  Conv-Deconv (Current, minus iB0 first smoothed 6 secs)',  rxtitle, ytitle, labellist, o3list, dfnplist,
                       'Currentmib0_RDif_Pair_2017_Convoluted_firstsmoothed6', folderpath, True, False)
errorPlot_ARDif_withtext(rdif_Ifastminib0deconv_smb6_gf1, rdif_Ifastminib0deconv_smb6_gf1_err, Yp, [-40, 40], [1000,5],  '2017 Data  Conv-Deconv (Current, minus iB0 first smoothed 6 secs gf1)',  rxtitle, ytitle, labellist, o3list, dfnplist,
                       'Currentmib0_RDif_Pair_2017_Convoluted_firstsmoothed6_gf1', folderpath, True, False)
errorPlot_ARDif_withtext(rdif_Ifastminib0deconv_smb6_gf2, rdif_Ifastminib0deconv_smb6_gf2_err, Yp, [-40, 40], [1000,5],  '2017 Data  Conv-Deconv (Current, minus iB0 first smoothed 6 secs gf2)',  rxtitle, ytitle, labellist, o3list, dfnplist,
                       'Currentmib0_RDif_Pair_2017_Convoluted_firstsmoothed6_gf2', folderpath, True, False)
errorPlot_ARDif_withtext(rdif_Ifastminib0deconv_smb6_gf4, rdif_Ifastminib0deconv_smb6_gf4_err, Yp, [-40, 40], [1000,5],  '2017 Data  Conv-Deconv (Current, minus iB0 first smoothed 6 secs gf4)',  rxtitle, ytitle, labellist, o3list, dfnplist,
                       'Currentmib0_RDif_Pair_2017_Convoluted_firstsmoothed6_gf4', folderpath, True, False)



adif_Ifastminib0deconv_smb8, adif_Ifastminib0deconv_smb8_err, rdif_Ifastminib0deconv_smb8, rdif_Ifastminib0deconv_smb8_err, Yp = \
    Calc_average_Dif(prof, 'Ifast_minib0_deconv_smb8', 'I_OPM_jma',  'pressure')
adif_Ifastminib0deconv_smb8_gf1, adif_Ifastminib0deconv_smb8_gf1_err, rdif_Ifastminib0deconv_smb8_gf1, rdif_Ifastminib0deconv_smb8_gf1_err, Yp = \
    Calc_average_Dif(prof, 'Ifast_minib0_deconv_smb8_gf1', 'I_OPM_jma',  'pressure')
adif_Ifastminib0deconv_smb8_gf2, adif_Ifastminib0deconv_smb8_gf2_err, rdif_Ifastminib0deconv_smb8_gf2, rdif_Ifastminib0deconv_smb8_gf2_err, Yp = \
    Calc_average_Dif(prof, 'Ifast_minib0_deconv_smb8_gf2', 'I_OPM_jma',  'pressure')
adif_Ifastminib0deconv_smb8_gf4, adif_Ifastminib0deconv_smb8_gf4_err, rdif_Ifastminib0deconv_smb8_gf4, rdif_Ifastminib0deconv_smb8_gf4_err, Yp = \
    Calc_average_Dif(prof, 'Ifast_minib0_deconv_smb8_gf4', 'I_OPM_jma',  'pressure')

errorPlot_ARDif_withtext(adif_Ifastminib0deconv_smb8, adif_Ifastminib0deconv_smb8_err, Yp, [-3, 3], [1000,5],  '2017 Data  Conv-Deconv (Current, minus iB0 first smoothed 8 secs)',  axtitlecur, ytitle, labellist, o3list, dfnplist,
                       'Currentmib0_ADif_Pair_2017_Convoluted_firstsmoothed8', folderpath ,  True, False)
errorPlot_ARDif_withtext(rdif_Ifastminib0deconv_smb8_gf1, rdif_Ifastminib0deconv_smb8_gf1_err, Yp, [-40, 40], [1000,5],  '2017 Data  Conv-Deconv (Current, minus iB0 first smoothed 8 secs gf1)',  rxtitle, ytitle, labellist, o3list, dfnplist,
                       'Currentmib0_RDif_Pair_2017_Convoluted_firstsmoothed8_gf1', folderpath, True, False)
errorPlot_ARDif_withtext(rdif_Ifastminib0deconv_smb8_gf2, rdif_Ifastminib0deconv_smb8_gf2_err, Yp, [-40, 40], [1000,5],  '2017 Data  Conv-Deconv (Current, minus iB0 first smoothed 8 secs gf2)',  rxtitle, ytitle, labellist, o3list, dfnplist,
                       'Currentmib0_RDif_Pair_2017_Convoluted_firstsmoothed8_gf2', folderpath, True, False)
errorPlot_ARDif_withtext(rdif_Ifastminib0deconv_smb8_gf2, rdif_Ifastminib0deconv_smb8_gf2_err, Yp, [-40, 40], [1000,5],  '2017 Data  Conv-Deconv (Current, minus iB0 first smoothed 8 secs gf2)',  rxtitle, ytitle, labellist, o3list, dfnplist,
                       'Currentmib0_RDif_Pair_2017_Convoluted_firstsmoothed8_gf2', folderpath, True, False)
errorPlot_ARDif_withtext(rdif_Ifastminib0deconv_smb8_gf4, rdif_Ifastminib0deconv_smb8_gf4_err, Yp, [-40, 40], [1000,5],  '2017 Data  Conv-Deconv (Current, minus iB0 first smoothed 8 secs gf4)',  rxtitle, ytitle, labellist, o3list, dfnplist,
                       'Currentmib0_RDif_Pair_2017_Convoluted_firstsmoothed8_gf4', folderpath, True, False)


### HV
adif_Ifastminib0deconv_sm4_gf15, adif_Ifastminib0deconv_sm4_gf15_err, rdif_Ifastminib0deconv_sm4_gf15, rdif_Ifastminib0deconv_sm4_gf15_err, Yp = \
    Calc_average_Dif(prof, 'Ifast_minib0_deconv_sm4_gf15', 'I_OPM_jma',  'pressure')

#


errorPlot_ARDif_withtext(rdif_Ifastminib0deconv_sm4_gf15, rdif_Ifastminib0deconv_sm4_gf15_err, Yp, [-40, 40], [1000,5],  '2017 Data  Conv-Deconv (Current, minus iB0 smoothed 4 secs gf15)',  rxtitle, ytitle, labellist, o3list, dfnplist,
                       'Currentmib0_RDif_Pair_2017_Convoluted_smoothed4_gf15', folderpath, True, False)



#

#
#
#
# # ## convoluted ones
# #
# errorPlot_ARDif_withtext(adif_Ifastdeconv, adif_Ifastdeconv_err, Yp, [-3, 3], [1000,5],  '0910 Data Conv-Deconv (Current )',  axtitlecur, ytitle,
#                      labellist, o3list, dfnplist,
#                        'Current_ADif_Pair_Convoluted_0910', folderpath ,  True, False)
#

#
# ## convoluted ones sm6
# errorPlot_ARDif_withtext(adif_Ifastdeconv_sm6, adif_Ifastdeconv_sm6_err, Yp, [-3, 3], [1000,5],  '0910 Data Conv-Deconv (Current Smoothed 6 secs)',  axtitlecur, ytitle,
#                      labellist, o3list, dfnplist,
#                        'Current_ADif_Pair_Convoluted_0910_smoothed6', folderpath ,  True, False)

#
# errorPlot_ARDif_withtext(adif_Ifastminib0deconv_sm6, adif_Ifastminib0deconv_sm6_err, Yp, [-3, 3], [1000,5],  '0910 Data  Conv-Deconv (Current, minus iB0 smoothed 6 secs)',  axtitlecur, ytitle, labellist, o3list, dfnplist,
#                        'Currentmib0_ADif_Pair_0910_Convoluted_smoothed6', folderpath ,  True, False)

#

#
# errorPlot_ARDif_withtext(rdif_Ifastminib0deconv_sm10, rdif_Ifastminib0deconv_sm10_err, Yp, [-40, 40], [1000,5],  '0910 Data  Conv-Deconv (Current, minus iB0 smoothed 10 secs)',  rxtitle, ytitle, labellist, o3list, dfnplist,
#                        'Currentmib0_RDif_Pair_0910_Convoluted_smoothed10', folderpath, True, False)
#

#

#



#
# #####  final plot for relative contribution of I_slow to the total current asaf of pressure
# #
# # print('check', len(avgprof_O3S_curSlow[0]), len(avgprof_O3S_cur[0]))
# # print(len(Ycur), len(Yslow))
# # dimension = len(Yslow)
# #
# # print('avgprof_O3S_curSlow', avgprof_O3S_curSlow[0])
# # print('avgprof_O3S_cur', avgprof_O3S_cur[0])
# #
# # adifcurSlow = [ (i - j)/i for i in avgprof_O3S_cur[0] for j in avgprof_O3S_curSlow[0] ]
# #
# # print('one adifcurSlow', adifcurSlow[0])
# #
# # adifcurSlow, adifcurSlowerr, rdifcurSlow, rdifcurSlowerr = Calc_Dif(avgprof_O3S_curSlow, avgprof_O3S_cur, avgprof_O3S_curSlowerr, dimension)
# #
# # print('adifcurSlow', adifcurSlow[0])
# # print('rdifcurSlow', rdifcurSlow[0])
# #
# # for k in range(4):
# #     for s in range(len(rdifcurSlow[k])):
# #         rdifcurSlow[k][s] = avgprof_O3S_curSlow[k][s]/ avgprof_O3S_cur[k][s] * 100
# #
# # print('rdifcurSlow two', rdifcurSlow[0])
# #
# # errorPlot_ARDif_withtext(adifcurSlow, adifcurSlowerr, Yslow, [-3, 3], [1000,5],  '0910 Data',  axtitle, ytitle, labellist, o3list, dfnplist,
# #                            'I_Slow_Contribution_ADif_Pair_0910', folderpath ,  True, False)
# #
# # errorPlot_ARDif_withtext(rdifcurSlow, rdifcurSlowerr, Yslow, [-20, 20], [1000,5],  '0910 Data',  r'I$_{slow}$conv./I$_{ECC}$ (%)', ytitle, labellist, o3list, dfnplist,
# #                            'I_Slow_Contribution_RDif_Pair_0910', folderpath, True, False)
# #
# # #####  final plot for relative contribution of I_slow to the total current asaf of time
# # dimension = len(Yt)
# #
# #
# # adifcurSlowT, adifcurSlowTerr, rdifcurSlowT, rdifcurSlowTerr = Calc_Dif(avgprof_O3S_curSlowT, avgprof_O3S_curT, avgprof_O3S_curSlowTerr, dimension)
# #
# # for kk in range(4):
# #     for ss in range(len(rdifcurSlow[kk])):
# #         rdifcurSlowT[kk][ss] = avgprof_O3S_curSlowT[kk][ss]/ avgprof_O3S_curT[kk][ss] * 100
# #
# # errorPlot_ARDif_withtext(adifcurSlowT, adifcurSlowTerr, Yt, [-3, 3], [0, 9000],  '0910 Data',  axtitle, ytitlet, labellist, o3list, dfnplist,
# #                            'I_Slow_Contribution_ADif_TSim_0910', folderpath ,  False, False)
# #
# # errorPlot_ARDif_withtext(rdifcurSlowT, rdifcurSlowTerr, Yt, [-20, 20], [0, 9000],  '0910 Data',    r'I$_{slow}$conv./I$_{ECC}$ (%)', ytitlet, labellist, o3list, dfnplist,
# #                            'I_Slow_Contribution_RDif_TSim_0910', folderpath, False, False)

#### time cuts


# df = df.drop(df[(2000 < df.Tsim) & (df.Tsim < 2500) & (df.Sim != 140) & (df.Sim != 162) & (df.Sim != 163) & (
#                 df.Sim != 166)].index)
# df = df.drop(df[(df.Tsim > 4000) & (df.Tsim < 4500) & (df.Sim != 140) & (df.Sim != 162) & (df.Sim != 163) & (
#                 df.Sim != 166)].index)
# df = df.drop(df[(df.Tsim > 6000) & (df.Tsim < 6500) & (df.Sim != 140) & (df.Sim != 162) & (df.Sim != 163) & (
#                 df.Sim != 166)].index)


#
# df = df.drop(df[(df.Sim == 158) & (df.Tsim > 7300) & (df.Tsim < 7700)].index)
# df = df.drop(df[(df.Sim == 159) & (df.Tsim > 7800) & (df.Tsim < 8000)].index)
# df = df.drop(df[(df.Sim == 161) & (df.Tsim > 6800) & (df.Tsim < 7200)].index)
#
#     # # additional cuts for specific simulations  v3
# df = df.drop(df[(df.Sim == 140) & (df.Tsim < 1000)].index)
# df = df.drop(df[(df.Sim == 140) & (df.Tsim > 2450) & (df.Tsim < 2800)].index)
# df = df.drop(df[(df.Sim == 140) & (df.Tsim > 4400) & (df.Tsim < 4800)].index)
# df = df.drop(df[(df.Sim == 140) & (df.Tsim > 6400) & (df.Tsim < 6800)].index)
#
# df = df.drop(df[(df.Sim == 162) & (df.Tsim > 2100) & (df.Tsim < 2550)].index)
# df = df.drop(df[(df.Sim == 162) & (df.Tsim > 4100) & (df.Tsim < 4600)].index)
# df = df.drop(df[(df.Sim == 162) & (df.Tsim > 5450) & (df.Tsim < 5800)].index)
# df = df.drop(df[(df.Sim == 162) & (df.Tsim > 6100) & (df.Tsim < 6550)].index)
#
# df = df.drop(df[(df.Sim == 163) & (df.Tsim > 2100) & (df.Tsim < 2550)].index)
# df = df.drop(df[(df.Sim == 163) & (df.Tsim > 4100) & (df.Tsim < 4600)].index)
# df = df.drop(df[(df.Sim == 163) & (df.Tsim > 5450) & (df.Tsim < 5800)].index)
# df = df.drop(df[(df.Sim == 163) & (df.Tsim > 6100) & (df.Tsim < 6550)].index)
#
# df = df.drop(df[(df.Sim == 166) & (df.Tsim > 2200) & (df.Tsim < 2650)].index)
# df = df.drop(df[(df.Sim == 166) & (df.Tsim > 4200) & (df.Tsim < 4700)].index)
# df = df.drop(df[(df.Sim == 166) & (df.Tsim > 6200) & (df.Tsim < 6650)].index)
# df = df.drop(df[(df.Sim == 166) & (df.Tsim > 7550) & (df.Tsim < 7750)].index)
# df = df.drop(df[(df.Sim == 166) & (df.Team == 1) & (df.Tsim > 4400) & (df.Tsim < 5400)].index)

