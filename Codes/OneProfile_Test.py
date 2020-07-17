import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from Josie_Functions import  Calc_average_profile_pressure, Calc_average_profile_time, Calc_Dif, Calc_average_profileCurrent_pressure, Calc_average_Dif
from Josie_PlotFunctions import  errorPlot_ARDif_withtext, errorPlot_general
from Analyse_Functions import cuts2017, cuts0910


df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv_1607.csv", low_memory=False)

# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_deconv_final.csv", low_memory=False)

df = cuts2017(df)

simlist = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Sim'])
teamlist = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Team'])
# adx = np.asarray(df.drop_duplicates(['Sim', 'Team'])['ADX'])
sol = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Sol'].tolist())
buff = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Buf'])
ensci = np.asarray(df.drop_duplicates(['Sim', 'Team'])['ENSCI'])

for j in range(len(simlist)):


    if ensci[j] == 0:
        sondestr = 'SPC'
    else:
        sondestr = 'ENSCI'
    # if adx[j] == 1:
    #     adxstr = 'ADX'
    # else:
    #     adxstr = ''
    if sol[j] == 2.0: solstr = '2p0'
    if sol[j] == 1.0: solstr = '1p0'
    if sol[j] == 0.5: solstr = '0p5'

    if buff[j] == 0.1: bufstr = '0p1'
    if buff[j] == 0.5: bufstr = '0p5'
    if buff[j] == 1.0: bufstr = '1p0'

    title = str(simlist[j]) + '_' + str(teamlist[j])
            # + '_' + adxstr + sondestr + solstr + '-' + bufstr + 'B'
    type = sondestr + ' ' + str(sol[j]) + '\% - ' + str(buff[j]) + 'B'
    sp = str(simlist[j]) + '-' + str(teamlist[j])
    ptitle = sp + ' ' + sondestr + ' ' + str(sol[j]) + '% - ' + str(buff[j]) + 'B'
    print(title)

    dft = df[(df.Sim == simlist[j]) & (df.Team == teamlist[j])]
    dft = dft.reset_index()

    fig, ax = plt.subplots()
    ax.set_yscale('log')
    plt.title(title)
    plt.xlabel('Current')
    plt.ylabel('Pair')
    # plt.xlim([-50, 50])
    # plt.ylim([1000, 5])


    dft['rdifI'] = (dft['Ifast_minib0_deconv_sm8'] -  dft['IM'])/ dft['IM'] * 100

    plt.plot(dft.IM.rolling(window=4).mean(), dft.Tsim, label='IM')
    plt.plot(dft.I_slow_conv.rolling(window=4).mean(), dft.Tsim, label='Islow conv')
    plt.plot(dft.Ifast_minib0_deconv_sm8.rolling(window=4).mean(), dft.Tsim, label = 'I fast - ib0 deconv')
    plt.plot(dft.I_OPM_jma.rolling(window=4).mean(), dft.Tsim, label = 'I OPM jma')
    # plt.plot(dft.rdifI, dft.Tsim, label='(Ifast-ib0 deconv) - IM [%]')


    ax.legend(loc='best', frameon=False, fontsize='small')

    # plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Profile_PerSim/Dif_' + title + '.png')
    plt.show()
    plt.close()

