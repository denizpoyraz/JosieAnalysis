import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Beta_Functions import ratiofunction_beta

tslow = 25 * 60
tfast = 20



#######################################################################################################################

df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_Data_nocut.csv", low_memory=False)

# df = df.drop(df[(df.Sim == 140)].index)
# df = df.drop(df[(df.Sim == 147)].index)

df = df[df.ADX == 0]

filtEN = df.ENSCI == 1
filtSP = df.ENSCI == 0

filtS10 = df.Sol == 1
filtS05 = df.Sol == 0.5

filtB10 = df.Buf == 1.0
filtB05 = df.Buf == 0.5

filterEN0505 = (filtEN & filtS05 & filtB05)
filterEN1010 = (filtEN & filtS10 & filtB10)
###
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

# rmean_en0505, rstd_en0505, rmedian_en0505 = ratiofunction_beta(df, sim_en0505, team_en0505, 'EN0505')
# rmean_en1010, rstd_en1010, rmedian_en1010 = ratiofunction_beta(df, sim_en1010, team_en1010, 'EN1010')
# rmean_sp0505, rstd_sp0505, rmedian_sp0505 = ratiofunction_beta(df, sim_sp0505, team_sp0505, 'SP0505')
# rmean_sp1010, rstd_sp1010, rmedian_sp1010= ratiofunction_beta(df, sim_sp1010, team_sp1010, 'SPsp1010')

rmean_en0505, rstd_en0505, rmedian_en0505, rqerr_en0505 = ratiofunction_beta(df, sim_en0505, team_en0505, 'EN0505')
rmean_en1010, rstd_en1010, rmedian_en1010, rqerr_en1010 = ratiofunction_beta(df, sim_en1010, team_en1010, 'EN1010')
rmean_sp0505, rstd_sp0505, rmedian_sp0505, rqerr_sp0505 = ratiofunction_beta(df, sim_sp0505, team_sp0505, 'SP0505')
rmean_sp1010, rstd_sp1010, rmedian_sp1010, rqerr_sp1010 = ratiofunction_beta(df, sim_sp1010, team_sp1010, 'SP1010')

r1_mean = np.concatenate((rmean_en0505[0], rmean_en1010[0], rmean_sp0505[0], rmean_sp1010[0]), axis=None)
r2_mean = np.concatenate((rmean_en0505[1], rmean_en1010[1], rmean_sp0505[1], rmean_sp1010[1]), axis=None)
r3_mean = np.concatenate((rmean_en0505[2], rmean_en1010[2], rmean_sp0505[2], rmean_sp1010[2]), axis=None)
r4_mean = np.concatenate((rmean_en0505[3], rmean_en1010[3], rmean_sp0505[3], rmean_sp1010[3]), axis=None)

r1_median = np.concatenate((rmedian_en0505[0], rmedian_en1010[0], rmedian_sp0505[0], rmedian_sp1010[0]), axis=None)
r2_median = np.concatenate((rmedian_en0505[1], rmedian_en1010[1], rmedian_sp0505[1], rmedian_sp1010[1]), axis=None)
r3_median = np.concatenate((rmedian_en0505[2], rmedian_en1010[2], rmedian_sp0505[2], rmedian_sp1010[2]), axis=None)
r4_median = np.concatenate((rmedian_en0505[3], rmedian_en1010[3], rmedian_sp0505[3], rmedian_sp1010[3]), axis=None)

r_en0505_R1_4 = np.concatenate((rmean_en0505[0], rmean_en0505[1], rmean_en0505[2], rmean_en0505[3]), axis=None)
r_en1010_R1_4 = np.concatenate((rmean_en1010[0], rmean_en1010[1], rmean_en1010[2], rmean_en1010[3]), axis=None)
r_sp0505_R1_4 = np.concatenate((rmean_sp0505[0], rmean_sp0505[1], rmean_sp0505[2], rmean_sp0505[3]), axis=None)
r_sp1010_R1_4 = np.concatenate((rmean_sp1010[0], rmean_sp1010[1], rmean_sp1010[3], rmean_sp1010[3]), axis=None)

r_en0505_R2_4 = np.concatenate((rmean_en0505[1], rmean_en0505[2], rmean_en0505[3]), axis=None)
r_en1010_R2_4 = np.concatenate((rmean_en1010[1], rmean_en1010[2], rmean_en1010[3]), axis=None)
r_sp0505_R2_4 = np.concatenate((rmean_sp0505[1], rmean_sp0505[2], rmean_sp0505[3]), axis=None)
r_sp1010_R2_4 = np.concatenate((rmean_sp1010[1], rmean_sp1010[2], rmean_sp1010[3]), axis=None)

r_en0505_R2_4_median = np.concatenate((rmedian_en0505[1], rmedian_en0505[2], rmedian_en0505[3]), axis=None)
r_en1010_R2_4_median = np.concatenate((rmedian_en1010[1], rmedian_en1010[2], rmedian_en1010[3]), axis=None)
r_sp0505_R2_4_median = np.concatenate((rmedian_sp0505[1], rmedian_sp0505[2], rmedian_sp0505[3]), axis=None)
r_sp1010_R2_4_median = np.concatenate((rmedian_sp1010[1], rmedian_sp1010[2], rmedian_sp1010[3]), axis=None)

beta_en0505 = np.nanmedian(r_en0505_R2_4_median)
beta_en1010 = np.nanmedian(r_en1010_R2_4_median)
beta_sp0505 = np.nanmedian(r_sp0505_R2_4_median)
beta_sp1010 = np.nanmedian(r_sp1010_R2_4_median)

print('betas median', beta_en0505, beta_en1010, beta_sp0505, beta_sp1010)

# now use this beta values * 0.1 for the deconvolution of the signal and make a DF

## if you want to convolute another data-set, like 2017, you need to introduce it here

# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_Data_nocut.csv", low_memory=False)
# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_Data_nocut.csv", low_memory=False)


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

for j in range(len(simlist)):

    sondestr = ''
    adxstr = ''
    solstr = ''
    bufstr = ''

    af = 1
    beta = 0

    if (ensci[j] == 1) & (sol[j] == 0.5) & (buff[j] == 0.5): beta = beta_en0505 * 0.1
    if (ensci[j] == 1) & (sol[j] == 1.0) & (buff[j] == 1.0): beta = beta_en1010 * 0.1
    if (ensci[j] == 0) & (sol[j] == 0.5) & (buff[j] == 0.5): beta = beta_sp0505 * 0.1
    if (ensci[j] == 0) & (sol[j] == 1.0) & (buff[j] == 1.0): beta = beta_sp1010 * 0.1
    if (ensci[j] == 1) & (sol[j] == 1.0) & (buff[j] == 0.1): beta = 0.031
    if (ensci[j] == 0) & (sol[j] == 1.0) & (buff[j] == 0.1): beta = 0.031


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
    dft[j] = dft[j].reset_index()

    size = len(dft[j])
    Islow = [0] * size
    Islow_conv = [0] * size
    Ifast = [0] * size
    Ifast_deconv = [0] * size
    Ifastminib0 = [0] * size
    Ifastminib0_deconv = [0] * size
    Ifast_deconv_smb = [0] * size


    for i in range(1, size - 1):
        t1 = dft[j].at[i + 1, 'Tsim']
        t2 = dft[j].at[i, 'Tsim']
        Xs = np.exp(-(t1 - t2) / tslow)
        Xf = np.exp(-(t1 - t2) / tfast)

        Islow[i] = beta * dft[j].at[i, 'I_OPM_jma']
        Islow_conv[i + 1] = Islow[i] - (Islow[i] - Islow_conv[i]) * Xs

        Ifast[i + 1] = af * (dft[j].at[i + 1, 'IM'] - Islow_conv[i + 1])
        Ifastminib0[i + 1] = af * (dft[j].at[i + 1, 'IM'] - Islow_conv[i + 1] - dft[j].at[i + 1, 'IB0'] )

        Ifast_deconv[i + 1] = (Ifast[i + 1] - Ifast[i] * Xf) / (1 - Xf)
        Ifastminib0_deconv[i + 1] = (Ifastminib0[i + 1] - Ifastminib0[i] * Xf) / (1 - Xf)


    dft[j]['I_slow'] = Islow
    dft[j]['I_slow_conv'] = Islow_conv
    dft[j]['I_fast'] = Ifast
    dft[j]['I_fast_smb'] = dft[j].I_fast.rolling(window=3).mean()

    for ii in range(0, size - 1):
        t1 = dft[j].at[i + 1, 'Tsim']
        t2 = dft[j].at[i, 'Tsim']
        Xs = np.exp(-(t1 - t2) / tslow)
        Xf = np.exp(-(t1 - t2) / tfast)

        Ifast_deconv_smb[ii + 1] = (dft[j].at[ii + 1, 'I_fast_smb'] - dft[j].at[ii, 'I_fast_smb'] * Xf) / (1 - Xf)




    dft[j]['I_fast_deconv_smb'] = Ifast_deconv_smb

    dft[j]['I_fast_deconv'] = Ifast_deconv

    dft[j]['I_fastminib0'] = Ifastminib0
    dft[j]['I_fastminib0_deconv'] = Ifastminib0_deconv


    for k in range(len(dft[j])):
        ## jma corrections
        for p in range(len(JMA) - 1):
            if (dft[j].at[k, 'Pair'] >= Pval[p + 1]) & (dft[j].at[k, 'Pair'] < Pval[p]):
                # print(p, Pval[p + 1], Pval[p ])
                dft[j].at[k, 'PO3_deconv_jma'] = 0.043085 * dft[j].at[k, 'TPint'] * dft[j].at[k, 'I_fast_deconv'] / \
                                                (dft[j].at[k, 'PFcor'] * JMA[p])
                dft[j].at[k, 'PO3_deconv_smb_jma'] = 0.043085 * dft[j].at[k, 'TPint'] * dft[j].at[k, 'I_fast_deconv_smb'] / \
                                                (dft[j].at[k, 'PFcor'] * JMA[p])
                dft[j].at[k, 'PO3_minib0_deconv_jma'] = 0.043085 * dft[j].at[k, 'TPint'] * dft[j].at[k, 'I_fastminib0_deconv'] / \
                                                (dft[j].at[k, 'PFcor'] * JMA[p])
                dft[j].at[k, 'PO3_slow_conv_jma'] = 0.043085 * dft[j].at[k, 'TPint'] * dft[j].at[k, 'I_slow_conv'] / \
                                                 (dft[j].at[k, 'PFcor'] * JMA[p])

        if (dft[j].at[k, 'Pair'] <= Pval[14]):
            dft[j].at[k, 'PO3_deconv_jma'] = 0.043085 * dft[j].at[k, 'TPint'] * dft[j].at[k, 'I_fast_deconv'] / \
                                            (dft[j].at[k, 'PFcor'] * JMA[14])
            dft[j].at[k, 'PO3_deconv_smb_jma'] = 0.043085 * dft[j].at[k, 'TPint'] * dft[j].at[k, 'I_fast_deconv_smb'] / \
                                            (dft[j].at[k, 'PFcor'] * JMA[14])
            dft[j].at[k, 'PO3_minib0_deconv_jma'] = 0.043085 * dft[j].at[k, 'TPint'] * dft[j].at[k, 'I_fastminib0_deconv'] / \
                                            (dft[j].at[k, 'PFcor'] * JMA[14])
            dft[j].at[k, 'PO3_slow_conv_jma'] = 0.043085 * dft[j].at[k, 'TPint'] * dft[j].at[k, 'I_slow_conv'] / \
                                             (dft[j].at[k, 'PFcor'] * JMA[14])

    dft[j]['PO3_deconv'] = 0.043085 * dft[j]['TPint'] * dft[j]['I_fast_deconv'] / dft[j]['PFcor']
    dft[j]['PO3_deconv_smb'] = 0.043085 * dft[j]['TPint'] * dft[j]['I_fast_deconv_smb'] / dft[j]['PFcor']

    dft[j]['PO3_minib0_deconv'] = 0.043085 * dft[j]['TPint'] * dft[j]['I_fastminib0_deconv'] / dft[j]['PFcor']

    dft[j]['PO3_slow_conv'] = 0.043085 * dft[j]['TPint'] * dft[j]['I_slow_conv'] / dft[j]['PFcor']

    dft[j]['PO3_deconv_jma_sm6'] = dft[j].PO3_deconv_jma.rolling(window=3).mean()
    dft[j]['PO3_deconv_sm6'] = dft[j].PO3_deconv.rolling(window=3).mean()
    dft[j]['I_fast_deconv_sm6'] = dft[j].I_fast_deconv.rolling(window=3).mean()

    dft[j]['PO3_deconv_jma_sm10'] = dft[j].PO3_deconv_jma.rolling(window=5).mean()
    dft[j]['PO3_deconv_sm10'] = dft[j].PO3_deconv.rolling(window=5).mean()
    dft[j]['I_fast_deconv_sm10'] = dft[j].I_fast_deconv.rolling(window=5).mean()

    dft[j]['PO3_deconv_jma_sm14'] = dft[j].PO3_deconv_jma.rolling(window=7).mean()
    dft[j]['PO3_deconv_sm14'] = dft[j].PO3_deconv.rolling(window=7).mean()
    dft[j]['I_fast_deconv_sm14'] = dft[j].I_fast_deconv.rolling(window=7).mean()

    list_data.append(dft[j])

df_dc = pd.concat(list_data, ignore_index=True)

df_dc.to_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_deconv.csv")

# df_dc.to_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv.csv")
