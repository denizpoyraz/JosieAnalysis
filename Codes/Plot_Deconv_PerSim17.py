import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.gridspec as gridspec
import pickle
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,AutoMinorLocator)

df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv_0510.csv", low_memory=False)

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

    dft[j] = df[(df.Sim == simlist[j]) & (df.Team == teamlist[j])]
    dft[j].TsimMin = dft[j].Tsim / 60
    
    dft[j]['Adif_sim'] = np.array(dft[j].Ifast_deconv.rolling(window=9 * 1, center = True).mean().tolist()) - np.array(dft[j].I_OPM_jma.tolist())
    dft[j]['Rdif_sim'] = 100 * (np.array(dft[j].Ifast_deconv.rolling(window=9 * 1, center = True).mean().tolist()) - np.array(dft[j].I_OPM_jma.tolist())) / np.array(dft[j].I_OPM_jma.tolist())
    dft[j]['Adif_ib1'] = np.array(dft[j].Ifast_deconv_ib1.rolling(window=9 * 1, center=True).mean().tolist()) - np.array(
        dft[j].I_OPM_jma.tolist())
    dft[j]['Rdif_ib1'] = 100 * (np.array(dft[j].Ifast_deconv_ib1.rolling(window=9 * 1, center=True).mean().tolist()) - np.array(
        dft[j].I_OPM_jma.tolist())) / np.array(dft[j].I_OPM_jma.tolist())
    dft[j]['Adif_ib2'] = np.array(dft[j].Ifast_deconv_ib2.rolling(window=9 * 1, center=True).mean().tolist()) - np.array(
        dft[j].I_OPM_jma.tolist())
    dft[j]['Rdif_ib2'] = 100 * (np.array(dft[j].Ifast_deconv_ib2.rolling(window=9 * 1, center=True).mean().tolist()) - np.array(
        dft[j].I_OPM_jma.tolist())) / np.array(dft[j].I_OPM_jma.tolist())

    # Adif_sim = np.array(dft[j].Ifast_minib0_deconv.rolling(window=9 * 1, center=True).mean().tolist()) - np.array(
    #     dft[j].I_OPM_jma.tolist())
    # Rdif_sim = 100 * (np.array(dft[j].Ifast_minib0_deconv.rolling(window=9 * 1, center=True).mean().tolist()) - np.array(
    #     dft[j].I_OPM_jma.tolist())) / np.array(dft[j].I_OPM_jma.tolist())
    # Adif_ib1 = np.array(dft[j].Ifast_minib0_deconv_ib1.rolling(window=9 * 1, center=True).mean().tolist()) - np.array(
    #     dft[j].I_OPM_jma.tolist())
    # Rdif_ib1 = 100 * (np.array(dft[j].Ifast_minib0_deconv_ib1.rolling(window=9 * 1, center=True).mean().tolist()) - np.array(
    #     dft[j].I_OPM_jma.tolist())) / np.array(dft[j].I_OPM_jma.tolist())
    # Adif_ib2 = np.array(dft[j].Ifast_minib0_deconv_ib2.rolling(window=9 * 1, center=True).mean().tolist()) - np.array(
    #     dft[j].I_OPM_jma.tolist())
    # Rdif_ib2 = 100 * (np.array(dft[j].Ifast_minib0_deconv_ib2.rolling(window=9 * 1, center=True).mean().tolist()) - np.array(
    #     dft[j].I_OPM_jma.tolist())) / np.array(dft[j].I_OPM_jma.tolist())
    
    
    gs = gridspec.GridSpec(4, 1)

    ax1 = plt.subplot(gs[:3, :])

    # fig, ax1 = plt.subplots()
    ax1.set_ylabel(r'Current ($\mu$A)')
    ax1.set_xlabel('Tsim (mins)')

    plt.ylim(0.0001, 8)
    plt.xlim(0, 120)
    ax1.xaxis.set_major_locator(MultipleLocator(10))
    ax1.xaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax1.xaxis.set_minor_locator(AutoMinorLocator())
    # ax1.set_yscale('log')

    plt.plot(dft[j].TsimMin, dft[j].IM - dft[j]['iB0'], label='I - iB0 ECC')
    plt.plot(dft[j].TsimMin, dft[j].I_OPM_jma, label='IOPM')

    # plt.plot(dft[j].TsimMin, dft[j].Islow_conv, label='Islow conv, standard')
    # plt.plot(dft[j].TsimMin, dft[j].Islow_conv_ib1, label='Islow conv, ib1')
    # plt.plot(dft[j].TsimMin, dft[j].Islow_conv_ib2, label='Islow conv, ib2')
    plt.plot(dft[j].TsimMin, dft[j].Ifast_deconv.rolling(window=9 * 1, center=True).mean(), label='Ifast deconv, standard')
    plt.plot(dft[j].TsimMin, dft[j].Ifast_deconv_ib1.rolling(window=9 * 1, center=True).mean(), label='Ifast deconv, ib1')
    plt.plot(dft[j].TsimMin, dft[j].Ifast_deconv_ib2.rolling(window=9 * 1, center=True).mean(), label='Ifast deconv, ib2')

    plt.legend(loc='upper left', fontsize='xx-small')


    ax2 = plt.subplot(gs[3, :])  # create the second subplot, that MIGHT be there
    ax2.set_xlabel('Tsim (min)')
    # ax2.set_ylabel(r'ADif($\mu$A)')
    ax2.set_ylabel(r'RDif(%)')

    ax2.xaxis.set_major_locator(MultipleLocator(10))
    ax2.xaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax2.xaxis.set_minor_locator(AutoMinorLocator())
    # plt.xlim(0, 8100)
    plt.plot(dft[j].TsimMin, dft[j].Rdif_sim.rolling(window=9 * 1, center=True).mean(),  label='standard')
    plt.plot(dft[j].TsimMin, dft[j].Rdif_ib1.rolling(window=9 * 1, center=True).mean(),  label='ib1')
    plt.plot(dft[j].TsimMin, dft[j].Rdif_ib2.rolling(window=9 * 1, center=True).mean(), linestyle="--",  label='ib2')

    plt.legend(loc='upper right', fontsize='xx-small')
    plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Josie_Islow_17/Islow_' + title + '.eps')
    plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Josie_Islow_17/Islow_' + title + '.png')
    plt.show()