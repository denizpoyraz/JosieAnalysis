import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from Josie_Functions import  Calc_average_profile_pressure, Calc_average_profile_time, Calc_Dif, Calc_average_profileCurrent_pressure, Calc_average_Dif
from Josie_PlotFunctions import  errorPlot_ARDif_withtext, errorPlot_general
from Analyse_Functions import cuts2017, cuts0910



# folderpath = 'Beta_scan_17_fixed'
# folderpath = 'Beta_scan_0910_fixed'
folderpath = 'Time_scan_0910'


# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_deconv_beta0_original_tempfixed.csv", low_memory=False)
# df0 = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_deconv_beta0_0_tempfixed.csv", low_memory=False)
# df1 = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv_beta0_1_tempfixed_paper.csv", low_memory=False)
# df2 = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv_beta0_2_tempfixed_paper.csv", low_memory=False)
# df3 = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv_beta0_3_tempfixed_paper.csv", low_memory=False)
# df4 = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv_beta0_4_tempfixed_paper.csv", low_memory=False)
# df5 = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv_beta0_5_tempfixed_paper.csv", low_memory=False)
# df6 = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv_beta0_6_tempfixed_paper.csv", low_memory=False)

# df1 = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv_beta0_1_tempfixed_0907.csv", low_memory=False)
# df2 = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv_beta0_2_tempfixed_0907.csv", low_memory=False)
# df3 = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv_beta0_3_tempfixed_0907.csv", low_memory=False)
# df4 = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv_beta0_4_tempfixed_0907.csv", low_memory=False)
# df5 = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv_beta0_5_tempfixed_0907.csv", low_memory=False)
# df6 = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv_beta0_6_tempfixed_0907.csv", low_memory=False)

df1 = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_deconv_beta0_tfast10_tempfixed_0907.csv", low_memory=False)
df2 = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_deconv_beta0_tfast15_tempfixed_0907.csv", low_memory=False)
df3 = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_deconv_beta0_tfast20_tempfixed_0907.csv", low_memory=False)
df4 = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_deconv_beta0_tfast25_tempfixed_0907.csv", low_memory=False)




# df = cuts0910(df)
df1 = cuts0910(df1)
df2 = cuts0910(df2)
df3 = cuts0910(df3)
df4 = cuts0910(df4)
# df5 = cuts2017(df5)
# df6 = cuts2017(df6)




# filtEN = df.ENSCI == 1
# filtSP = df.ENSCI == 0
# filtS10 = df.Sol == 1
# filtS05 = df.Sol == 0.5
# filtB01 = df.Buf == 0.1
# filtB05 = df.Buf == 0.5
# filtB10 = df.Buf == 1.0

# filtEN_0 = df0.ENSCI == 1
# filtSP_0 = df0.ENSCI == 0
# filtS10_0 = df0.Sol == 1
# filtS05_0 = df0.Sol == 0.5
# filtB01_0 = df0.Buf == 0.1
# filtB05_0 = df0.Buf == 0.5
# filtB10_0 = df0.Buf == 1.0

# filterEN0505 = (filtEN & filtS05 * filtB05)
# filterEN0505_0 = (filtEN_0 & filtS05_0 * filtB05_0)
#
# filterEN1010 = (filtEN & filtS10 * filtB10)
# filterEN1010_0 = ((df0.ENSCI == 1) & (df0.Sol == 1.0) & (df0.Buf == 1.0))
filterEN1010_1 = ((df1.ENSCI == 1) & (df1.Sol == 1.0) & (df1.Buf == 1.0))
filterEN1010_2 = ((df2.ENSCI == 1) & (df2.Sol == 1.0) & (df2.Buf == 1.0))
filterEN1010_3 = ((df3.ENSCI == 1) & (df3.Sol == 1.0) & (df3.Buf == 1.0))
filterEN1010_4 = ((df4.ENSCI == 1) & (df4.Sol == 1.0) & (df4.Buf == 1.0))
# filterEN1010_5 = ((df5.ENSCI == 1) & (df5.Sol == 1.0) & (df5.Buf == 1.0))
# filterEN1010_6 = ((df6.ENSCI == 1) & (df6.Sol == 1.0) & (df6.Buf == 1.0))

# #2017
# filterEN1010 = (filtEN & filtS10 & filtB01)
# filterEN1010_1 = ((df1.ENSCI == 1) & (df1.Sol == 1.0) & (df1.Buf == 0.1))
# filterEN1010_2 = ((df2.ENSCI == 1) & (df2.Sol == 1.0) & (df2.Buf == 0.1))
# filterEN1010_3 = ((df3.ENSCI == 1) & (df3.Sol == 1.0) & (df3.Buf == 0.1))
# filterEN1010_4 = ((df4.ENSCI == 1) & (df4.Sol == 1.0) & (df4.Buf == 0.1))
# filterEN1010_5 = ((df5.ENSCI == 1) & (df5.Sol == 1.0) & (df5.Buf == 0.1))
# filterEN1010_6 = ((df6.ENSCI == 1) & (df6.Sol == 1.0) & (df6.Buf == 0.1))


# filterEN1001 = (filtEN & filtS10 & filtB01)
#
# filterSP0505 = (filtSP & filtS05 & filtB05)
# filterSP0505_0 = ((df0.ENSCI == 0) & (df0.Sol == 0.5) & (df0.Buf == 0.5))
filterSP0505_1 = ((df1.ENSCI == 0) & (df1.Sol == 0.5) & (df1.Buf == 0.5))
filterSP0505_2 = ((df2.ENSCI == 0) & (df2.Sol == 0.5) & (df2.Buf == 0.5))
filterSP0505_3 = ((df3.ENSCI == 0) & (df3.Sol == 0.5) & (df3.Buf == 0.5))
filterSP0505_4 = ((df4.ENSCI == 0) & (df4.Sol == 0.5) & (df4.Buf == 0.5))
# filterSP0505_5 = ((df5.ENSCI == 0) & (df5.Sol == 0.5) & (df5.Buf == 0.5))
# filterSP0505_6 = ((df6.ENSCI == 0) & (df6.Sol == 0.5) & (df6.Buf == 0.5))

# ## 2017
# filterSP0505 = (filtSP & filtS10 & filtB01)
# filterSP0505_1 = ((df1.ENSCI == 0) & (df1.Sol == 1.0) & (df1.Buf == 0.1))
# filterSP0505_2 = ((df2.ENSCI == 0) & (df2.Sol == 1.0) & (df2.Buf == 0.1))
# filterSP0505_3 = ((df3.ENSCI == 0) & (df3.Sol == 1.0) & (df3.Buf == 0.1))
# filterSP0505_4 = ((df4.ENSCI == 0) & (df4.Sol == 1.0) & (df4.Buf == 0.1))
# filterSP0505_5 = ((df5.ENSCI == 0) & (df5.Sol == 1.0) & (df5.Buf == 0.1))
# filterSP0505_6 = ((df6.ENSCI == 0) & (df6.Sol == 1.0) & (df6.Buf == 0.1))
#

# filterSP1010 = (filtSP & filtS10 & filtB10)
# filterSP1010_0 = ((df0.ENSCI == 0) & (df0.Sol == 1.0) & (df0.Buf == 1.0))
filterSP1010_1 = ((df1.ENSCI == 0) & (df1.Sol == 1.0) & (df1.Buf == 1.0))
filterSP1010_2 = ((df2.ENSCI == 0) & (df2.Sol == 1.0) & (df2.Buf == 1.0))
filterSP1010_3 = ((df3.ENSCI == 0) & (df3.Sol == 1.0) & (df3.Buf == 1.0))
filterSP1010_4 = ((df4.ENSCI == 0) & (df4.Sol == 1.0) & (df4.Buf == 1.0))
# filterSP1010_5 = ((df5.ENSCI == 0) & (df5.Sol == 1.0) & (df5.Buf == 1.0))
# filterSP1010_6 = ((df6.ENSCI == 0) & (df6.Sol == 1.0) & (df6.Buf == 1.0))


# filterSP1001 = (filtSP & filtS10 & filtB01)

profEN0505 = [ df1[(df1.ENSCI == 1) & (df1.Sol == 0.5) & (df1.Buf == 0.5)], df2[(df2.ENSCI == 1) & (df2.Sol == 0.5) & (df2.Buf == 0.5)],
               df3[(df3.ENSCI == 1) & (df3.Sol == 0.5) & (df3.Buf == 0.5)] , df4[(df4.ENSCI == 1) & (df4.Sol == 0.5) & (df4.Buf == 0.5)]]
# ,
    #            df5[(df5.ENSCI == 1) & (df5.Sol == 0.5) & (df5.Buf == 0.5)], df6[(df6.ENSCI == 1) & (df6.Sol == 0.5) & (df6.Buf == 0.5)]]

profEN1010 = [ df1[filterEN1010_1], df2[filterEN1010_2], df3[filterEN1010_3] , df4[filterEN1010_4]]
# ,df5[filterEN1010_5], df6[filterEN1010_6]]

profSP0505 = [  df1[filterSP0505_1], df2[filterSP0505_2], df3[filterSP0505_3], df4[filterSP0505_4]]
# ,df5[filterSP0505_5], df6[filterSP0505_6]]
profSP1010 = [  df1[filterSP1010_1], df2[filterSP1010_2], df3[filterSP1010_3]  , df4[filterSP1010_4]]
# ,df5[filterSP1010_5], df6[filterSP1010_6]]

adif_IM_deconv_en0505, adif_IM_deconv_en0505_err, rdif_IM_deconv_en0505, rdif_IM_deconv_en0505_err, Yp = \
    Calc_average_Dif(profEN0505, 'Ifast_minib0_deconv_sm8', 'I_OPM_jma',  'pressure')

adif_IM_deconv_en1010, adif_IM_deconv_en1010_err, rdif_IM_deconv_en1010, rdif_IM_deconv_en1010_err, Yp = \
    Calc_average_Dif(profEN1010, 'Ifast_minib0_deconv_sm8', 'I_OPM_jma',  'pressure')

adif_IM_deconv_sp0505, adif_IM_deconv_sp0505_err, rdif_IM_deconv_sp0505, rdif_IM_deconv_sp0505_err, Yp = \
    Calc_average_Dif(profSP0505, 'Ifast_minib0_deconv_sm8', 'I_OPM_jma',  'pressure')

adif_IM_deconv_sp1010, adif_IM_deconv_sp1010_err, rdif_IM_deconv_sp1010, rdif_IM_deconv_sp1010_err, Yp = \
    Calc_average_Dif(profSP1010, 'Ifast_minib0_deconv_sm8', 'I_OPM_jma',  'pressure')

# labellist = ['beta=0', 'beta=0.005', 'beta=0.010', 'beta=0.015', 'beta=0.020', 'beta=0.025', 'beta=0.030' ]
# labellist_0505 = ['beta0=0.005', 'beta0=0.010', 'beta0=0.015', 'beta0=0.020', 'beta0=0.025', 'beta0=0.030' ]
# labellist_1010 = ['beta0=0.025', 'beta0=0.035', 'beta0=0.045', 'beta0=0.055', 'beta0=0.065', 'beta0=0.075' ]
# labellist_1001 = ['beta0=0.001', 'beta0=0.015', 'beta0=0.02', 'beta0=0.025', 'beta0=0.03', 'beta0=0.035' ]
labellist_0505 = ['tfast=10 sec', 'tfast=15 sec.', 'tfast=20 min.', 'tfast=25 min.']
labellist_1010 = ['tfast=10 sec', 'tfast=15 sec.', 'tfast=20 min.', 'tfast=25 min.']
labellist_1001 = ['tfast=10 sec', 'tfast=15 sec.', 'tfast=20 min.', 'tfast=25 min.']

# , 'beta=0.015', 'beta=0.020', 'beta=0.025', 'beta=0.030' ]

colorlist = ['#1f77b4', '#ff7f0e', '#2ca02c' ,'#d62728']
# , '#9467bd', '#8c564b', '#e377c2']

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

axtitlecur = r'Sonde - OPM[JMA]  Difference ($\mu$A)'
rxtitlecur = 'Sonde - OPM[JMA]  Difference (%)'
rxtitlecurb = 'Sonde - OPM[JMA] smoothed  Difference (%)'

# errorPlot_ARDif_withtext(rdif_IM_deconv8, rdif_IM_deconv8_err, Yp, [-40, 40], [1000,5],  '0910 Data Conv-Deconv (Current Smoothed 8 secs)',
#                          rxtitlecur, ytitle,labellist, [0], [0],'SP_smoothed8', folderpath, True, False)

errorPlot_general(rdif_IM_deconv_en0505, rdif_IM_deconv_en0505_err, Yp, [-20, 20], [1000,5],  '0910 Data Conv-Deconv (Current - iB0 Smoothed 8 secs) ENSCI 0.5%-0.5',
                         rxtitlecur, ytitle,labellist_0505, colorlist, 'tfast_EN0505_smoothed8', folderpath, True, False, False)
#
errorPlot_general(rdif_IM_deconv_en1010, rdif_IM_deconv_en1010_err, Yp, [-20, 20], [1000,5],  '0910 Data Conv-Deconv (Current - iB0 Smoothed 8 secs) ENSCI 1.0%-1.0',
                         rxtitlecur, ytitle,labellist_1010, colorlist, 'tfastEN1010_smoothed8', folderpath, True, False, False)

# errorPlot_general(rdif_IM_deconv_en1010, rdif_IM_deconv_en1010_err, Yp, [-20, 20], [1000,5],  '0910 Data Conv-Deconv (Current Smoothed 8 secs) ENSCI 1.0%-0.1',
#                          rxtitlecur, ytitle,labellist_1001, colorlist, 'tfast_EN1001_smoothed8', folderpath, True, False, False)

errorPlot_general(rdif_IM_deconv_sp0505, rdif_IM_deconv_sp0505_err, Yp, [-20, 20], [1000,5],  '0910 Data Conv-Deconv (Current - iB0 Smoothed 8 secs) SP 0.5%-0.5',
                         rxtitlecur, ytitle,labellist_0505, colorlist, 'tfastSP0505_smoothed8', folderpath, True, False, False)

# errorPlot_general(rdif_IM_deconv_sp0505, rdif_IM_deconv_sp0505_err, Yp, [-20, 20], [1000,5],  '0910 Data Conv-Deconv (Current Smoothed 8 secs) SP 1.0%-0.1',
#                          rxtitlecur, ytitle,labellist_1001, colorlist, 'tfast_SP1001_smoothed8', folderpath, True, False, False)


errorPlot_general(rdif_IM_deconv_sp1010, rdif_IM_deconv_sp1010_err, Yp, [-20, 20], [1000,5],  '0910 Data Conv-Deconv (Current - iB0 Smoothed 8 secs) SP 1.0%-1.0',
                         rxtitlecur, ytitle,labellist_1010, colorlist, 'tfast_SP1010_smoothed8', folderpath, True, False, False)




