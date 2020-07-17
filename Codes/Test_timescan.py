import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from Josie_Functions import  Calc_average_profile_pressure, Calc_average_profile_time, Calc_Dif, Calc_average_profileCurrent_pressure, Calc_average_Dif
from Josie_PlotFunctions import  errorPlot_ARDif_withtext, errorPlot_general
from Analyse_Functions import cuts2017, cuts0910

df1 = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_deconv_beta0_tfast10_tempfixed_0907.csv", low_memory=False)
df2 = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_deconv_beta0_tfast15_tempfixed_0907.csv", low_memory=False)
df3 = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_deconv_beta0_tfast20_tempfixed_0907.csv", low_memory=False)
df4 = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_deconv_beta0_tfast25_tempfixed_0907.csv", low_memory=False)
df5 = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_deconv_beta0_tfast50.csv", low_memory=False)

# df = cuts0910(df)
df1 = cuts0910(df1)
df2 = cuts0910(df2)
df3 = cuts0910(df3)
df4 = cuts0910(df4)
df5 = cuts0910(df5)

simlist = np.asarray(df1.drop_duplicates(['Sim', 'Team'])['Sim'])
teamlist = np.asarray(df1.drop_duplicates(['Sim', 'Team'])['Team'])

simlist = [136]
teamlist = [1]
print('simlits', simlist)

for j in range(len(simlist)):

    print(j, str(simlist[j]) + '_' + str(teamlist[j]))
    title = str(simlist[j]) + '_' + str(teamlist[j])

    dft1 = df1[(df1.Sim == simlist[j]) & (df1.Team == teamlist[j])]
    dft2 = df2[(df2.Sim == simlist[j]) & (df2.Team == teamlist[j])]
    dft3 = df3[(df3.Sim == simlist[j]) & (df3.Team == teamlist[j])]
    dft4 = df4[(df4.Sim == simlist[j]) & (df4.Team == teamlist[j])]
    dft5 = df5[(df5.Sim == simlist[j]) & (df5.Team == teamlist[j])]

    #

    dft1['rdif'] = 100 * (dft1['Ifast_minib0_deconv_sm8'] - dft1['I_OPM_jma']) / dft1['I_OPM_jma']
    dft2['rdif'] = 100 * (dft2['Ifast_minib0_deconv_sm8'] - dft2['I_OPM_jma']) / dft2['I_OPM_jma']
    dft3['rdif'] = 100 * (dft3['Ifast_minib0_deconv_sm8'] - dft3['I_OPM_jma']) / dft3['I_OPM_jma']
    dft4['rdif'] = 100 *(dft4['Ifast_minib0_deconv_sm8'] - dft4['I_OPM_jma']) / dft4['I_OPM_jma']
    dft5['rdif'] = 100 *(dft5['Ifast_minib0_deconv_sm8'] - dft5['I_OPM_jma']) / dft5['I_OPM_jma']


    fig, ax = plt.subplots()

    plt.title(title)
    # plt.xlim([-40, 40])

    # plt.plot(dft4['rdif'], dft4['Pair'], label="25 secs")
    # plt.plot(dft3['rdif'], dft3['Pair'], label="20 secs")
    # plt.plot(dft2['rdif'], dft2['Pair'], label="15 secs")
    # plt.plot(dft1['rdif'], dft1['Pair'], label="10 secs")


    #
    plt.plot(dft5['Tsim'], dft5['Ifast_minib0_deconv_sm8'],  label="50 secs")
    plt.plot(dft4['Tsim'], dft4['Ifast_minib0_deconv_sm8'],  label="25 secs")
    plt.plot(dft3['Tsim'], dft3['Ifast_minib0_deconv_sm8'], label="20 secs")
    plt.plot(dft2['Tsim'], dft2['Ifast_minib0_deconv_sm8'], label="15 secs")
    plt.plot(dft1['Tsim'], dft1['Ifast_minib0_deconv_sm8'], label="10 secs")
    plt.plot(dft1['Tsim'], dft1['I_OPM_jma'], label="OPM")
    # # plt.plot(dft4['Tsim'], dft4['Ifast_minib0'], label=" I fast -ibo 25 secs")
    # plt.plot(dft3['Tsim'], dft3['Ifast_minib0'], label=" I fast -ibo")

    # plt.plot(dft4['Tsim'], dft4['Ifast_minib0_deconv'],  label="25 secs")
    # plt.plot(dft3['Tsim'], dft3['Ifast_minib0_deconv'], label="20 secs")
    # plt.plot(dft2['Tsim'], dft2['Ifast_minib0_deconv'], label="15 secs")
    # plt.plot(dft1['Tsim'], dft1['Ifast_minib0_deconv'], label="10 secs")
    # plt.plot(dft1['Tsim'], dft1['I_OPM_jma'], label="OPM")
    # plt.plot(dft4['Tsim'], dft4['Ifast_minib0'], label=" I fast -ibo 25 secs")
    # plt.plot(dft3['Tsim'], dft3['Ifast_minib0'], label=" I fast -ibo")
    # plt.plot(dft3['Tsim'], dft3['Ifast_minib0'].rolling(window=4).mean(), label=" I fast -ibo smoothed")





    ax.legend(loc='best', frameon=False, fontsize='small')
    # ax.set_yscale('log')

    # plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Time_scan_0910/TimeScan_PerSim_Rdif' + title + '.pdf')
    # plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Time_scan_0910/TimeScan_PerSim_Rdif' + title + '.png')

    plt.show()

    plt.close()
