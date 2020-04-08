import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pickle

df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv.csv", low_memory=False)

# df = df[df.ADX == 0]
## apply cuts here

simlist = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Sim'])
teamlist = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Team'])
# adx = np.asarray(df.drop_duplicates(['Sim', 'Team'])['ADX'])
sol = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Sol'].tolist())
buff = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Buf'])
ensci = np.asarray(df.drop_duplicates(['Sim', 'Team'])['ENSCI'])

dft = {}



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

    # print(j, buf[j])
    title = str(simlist[j]) + '_' + str(teamlist[j])
            # + '_' + adxstr + sondestr + solstr + '-' + bufstr + 'B'
    type = sondestr + ' ' + str(sol[j]) + '\% - ' + str(buff[j]) + 'B'
    sp = str(simlist[j]) + '-' + str(teamlist[j])
    ptitle = sp + ' ' + sondestr + ' ' + str(sol[j]) + '% - ' + str(buff[j]) + 'B'
    print(title)

    dft[j] = df[(df.Sim == simlist[j]) & (df.Team == teamlist[j])]
    dft[j] = dft[j].reset_index()


    ## Plotting

    plt.close('all)')

    fig, ax = plt.subplots()
    plt.ylim(-0.01,30)
    plt.xlim(0,9000)
    plt.title(ptitle)
    ax.set_ylabel('Pair (mPa)')
    ax.set_xlabel('Tsim (secs)')

    # plt.plot(dft[j].Tsim, dft[j].PO3_deconv_jma, label = 'PO3 fast deconv', linestyle = "--")

    # plt.plot(dft[j].Tsim, dft[j].PO3_deconv_jma.rolling(window=3).mean(), label = 'PO3 fast deconv. RA(6 secs)', linestyle = "--")
    plt.plot(dft[j].Tsim, dft[j].PO3_deconv_jma.rolling(window=5).mean(), label = 'PO3 fast deconv. RA(10 secs)', linestyle = "--")

    plt.plot(dft[j].Tsim, dft[j].PO3_OPM, label='OPM',  linestyle = "--")
    plt.plot(dft[j].Tsim, dft[j].PO3, label='PO3', linestyle = "--")
    plt.plot(dft[j].Tsim, dft[j].PO3_slow_conv, label='PO3 slow conv. ')

    plt.legend(loc='upper left', fontsize = 'x-small')

    # plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Deconv_PerSim_2017/PO3_' + title + '.eps')
    # plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Deconv_PerSim_2017/PO3_' + title + '.png')
    #
    # pickle.dump(fig, open('/home/poyraden/Analysis/JosieAnalysis/Plots/pickle_plots/PO3_' + title+'_2017.pickle', 'wb'))

    # plt.show()
    # new_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

    # blue, orange, green, red, purple, brown, pinkish, greyish, yellowish, bluish

    # fig, ax2 = plt.subplots()
    # ax2.set_ylabel(r'Current ($\mu$A)')
    # ax2.set_xlabel('Tsim (secs)')
    # # ax2.set_yscale('log')
    #
    # plt.plot(dft[j].Tsim, dft[j].I_fast_deconv.rolling(window=3).mean(), label='I fast deconv. RA(6 secs)',
    #          linestyle="--")
    # plt.plot(dft[j].Tsim, dft[j].I_OPM, label='I OPM', linestyle="--")
    # plt.plot(dft[j].Tsim, dft[j].IM, label='I ECC')
    # plt.plot(dft[j].Tsim, dft[j].I_slow_conv, label='I slow conv. ', color='#d62728')
    # plt.title(ptitle)
    # plt.legend(loc='upper left', fontsize = 'x-small')
    # # plt.ylim(-0.01,25)
    # # plt.xlim(0, 9000)
    # plt.ylim(0, 10)
    # # plt.xlim(500, 2600)
    #
    # plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Deconv_PerSim_2017/Current_' + title + '.eps')
    # plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Deconv_PerSim_2017/Current_' + title + '.png')
    #
    # pickle.dump(fig, open('/home/poyraden/Analysis/JosieAnalysis/Plots/pickle_plots/Current_' + title+'_2017.pickle', 'wb'))
    #
    # # # plt.show()
    # # plt.close('all)')
    # #
