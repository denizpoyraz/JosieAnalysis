import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.gridspec as gridspec
import pickle

# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv.csv", low_memory=False)
# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_Data_nocut.csv", low_memory=False)

# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_deconv_beta2ib0.csv", low_memory=False)
df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_deconv_beta0alldata.csv", low_memory=False)

# df = df.drop(df[(df.Sim == 179) & (df.Team == 4)].index)
# df = df.drop(df[(df.Sim == 172) & (df.Team == 1)].index)
# df = df.drop(df[(df.Sim == 178) & (df.Team == 3)].index)
# df = df.drop(df[((df.Sim == 175))].index)
#
#
# df = df.drop(df[(df.Sim == 179) & (df.Team == 4) & (df.Tsim > 4000)].index)
# df = df.drop(df[(df.Sim == 172) & (df.Tsim < 500)].index)
# df = df.drop(df[(df.Sim == 172) & (df.Team == 1) & (df.Tsim > 5000) & (df.Tsim < 5800)].index)
# df = df.drop(df[(df.Sim == 178) & (df.Team == 3) & (df.Tsim > 1700) & (df.Tsim < 2100)].index)
# df = df.drop(df[(df.Sim == 178) & (df.Team == 3) & (df.Tsim > 2500) & (df.Tsim < 3000)].index)
#
# df = df.drop(df[((df.Sim == 186) &  (df.Tsim > 5000))].index)
# df = df.drop(df[((df.Tsim > 7000))].index)

# df = df[df.ADX == 0]
## apply cuts here

simlist = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Sim'])
teamlist = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Team'])
# adx = np.asarray(df.drop_duplicates(['Sim', 'Team'])['ADX'])
sol = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Sol'].tolist())
buff = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Buf'])
ensci = np.asarray(df.drop_duplicates(['Sim', 'Team'])['ENSCI'])


dft = {}

simlist = [140, 140, 140, 140]
teamlist = [1 ,2 ,3 ,4]

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

    ######

    dft[j] = df[(df.Sim == simlist[j]) & (df.Team == teamlist[j])]
    dft[j] = dft[j].reset_index()

    ## 9602
    # t1_stop = dft[j].iloc[0]['R1_Tstop']
    # t2_stop = dft[j].iloc[0]['R2_Tstop']

    ## Plotting
    rdifbool = 1

    gs = gridspec.GridSpec(3, 1)
    #
    if not rdifbool:
        ax2 = plt.subplot(gs[:, :])  # create the first subplot that will ALWAYS be there
        ax2.set_ylabel(r'Current ($\mu$A)')
        ax2.set_xlabel('Tsim (secs)')
        plt.plot(dft[j].Tsim, dft[j].I_OPM_jma, label='I OPM JMA', linestyle="--")
        plt.plot(dft[j].Tsim, dft[j].IM, label='I ECC')
        plt.plot(dft[j].Tsim, dft[j].I_fast_smb6, label='I fast smb6')

        # plt.plot(dft[j].Tsim, dft[j].I_fast_smb12, label='I fast smb12')
        # plt.plot(dft[j].Tsim, dft[j].I_fast_deconv_sm6, label='I deconv. sm.')
        # plt.plot(dft[j].Tsim, dft[j].I_fast_deconv_smb6, label='I sm. deconv.')

        plt.plot(dft[j].Tsim, 0.1 * dft[j].I_conv_slow, label='0.1 * I slow conv. ', color='#d62728')
        plt.title(ptitle)
        plt.legend(loc='upper left', fontsize='x-small')
        plt.ylim(-0.01,7)
        plt.xlim(0, 9000)
        # plt.ylim(0.03, 30)
        # ax2.set_yscale('log')
        ## 9602
        # ax2.axvline(x=t1_stop, color='grey', linestyle='--')
        # ax2.axvline(x=t2_stop, color='grey', linestyle='--')
        plt.show()


    else:
        ax2 = plt.subplot(gs[:2, :])
        ax2.set_ylabel(r'Current ($\mu$A)')
        ax2.set_xticklabels([])
        # ax2.set_xlabel('Tsim (secs)')
        plt.plot(dft[j].Tsim, dft[j].I_OPM_jma.rolling(window=4, win_type='gaussian', center=True).mean(std=2), label='I OPM JMA', linestyle="--")
        plt.plot(dft[j].Tsim, dft[j].IM.rolling(window=4, win_type='gaussian', center=True).mean(std=2), label='I ECC')
        plt.plot(dft[j].Tsim, dft[j].Ifast_deconv_sm8, label='I fast deconv sm8')
        # plt.plot(dft[j].Tsim, dft[j].I_fast_deconv_sm12, label='I fast deconv sm12',  linestyle="--" )
        # plt.plot(dft[j].Tsim, dft[j].I_fast_deconv_smb6, label='I fast sm6 deconv ')

        plt.plot(dft[j].Tsim, 0.1 * dft[j].I_conv_slow, label='0.1 * I slow conv. ', color='#d62728')
        # ax2.set_ylabel(r'Pressure (mPa)')
        ax2.set_xticklabels([])
        # ax2.set_xlabel('Tsim (secs)')
        # plt.plot(dft[j].Tsim, 0.1 * dft[j].I_conv_slow, label='0.1 * I slow conv. ', color='#d62728')
        plt.title(ptitle)
        plt.legend(loc='upper left', fontsize='x-small')
        plt.ylim(-0.01,10)
        plt.xlim(0, 8100)
        # plt.ylim(-0.03, 1)
        # ax2.set_yscale('log')
        # ax2.axvline(x=2375, color='grey', linestyle='--')
        # ax2.axvline(x=4375, color='grey', linestyle='--')
        # ax2.axvline(x=6375, color='grey', linestyle='--')
        # ax2.axvline(x=8375, color='grey', linestyle='--')


        # ax2.axvline(x=t2_stop, color='grey', linestyle='--')

        dft[j]['Ratio'] = dft[j].IM / (0.10 * dft[j].I_conv_slow)

        ax2 = plt.subplot(gs[2, :])  # create the second subplot, that MIGHT be there
        ax2.set_xlabel('Tsim (secs)')

        # # # ## Ratio
        # ax2.set_ylabel(r'I ECC/ 0.10 * I slow conv ')
        # plt.ylim(0, 2)
        # plt.xlim(0, 9000)
        # plt.yticks(np.arange(0, 2.5, 0.5))
        # # ax2.set_yscale('log')
        # plt.plot(dft[j].Tsim, dft[j].Ratio,  linestyle="--", color = '#2ca02c')
        # ax2.axhline(y=1, color='grey', linestyle='--')
        # ax2.axhline(y=0.5, color='grey', linestyle='--')


        ## RDif
        dft[j]['RDif_I'] = 100 * (dft[j].Ifast_deconv_sm8 - dft[j].I_OPM_jma) / dft[j].I_OPM_jma
        ax2.set_ylabel(r'I$_{fast}(deconv sm6)$ - I$_{OPM,jma}$ (%) ')
        plt.ylim(-40, 40)
        plt.xlim(0, 8100)
        plt.plot(dft[j].Tsim, dft[j].RDif_I, linestyle="--", color='#2ca02c')
        ax2.axhline(y=10, color='grey', linestyle='--')
        ax2.axhline(y=0, color='grey', linestyle='--')
        ax2.axhline(y=-10, color='grey', linestyle='--')

        ## ADif
        # ax2.set_ylabel(r'I$_{ECC}$ - I$_{OPM}$ ')
        # plt.ylim(-1, 1)
        # plt.plot(dft[j].Tsim, dft[j].ADif_I, linestyle="--", color='#2ca02c')
        # ax2.axvline(x=t1_stop, color='grey', linestyle='--')
        # ax2.axvline(x=t2_stop, color='grey', linestyle='--')

        # plt.show()
        plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Deconv_PerSim_0910_debug/Current_RDif_' + title + '.eps')
        plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Deconv_PerSim_0910_debug/Current_RDif_' + title + '.png')
        plt.show()
        # fig, ax2 = plt.subplots()
        # ax2.set_ylabel(r'Current ($\mu$A)')
        # ax2.set_xlabel('Tsim (secs)')
        # # ax2.set_yscale('log')
        # #
        # # plt.ylim(-0.01,25)
        # # plt.xlim(0, 9000)
        # plt.ylim(0.03, 30)
        # ax2.set_yscale('log')
        # ax2.axvline(x=t1_stop, color='grey', linestyle='--')
        # ax2.axvline(x=t2_stop, color='black', linestyle='--')

        # plt.xlim(500, 2600)
        #
        # plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Deconv_PerSim_0910_debug/Current_' + title + '.eps')
        # plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Deconv_PerSim_0910_debug/Current_' + title + '.png')
        # #
        # pickle.dump(fig, open('/home/poyraden/Analysis/JosieAnalysis/Plots/pickle_plots/Current_' + title+'_2017.pickle', 'wb'))
        #
        # plt.show()
        # # plt.close('all)')
        # #


# fig, ax = plt.subplots()
        # plt.ylim(-0.01,30)
        # plt.xlim(0,9000)
        # plt.title(ptitle)
        # ax.set_ylabel('Pair (mPa)')
        # ax.set_xlabel('Tsim (secs)')

        # plt.plot(dft[j].Tsim, dft[j].PO3_deconv_jma, label = 'PO3 fast deconv', linestyle = "--")

        # plt.plot(dft[j].Tsim, dft[j].PO3_deconv_jma.rolling(window=3).mean(), label = 'PO3 fast deconv. RA(6 secs)', linestyle = "--")
        # plt.plot(dft[j].Tsim, dft[j].PO3_deconv_jma.rolling(window=5).mean(), label = 'PO3 fast deconv. RA(10 secs)', linestyle = "--")
        #
        # plt.plot(dft[j].Tsim, dft[j].PO3_OPM, label='OPM',  linestyle = "--")
        # plt.plot(dft[j].Tsim, dft[j].PO3, label='PO3', linestyle = "--")
        # plt.plot(dft[j].Tsim, dft[j].PO3_slow_conv, label='PO3 slow conv. ')
        #
        # plt.legend(loc='upper left', fontsize = 'x-small')

        # plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Deconv_PerSim_0910_debug/PO3_' + title + '.eps')
        # plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Deconv_PerSim_0910_debug/PO3_' + title + '.png')
        #
        # pickle.dump(fig, open('/home/poyraden/Analysis/JosieAnalysis/Plots/pickle_plots/PO3_' + title+'_2017.pickle', 'wb'))

        # plt.show()
        # new_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

        # blue, orange, green, red, purple, brown, pinkish, greyish, yellowish, bluish

        # t1_stop = dft[j].iloc[0]['R1_Tstop']
        # t2_stop = dft[j].iloc[0]['R2_Tstop']