import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.gridspec as gridspec
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,AutoMinorLocator)
from scipy.ndimage import gaussian_filter1d
import scipy.signal

# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_Deconv_preparationadded_all_test.csv", low_memory=False)
df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_Data_nocut.csv", low_memory=False)

# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_deconv.csv", low_memory=False)
# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie9602_Data.csv", low_memory=False)
# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_Deconv_preparationadded_min_t.csv", low_memory=False)

# df_dc.to_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_Deconv_preparationadded_all_test.csv")
# df_o.to_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_Deconv_preparationadded_simulation_test.csv")
#
# dfo = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_Deconv_preparationadded_mino_t.csv", low_memory=False)

df = df[(df.Sim == 140) | (df.Sim == 138) | (df.Sim == 158) |  (df.Sim == 166)]
# dfo = dfo[(dfo.Sim == 136) & (dfo.Team == 3)]

simlist = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Sim'])
teamlist = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Team'])
# adx = np.asarray(df.drop_duplicates(['Sim', 'Team'])['ADX'])
sol = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Sol'].tolist())
buff = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Buf'])
ensci = np.asarray(df.drop_duplicates(['Sim', 'Team'])['ENSCI'])

dft = {}
dfto = {}

print(simlist, teamlist)

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
    # dfto[j] = dfo[(dfo.Sim == simlist[j]) & (dfo.Team == teamlist[j])]

    # dft[j] = dft[j].reset_index()
    # dfto[j] = dfto[j].reset_index()

    dft[j].TsimMin = dft[j].Tsim / 60
    # dfto[j].TsimMin = dfto[j].Tsim / 60

    ## 9602
    # t1_stop = dft[j].iloc[0]['R1_Tstop']
    # t2_stop = dft[j].iloc[0]['R2_Tstop']
    #
    # dftest = dft[j][(dft[j].Tsim_original >= 0)]
    # dftest.TsimMin = dftest.Tsim / 60
    ## Plotting
    rdifbool = 0

    # dft[j].loc[dft[j]['TimeBool'] == 0, 'Adif_sim'] = 0
    # dft[j].loc[dft[j]['Tsim_original'] >= 0, 'Adif_sim'] = (dfto[j].I_slow_convo - dftest.I_slow_conv)
    #
    # Adif_sim = np.array(dfto[j].I_slow_convo.tolist()) - np.array(dftest.I_slow_conv.tolist())
    # Adif_exp = np.array(dfto[j].I_slow_conv_tesths.tolist()) - np.array(dftest.I_slow_conv.tolist())
    # Adif_ib1decay = np.array(dfto[j].I_slow_conv_ib1_decay.tolist()) - np.array(dftest.I_slow_conv.tolist())
    # Adif_ib1 = np.array(dfto[j].I_slow_conv_testib1.tolist()) - np.array(dftest.I_slow_conv.tolist())
    # Adif_ib2 = np.array(dfto[j].I_slow_conv_testib2.tolist()) - np.array(dftest.I_slow_conv.tolist())
    #
    # Rdif_sim = 100 * (np.array(dfto[j].I_slow_convo.tolist()) - np.array(dftest.I_slow_conv.tolist())) / np.array(dftest.I_slow_conv.tolist())
    # Rdif_exp = 100 * (np.array(dfto[j].I_slow_conv_tesths.tolist()) - np.array(dftest.I_slow_conv.tolist())) / np.array(dftest.I_slow_conv.tolist())
    # Rdif_ib1decay = 100 * (np.array(dfto[j].I_slow_conv_ib1_decay.tolist()) - np.array(dftest.I_slow_conv.tolist())) / np.array(dftest.I_slow_conv.tolist())
    # Rdif_ib1 = 100 * (np.array(dfto[j].I_slow_conv_testib1.tolist()) - np.array(dftest.I_slow_conv.tolist())) / np.array(dftest.I_slow_conv.tolist())
    # Rdif_ib2 = 100 * (np.array(dfto[j].I_slow_conv_testib2.tolist()) - np.array(dftest.I_slow_conv.tolist())) / np.array(dftest.I_slow_conv.tolist())

    # ifast_gaussian_1 = gaussian_filter1d(np.array(dft[j].Ifast_minib0_deconv.tolist()), 1)
    # ifast_gaussian_3 = gaussian_filter1d(np.array(dft[j].Ifast_minib0_deconv.tolist()), 3)
    #
    # ifast_savgol_51 = scipy.signal.savgol_filter(np.array(dft[j].Ifast_minib0_deconv.tolist()), 9, 3, mode='nearest')  # window size 51, polynomial order 3
    # ifast_savgol_53 = scipy.signal.savgol_filter(np.array(dft[j].Ifast_minib0_deconv.tolist()), 9, 5, mode='nearest')  # window size 51, polynomial order 3

    gs = gridspec.GridSpec(4, 1)
    #
    if not rdifbool:
        ax2 = plt.subplot(gs[:, :])  # create the first subplot that will ALWAYS be there
        # fig, ax2 = plt.subplots()

        ax2.set_ylabel(r'Current ($\mu$A)')
        ax2.set_xlabel('Tsim (mins)')

        # plt.ylim(0.0001, 8)
        # plt.xlim(0, 120)
        ax2.xaxis.set_major_locator(MultipleLocator(10))
        ax2.xaxis.set_major_formatter(FormatStrFormatter('%d'))
        ax2.xaxis.set_minor_locator(AutoMinorLocator())
        # ax2.set_yscale('log')

        plt.plot(dft[j].TsimMin, dft[j].IM - dft[j]['iB0'], label='I - iB0 ECC')
        plt.plot(dft[j].TsimMin, dft[j].I_OPM_jma, label='I OPM JMA')
        # plt.plot(dft[j].TsimMin, dft[j].Ifast_deconv.rolling(window = 9, center = True).mean(), label='I fast deconv. sm9')
        # plt.plot(dft[j].TsimMin, dft[j].Ifast_minib0_deconv.rolling(window = 9, center = True).mean(), label='I fast min ibo deconv. sm9')
        # plt.plot(dft[j].TsimMin,ifast_gaussian_1, label='I fast min ibo deconv. gaus1d sigma1')
        # plt.plot(dft[j].TsimMin,ifast_gaussian_3, label='I fast min ibo deconv. gaus1d sigma3')
        # plt.plot(dft[j].TsimMin,ifast_savgol_51, label='I fast min ibo deconv. savgol filter 1')
        # plt.plot(dft[j].TsimMin,ifast_savgol_53, label='I fast min ibo deconv. savgol filter 3')



        # plt.plot(dft[j].TsimMin, dft[j].I_slow_conv, label='Islow conv, allrange')
        # plt.plot(dfto[j].TsimMin, dfto[j].I_slow_convo, label='Islow conv, sim. range')
        # plt.plot(dfto[j].TsimMin, dfto[j].I_slow_conv_tesths,
        #          label='[Islow conv (I_atIB1-iB0)*exp decay]')
        # plt.plot(dfto[j].TsimMin, dfto[j].I_slow_conv_ib1_decay,
        #          label='Islow conv (iB1-iB0)*exp decay]', linewidth = '2.0')
        # plt.plot(dfto[j].TsimMin, dfto[j].I_slow_conv_testib1,
        #          label='Islow conv [iB1-iB0]')
        # plt.plot(dfto[j].TsimMin, dfto[j].I_slow_conv_testib2,
        #          label='Islow conv [iB2-iB0]', linestyle='dashed', linewidth = '2.0')
        # plt.plot(dft[j].TsimMin, dft[j]['i_at_timeib1'] - dft[j]['iB0'], label='I_atIB1-iB0')
        # plt.plot(dft[j].TsimMin, dft[j]['iB1'] - dft[j]['iB0'], label='iB1 - iB0')
        # plt.plot(dfto[j].TsimMin, dfto[j]['iB2'] - dfto[j]['iB0'], label='iB2 - iB0')
        # plt.plot(dft[j].TsimMin, dft[j]['I0_var'], label='I0_var=(I_atIB1-iB0)*exp decay]')
        #
        # ax2.axvline(x= dft[j].at[dft[j].first_valid_index(),'time_ib1'], color='red', linestyle='--', label = 'time iB1')

        plt.title(ptitle)
        plt.legend(loc='upper right', fontsize='xx-small')
        # plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Josie_sm/Ifast_' + title + '.eps')
        # plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Josie_sm/Ifast_' + title + '.png')
        plt.show()
    else:
        ax1 = plt.subplot(gs[:3, :])
        ax1.set_ylabel(r'Current ($\mu$A)')
        # ax1.set_ylabel(r'PO3 (mPa)')
        ax1.set_xticklabels([])

        plt.ylim(0.0001, 8)
        plt.xlim(0, 150)

        if ((simlist[j] == 139) | (simlist[j] == 140) | (simlist[j] == 145) | (simlist[j] == 158) | (
                simlist[j] == 160) | (simlist[j] == 163) | (simlist[j] == 166)):
            plt.xlim(0, 250)
        ax1.set_yscale('log')

        plt.plot(dft[j].TsimMin, dft[j].IM - dft[j]['iB0'], label='I - iB0 ECC')
        plt.plot(dft[j].TsimMin, dft[j].I_slow_conv, label='Islow conv, allrange')
        plt.plot(dfto[j].TsimMin, dfto[j].I_slow_convo, label='Islow conv, sim. range')
        plt.plot(dfto[j].TsimMin, dfto[j].I_slow_conv_tesths,
                 label='[Islow conv (I_atIB1-iB0)*exp decay]')
        plt.plot(dfto[j].TsimMin, dfto[j].I_slow_conv_ib1_decay,
                 label='Islow conv (iB1-iB0)*exp decay]', linewidth='2.0')
        plt.plot(dfto[j].TsimMin, dfto[j].I_slow_conv_testib1,
                 label='Islow conv [iB1-iB0]')
        plt.plot(dfto[j].TsimMin, dfto[j].I_slow_conv_testib2,
                 label='Islow conv [iB2-iB0]', linestyle='dashed', linewidth='2.0')
        plt.plot(dft[j].TsimMin, dft[j]['i_at_timeib1'] - dft[j]['iB0'], label='I_atIB1-iB0')
        plt.plot(dft[j].TsimMin, dft[j]['iB1'] - dft[j]['iB0'], label='iB1 - iB0')
        plt.plot(dfto[j].TsimMin, dfto[j]['iB2'] - dfto[j]['iB0'], label='iB2 - iB0')
        plt.plot(dft[j].TsimMin, dft[j]['I0_var'], label='I0_var=(I_atIB1-iB0)*exp decay]')

        ax1.axvline(x=dft[j].at[dft[j].first_valid_index(), 'time_ib1'], color='red', linestyle='--')

        plt.title(ptitle)
        plt.legend(loc='upper right', fontsize='xx-small')
        #
        plt.title(ptitle)
        # plt.xlim(66, 72)
        # plt.xlim(53, 59)
        ax1.yaxis.set_major_locator(MultipleLocator(5))
        ax1.yaxis.set_major_formatter(FormatStrFormatter('%d'))
        ax1.yaxis.set_minor_locator(AutoMinorLocator())

        ax2 = plt.subplot(gs[3, :])  # create the second subplot, that MIGHT be there
        ax2.set_xlabel('Tsim (min)')
        # ax2.set_ylabel(r'ADif($\mu$A)')
        ax2.set_ylabel(r'RDif(%)')

        # plt.xlim(66, 72)
        # plt.xlim(53, 59)
        # ax2.yaxis.set_major_locator(MultipleLocator(2))
        # ax2.yaxis.set_major_formatter(FormatStrFormatter('%d'))
        # ax2.yaxis.set_minor_locator(AutoMinorLocator(10))

        # plt.yticks(np.arange(-2, 2, 200))
        # plt.ylim(-0.005, 0.005)

        plt.xlim(0, 150)
        # plt.ylim(-100, 100)

        if ((simlist[j] == 139) | (simlist[j] == 140 ) | (simlist[j] == 145) | (simlist[j] == 158) | (simlist[j] == 160) | (simlist[j] == 163) | (simlist[j] == 166)):
            plt.xlim(0, 250)
            plt.tick_params(axis='x', labelsize=6)

        ax2.xaxis.set_major_locator(MultipleLocator(10))
        ax2.xaxis.set_major_formatter(FormatStrFormatter('%d'))
        ax2.xaxis.set_minor_locator(AutoMinorLocator())
        # plt.xlim(0, 8100)
        plt.plot(dftest.TsimMin, Adif_sim, color='#2ca02cff', label = 'sim_range')
        plt.plot(dftest.TsimMin, Adif_exp, color='#d62728ff', label = 'I_atiB1_expdecay')
        plt.plot(dftest.TsimMin, Adif_ib1decay, color='#9467bdff', label = 'ib1 expdecay')
        plt.plot(dftest.TsimMin, Adif_ib1, color='#8c564bff', label = 'ib1')
        plt.plot(dftest.TsimMin, Adif_ib2, linestyle="--", color='#e377c2ff', label = 'ib2')

        plt.legend(loc='upper left ', fontsize='xx-small')

        #
        # ax2.axhline(y=10, color='grey', linestyle='--')
        # ax2.axhline(y=0, color='grey', linestyle='--')
        # ax2.axhline(y=-10, color='grey', linestyle='--')
        ax2.axhline(y=0,  color='grey', linestyle='--')

        # plt.show()
        # plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Josie_Islow/ADif_' + title + '.eps')
        # plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Josie_Islow/ADif_' + title + '.png')
        plt.show()

        # new_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        # blue, orange, green, red, purple, brown, pinkish, greyish, yellowish, bluish


