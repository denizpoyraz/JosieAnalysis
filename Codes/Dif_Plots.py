import pandas as pd
import matplotlib.pyplot as plt

from Josie_Functions import  Calc_averageCurrent_Dif, Calc_average_profile_pressure, Calc_average_profile_time, Calc_Dif, Calc_average_profileCurrent_pressure, Calc_average_profileCurrent_time
from Josie_PlotFunctions import  errorPlot_ARDif_withtext, errorPlot_general


folderpath = 'Dif_2009_debug'


# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie_deconv_beta0alldata.csv", low_memory=False)
df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_deconv_beta2ib0.csv", low_memory=False)

print(list(df))

df = df.drop(df[(df.PO3 < 0)].index)
df = df.drop(df[(df.PO3_OPM < 0)].index)
df = df[df.ADX == 0]

test = df.drop_duplicates(['Sim', 'Team'])
print(len(test))

## cuts for 0910
df=df[df.Tsim > 900]
df=df[df.Tsim <= 8100]

# df = df.drop(df[(df.Sim == 141) & (df.Team == 3)].index)
# df = df.drop(df[(df.Sim == 143) & (df.Team == 2) & (df.Tsim > 7950) & (df.Tsim < 8100)].index)
# df = df.drop(df[(df.Sim == 147) & (df.Team == 3)].index)
# df = df.drop(df[(df.Sim == 158) & (df.Team == 2)].index)
# df = df.drop(df[(df.Sim == 167) & (df.Team == 4)].index)
# ## new cuts v2 20/05
# df = df.drop(df[(df.Sim == 160) & (df.Team == 4)].index)
# df = df.drop(df[(df.Sim == 165) & (df.Team == 4)].index)
#
# # # ## v3 cuts
# ### I think these cuts are not needed## checkcheck
# df = df.drop(df[(df.Sim == 159) & (df.Team == 1)].index) ##??
# df = df.drop(df[(df.Sim == 158) & (df.Team == 1)].index)
# df = df.drop(df[(df.Sim == 163) & (df.Team == 4)].index)
# df = df.drop(df[(df.Sim == 159) & (df.Team == 4)].index)

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

ytitle = 'Pressure (hPa)'

###############################################
# Filters for Sonde, Solution, Buff er selection
# 1, 0.1 ENSCI vs SPC
filtEN = df.ENSCI == 1
filtSP = df.ENSCI == 0

filtS10 = df.Sol == 1
filtS05 = df.Sol == 0.5

filtB10 = df.Buf == 1.0
filtB05 = df.Buf == 0.5

filterEN0505 = (filtEN & filtS05 & filtB05)
filterEN1010 = (filtEN & filtS10 & filtB10)

profEN0505 = df.loc[filterEN0505]
profEN1010 = df.loc[filterEN1010]

profEN0505_nodup = profEN0505.drop_duplicates(['Sim', 'Team'])
profEN1010_nodup = profEN1010.drop_duplicates(['Sim', 'Team'])

print(profEN0505_nodup[['Sim','Team']])

totO3_EN0505 = profEN0505_nodup.frac.mean()
totO3_EN1010 = profEN1010_nodup.frac.mean()


filterSP1010 = (filtSP & filtS10 & filtB10)
filterSP0505 = (filtSP & filtS05 & filtB05)

profSP1010 = df.loc[filterSP1010]
profSP0505 = df.loc[filterSP0505]

profSP1010_nodup = profSP1010.drop_duplicates(['Sim', 'Team'])
profSP0505_nodup = profSP0505.drop_duplicates(['Sim', 'Team'])

totO3_SP1010 = profSP1010_nodup.frac.mean()
totO3_SP0505 = profSP0505_nodup.frac.mean()




### Plotting
axtitle_nojma = 'Sonde - OPM  Difference (mPa)'
axtitle = 'Sonde[JMA] - OPM  Difference (mPa)'

rxtitle_nojma = 'Sonde - OPM  Difference (%)'
rxtitle = 'Sonde[JMA] - OPM  Difference (%)'

axtitlecur = r'Sonde - OPM[JMA]  Difference ($\mu$A)'
rxtitlecur = 'Sonde - OPM[JMA]  Difference (%)'


labellist = ['EN 0.5%-0.5B','EN 1.0%-1.0B', 'SP 0.5%-0.5B', 'SP 1.0%-1.0B']
o3list = [totO3_EN0505, totO3_EN1010,  totO3_SP0505, totO3_SP1010]
dfnplist = [profEN0505.drop_duplicates(['Sim', 'Team']), profEN1010.drop_duplicates(['Sim', 'Team']), profSP0505_nodup,
            profSP1010_nodup]


adif_IM, adif_IM_err, rdif_IM, rdif_IM_err, Yp = Calc_averageCurrent_Dif([profEN0505, profEN1010, profSP0505, profSP1010], 'IM', 'I_OPM_jma',  'pressure')

adif_PO3, adif_PO3_err, rdif_PO3, rdif_PO3_err, Yp = Calc_averageCurrent_Dif([profEN0505, profEN1010, profSP0505, profSP1010], 'PO3', 'PO3_OPM',  'pressure')

adif_ifdcsm, adif_ifdcsm_err, rdif_ifdcsm, rdif_ifdcsm_err, Yp = Calc_averageCurrent_Dif([profEN0505, profEN1010, profSP0505, profSP1010], 'I_fast_deconv_sm6', 'I_OPM_jma',  'pressure')
adif_ifdcsmib0, adif_ifdcsmib0_err, rdif_ifdcsmib0, rdif_ifdcsmib0_err, Yp = Calc_averageCurrent_Dif([profEN0505, profEN1010, profSP0505, profSP1010], 'Ifast_minib0_deconv_sm6', 'I_OPM_jma',  'pressure')



errorPlot_ARDif_withtext(rdif_IM, rdif_IM_err, Yp, [-40, 40], [1000,5],  '0910 Data (Current)',  rxtitlecur, ytitle, labellist, o3list, dfnplist,
                           'debug_Rdif_im', folderpath ,  True, False)

errorPlot_ARDif_withtext(rdif_PO3, rdif_PO3_err, Yp, [-40, 40], [1000,5],  '0910 Data (Pressure)',  rxtitle_nojma, ytitle, labellist, o3list, dfnplist,
                           'debug_Rdif_po3', folderpath ,  True, False)

errorPlot_ARDif_withtext(rdif_ifdcsm, rdif_ifdcsm_err, Yp, [-40, 40], [1000,5],  '0910 Data (Current deconv smoothed 6 secs.)',  rxtitlecur, ytitle, labellist, o3list, dfnplist,
                           'debug_Rdif_ifastdeconv', folderpath ,  True, False)

errorPlot_ARDif_withtext(rdif_ifdcsmib0, rdif_ifdcsmib0_err, Yp, [-40, 40], [1000,5],  '0910 Data (Current - ib0 deconv smoothed 6 secs.)',  rxtitlecur, ytitle, labellist, o3list, dfnplist,
                           'debug_Rdif_ifastdeconv_miniB0', folderpath ,  True, False)