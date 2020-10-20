import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.gridspec as gridspec
import pickle
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,AutoMinorLocator)

df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_Deconv_preparationadded_all_ft.csv", low_memory=False)
dfo = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_Deconv_preparationadded_simulation_ft.csv", low_memory=False)


simlist = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Sim'])
teamlist = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Team'])
# adx = np.asarray(df.drop_duplicates(['Sim', 'Team'])['ADX'])
sol = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Sol'].tolist())
buff = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Buf'])
ensci = np.asarray(df.drop_duplicates(['Sim', 'Team'])['ENSCI'])

dft = {}
dfto = {}

difarr = [0.0] * simlist
decaytime = [0.0] * simlist

iB0 = np.zeros(len(simlist));
iB1 = np.zeros(len(simlist));
Y1 = np.zeros(len(simlist));
Y2ep = np.zeros(len(simlist));
Y2bs = np.zeros(len(simlist))
Y2mY1 = np.zeros(len(simlist));
Y3 = np.zeros(len(simlist));
Y3D = np.zeros(len(simlist));
Y4 = np.zeros(len(simlist));
Y4mY3 = np.zeros(len(simlist));
Y5 = np.zeros(len(simlist));
iB2 = np.zeros(len(simlist));
Y6 = np.zeros(len(simlist));
Y5mY6 = np.zeros(len(simlist))
t_decay = np.zeros(len(simlist))
t3 = np.zeros(len(simlist))

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

    dft[j] = df[(df.Sim == simlist[j]) & (df.Team == teamlist[j])]
    dfto[j] = dfo[(dfo.Sim == simlist[j]) & (dfo.Team == teamlist[j])]

    difarr[j]  = np.array(dft[j][dft[j].Tsim_original == 10]['I_slow_conv'].tolist())[0] - np.array(dfto[j][dfto[j].Tsim_original ==10]['I_slow_conv_ib1_decay'].tolist())[0]
    decaytime[j] = dft[j].at[dft[j].first_valid_index(), 'decay_time']/60



    t_prep_end = dft[j][(dft[j].TimeTag == 'Prep')].Tsim.max()
    t_sim_begin = dft[j][(dft[j].TimeTag == 'Sim')].Tsim.min()
    t3[j] = t_sim_begin - t_prep_end
    t_decay[j] = dft[j].at[dft[j].first_valid_index(), 'decay_time']
    t_ib2 = t_sim_begin + 7 * 60

    iB0[j] = dft[j].at[dft[j].first_valid_index(), 'iB0']
    iB1[j] = dft[j].at[dft[j].first_valid_index(), 'iB1']
    Y1[j] = iB1[j] - iB0[j]
    Y2ep[j] = dft[j][dft[j].Tsim == t_prep_end].I_slow_conv.tolist()[0]
    Y2bs[j] = dft[j][dft[j].Tsim == t_sim_begin].I_slow_conv.tolist()[0]
    Y2mY1[j] = Y2ep[j] - Y1[j]
    Y3[j] = (Y1[j]) * np.exp(-t3[j] / (25 * 60))
    Y3D[j] = (Y1[j]) * np.exp(-t_decay[j] / (25 * 60))
    Y4[j] = dft[j][dft[j].Tsim == t_sim_begin].I_slow_conv.tolist()[0]
    Y4mY3[j] = Y4[j] - Y3[j]
    Y5[j] = dft[j][dft[j].Tsim == t_ib2].I_slow_conv.tolist()[0]
    iB2[j] = dft[j].at[dft[j].first_valid_index(), 'iB2']
    Y6[j] = iB2[j] - iB0[j]
    Y5mY6[j] = Y5[j] - Y6[j]

    # print(decaytime[j])

    # print(np.array(dft[j][dft[j].Tsim_original == 10]['I_slow_conv'].tolist())[0] - np.array(dfto[j][dfto[j].Tsim_original ==10]['I_slow_conv_ib1_decay'].tolist())[0], np.array(dfto[j][dfto[j].Tsim_original == 10]['I_slow_conv_ib1_decay'].tolist()))
    # print(difarr[j])
    # print(decaytime[j])
fig, ax = plt.subplots()
# fig,ax = plt.figure()
# ax=fig.add_axes([0,0,1,1])
ax.scatter(decaytime, difarr, color='r', label = r'Islow$_{reference}$ - Islow$_{ib1decay}$' )
ax.scatter(decaytime, difarr, color='r', label = r'Islow$_{reference}$ - Islow$_{ib1decay}$' )

# ax.set_ylabel(r'Islow$_{reference}$ - Islow$_{ib1decay}$')
ax.set_xlabel('Decay Time (mins)')

# fig, ax2 = plt.subplots()
# # fig,ax = plt.figure()
# # ax=fig.add_axes([0,0,1,1])
# ax2.scatter(decaytime, difarr, color='r')
# ax2.set_ylabel(r'Islow$_{reference}$ - Islow$_{ib1decay}$')
# ax2.set_xlabel('Decay Time (mins)')

# plt.plot(decaytime, difarr)
plt.show()