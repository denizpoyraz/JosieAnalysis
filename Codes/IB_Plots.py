import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from Josie_Functions import  Calc_average_profile_pressure, Calc_average_profile_time, Calc_Dif, Calc_average_profileCurrent_pressure, Calc_average_Dif
from Josie_PlotFunctions import  errorPlot_ARDif_withtext, errorPlot_general

def cuts2017(dfm):

    dfm = dfm.drop(dfm[(dfm.PO3 < 0)].index)
    dfm = dfm.drop(dfm[(dfm.PO3_OPM < 0)].index)

    dfm = dfm.drop(dfm[(dfm.Sim == 179) & (dfm.Team == 4)].index)
    dfm = dfm.drop(dfm[(dfm.Sim == 172) & (dfm.Team == 1)].index)
    dfm = dfm.drop(dfm[(dfm.Sim == 178) & (dfm.Team == 3)].index)
    dfm = dfm.drop(dfm[((dfm.Sim == 175))].index)

    dfm = dfm.drop(dfm[(dfm.Sim == 179) & (dfm.Team == 4) & (dfm.Tsim > 4000)].index)
    dfm = dfm.drop(dfm[(dfm.Sim == 172) & (dfm.Tsim < 500)].index)
    dfm = dfm.drop(dfm[(dfm.Sim == 172) & (dfm.Team == 1) & (dfm.Tsim > 5000) & (dfm.Tsim < 5800)].index)
    dfm = dfm.drop(dfm[(dfm.Sim == 178) & (dfm.Team == 3) & (dfm.Tsim > 1700) & (dfm.Tsim < 2100)].index)
    dfm = dfm.drop(dfm[(dfm.Sim == 178) & (dfm.Team == 3) & (dfm.Tsim > 2500) & (dfm.Tsim < 3000)].index)

    dfm = dfm.drop(dfm[((dfm.Sim == 186) & (dfm.Tsim > 5000))].index)
    dfm = dfm.drop(dfm[((dfm.Tsim > 7000))].index)


    return dfm

def cuts0910(dfm):

    dfm = dfm.drop(dfm[(dfm.PO3 < 0)].index)
    dfm = dfm.drop(dfm[(dfm.PO3_OPM < 0)].index)

    dfm = dfm[dfm.ADX == 0]
    # # v2 cuts, use this and v3 standard more conservative cuts not valid for 140, 1122, 163, 166  v2
    dfm=dfm[dfm.Tsim > 900]
    dfm=dfm[dfm.Tsim <= 8100]
    dfm = dfm.drop(dfm[(dfm.Sim == 141) & (dfm.Team == 3)].index)
    # dfm = dfm.drop(dfm[(dfm.Sim == 143) & (dfm.Team == 2) & (dfm.Tsim > 7950) & (dfm.Tsim < 8100)].index)
    dfm = dfm.drop(dfm[(dfm.Sim == 147) & (dfm.Team == 3)].index)
    dfm = dfm.drop(dfm[(dfm.Sim == 158) & (dfm.Team == 2)].index)
    dfm = dfm.drop(dfm[(dfm.Sim == 167) & (dfm.Team == 4)].index)
    # ## new cuts v2 20/05
    # dfm = dfm.drop(dfm[(dfm.Sim == 160) & (dfm.Team == 4)].index)
    # dfm = dfm.drop(dfm[(dfm.Sim == 165) & (dfm.Team == 4)].index)

    # # ## v3 cuts
    ### I think these cuts are not needed## checkcheck
    dfm = dfm.drop(dfm[(dfm.Sim == 159) & (dfm.Team == 1)].index)
    dfm = dfm.drop(dfm[(dfm.Sim == 158) & (dfm.Team == 1)].index)
    dfm = dfm.drop(dfm[(dfm.Sim == 163) & (dfm.Team == 4)].index)
    dfm = dfm.drop(dfm[(dfm.Sim == 159) & (dfm.Team == 4)].index)

    return dfm

def filter0910(dfm):

    filtEN = dfm.ENSCI == 1
    filtSP = dfm.ENSCI == 0

    filtS10 = dfm.Sol == 1
    filtS05 = dfm.Sol == 0.5

    filtB10 = dfm.Buf == 1.0
    filtB05 = dfm.Buf == 0.5

    filterEN0505 = (filtEN & filtS05 & filtB05)
    filterEN1010 = (filtEN & filtS10 & filtB10)

    profEN0505 = dfm.loc[filterEN0505]
    profEN1010 = dfm.loc[filterEN1010]

    profEN0505_nodup = profEN0505.drop_duplicates(['Sim', 'Team'])
    profEN1010_nodup = profEN1010.drop_duplicates(['Sim', 'Team'])

    totO3_EN0505 = profEN0505_nodup.frac.mean()
    totO3_EN1010 = profEN1010_nodup.frac.mean()

    filterSP1010 = (filtSP & filtS10 & filtB10)
    filterSP0505 = (filtSP & filtS05 & filtB05)

    profSP1010 = dfm.loc[filterSP1010]
    profSP0505 = dfm.loc[filterSP0505]

    profSP1010_nodup = profSP1010.drop_duplicates(['Sim', 'Team'])
    profSP0505_nodup = profSP0505.drop_duplicates(['Sim', 'Team'])

    totO3_SP1010 = profSP1010_nodup.frac.mean()
    totO3_SP0505 = profSP0505_nodup.frac.mean()

    prof = [profEN0505, profEN1010, profSP0505, profSP1010]

    o3list = [totO3_EN0505, totO3_EN1010, totO3_SP0505, totO3_SP1010]
    dfnplist = [profEN0505.drop_duplicates(['Sim', 'Team']), profEN1010.drop_duplicates(['Sim', 'Team']), profSP0505_nodup,profSP1010_nodup]

    return prof, o3list, dfnplist

###################################################


def filter2017(dfm):

     filtEN = dfm.ENSCI == 1
     filtSP = dfm.ENSCI == 0

     filtS10 = dfm.Sol == 1
     filtS05 = dfm.Sol == 0.5

     filtB10 = dfm.Buf == 1.0
     filtB05 = dfm.Buf == 0.5
     filtB01 = dfm.Buf == 0.1

     filterEN0505 = (filtEN & filtS05 & filtB05)
     filterEN1001 = (filtEN & filtS10 & filtB01)

     profEN0505 = dfm.loc[filterEN0505]
     profEN1001 = dfm.loc[filterEN1001]

     profEN0505_nodup = profEN0505.drop_duplicates(['Sim', 'Team'])
     profEN1001_nodup = profEN1001.drop_duplicates(['Sim', 'Team'])

     totO3_EN0505 = profEN0505_nodup.frac.mean()
     totO3_EN1001 = profEN1001_nodup.frac.mean()

     filterSP1010 = (filtSP & filtS10 & filtB10)
     filterSP1001 = (filtSP & filtS10 & filtB01)

     profSP1010 = dfm.loc[filterSP1010]
     profSP1001 = dfm.loc[filterSP1001]

     profSP1010_nodup = profSP1010.drop_duplicates(['Sim', 'Team'])
     profSP1001_nodup = profSP1001.drop_duplicates(['Sim', 'Team'])

     totO3_SP1010 = profSP1010_nodup.frac.mean()
     totO3_SP1001 = profSP1001_nodup.frac.mean()

     prof = [profEN0505, profEN1001, profSP1001, profSP1010]

     o3list = [totO3_EN0505, totO3_EN1001, totO3_SP1001, totO3_SP1010]
     dfnplist = [profEN0505.drop_duplicates(['Sim', 'Team']), profEN1001.drop_duplicates(['Sim', 'Team']),
                 profSP1001_nodup, profSP1010_nodup]

     return prof, o3list, dfnplist

###########

def add_variable(dfm, varout, varin, betastr):

    if betastr == 'beta':

        beta_en0505 = 0.24791411481547287
        beta_en1010 = 0.5537230764611312
        beta_sp0505 = 0.23766405914759725
        beta_sp1010 = 0.625611421042088

        dfm[(dfm.ENSCI == 1) & (dfm.Sol == 0.5) & (dfm.Buf == 0.5)].varout = beta_en0505 * 0.1 * dfm[
            (dfm.ENSCI == 1) & (dfm.Sol == 0.5) & (dfm.Buf == 0.5)].varin
        dfm[(dfm.ENSCI == 1) & (dfm.Sol == 1.0) & (dfm.Buf == 1.0)].varout = beta_en1010 * 0.1 * dfm[
            (dfm.ENSCI == 1) & (dfm.Sol == 1.0) & (dfm.Buf == 1.0)].varin
        dfm[(dfm.ENSCI == 0) & (dfm.Sol == 0.5) & (dfm.Buf == 0.5)].varout = beta_sp0505 * 0.1 * dfm[
            (dfm.ENSCI == 0) & (dfm.Sol == 0.5) & (dfm.Buf == 0.5)].varin
        dfm[(dfm.ENSCI == 0) & (dfm.Sol == 1.0) & (dfm.Buf == 1.0)].varout = beta_sp1010 * 0.1 * dfm[
            (dfm.ENSCI == 0) & (dfm.Sol == 1.0) & (df.Buf == 1.0)].varin

    if betastr == 'beta0':

        beta_en0505 = 0.1552677859550236
        beta_en1010 = 0.45145867983583615
        beta_sp0505 = 0.15417919516510625
        beta_sp1010 = 0.5114834887069901

        dfm[(dfm.ENSCI == 1) & (dfm.Sol == 0.5) & (dfm.Buf == 0.5)].varout = beta_en0505 * 0.1 * dfm[
            (dfm.ENSCI == 1) & (dfm.Sol == 0.5) & (dfm.Buf == 0.5)].varin
        dfm[(dfm.ENSCI == 1) & (dfm.Sol == 1.0) & (dfm.Buf == 1.0)].varout = beta_en1010 * 0.1 * dfm[
            (dfm.ENSCI == 1) & (dfm.Sol == 1.0) & (dfm.Buf == 1.0)].varin
        dfm[(dfm.ENSCI == 0) & (dfm.Sol == 0.5) & (dfm.Buf == 0.5)].varout = beta_sp0505 * 0.1 * dfm[
            (dfm.ENSCI == 0) & (dfm.Sol == 0.5) & (dfm.Buf == 0.5)].varin
        dfm[(dfm.ENSCI == 0) & (dfm.Sol == 1.0) & (dfm.Buf == 1.0)].varout = beta_sp1010 * 0.1 * dfm[
            (dfm.ENSCI == 0) & (dfm.Sol == 1.0) & (df.Buf == 1.0)].varin


    return dfm

folderpath = 'IB_plots'

# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_Data_nocut.csv", low_memory=False)
# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_Data_nocut.csv", low_memory=False)
df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_deconv_1607.csv", low_memory=False)

#
df = cuts0910(df)
# df['Islow_beta'] = 0
# df['Islow_beta0'] = 0
# df['Ifast_beta'] = 0
# df['Ifast_beta0'] = 0
#
# # df = add_variable(df, 'Islow_beta', 'I_OPM_jma', 'beta')
# # df = add_variable(df, 'Islow_beta0', 'I_OPM_jma', 'beta0')
#
# beta_en0505 = 0.24791411481547287
# beta_en1010 = 0.5537230764611312
# beta_en1001 = 0.3
#
# beta_sp0505 = 0.23766405914759725
# beta_sp1010 = 0.625611421042088
# beta_sp1001 = 0.3


# df.loc[(df.ENSCI == 1) & (df.Sol == 0.5) & (df.Buf == 0.5), 'Islow_beta'] = beta_en0505 * 0.1 * df[(df.ENSCI == 1) & (df.Sol == 0.5) & (df.Buf == 0.5)]['I_OPM_jma']
# df.loc[(df.ENSCI == 1) & (df.Sol == 1.0) & (df.Buf == 1.0), 'Islow_beta'] = beta_en1010 * 0.1 * df[(df.ENSCI == 1) & (df.Sol == 1.0) & (df.Buf == 1.0)]['I_OPM_jma']
# df.loc[(df.ENSCI == 0) & (df.Sol == 0.5) & (df.Buf == 0.5), 'Islow_beta'] = beta_sp0505 * 0.1 * df[(df.ENSCI == 0) & (df.Sol == 0.5) & (df.Buf == 0.5)]['I_OPM_jma']
# df.loc[(df.ENSCI == 0) & (df.Sol == 1.0) & (df.Buf == 1.0), 'Islow_beta'] = beta_sp1010 * 0.1 * df[(df.ENSCI == 0) & (df.Sol == 1.0) & (df.Buf == 1.0)]['I_OPM_jma']
#
# df.loc[(df.ENSCI == 1) & (df.Sol == 0.5) & (df.Buf == 0.5), 'Islow_beta'] = beta_en0505 * 0.1 * df[(df.ENSCI == 1) & (df.Sol == 0.5) & (df.Buf == 0.5)]['I_OPM_jma']
# df.loc[(df.ENSCI == 1) & (df.Sol == 1.0) & (df.Buf == 0.1), 'Islow_beta'] = beta_en1001 * 0.1 * df[(df.ENSCI == 1) & (df.Sol == 1.0) & (df.Buf == 0.1)]['I_OPM_jma']
# df.loc[(df.ENSCI == 0) & (df.Sol == 1.0) & (df.Buf == 0.1), 'Islow_beta'] = beta_sp1001 * 0.1 * df[(df.ENSCI == 0) & (df.Sol == 1.0) & (df.Buf == 0.1)]['I_OPM_jma']
# df.loc[(df.ENSCI == 0) & (df.Sol == 1.0) & (df.Buf == 1.0), 'Islow_beta'] = beta_sp1010 * 0.1 * df[(df.ENSCI == 0) & (df.Sol == 1.0) & (df.Buf == 1.0)]['I_OPM_jma']

# beta0_en0505 = 0.1552677859550236
# beta0_en1010 = 0.45145867983583615
# beta0_en1001 = 0.3
# beta0_sp0505 = 0.15417919516510625
# beta0_sp1010 = 0.5114834887069901
# beta0_sp1001 = 0.3

df = df.drop(df[(df.iB1 < -1)].index)
df = df.drop(df[(df.iB2 < -1)].index)
# 
# df.loc[(df.ENSCI == 1) & (df.Sol == 0.5) & (df.Buf == 0.5),'Islow_beta0'] = beta0_en0505 * 0.1 * df[(df.ENSCI == 1) & (df.Sol == 0.5) & (df.Buf == 0.5)]['I_OPM_jma']
# df.loc[(df.ENSCI == 1) & (df.Sol == 1.0) & (df.Buf == 1.0),'Islow_beta0'] = beta0_en1010 * 0.1 * df[(df.ENSCI == 1) & (df.Sol == 1.0) & (df.Buf == 1.0)]['I_OPM_jma']
# df.loc[(df.ENSCI == 0) & (df.Sol == 0.5) & (df.Buf == 0.5),'Islow_beta0'] = beta0_sp0505 * 0.1 * df[(df.ENSCI == 0) & (df.Sol == 0.5) & (df.Buf == 0.5)]['I_OPM_jma']
# df.loc[(df.ENSCI == 0) & (df.Sol == 1.0) & (df.Buf == 1.0),'Islow_beta0'] = beta0_sp1010 * 0.1 * df[(df.ENSCI == 0) & (df.Sol == 1.0) & (df.Buf == 1.0)]['I_OPM_jma']

# df.loc[(df.ENSCI == 1) & (df.Sol == 0.5) & (df.Buf == 0.5),'Islow_beta0'] = beta0_en0505 * 0.1 * df[(df.ENSCI == 1) & (df.Sol == 0.5) & (df.Buf == 0.5)]['I_OPM_jma']
# df.loc[(df.ENSCI == 1) & (df.Sol == 1.0) & (df.Buf == 0.1),'Islow_beta0'] = beta0_en1001 * 0.1 * df[(df.ENSCI == 1) & (df.Sol == 0.1) & (df.Buf == 1.0)]['I_OPM_jma']
# df.loc[(df.ENSCI == 0) & (df.Sol == 1.0) & (df.Buf == 0.1),'Islow_beta0'] = beta0_sp1001 * 0.1 * df[(df.ENSCI == 0) & (df.Sol == 1.0) & (df.Buf == 0.1)]['I_OPM_jma']
# df.loc[(df.ENSCI == 0) & (df.Sol == 1.0) & (df.Buf == 1.0),'Islow_beta0'] = beta0_sp1010 * 0.1 * df[(df.ENSCI == 0) & (df.Sol == 1.0) & (df.Buf == 1.0)]['I_OPM_jma']

print(list(df))

# df['Ifast_beta'] = df['IM'] - df['Islow_beta']
# df['Ifast_beta0'] = df['IM'] - df['Islow_beta0']
# df['Ifast_beta0_minob0'] = df['IM'] - df['Islow_beta0'] - df['iB0']

filtEN = df.ENSCI == 1
filtSP = df.ENSCI == 0

filtS10 = df.Sol == 1
filtS05 = df.Sol == 0.5

filtB10 = df.Buf == 1.0
filtB05 = df.Buf == 0.5
filtB01 = df.Buf == 0.1

filterEN0505 = (filtEN & filtS05 & filtB05)
filterEN1010 = (filtEN & filtS10 & filtB10)
#2017
# filterEN1010 = (filtEN & filtS10 & filtB01)

###
profEN0505 = df.loc[filterEN0505]
profEN1010 = df.loc[filterEN1010]
profEN0505_nodup = profEN0505.drop_duplicates(['Sim', 'Team'])
profEN1010_nodup = profEN1010.drop_duplicates(['Sim', 'Team'])
###
filterSP1010 = (filtSP & filtS10 & filtB10)
filterSP0505 = (filtSP & filtS05 & filtB05)
#2017
# filterSP0505 = (filtSP & filtS10 & filtB01)

profSP1010 = df.loc[filterSP1010]
profSP0505 = df.loc[filterSP0505]
profSP1010_nodup = profSP1010.drop_duplicates(['Sim', 'Team'])
profSP0505_nodup = profSP0505.drop_duplicates(['Sim', 'Team'])


av_islow, av_islow_err, Y = Calc_average_profileCurrent_pressure([profSP1010], 'I_slow_conv')
# av_islow0, av_islow0_err, Y = Calc_average_profileCurrent_pressure([profSP1010], 'Islow_beta0')
av_ifast, av_ifast_err, Y = Calc_average_profileCurrent_pressure([profSP1010], 'I_fast')
av_ifast0, av_ifast0_err, Y = Calc_average_profileCurrent_pressure([profSP1010], 'Ifast_deconv_sm8')
av_ifast0_minib0, av_ifast0_minib0_err, Y = Calc_average_profileCurrent_pressure([profSP1010], 'Ifast_minib0_deconv_sm8')

av_cur, av_cur_err, Y =  Calc_average_profileCurrent_pressure([profSP1010], 'IM')
av_ib0, av_ib0_err, Y = Calc_average_profileCurrent_pressure([profSP1010], 'iB0')
av_ib1, av_ib0_err, Y = Calc_average_profileCurrent_pressure([profSP1010], 'iB1')
av_ib2, av_ib0_err, Y = Calc_average_profileCurrent_pressure([profSP1010], 'iB2')
av_opm, av_opm_err, Y = Calc_average_profileCurrent_pressure([profSP1010], 'I_OPM_jma')

#the relative   contribution of IB0, IB1,IB2, IB_Slow (Beta)  and IB_Slow(Beta0)  with respect to IECC (raw current)

zero = [0] * len(av_islow[0])

# print(zero)
# print(av_islow[0])
# print(av_ifast[0])
# print(av_cur[0])
# print(av_ib0 )


rdif_ib0 = [i/j * 100 for i, j in zip(av_ib0[0], av_cur[0])]
rdif_ib1 = [i/j  * 100for i, j in zip(av_ib1[0], av_cur[0])]
rdif_ib2 = [i/j * 100 for i, j in zip(av_ib2[0], av_cur[0])]

rdif_islow = [i/j * 100 for i, j in zip(av_islow[0], av_cur[0])]
# rdif_islow0 = [i/j * 100 for i, j in zip(av_islow0[0], av_cur[0])]

print(rdif_ib0)
print(rdif_islow)

title = '0910 Data SP 1.0%-1.0B'
# title = '0910 Data SP 0.5%-0.5B'
# title = '2017 Data SP 1.0%-0.1B'

# errorPlot_general([av_islow[0], av_islow0[0], av_ifast[0], av_ifast0[0], av_ifast0_minib0[0],  av_cur[0], av_opm[0], av_ib0[0], av_ib1[0], av_ib2[0] ] ,
#                   [zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero], Y, [0, 10], [1000,5], title, r'Current($\mu$A)', 'Pressure (hPa)',
#                   [r'I slow beta', 'I slow beta0', 'I fast beta', 'I fast beta0', 'I fast beta0 - iB0', 'I ECC', 'I OPM JMA', 'iB0', 'iB1', 'iB2'],
#                   ['black','red', 'black','red', 'magenta', 'gold', 'green', 'green', 'magenta', 'lime'], 'SP1010_2017_ib', folderpath, True, False, False)
#
#
# errorPlot_general([rdif_ib0, rdif_ib1, rdif_ib2, rdif_islow, rdif_islow0 ] , [zero, zero, zero, zero, zero, zero], Y, [0, 40], [1000,5], title, r'RDif', 'Pressure (hPa)',
#                   [r'iB0 / I ECC', 'iB1 / I ECC', 'iB2 / I ECC', 'I slow / I ECC', 'I slow0 / I ECC'],
#                   ['black','red', 'green','blue', 'lime'], 'SP1010_2017_rdif', folderpath, True, False, False)

errorPlot_general([av_islow[0], av_ifast[0], av_ifast0[0], av_ifast0_minib0[0],  av_cur[0], av_opm[0], av_ib0[0], av_ib1[0], av_ib2[0] ] ,
                  [zero, zero, zero, zero, zero, zero, zero, zero, zero, zero], Y, [0, 10], [1000,5], title, r'Current($\mu$A)', 'Pressure (hPa)',
                  [r'I slow',  'I fast ', 'I fast deconv', 'I fast - iB0 deconv', 'I ECC', 'I OPM JMA', 'iB0', 'iB1', 'iB2'],
                  ['black','red', 'blue', 'magenta', 'gold', 'green', 'green', 'magenta', 'lime'], 'SP1010_0910_ib', folderpath, True, False, False)


errorPlot_general([rdif_ib0, rdif_ib1, rdif_ib2, rdif_islow] , [zero, zero, zero, zero, zero], Y, [0, 10], [1000,5], title, r'RDif', 'Pressure (hPa)',
                  [r'iB0 / I ECC', 'iB1 / I ECC', 'iB2 / I ECC', 'I slow conv / I ECC'],
                  ['black','red', 'green','blue', 'lime'], 'SP1010_0910_rdif', folderpath, True, False, False)

