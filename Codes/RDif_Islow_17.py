import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math


from Josie_Functions import  Calc_average_profile_pressure, Calc_average_profile_time, Calc_Dif, \
    Calc_average_profileCurrent_pressure, Calc_average_Dif, sst_filter17, Calc_average_Dif
from Josie_PlotFunctions import  errorPlot_ARDif_withtext, errorPlot_general
from Analyse_Functions import cuts2017

df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv_0510.csv", low_memory=False)
df = df[df['iB2'] >= -0.1]
df = df[df['iB1'] >= -0.1]


folderpath = 'Dif_Islow_17'

df = cuts2017(df)
prof, tot03 = sst_filter17(df)

## order of prof and tot03 arrays are always en0.50.5, en1010, sp0.50.5, sp1010
labellist_sst= ['EN 0.5%-0.5B','EN 1.0%-1.0B', 'SP 0.5%-0.5B', 'SP 1.0%-1.0B']
labellist_method= ['standard method', 'iB1', 'iB2']
#
adif_sim, adif_sim_err, rdif_sim, rdif_sim_err, Yp = Calc_average_Dif(prof, 'Ifast_deconv', 'I_OPM_jma','time')
adif_ib1, adif_ib1_err, rdif_ib1, rdif_ib1_err, Yp = Calc_average_Dif(prof, 'Ifast_deconv_ib1', 'I_OPM_jma', 'time')
adif_ib2, adif_ib2_err, rdif_ib2, rdif_ib2_err, Yp = Calc_average_Dif(prof, 'Ifast_deconv_ib2', 'I_OPM_jma', 'time')

# adif_sim, adif_sim_err, rdif_sim, rdif_sim_err, Yp = Calc_average_Dif(prof, 'Ifast_minib0_deconv', 'I_OPM_jma','time')
# adif_ib1, adif_ib1_err, rdif_ib1, rdif_ib1_err, Yp = Calc_average_Dif(prof, 'Ifast_minib0_deconv_ib1', 'I_OPM_jma', 'time')
# adif_ib2, adif_ib2_err, rdif_ib2, rdif_ib2_err, Yp = Calc_average_Dif(prof, 'Ifast_minib0_deconv_ib2', 'I_OPM_jma', 'time')



dimension = len(Yp)
nol = 4

print('adif_sim', type(adif_sim), len(adif_sim), adif_sim[0] )
#
#     A1verr = [[-9999.0] * dimension for i in range(nol)]
# adif = [[-9999.0] * dimension for i in range(nol)]; adif_err = [[-9999.0] * dimension for i in range(nol)]
# rdif = [[-9999.0] * dimension for i in range(nol)]; rdif_err = [[-9999.0] * dimension for i in range(nol)]
adif_err = [[0] * 5 for i in range(nol)]
adif = [[0] * 5 for i in range(nol)]
rdif_err = [[0] * 5 for i in range(nol)]
rdif = [[0] * 5 for i in range(nol)]

Ymin = [i/60 for i in Yp]
# print(len(adif_sim[0]))
# print(len(adif_sim))

for i in range(nol):

    adif[i] = [adif_sim[i], adif_ib1[i], adif_ib2[i]]

    rdif[i] = [rdif_sim[i], rdif_ib1[i], rdif_ib2[i]]
    adif_err[i] = [adif_sim_err[i], adif_ib1_err[i], adif_ib2_err[i]]
    rdif_err[i] = [rdif_sim_err[i], rdif_ib1_err[i], rdif_ib2_err[i]]

axtitlecur = r'Ifast(method)-I_OPM_JMA Difference ($\mu$A)'
rxtitlecur = 'Ifast(method)-I_OPM_JMA) Difference(%)'
rxtitlecurb = 'Sonde - OPM[Komhyr]smoothed  Difference (%)'
ytitle = 'Time (min.)'

errorPlot_ARDif_withtext(adif[0], adif_err[0], Ymin, [-0.5, 0.5], [0, 150],  '2017 Data ADif w.r.t. I OPM jma EN0.50.5',
                         axtitlecur, ytitle,labellist_method, tot03[0], prof[0].drop_duplicates(['Sim','Team']),'Ifast_ADif_en0.50.5', folderpath, False, False)

errorPlot_ARDif_withtext(adif[1], adif_err[1], Ymin, [-0.5, 0.5], [0, 150],  '2017 Data ADif w.r.t. I OPM jma EN1010',
                         axtitlecur, ytitle,labellist_method, tot03[1], prof[1].drop_duplicates(['Sim','Team']),'Ifast_ADif_en1010', folderpath, False, False)
I
errorPlot_ARDif_withtext(adif[2], adif_err[2], Ymin, [-0.5, 0.5], [0, 150],  '2017 Data ADif w.r.t. I OPM jma SP0.50.5',
                         axtitlecur, ytitle,labellist_method, tot03[2], prof[2].drop_duplicates(['Sim','Team']),'Ifast_ADif_sp0.50.5', folderpath, False, False)

errorPlot_ARDif_withtext(adif[3], adif_err[3], Ymin, [-0.5, 0.5], [0, 150],  '2017 Data ADif w.r.t. I OPM jma SP1010',
                         axtitlecur, ytitle,labellist_method, tot03[3], prof[3].drop_duplicates(['Sim','Team']),'Ifast_ADif_sp1010', folderpath, False, False)

errorPlot_ARDif_withtext(rdif[0], rdif_err[0], Ymin, [-25, 25], [0, 150],  '2017 Data RDif w.r.t. I OPM jma EN0.50.5',
                         rxtitlecur, ytitle,labellist_method, tot03[0], prof[0].drop_duplicates(['Sim','Team']),'Ifast_RDif_en0.50.5', folderpath, False, False)

errorPlot_ARDif_withtext(rdif[1], rdif_err[1], Ymin, [-25, 25], [0, 150],  '2017 Data RDif w.r.t. I OPM jma EN1010',
                         rxtitlecur, ytitle,labellist_method, tot03[1], prof[1].drop_duplicates(['Sim','Team']),'Ifast_RDif_en1010', folderpath, False, False)

errorPlot_ARDif_withtext(rdif[2], rdif_err[2], Ymin, [-25, 25], [0, 150],  '2017 Data RDif w.r.t. I OPM jma SP0.50.5',
                         rxtitlecur, ytitle,labellist_method, tot03[2], prof[2].drop_duplicates(['Sim','Team']),'Ifast_RDif_sp0.50.5', folderpath, False, False)

errorPlot_ARDif_withtext(rdif[3], rdif_err[3], Ymin, [-25, 25], [0, 150],  '2017 Data RDif w.r.t. I OPM jma SP1010',
                         rxtitlecur, ytitle,labellist_method, tot03[3], prof[3].drop_duplicates(['Sim','Team']),'Ifast_RDif_sp1010', folderpath, False, False)