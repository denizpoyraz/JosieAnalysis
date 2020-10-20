import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

from Josie_Functions import  Calc_average_profile_pressure, Calc_average_profile_time, Calc_Dif, \
    Calc_average_profileCurrent_pressure, Calc_average_Dif, sst_filter, Calc_average_Dif_2df
from Josie_PlotFunctions import  errorPlot_ARDif_withtext, errorPlot_general
from Analyse_Functions import cuts2017

def cuts0910(dfm):

    dfm = dfm.drop(dfm[(dfm.PO3 < 0)].index)
    dfm = dfm.drop(dfm[(dfm.PO3_OPM < 0)].index)

    dfm = dfm[dfm.ADX == 0]
    # # v2 cuts, use this and v3 standard more conservative cuts not valid for 140, 1122, 163, 166  v2
    # dfm=dfm[dfm.Tsim > 900]
    # dfm=dfm[dfm.Tsim <= 8100]
    dfm = dfm.drop(dfm[(dfm.Sim == 141) & (dfm.Team == 3)].index)
    # dfm = dfm.drop(dfm[(dfm.Sim == 143) & (dfm.Team == 2) & (dfm.Tsim > 7950) & (dfm.Tsim < 8100)].index)
    dfm = dfm.drop(dfm[(dfm.Sim == 147) & (dfm.Team == 3)].index)
    dfm = dfm.drop(dfm[(dfm.Sim == 158) & (dfm.Team == 2)].index)
    dfm = dfm.drop(dfm[(dfm.Sim == 167) & (dfm.Team == 4)].index)
    # ## new cuts v2 20/05
    # dfm = dfm.drop(dfm[(dfm.Sim == 160) & (dfm.Team == 4)].index)
    # dfm = dfm.drop(dfm[(dfm.Sim == 165) & (dfm.Team == 4)].index)

    # # ## v3 cuts
    ### I think these cuts are not needed## checkcheck
    dfm = dfm.drop(dfm[(dfm.Sim == 159) & (dfm.Team == 1)].index)
    dfm = dfm.drop(dfm[(dfm.Sim == 158) & (dfm.Team == 1)].index)
    dfm = dfm.drop(dfm[(dfm.Sim == 163) & (dfm.Team == 4)].index)
    dfm = dfm.drop(dfm[(dfm.Sim == 159) & (dfm.Team == 4)].index)

    return dfm

folderpath = 'Dif_Islow'

df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_Deconv_preparationadded_min_t.csv", low_memory=False)
dfo = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_Deconv_preparationadded_mino_t.csv", low_memory=False)

df = cuts0910(df)
df = df[df.Tsim_original >= 0]
dfo = cuts0910(dfo)

prof, tot03 = sst_filter(df)
profo, tot03o = sst_filter(dfo)

dt = [0] * 4
sdt = [0] * 4

for k in range(4):
    dt[k] = np.median(profo[k].decay_time)
    # sdt[k] = np.std(profo[k].decay_time)
    sdt[k] = 300
    prof[k] = prof[k][(prof[k].decay_time < dt[k] + sdt[k]) & (prof[k].decay_time > dt[k] -sdt[k])]
    profo[k] = profo[k][(profo[k].decay_time < dt[k] + sdt[k]) & (profo[k].decay_time > dt[k] -sdt[k])]

## order of prof and tot03 arrays are always en0505, en1010, sp0505, sp1010
labellist_sst= ['EN 0.5%-0.5B','EN 1.0%-1.0B', 'SP 0.5%-0.5B', 'SP 1.0%-1.0B']
labellist_method= ['standard method','I at time iB1 decay', 'iB1 decay', 'iB1', 'iB2']
# dfnplist = [profEN0505.drop_duplicates(['Sim', 'Team']), profEN1010.drop_duplicates(['Sim', 'Team']), profSP0505_nodup,
#         profSP1010_nodup]

print('decay times', np.mean(profo[0].decay_time), np.mean(profo[1].decay_time), np.mean(profo[2].decay_time), np.mean(profo[3].decay_time) )
print('decay times', np.median(profo[0].decay_time), np.median(profo[1].decay_time), np.median(profo[2].decay_time), np.median(profo[3].decay_time) )
print('std decay times', np.std(profo[0].decay_time), np.std(profo[1].decay_time), np.std(profo[2].decay_time), np.std(profo[3].decay_time) )


print('decay times', np.mean(dfo.decay_time), np.mean(df.decay_time))


# def Calc_average_Dif_2df(dataframelist, dfref,  xcolumn, refcolumn,  stringy):

# adif_sim, adif_sim_err, rdif_sim, rdif_sim_err, Yp = Calc_average_Dif_2df(profo, prof, 'I_slow_convo', 'I_slow_conv','time')
# adif_exp, adif_exp_err, rdif_exp, rdif_exp_err, Yp = Calc_average_Dif_2df(profo, prof, 'I_slow_conv_tesths', 'I_slow_conv', 'time')
# adif_ib1decay, adif_ib1decay_err, rdif_ib1decay, rdif_ib1decay_err, Yp = Calc_average_Dif_2df(profo, prof, 'I_slow_conv_ib1_decay', 'I_slow_conv', 'time')
# adif_ib1, adif_ib1_err, rdif_ib1, rdif_ib1_err, Yp = Calc_average_Dif_2df(profo, prof, 'I_slow_conv_testib1', 'I_slow_conv', 'time')
# adif_ib2, adif_ib2_err, rdif_ib2, rdif_ib2_err, Yp = Calc_average_Dif_2df(profo, prof, 'I_slow_conv_testib2', 'I_slow_conv', 'time')
#
adif_sim, adif_sim_err, rdif_sim, rdif_sim_err, Yp = Calc_average_Dif_2df(profo, prof, 'Ifast_deconvo', 'I_OPM_jma','time')
adif_exp, adif_exp_err, rdif_exp, rdif_exp_err, Yp = Calc_average_Dif_2df(profo, prof, 'Ifast_deconv_tesths', 'I_OPM_jma', 'time')
adif_ib1decay, adif_ib1decay_err, rdif_ib1decay, rdif_ib1decay_err, Yp = Calc_average_Dif_2df(profo, prof, 'Ifast_deconv_ib1_decay', 'I_OPM_jma', 'time')
adif_ib1, adif_ib1_err, rdif_ib1, rdif_ib1_err, Yp = Calc_average_Dif_2df(profo, prof, 'Ifast_deconv_testib1', 'I_OPM_jma', 'time')
adif_ib2, adif_ib2_err, rdif_ib2, rdif_ib2_err, Yp = Calc_average_Dif_2df(profo, prof, 'Ifast_deconv_testib2', 'I_OPM_jma', 'time')

dimension = len(Yp)
nol = 4

print('adif_sim', type(adif_sim), len(adif_sim), adif_sim[0] )
#
#     A1verr = [[-9999.0] * dimension for i in range(nol)]
# adif = [[-9999.0] * dimension for i in range(nol)]; adif_err = [[-9999.0] * dimension for i in range(nol)]
# rdif = [[-9999.0] * dimension for i in range(nol)]; rdif_err = [[-9999.0] * dimension for i in range(nol)]
adif_err = [[0] * 5 for i in range(4)]
adif = [[0] * 5 for i in range(4)]
rdif_err = [[0] * 5 for i in range(4)]
rdif = [[0] * 5 for i in range(4)]

Ymin = [i/60 for i in Yp]
# print(len(adif_sim[0]))
# print(len(adif_sim))

for i in range(nol):

    adif[i] = [adif_sim[i], adif_exp[i], adif_ib1decay[i], adif_ib1[i], adif_ib2[i]]

    rdif[i] = [rdif_sim[i], rdif_exp[i], rdif_ib1decay[i], rdif_ib1[i], rdif_ib2[i]]
    adif_err[i] = [adif_sim_err[i], adif_exp_err[i], adif_ib1decay_err[i], adif_ib1_err[i], adif_ib2_err[i]]
    rdif_err[i] = [rdif_sim_err[i], rdif_exp_err[i], rdif_ib1decay_err[i], rdif_ib1_err[i], rdif_ib2_err[i]]


axtitlecur = r'Ifast(method)-I_OPM_JMA Difference ($\mu$A)'
rxtitlecur = 'Ifast(method)-I_OPM_JMA) Difference(%)'

# axtitlecur = r'Islow(method)- reference method Difference ($\mu$A)'
# rxtitlecur = 'Islow(method)- reference method Difference(%)'
rxtitlecurb = 'Sonde - OPM[Komhyr]smoothed  Difference (%)'
ytitle = 'Time (min.)'

print(len(adif[0]), len(adif_err[0]), len(Ymin) )


#
errorPlot_ARDif_withtext(adif[0], adif_err[0], Ymin, [-0.3, 0.3], [0, 150],  '0910 Data ADif w.r.t. correct I slow conv. EN0505',
                         axtitlecur, ytitle,labellist_method, tot03[0], prof[0].drop_duplicates(['Sim','Team']),'DecayTime_median300secs_Ifast_ADif_en0505', folderpath, False, False)

errorPlot_ARDif_withtext(adif[1], adif_err[1], Ymin, [-0.3, 0.3], [0, 150],  '0910 Data ADif w.r.t. correct I slow conv. EN1010',
                         axtitlecur, ytitle,labellist_method, tot03[1], prof[1].drop_duplicates(['Sim','Team']),'DecayTime_median300secs_Ifast_ADif_en1010', folderpath, False, False)

errorPlot_ARDif_withtext(adif[2], adif_err[2], Ymin, [-0.3, 0.3], [0, 150],  '0910 Data ADif w.r.t. correct I slow conv. SP0505',
                         axtitlecur, ytitle,labellist_method, tot03[2], prof[2].drop_duplicates(['Sim','Team']),'DecayTime_median300secs_Ifast_ADif_sp0505', folderpath, False, False)

errorPlot_ARDif_withtext(adif[3], adif_err[3], Ymin, [-0.3, 0.3], [0, 150],  '0910 Data ADif w.r.t. correct I slow conv. SP1010',
                         axtitlecur, ytitle,labellist_method, tot03[3], prof[3].drop_duplicates(['Sim','Team']),'DecayTime_median300secs_Ifast_ADif_sp1010', folderpath, False, False)

errorPlot_ARDif_withtext(rdif[0], rdif_err[0], Ymin, [-100, 100], [0, 150],  '0910 Data RDif w.r.t. correct I slow conv. EN0505',
                         rxtitlecur, ytitle,labellist_method, tot03[0], prof[0].drop_duplicates(['Sim','Team']),'DecayTime_median300secs_Ifast_RDif_en0505', folderpath, False, False)

errorPlot_ARDif_withtext(rdif[1], rdif_err[1], Ymin, [-100, 100], [0, 150],  '0910 Data RDif w.r.t. correct I slow conv. EN1010',
                         rxtitlecur, ytitle,labellist_method, tot03[1], prof[1].drop_duplicates(['Sim','Team']),'DecayTime_median300secs_Ifast_RDif_en1010', folderpath, False, False)

errorPlot_ARDif_withtext(rdif[2], rdif_err[2], Ymin, [-100, 100], [0, 150],  '0910 Data RDif w.r.t. correct I slow conv. SP0505',
                         rxtitlecur, ytitle,labellist_method, tot03[2], prof[2].drop_duplicates(['Sim','Team']),'DecayTime_median300secs_Ifast_RDif_sp0505', folderpath, False, False)

errorPlot_ARDif_withtext(rdif[3], rdif_err[3], Ymin, [-100, 100], [0, 150],  '0910 Data RDif w.r.t. correct I slow conv. SP1010',
                         rxtitlecur, ytitle,labellist_method, tot03[3], prof[3].drop_duplicates(['Sim','Team']),'DecayTime_median300secs_Ifast_RDif_sp1010', folderpath, False, False)
# #
# #

########## for all the profile

# now plot averaged I fast, Ifats deconv, I OPM plots to see the effect of the shift

# adif_sim, adif_sim_err, rdif_sim, rdif_sim_err, Yp = Calc_average_Dif_2df(profo, prof, 'Ifast_deconvo', 'I_OPM_jma','time')
#adif_ib1decay, adif_ib1decay_err, rdif_ib1decay, rdif_ib1decay_err, Yp = Calc_average_Dif_2df(profo, prof, 'Ifast_deconv_ib1_decay', 'I_OPM_jma', 'time')

#
Ifast_ib1, Ifast_ib1_err, OPM, OPM_err, Yf = Calc_average_profile_time(profo,prof,  'Ifast_deconv_ib1_decay', 'I_OPM_jma', 'Tsim_original', 400, 50, 10000, 1)
Ifast_minib0_ib1_decay, Ifast_minib0_ib1_err, Yf = Calc_average_profile_time(profo, prof,  'Ifast_minib0_deconv_ib1_decay', 'I_OPM_jma', 'Tsim_original', 400, 50, 10000, 0)
Ifast_sim, Ifast_sim_err, Yf = Calc_average_profile_time(profo, prof,  'Ifast_deconvo', 'I_OPM_jma', 'Tsim_original', 400, 50, 10000, 0)
Ifast_minib0_sim, Ifast_minib0_sim_err, Yf = Calc_average_profile_time(profo, prof,  'Ifast_minib0_deconvo', 'I_OPM_jma', 'Tsim_original', 400, 50, 10000, 0)

# ifast_ib1_err = [[0] * 5 for i in range(4)]
# ifast_ib1 = [[0] * 5 for i in range(4)]
# ifast_minib0_ib1_err = [[0] * 5 for i in range(4)]
# ifast_minib0_ib1 = [[0] * 5 for i in range(4)]
# ifast_sim_err = [[0] * 5 for i in range(4)]
# ifast_sim = [[0] * 5 for i in range(4)]
# ifast_sim_err = [[0] * 5 for i in range(4)]
# ifast_sim = [[0] * 5 for i in range(4)]

all = [[0] * 5 for i in range(4)]
all_err = [[0] * 5 for i in range(4)]


Ymin = [i/60 for i in Yp]
# print(len(adif_sim[0]))
# print(len(adif_sim))

# labellist_all = ['Ifast_ib1decay', 'Ifastminib0_ib1decay', 'ifast_sim', 'ifast_minib0_sim', 'OPM']
#
# Yminf = [i/60 for i in Yf]
#
# axtitlecurall = r'Ifast(method)($\mu$A)'
#
# for i in range(nol):
#
#     all[i] = [Ifast_ib1[i], Ifast_minib0_ib1_decay[i], Ifast_sim[i], Ifast_minib0_sim[i], OPM[i]]
#     all_err[i] = [Ifast_ib1_err[i], Ifast_minib0_ib1_err[i], Ifast_sim_err[i], Ifast_minib0_sim_err[i], OPM_err[i]]
#
# errorPlot_ARDif_withtext(all[0], all_err[0], Yminf, [0,8], [0, 150],  '0910 Data EN0505',
#                          axtitlecurall, ytitle,labellist_all, tot03[0], prof[0].drop_duplicates(['Sim','Team']),'DecayTime_median300secs_IfastAll_en0505', folderpath, False, False)
#
# errorPlot_ARDif_withtext(all[1], all_err[1], Yminf, [0,8], [0, 150],  '0910 Data EN1010',
#                          axtitlecurall, ytitle,labellist_all, tot03[1], prof[1].drop_duplicates(['Sim','Team']),'DecayTime_median300secs_IfastAll_en1010', folderpath, False, False)
#
# errorPlot_ARDif_withtext(all[2], all_err[2], Yminf, [0,8], [0, 150],  '0910 Data SP0505',
#                          axtitlecurall, ytitle,labellist_all, tot03[2], prof[2].drop_duplicates(['Sim','Team']),'DecayTime_median300secs_IfastAll_sp0505', folderpath, False, False)
#
# errorPlot_ARDif_withtext(all[3], all_err[3], Yminf, [0,8], [0, 150],  '0910 Data SP0505',
#                          axtitlecurall, ytitle,labellist_all, tot03[3], prof[3].drop_duplicates(['Sim','Team']),'DecayTime_median300secs_IfastAll_sp1010', folderpath, False, False)
#
# print(len(all[0][0]), len(all_err[0]), len(Yminf) )
# # errorPlot_ARDif_withtext(all[0], all_err[0], Yminf, [-100, 100], [0, 150],  '0910 Data RDif w.r.t. correct I slow conv. SP1010',
# #                          rxtitlecur, ytitle,labellist_method, tot03[3], prof[0].drop_duplicates(['Sim','Team']),'DecayTime_median300secs_Islow_RDif_sp1010', folderpath, False, False)
# # #