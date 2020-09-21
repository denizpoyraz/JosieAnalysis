import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.gridspec as gridspec
import pickle
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,AutoMinorLocator)

# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2000_deconv_beta0_every5sec.csv", low_memory=False)
# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_Data_nocut.csv", low_memory=False)

df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_Deconv_preparationadded_min.csv", low_memory=False)
# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_deconv_sm.csv", low_memory=False)
# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie9602_Data.csv", low_memory=False)

dfo = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_Deconv_preparationadded_mino.csv", low_memory=False)


# df = df[(df.Sim == 136) & (df.Team == 3)]
#
# dfo = dfo[(dfo.Sim == 136) & (dfo.Team == 3)]


simlist = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Sim'])
teamlist = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Team'])
# adx = np.asarray(df.drop_duplicates(['Sim', 'Team'])['ADX'])
sol = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Sol'].tolist())
buff = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Buf'])
ensci = np.asarray(df.drop_duplicates(['Sim', 'Team'])['ENSCI'])


dft = {}

dfto = {}

# simlist = [92, 92, 92, 92]
# teamlist = [1 ,2 ,3 ,4]

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
    dfto[j] = dfo[(dfo.Sim == simlist[j]) & (dfo.Team == teamlist[j])]

    dft[j] = dft[j].reset_index()
    dfto[j] = dfto[j].reset_index()

    dft[j].TsimMin = dft[j].Tsim / 1
    dfto[j].TsimMin = dfto[j].Tsim / 1

    ## 9602
    # t1_stop = dft[j].iloc[0]['R1_Tstop']
    # t2_stop = dft[j].iloc[0]['R2_Tstop']

    ## Plotting
    rdifbool = 0

    gs = gridspec.GridSpec(3, 1)
    #
    if not rdifbool:
        ax2 = plt.subplot(gs[:, :])  # create the first subplot that will ALWAYS be there
        # fig, ax2 = plt.subplots()

        ax2.set_ylabel(r'Current ($\mu$A)')
        ax2.set_xlabel('Tsim (mins)')

        plt.ylim(0.0001, 8)
        # plt.xlim(66, 72)
        ax2.set_yscale('log')

        #
        # plt.plot(dft[j].TsimMin, dft[j].I_OPM_jma, label='I OPM JMA')
        # # plt.plot(dft[j].TsimMin, dft[j].I_OPM_jma_sm12, label='I OPM JMA sm12')
        plt.plot(dft[j].TsimMin, dft[j].IM - dft[j]['iB0'], label='I - iB0 ECC')
        plt.plot(dft[j].TsimMin, dft[j].I_slow_conv, label='Islow(beta * IM) conv (allrange)')
        plt.plot(dfto[j].TsimMin, dfto[j].I_slow_convo, label='Islow(beta * IM) conv  (simulation range)')
        # # plt.plot(dfto[j].TsimMin , dfto[j].I_slow_conv_testpre, label='Islow(beta * IM + IM_lastpre - iB0) conv')
        plt.plot(dfto[j].TsimMin , dfto[j].I_slow_conv_tesths, label='Islow(beta * IM) [I slow conv[0] = IM_last_pre - iBo] conv')
        # # plt.plot(dft[j].TsimMin , dft[j].I_slow_conv_test, label='Islow(beta *(IM-iB0)) conv')
        plt.plot(dft[j].TsimMin, dft[j]['iB2'] - dft[j]['iB0'], label='iB2 - iB0')
        plt.plot(dft[j].TsimMin, dft[j]['iB1'] - dft[j]['iB0'], label='iB1 - iB0')

        print(dft[j]['iB2'] , dft[j]['iB0'])


        # plt.plot(dft[j].TsimMin, dft[j].I_OPM_jma, label='I OPM JMA')
        # # plt.plot(dft[j].TsimMin, dft[j].I_OPM_jma_sm12, label='I OPM JMA sm12')
        # plt.plot(dft[j].TsimMin, dft[j].IM - dft[j]['iB0'], label='I - iB0 ECC')
        # plt.plot(dft[j].TsimMin, dft[j].Ifast_minib0_deconv.rolling(window=5, center=True).mean(), label='Ifast (beta * IM) deconv (allrange)')
        # plt.plot(dfto[j].TsimMin, dfto[j].Ifast_minib0_deconvo.rolling(window=5, center=True).mean(), label='Ifast (beta * IM) deconv  (simulation range)')
        # # plt.plot(dfto[j].TsimMin , dfto[j].I_slow_conv_testpre, label='Islow(beta * IM + IM_lastpre - iB0) conv')
        # plt.plot(dfto[j].TsimMin , dfto[j].Ifast_minib0_deconv_tesths.rolling(window=5, center=True).mean(), label='Ifast (beta * IM) [I slow conv[0] = IM_last_pre - iBo] conv')
        # # plt.plot(dft[j].TsimMin , dft[j].I_slow_conv_test, label='Islow(beta *(IM-iB0)) conv')

        # plt.plot(dfto[j].TsimMin , dfto[j].Ifast_minib0_tesths.rolling(window=5, center=True).mean(), label='Ifast (beta * IM) [I slow conv[0] = IM_last_pre - iBo] conv')
        # plt.plot(dft[j].TsimMin, dft[j].Ifast_minib0_deconv.rolling(window=5, center=True).mean(), label='Ifast (beta * IM) deconv (allrange)')


        # plt.plot(dft[j].TsimMin, dft[j].I_OPM_jma, label='I OPM JMA')
        # # plt.plot(dft[j].TsimMin, dft[j].I_OPM_jma_sm12, label='I OPM JMA sm12')
        # plt.plot(dft[j].TsimMin, dft[j].IM - dft[j]['iB0'], label='I - iB0 ECC')
        # plt.plot(dft[j].TsimMin, dft[j].Ifast_deconv.rolling(window=5, center=True).mean(),
        #          label='Ifast (beta * IM) deconv (allrange)')
        # plt.plot(dfto[j].TsimMin, dfto[j].Ifast_deconvo.rolling(window=5, center=True).mean(),
        #          label='Ifast (beta * IM) deconv  (simulation range)')
        # # plt.plot(dfto[j].TsimMin , dfto[j].I_slow_conv_testpre, label='Islow(beta * IM + IM_lastpre - iB0) conv')
        # plt.plot(dfto[j].TsimMin, dfto[j].Ifast_deconv_tesths.rolling(window=5, center=True).mean(),
        #          label='Ifast (beta * IM) [I slow conv[0] = IM_last_pre - iBo] conv')
        # # plt.plot(dft[j].TsimMin , dft[j].I_slow_conv_test, label='Islow(beta *(IM-iB0)) conv')

        ################################
        # plt.plot(dft[j].TsimMin, dft[j].IM, label='I ECC')
        # plt.plot(dft[j].TsimMin, dft[j].Ifast_deconv.rolling(window=5, center=True).mean(), label='[IM - Islow(beta * IM)] deconv (allrange)')
        # plt.plot(dfto[j].TsimMin, dfto[j].Ifast_deconvo.rolling(window=5, center=True).mean(), label='[IM - Islow(beta * IM)] deconv  (simulation range)')
        # plt.plot(dfto[j].TsimMin, dfto[j].Ifast_deconv_testpre.rolling(window=5, center=True).mean(),label='[IM - Islow(beta * IM + IM_lastpre * exp(-t/tslow)] deconv')
        # plt.plot(dfto[j].TsimMin, dfto[j].Ifast_deconv_tesths.rolling(window=5, center=True).mean(), label='[IM - Islow(beta * IM)], [I slow conv[0] = IM_last_pre] deconv')
        ################################
        # plt.plot(dft[j].TsimMin, dft[j].IM, label='I ECC')
        # plt.plot(dft[j].TsimMin, dft[j].Ifast_minib0_deconv.rolling(window=5, center=True).mean(),
        #          label='[IM - Islow(beta * IM) - iB0] deconv (allrange)')
        # plt.plot(dfto[j].TsimMin, dfto[j].Ifast_minib0_deconvo.rolling(window=5, center=True).mean(),
        #          label='[IM - Islow(beta * IM) - iB0] deconv  (simulation range)')
        # plt.plot(dfto[j].TsimMin, dfto[j].Ifast_minib0_deconv_testpre.rolling(window=5, center=True).mean(),
        #          label='[IM - Islow(beta * IM + IM_lastpre * exp(-t/tslow)) - iB0] deconv')
        # plt.plot(dfto[j].TsimMin, dfto[j].Ifast_minib0_deconv_tesths.rolling(window=5, center=True).mean(),
        #          label='[IM - Islow(beta * IM) - iB0], [I slow conv[0] = IM_last_pre] deconv')



        plt.title(ptitle)
        plt.legend(loc='upper left', fontsize='x-small')
        # plt.show()

        # fig, ax3 = plt.subplots()
        #
        # ax3 = plt.subplot()  # create the first subplot that will ALWAYS be there
        # ax3.set_ylabel(r'Current ($\mu$A)')
        # ax3.set_xlabel('Tsim (mins)')
        #
        #
        # plt.plot(dft[j].TsimMin, dft[j].I_OPM_jma.rolling(window=5, center=True).mean(), label='I OPM JMA sm10')
        # plt.plot(dft[j].TsimMin, dft[j].IM.rolling(window=5, center=True).mean(), label='I ECC sm 10')
        # plt.plot(dft[j].TsimMin, dft[j].Ifast_minib0_deconv_f.rolling(window=10, center=True).mean(),
        #          label='Ifast minib0 deconv. sm20')
        #
        # plt.title(ptitle)
        # plt.legend(loc='upper left', fontsize='small')
        plt.show()


    else:
        ax1 = plt.subplot(gs[:2, :])
        ax1.set_ylabel(r'Current ($\mu$A)')
        # ax1.set_ylabel(r'PO3 (mPa)')

        ax1.set_xticklabels([])

        # plt.plot(dft[j].TsimMin, dft[j].I_OPM_jma, label='I OPM JMA')
        # # plt.plot(dft[j].TsimMin, dft[j].I_OPM_jma_sm12, label='I OPM JMA sm12')
        # plt.plot(dft[j].TsimMin, dft[j].IM - dft[j]['iB0'], label='I - iB0 ECC')
        # plt.plot(dft[j].TsimMin, dft[j].I_slow_conv, label='Islow(beta * IM) conv (allrange)')
        # plt.plot(dfto[j].TsimMin, dfto[j].I_slow_convo, label='Islow(beta * IM) conv  (simulation range)')
        # # plt.plot(dfto[j].TsimMin , dfto[j].I_slow_conv_testpre, label='Islow(beta * IM + IM_lastpre - iB0) conv')
        # plt.plot(dfto[j].TsimMin , dfto[j].I_slow_conv_tesths, label='Islow(beta * IM) [I slow conv[0] = IM_last_pre - iBo] conv')
        # # plt.plot(dft[j].TsimMin , dft[j].I_slow_conv_test, label='Islow(beta *(IM-iB0)) conv')

        # ax1.set_xlabel('Tsim (secs)')
        plt.plot(dft[j].TsimMin, dft[j].I_OPM_jma, label='I OPM JMA')
        plt.plot(dft[j].TsimMin, dft[j].IM - dft[j]['iB0'], label='I - iB0 ECC')
        plt.plot(dft[j].TsimMin, dft[j].Ifast_minib0_deconv.rolling(window=5, center=True).mean(), label='Ifast (beta * IM) deconv (allrange)')
        plt.plot(dfto[j].TsimMin, dfto[j].Ifast_minib0_deconvo.rolling(window=5, center=True).mean(), label='Ifast (beta * IM) deconv  (simulation range)')
        plt.plot(dfto[j].TsimMin , dfto[j].Ifast_minib0_deconv_tesths.rolling(window=5, center=True).mean(), label='Ifast (beta * IM) [I slow conv[0] = IM_last_pre - iBo] conv')

        #
        plt.title(ptitle)
        plt.legend(loc='best', fontsize='x-small')
        plt.ylim(0,10)
        # plt.xlim(66, 72)
        # plt.xlim(53, 59)
        ax1.yaxis.set_major_locator(MultipleLocator(5))
        ax1.yaxis.set_major_formatter(FormatStrFormatter('%d'))
        ax1.yaxis.set_minor_locator(AutoMinorLocator())

        # plt.yticks(np.arange(0, 21, step = 0.5))



        # dft[j]['RDif_I'] = 100 * (dft[j].Ifast_deconv_sm8 - dft[j].I_OPM_jma) / dft[j].I_OPM_jma
        # dft[j]['Adif'] = dft[j].IM - dft[j]['iB0'] - dft[j].I_OPM_jma
        #
        # dft[j]['Adif_all'] =  dft[j].Ifast_minib0_deconv.rolling(window=5, center=True).mean() - dft[j].I_OPM_jma
        # dfto[j]['Adif_sim'] = dfto[j].Ifast_minib0_deconvo.rolling(window=5, center=True).mean()  - dfto[j].I_OPM_jma
        # dfto[j]['Adif_hs'] =   dfto[j].Ifast_minib0_deconv_tesths.rolling(window=5, center=True).mean() - dfto[j].I_OPM_jma
        # dft[j]['Adif_Pcor_jma'] = dft[j].PO3_minib0_deconv_jma - dft[j].PO3_OPM
        # dft[j]['Adif_Pcor_komhyr'] = dft[j].PO3_minib0_deconv_komhyr - dft[j].PO3_OPM

        dft[j]['Adif'] = 100 * (dft[j].IM - dft[j]['iB0'] - dft[j].I_OPM_jma) / dft[j].I_OPM_jma

        dft[j]['Adif_all'] = 100 * ( dft[j].Ifast_minib0_deconv.rolling(window=5, center=True).mean() - dft[j].I_OPM_jma) / dft[j].I_OPM_jma
        dfto[j]['Adif_sim'] = 100 * (dfto[j].Ifast_minib0_deconvo.rolling(window=5, center=True).mean() - dfto[j].I_OPM_jma) / dft[j].I_OPM_jma
        dfto[j]['Adif_hs'] = 100 * (dfto[j].Ifast_minib0_deconv_tesths.rolling(window=5, center=True).mean() - dfto[
            j].I_OPM_jma) / dft[j].I_OPM_jma

        ax2 = plt.subplot(gs[2, :])  # create the second subplot, that MIGHT be there
        ax2.set_xlabel('Tsim (min)')
        ax2.set_ylabel(r'ADif')
        # plt.xlim(66, 72)
        # plt.xlim(53, 59)
        ax2.yaxis.set_major_locator(MultipleLocator(2))
        ax2.yaxis.set_major_formatter(FormatStrFormatter('%d'))
        ax2.yaxis.set_minor_locator(AutoMinorLocator(10))

        # plt.yticks(np.arange(-2, 2, 200))
        plt.ylim(-2, 2)


        # plt.xlim(0, 8100)
        plt.plot(dft[j].TsimMin, dft[j].Adif, linestyle="--", color='orange', label = 'I - iB0')

        plt.plot(dft[j].TsimMin, dft[j].Adif_all.rolling(window=5, center=True).mean(), linestyle="--", color='green', label = 'all range')
        plt.plot(dfto[j].TsimMin, dfto[j].Adif_sim.rolling(window=5, center=True).mean(), linestyle="--", color='red', label = 'simulation range')
        plt.plot(dfto[j].TsimMin, dfto[j].Adif_hs.rolling(window=5, center=True).mean(), linestyle="--", color='purple', label = 'I_slow_conv[0] = IM_lastpre - iB0')

        plt.legend(loc='best', fontsize='x-small')

        #
        # ax2.axhline(y=10, color='grey', linestyle='--')
        ax2.axhline(y=0, color='grey', linestyle='--')
        # ax2.axhline(y=-10, color='grey', linestyle='--')


        # plt.show()
        # plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/HV_compare/5sec_PO3_' + title + '.eps')
        # plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/HV_compare/5sec_PO3_' + title + '.png')
        plt.show()

        # new_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

        # blue, orange, green, red, purple, brown, pinkish, greyish, yellowish, bluish



# Josie9602_Data.csv

# Josie0910_deconv_beta0_timereversed
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