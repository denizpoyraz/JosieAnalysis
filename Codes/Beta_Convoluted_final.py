import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Beta_Functions import ratiofunction_beta, ratiofunction_beta_9602
from Convolution_Functions import convolution, convolution_test, smooth_and_convolute, convolution_islow0


def mederr(med):
    err = (np.nanquantile(med, 0.75) - np.nanquantile(med, 0.25)) / (2 * 0.6745)
    return err


tslow = 25 * 60
tfast = 20


def filter(df):

    filtEN = df.ENSCI == 1
    filtSP = df.ENSCI == 0

    filtS10 = df.Sol == 1
    filtS05 = df.Sol == 0.5

    filtB10 = df.Buf == 1.0
    filtB05 = df.Buf == 0.5

    filterEN0505 = (filtEN & filtS05 & filtB05)
    filterEN1010 = (filtEN & filtS10 & filtB10)

    profEN0505 = df.loc[filterEN0505]
    profEN1010 = df.loc[filterEN1010]
    profEN0505_nodup = profEN0505.drop_duplicates(['Sim', 'Team'])
    profEN1010_nodup = profEN1010.drop_duplicates(['Sim', 'Team'])

    ###
    filterSP1010 = (filtSP & filtS10 & filtB10)
    filterSP0505 = (filtSP & filtS05 & filtB05)

    profSP1010 = df.loc[filterSP1010]
    profSP0505 = df.loc[filterSP0505]
    profSP1010_nodup = profSP1010.drop_duplicates(['Sim', 'Team'])
    profSP0505_nodup = profSP0505.drop_duplicates(['Sim', 'Team'])

    sim_en0505 = profEN0505_nodup.Sim.tolist()
    team_en0505 = profEN0505_nodup.Team.tolist()

    sim_en1010 = profEN1010_nodup.Sim.tolist()
    team_en1010 = profEN1010_nodup.Team.tolist()

    sim_sp0505 = profSP0505_nodup.Sim.tolist()
    team_sp0505 = profSP0505_nodup.Team.tolist()

    sim_sp1010 = profSP1010_nodup.Sim.tolist()
    team_sp1010 = profSP1010_nodup.Team.tolist()

    sim = [sim_en0505, sim_en1010, sim_sp0505, sim_sp1010]
    team = [team_en0505, team_en1010, team_sp0505, team_sp1010]

    return sim, team


#######################################################################################################################
# clist =[ 'Tsim', 'Sim', 'Team', 'ENSCI', 'Sol', 'Buf', 'Pair','PO3', 'IM','TPint', 'PO3_OPM', 'I_OPM', 'I_OPM_jma',
#          'I_conv_slow',  'PFcor', 'R1_Tstart', 'R1_Tstop', 'R2_Tstart', 'R2_Tstop']

# df1 = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_Data_nocut_1607.csv", low_memory=False)
# # df1 = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_Data_nocut_tempfixed_ml.csv", low_memory=False)
#
#
# df1 = df1[df1.ADX == 0]
#
# df1 = df1.drop(df1[(df1.Sim == 147) & (df1.Team == 3)].index)
# df1 = df1.drop(df1[(df1.Sim == 158) & (df1.Team == 1)].index)
# df1 = df1.drop(df1[(df1.Sim == 158) & (df1.Team == 2)].index)
# df1 = df1.drop(df1[(df1.Sim == 160) & (df1.Team == 4)].index)
# df1 = df1.drop(df1[(df1.Sim == 165) & (df1.Team == 4)].index)
#
#
# df2 = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie9602_Data.csv", low_memory=False)
#
# df2 = df2.drop([ 'SST_Nr', 'SondeTypeNr'], axis=1)
#
# df2 = df2.drop(df2[(df2.Sim == 92) & (df2.Team == 3)].index)
# df2 = df2.drop(df2[(df2.Sim == 98) & (df2.Team == 7)].index)
# df2 = df2.drop(df2[(df2.Sim == 99) & (df2.Team == 7)].index)
# df2 = df2.drop(df2[(df2.Sim == 97) & (df2.Team == 6)].index)
# df2 = df2.drop(df2[(df2.Sim == 98) & (df2.Team == 6)].index)
# df2 = df2.drop(df2[(df2.Sim == 99) & (df2.Team == 6)].index)
# df2 = df2.drop(df2[(df2.Sim == 92) & (df2.Team == 4)].index)
# df2 = df2.drop(df2[(df2.Sim == 97) & (df2.Team == 5)].index)
# df2 = df2.drop(df2[(df2.Sim == 98) & (df2.Team == 5)].index)
# df2 = df2.drop(df2[(df2.Sim == 99) & (df2.Team == 5)].index)
#
#
# sim_0910, team_0910 = filter(df1)
# sim_9602, team_9602 = filter(df2)
#
# ## for 0910
# rmean_en0505_0910, rstd_en0505, rmedian_en0505_0910, rqerr_en0505 = ratiofunction_beta(df1, sim_0910[0], team_0910[0], 'EN0505', 1, tslow, tfast)
# rmean_en1010_0910, rstd_en1010, rmedian_en1010_0910, rqerr_en1010 = ratiofunction_beta(df1, sim_0910[1], team_0910[1], 'EN1010', 1, tslow, tfast)
# rmean_sp0505_0910, rstd_sp0505, rmedian_sp0505_0910, rqerr_sp0505 = ratiofunction_beta(df1, sim_0910[2], team_0910[2], 'SP0505', 1, tslow, tfast)
# rmean_sp1010_0910, rstd_sp1010, rmedian_sp1010_0910, rqerr_sp1010 = ratiofunction_beta(df1, sim_0910[3], team_0910[3], 'SP1010', 1, tslow, tfast)
#
# r_en0505_R2_4_median = np.concatenate((rmedian_en0505_0910[1], rmedian_en0505_0910[2], rmedian_en0505_0910[3]), axis=None)
# r_en1010_R2_4_median = np.concatenate((rmedian_en1010_0910[1], rmedian_en1010_0910[2], rmedian_en1010_0910[3]), axis=None)
# r_sp0505_R2_4_median = np.concatenate((rmedian_sp0505_0910[1], rmedian_sp0505_0910[2], rmedian_sp0505_0910[3]), axis=None)
# r_sp1010_R2_4_median = np.concatenate((rmedian_sp1010_0910[1], rmedian_sp1010_0910[2], rmedian_sp1010_0910[3]), axis=None)
#
#
# ## for 9602
# rmean_en0505_9602, rstd_en0505_9602, rmedian_en0505_9602, rqerr_en0505_9602 = ratiofunction_beta_9602(df2, sim_9602[0], team_9602[0], 'EN0505', 1, tslow, tfast)
# rmean_en1010_9602, rstd_en1010_9602, rmedian_en1010_9602, rqerr_en1010_9602 = ratiofunction_beta_9602(df2, sim_9602[1], team_9602[1], 'EN1010', 1, tslow, tfast)
# rmean_sp0505_9602, rstd_sp0505_9602, rmedian_sp0505_9602, rqerr_sp0505_9602 = ratiofunction_beta_9602(df2, sim_9602[2], team_9602[2], 'SP0505', 1, tslow, tfast)
# rmean_sp1010_9602, rstd_sp1010_9602, rmedian_sp1010_9602, rqerr_sp1010_9602 = ratiofunction_beta_9602(df2, sim_9602[3], team_9602[3], 'SP1010', 1, tslow, tfast)
#
#
# rmean_en0505 = np.concatenate((rmean_en0505_9602, rmean_en0505_0910),  axis=None)
# rmean_en1010 = np.concatenate((rmean_en1010_9602, rmean_en1010_0910),  axis=None)
# rmean_sp0505 = np.concatenate((rmean_sp0505_9602, rmean_sp0505_0910),  axis=None)
# rmean_sp1010 = np.concatenate((rmean_sp1010_9602, rmean_sp1010_0910),  axis=None)
#
# # rmedian_en0505 = np.concatenate((rmedian_en0505_9602, rmedian_en0505_0910),  axis=None)
# # rmedian_en1010 = np.concatenate((rmedian_en1010_9602, rmedian_en1010_0910),  axis=None)
# # rmedian_sp0505 = np.concatenate((rmedian_sp0505_9602, rmedian_sp0505_0910),  axis=None)
# # rmedian_sp1010 = np.concatenate((rmedian_sp1010_9602, rmedian_sp1010_0910),  axis=None)
#
# rmedian_en0505 = np.concatenate((rmedian_en0505_9602, r_en0505_R2_4_median),  axis=None)
# rmedian_en1010 = np.concatenate((rmedian_en1010_9602, r_en1010_R2_4_median),  axis=None)
# rmedian_sp0505 = np.concatenate((rmedian_sp0505_9602, r_sp0505_R2_4_median),  axis=None)
# rmedian_sp1010 = np.concatenate((rmedian_sp1010_9602, r_sp1010_R2_4_median),  axis=None)
#
#
#
# # print('0910')
# # print(np.nanmedian(r_en0505_R2_4_median), np.nanmedian(r_en1010_R2_4_median), np.nanmedian(r_sp0505_R2_4_median), np.nanmedian(r_sp1010_R2_4_median))
# # print('0910 error qerr')
# # print(mederr(r_en0505_R2_4_median), mederr(r_en1010_R2_4_median), mederr(r_sp0505_R2_4_median), mederr(r_sp1010_R2_4_median))
# # # print('0910 error std')
# # print(stm_1, stm_2, stm_3, stm_4)
#
# # print(np.nanquantile(r_en0505_R2_4_median, 0.1587), np.nanquantile(r_en1010_R2_4_median, 0.1587), np.nanquantile(r_sp0505_R2_4_median, 0.1587),
# #       np.nanquantile(r_sp1010_R2_4_median, 0.1587))
#
# print('9602')
# print(np.nanmedian(rmedian_en0505_9602), np.nanmedian(rmedian_en1010_9602), np.nanmedian(rmedian_sp0505_9602), np.nanmedian(rmedian_sp1010_9602))
# print('9602 err')
# print(mederr(rmedian_en0505_9602), mederr(rmedian_en1010_9602), mederr(rmedian_sp0505_9602), mederr(rmedian_sp1010_9602))
# print('median en0505  en1010 sp0505 sp1010')
# print(np.nanmedian(rmedian_en0505), np.nanmedian(rmedian_en1010), np.nanmedian(rmedian_sp0505), np.nanmedian(rmedian_sp1010))
# print('all err')
# print(mederr(rmedian_en0505), mederr(rmedian_en1010), mederr(rmedian_sp0505), mederr(rmedian_sp1010))
# print('size')
# print(len(sim_0910[0]), len(sim_0910[1]), len(sim_0910[2]), len(sim_0910[3]))
# print(len(sim_9602[0]), len(sim_9602[1]), len(sim_9602[2]), len(sim_9602[3]))
#
#
#
# ######  0910 Data
# #
# # beta_en0505 = np.nanmedian(r_en0505_R2_4_median)
# # beta_en1010 = np.nanmedian(r_en1010_R2_4_median)
# # beta_sp0505 = np.nanmedian(r_sp0505_R2_4_median)
# # beta_sp1010 = np.nanmedian(r_sp1010_R2_4_median)
#
# ###### 0910 and 9602 Data
#
# beta_en0505 = np.nanmedian(rmedian_en0505)
# beta_en1010 = np.nanmedian(rmedian_en1010)
# beta_sp0505 = np.nanmedian(rmedian_sp0505)
# beta_sp1010 = np.nanmedian(rmedian_sp1010)
#
# beta_en0505_err = mederr(rmedian_en0505)
# beta_en1010_err = mederr(rmedian_en1010)
# beta_sp0505_err = mederr(rmedian_sp0505)
# beta_sp1010_err = mederr(rmedian_sp1010)
#
# print('betas median', beta_en0505, beta_en1010, beta_sp0505, beta_sp1010)

beta_en0505 = 0.1552231224907112
beta_en1010 = 0.46269323794360606
beta_sp0505 = 0.14767593999681244
beta_sp1010 = 0.5063263074879945

#
# now use this beta values * 0.1 for the deconvolution of the signal and make a DF

# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_Data_nocut_1607.csv", low_memory=False)
# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_Data_nocut.csv", low_memory=False)
df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_Data_nocut.csv", low_memory=False)
df['TS'] = pd.to_datetime(df.Tsim, unit = 's')



df['IM_sm12'] = df['IM'].rolling(window=6, center=True).mean()
df['I_OPM_jma_sm12'] = df['I_OPM_jma'].rolling(window=6, center=True).mean()

df['IMminusIB0'] = df['IM'] - df['iB0']

simlist = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Sim'])
teamlist = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Team'])
# adx = np.asarray(df.drop_duplicates(['Sim', 'Team'])['ADX'])
sol = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Sol'].tolist())
buff = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Buf'])
ensci = np.asarray(df.drop_duplicates(['Sim', 'Team'])['ENSCI'])

dft = {}
list_data = []

## jma corrections
Pval = np.array([1000, 730, 535, 382, 267, 185, 126, 85, 58, 39, 26.5, 18.1, 12.1, 8.3, 6])
JMA = np.array([0.999705941, 0.997216654, 0.995162562, 0.992733959, 0.989710199, 0.985943645, 0.981029252, 0.974634364,
                0.966705137, 0.956132227, 0.942864263, 0.9260478, 0.903069813, 0.87528384, 0.84516337])


##now try to use a different dataset: data every 12 seconds


for j in range(len(simlist)):

    sondestr = ''
    adxstr = ''
    solstr = ''
    bufstr = ''

    af = 1
    beta = 0

    if (ensci[j] == 1) & (sol[j] == 0.5) & (buff[j] == 0.5): beta = beta_en0505 * 0.1
    if (ensci[j] == 1) & (sol[j] == 1.0) & (buff[j] == 1.0): beta = beta_en1010  * 0.1
    if (ensci[j] == 0) & (sol[j] == 0.5) & (buff[j] == 0.5): beta = beta_sp0505   * 0.1
    if (ensci[j] == 0) & (sol[j] == 1.0) & (buff[j] == 1.0): beta = beta_sp1010  * 0.1
    if (ensci[j] == 1) & (sol[j] == 1.0) & (buff[j] == 0.1): beta = 0.030
    if (ensci[j] == 0) & (sol[j] == 1.0) & (buff[j] == 0.1): beta = 0.030

    # if (ensci[j] == 1) & (sol[j] == 0.5) & (buff[j] == 0.5): beta = (beta_en0505 - beta_en0505_err) * 0.1
    # if (ensci[j] == 1) & (sol[j] == 1.0) & (buff[j] == 1.0): beta = (beta_en1010  - beta_en1010_err)* 0.1
    # if (ensci[j] == 0) & (sol[j] == 0.5) & (buff[j] == 0.5): beta = (beta_sp0505 - beta_sp0505_err)  * 0.1
    # if (ensci[j] == 0) & (sol[j] == 1.0) & (buff[j] == 1.0): beta = (beta_sp1010 - beta_sp1010_err) * 0.1
    # if (ensci[j] == 1) & (sol[j] == 1.0) & (buff[j] == 0.1): beta = 0.031 - 0.010
    # if (ensci[j] == 0) & (sol[j] == 1.0) & (buff[j] == 0.1): beta = 0.031 - 0.010


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

    title = str(simlist[j]) + '_' + str(teamlist[j]) + '_' + adxstr + sondestr + solstr + '-' + bufstr + 'B'
    type = sondestr + ' ' + str(sol[j]) + '\% - ' + str(buff[j]) + 'B'
    sp = str(simlist[j]) + '-' + str(teamlist[j])
    ptitle = sp + ' ' + sondestr + ' ' + str(sol[j]) + '% - ' + str(buff[j]) + 'B'
    print(title)

    dft[j] = df[(df.Sim == simlist[j]) & (df.Team == teamlist[j])]
    ### for data of every 12 seconds
    # dft[j] = dft[j].resample('12S', on='TS').mean().interpolate()
    # df = df.reset_index()
    dft[j] = dft[j].reset_index()

    ##only for 2017
    # tfast = dft[j].loc[0,'RespTime_4_1p5_sec_p1']
    # if tfast < 0: tfast = 20
    # # print(j, title, tfast)

    # dft[j]['IM_sm12'] = dft[j]['IM'].rolling(window=6, center=True).mean()
    # dft[j]['I_OPM_jma_sm12'] = dft[j]['I_OPM_jma'].rolling(window=6, center=True).mean()


    # dft[j]



    Islow, Islow_conv, Ifast, Ifast_deconv, Ifastminib0, Ifastminib0_deconv = convolution(dft[j], 'I_OPM_jma', 'IM', 'Tsim', beta, 1)
    Islow_sm, Islow_conv_sm, Ifast_sm, Ifast_deconv_sm, Ifastminib0_sm, Ifastminib0_deconv_sm = convolution(dft[j], 'I_OPM_jma_sm12', 'IM_sm12', 'Tsim', beta, 1)
    iB1_var = (dft[j].at[0,'iB1'] - dft[j].at[0,'iB0'])
    iB2_var = (dft[j].at[0,'iB2'] - dft[j].at[0,'iB0'])
    print(title,dft[j].at[0,'iB1'] , dft[j].at[0,'iB2'] )
    Imean_simbegin = np.median(dft[j][(dft[j].Tsim >= 4) & (dft[j].Tsim < 150)]['IM'].tolist())
    I0_var = Imean_simbegin - dft[j].at[0,'iB0']
    iB1_var = (dft[j].at[0,'iB1'] - dft[j].at[0,'iB0'])

    dft[j]['IMminusIB0'] = dft[j]['IM'] - dft[j]['iB0']


    Islow_i0var, Islow_conv_i0var, Ifast_i0var, Ifast_deconv_i0var, Ifastminib0_i0var, Ifastminib0_deconv_i0var = \
        convolution_islow0(dft[j], I0_var ,'IMminusIB0', 'IM', 'Tsim', beta, 1)
    Islow_ib1, Islow_conv_ib1, Ifast_ib1, Ifast_deconv_ib1, Ifastminib0_ib1, Ifastminib0_deconv_ib1 = \
        convolution_islow0(dft[j], iB1_var ,'IMminusIB0', 'IM', 'Tsim', beta, 1)
    Islow_ib2, Islow_conv_ib2, Ifast_ib2, Ifast_deconv_ib2, Ifastminib0_ib2, Ifastminib0_deconv_ib2 = \
        convolution_islow0(dft[j], iB2_var ,'IMminusIB0', 'IM', 'Tsim', beta, 1)

    dft[j]['Islow'] = Islow
    dft[j]['Islow_conv'] = Islow_conv
    dft[j]['Ifast'] = Ifast
    dft[j]['Ifast_minib0'] = Ifastminib0
    dft[j]['Ifast_deconv'] = Ifast_deconv
    dft[j]['Ifast_minib0_deconv'] = Ifastminib0_deconv

    dft[j]['Islow_i0var'] = Islow_i0var
    dft[j]['Islow_conv_i0var'] = Islow_conv_i0var
    dft[j]['Ifast_i0var'] = Ifast_i0var
    dft[j]['Ifast_minib0_i0var'] = Ifastminib0_i0var
    dft[j]['Ifast_deconv_i0var'] = Ifast_deconv_i0var
    dft[j]['Ifast_minib0_deconv_i0var'] = Ifastminib0_deconv_i0var

    dft[j]['Islow_ib1'] = Islow_ib1
    dft[j]['Islow_conv_ib1'] = Islow_conv_ib1
    dft[j]['Ifast_ib1'] = Ifast_ib1
    dft[j]['Ifast_minib0_ib1'] = Ifastminib0_ib1
    dft[j]['Ifast_deconv_ib1'] = Ifast_deconv_ib1
    dft[j]['Ifast_minib0_deconv_ib1'] = Ifastminib0_deconv_ib1

    dft[j]['Islow_ib2'] = Islow_ib2
    dft[j]['Islow_conv_ib2'] = Islow_conv_ib2
    dft[j]['Ifast_ib2'] = Ifast_ib2
    dft[j]['Ifast_minib0_ib2'] = Ifastminib0_ib2
    dft[j]['Ifast_deconv_ib2'] = Ifast_deconv_ib2
    dft[j]['Ifast_minib0_deconv_ib2'] = Ifastminib0_deconv_ib2


    dft[j]['Islow_sm12'] = Islow_sm
    dft[j]['Islow_conv_sm12'] = Islow_conv_sm
    dft[j]['Ifast_sm12'] = Ifast_sm
    dft[j]['Ifast_minib0_sm12'] = Ifastminib0_sm
    dft[j]['Ifast_deconv_sm12'] = Ifast_deconv_sm
    dft[j]['Ifast_minib0_deconv_sm12'] = Ifastminib0_deconv_sm



    # for k in range(len(dft[j])):
    #     ## jma corrections
    #     for p in range(len(JMA) - 1):
    #         if (dft[j].at[k, 'Pair'] >= Pval[p + 1]) & (dft[j].at[k, 'Pair'] < Pval[p]):
    #             # print(p, Pval[p + 1], Pval[p ])
    #             dft[j].at[k, 'PO3_deconv_jma'] = 0.043085 * dft[j].at[k, 'TPext'] * dft[j].at[k, 'Ifast_deconv'] / \
    #                                             (dft[j].at[k, 'PFcor'] * JMA[p])
    #             dft[j].at[k, 'PO3_minib0_deconv'] = 0.043085 * dft[j].at[k, 'TPext'] * dft[j].at[k, 'Ifast_minib0_deconv'] / \
    #                                             (dft[j].at[k, 'PFcor'] * JMA[p])
    #
    #
    #     if (dft[j].at[k, 'Pair'] <= Pval[14]):
    #         dft[j].at[k, 'PO3_deconv_jma'] = 0.043085 * dft[j].at[k, 'TPext'] * dft[j].at[k, 'Ifast_deconv'] / \
    #                                         (dft[j].at[k, 'PFcor'] * JMA[14])
    #         dft[j].at[k, 'PO3_minib0_deconv'] = 0.043085 * dft[j].at[k, 'TPext'] * dft[j].at[k, 'Ifast_minib0_deconv'] / \
    #                                         (dft[j].at[k, 'PFcor'] * JMA[14])




    list_data.append(dft[j])

df_dc = pd.concat(list_data, ignore_index=True)

# df_dc.to_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv_0510.csv")

# df_dc.to_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_deconv.csv")

# df_dc.to_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_deconv_final.csv")

## naming beta2:  used all data for betas, also en0505 and spc0505 in 9602 data

#
# Islow = [0] * size
# Islow_conv = [0] * size
# Ifast = [0] * size
# Ifastminib0 = [0] * size
# Ifast_deconv = [0] * size
# Ifastminib0_deconv = [0] * size
#
# Ifast_deconv_hv = [0] * size
# Ifastminib0_deconv_hv = [0] * size
# Ifast_deconv_hs = [0] * size
# Ifastminib0_deconv_hs = [0] * size
#
# for i in range(0, size - 1):
#     t1 = dft[j].at[i + 1, 'Tsim']
#     t2 = dft[j].at[i, 'Tsim']
#
#     Xs = np.exp(-(t1 - t2) / tslow)
#     Xf = np.exp(-(t1 - t2) / tfast)
#
#     # ###########  for 0910 data
#     # dft[j].at[i,'iB0'] = 0.014
#
#     Islow[i] = beta * dft[j].at[i, 'I_OPM_jma']
#     Islow_conv[i + 1] = Islow[i + 1] - (Islow[i + 1] - Islow_conv[i]) * Xs
#
#     Ifast[i + 1] = af * (dft[j].at[i + 1, 'IM'] - Islow_conv[i + 1])
#     Ifastminib0[i + 1] = af * (dft[j].at[i + 1, 'IM'] - Islow_conv[i + 1] - dft[j].at[i + 1, 'iB0'])
#
#     Ifast_deconv[i + 1] = (Ifast[i + 1] - Ifast[i] * Xf) / (1 - Xf)
#     Ifastminib0_deconv[i + 1] = (Ifastminib0[i + 1] - Ifastminib0[i] * Xf) / (1 - Xf)
#
#     Ifast_deconv_hs[i + 1] = Ifast[i] + tfast / (t1 - t2) * (Ifast[i + 1] - Ifast[i])
#     Ifastminib0_deconv_hs[i + 1] = Ifastminib0[i] + tfast / (t1 - t2) * (Ifastminib0[i + 1] - Ifastminib0[i])
#
#     Ifast_deconv_hv[i + 1] = Ifast[i + 1] + tfast / (t1 - t2) * (Ifast[i + 1] - Ifast[i])
#     Ifastminib0_deconv_hv[i + 1] = Ifastminib0[i + 1] + tfast / (t1 - t2) * (Ifastminib0[i + 1] - Ifastminib0[i])