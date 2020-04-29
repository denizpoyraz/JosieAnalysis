## 0910 branch

#!/usr/bin/env python
# coding: utf-8
# Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from Josie_Functions import  Calc_average_profile_pressure, Calc_average_profile_time, Calc_Dif, Calc_average_profileCurrent_pressure, Calc_average_profileCurrent_time
from Josie_PlotFunctions import  errorPlot_ARDif_withtext, errorPlot_general

path = 'Dif_0910_All'

df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_deconv.csv", low_memory=False)
# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv.csv", low_memory=False)

df = df.drop(df[(df.PO3 < 0)].index)
df = df.drop(df[(df.PO3_OPM < 0)].index)

# df = df[df.ADX == 0]

test = df.drop_duplicates(['Sim', 'Team'])
print(len(test))

df = df[df.ADX == 0]

test = df.drop_duplicates(['Sim', 'Team'])
print(len(test))



## cuts for Josie0910 data
# # v2 cuts, use this and v3 standard more conservative cuts not valid for 140, 162, 163, 166  v2
df=df[df.Tsim > 900]
df=df[df.Tsim <= 8100]
df = df.drop(df[(2000 < df.Tsim) & (df.Tsim < 2500) & (df.Sim != 140) & (df.Sim != 162) & (df.Sim != 163) & (
                df.Sim != 166)].index)
df = df.drop(df[(df.Tsim > 4000) & (df.Tsim < 4500) & (df.Sim != 140) & (df.Sim != 162) & (df.Sim != 163) & (
                df.Sim != 166)].index)
df = df.drop(df[(df.Tsim > 6000) & (df.Tsim < 6500) & (df.Sim != 140) & (df.Sim != 162) & (df.Sim != 163) & (
                df.Sim != 166)].index)

df = df.drop(df[(df.Sim == 141) & (df.Team == 3)].index)
df = df.drop(df[(df.Sim == 143) & (df.Team == 2) & (df.Tsim > 7950) & (df.Tsim < 8100)].index)
df = df.drop(df[(df.Sim == 147) & (df.Team == 3)].index)
df = df.drop(df[(df.Sim == 158) & (df.Team == 2)].index)
df = df.drop(df[(df.Sim == 167) & (df.Team == 4)].index)
## new cuts v4 08/04
# df = df.drop(df[(df.Sim == 160) & (df.Team == 4)].index)
# df = df.drop(df[(df.Sim == 166) & (df.Team == 1)].index)

# # ## v3 cuts 
### I think these cuts are not needed## checkcheck
df = df.drop(df[(df.Sim == 159) & (df.Team == 1)].index) ##??
df = df.drop(df[(df.Sim == 158) & (df.Team == 1)].index)
df = df.drop(df[(df.Sim == 163) & (df.Team == 4)].index)
df = df.drop(df[(df.Sim == 159) & (df.Team == 4)].index)
####

df = df.drop(df[(df.Sim == 158) & (df.Tsim > 7300) & (df.Tsim < 7700)].index)
df = df.drop(df[(df.Sim == 159) & (df.Tsim > 7800) & (df.Tsim < 8000)].index)
df = df.drop(df[(df.Sim == 161) & (df.Tsim > 6800) & (df.Tsim < 7200)].index)

    # # additional cuts for specific simulations  v3
df = df.drop(df[(df.Sim == 140) & (df.Tsim < 1000)].index)
df = df.drop(df[(df.Sim == 140) & (df.Tsim > 2450) & (df.Tsim < 2800)].index)
df = df.drop(df[(df.Sim == 140) & (df.Tsim > 4400) & (df.Tsim < 4800)].index)
df = df.drop(df[(df.Sim == 140) & (df.Tsim > 6400) & (df.Tsim < 6800)].index)

df = df.drop(df[(df.Sim == 162) & (df.Tsim > 2100) & (df.Tsim < 2550)].index)
df = df.drop(df[(df.Sim == 162) & (df.Tsim > 4100) & (df.Tsim < 4600)].index)
df = df.drop(df[(df.Sim == 162) & (df.Tsim > 5450) & (df.Tsim < 5800)].index)
df = df.drop(df[(df.Sim == 162) & (df.Tsim > 6100) & (df.Tsim < 6550)].index)

df = df.drop(df[(df.Sim == 163) & (df.Tsim > 2100) & (df.Tsim < 2550)].index)
df = df.drop(df[(df.Sim == 163) & (df.Tsim > 4100) & (df.Tsim < 4600)].index)
df = df.drop(df[(df.Sim == 163) & (df.Tsim > 5450) & (df.Tsim < 5800)].index)
df = df.drop(df[(df.Sim == 163) & (df.Tsim > 6100) & (df.Tsim < 6550)].index)

df = df.drop(df[(df.Sim == 166) & (df.Tsim > 2200) & (df.Tsim < 2650)].index)
df = df.drop(df[(df.Sim == 166) & (df.Tsim > 4200) & (df.Tsim < 4700)].index)
df = df.drop(df[(df.Sim == 166) & (df.Tsim > 6200) & (df.Tsim < 6650)].index)
df = df.drop(df[(df.Sim == 166) & (df.Tsim > 7550) & (df.Tsim < 7750)].index)
df = df.drop(df[(df.Sim == 166) & (df.Team == 1) & (df.Tsim > 4400) & (df.Tsim < 5400)].index)

# df['CurMinBkg'] = df['IM'] - df['Header_IB1']
# df['I_fast_deconvMinBkg'] = df['I_fast_deconv'] - df['Header_IB1']

ytitle = 'Pressure (hPa)'
ytitlet = 'Time (sec.)'


###############################################
# Filters for Sonde, Solution, Buff er selection
# 1, 0.1 ENSCI vs SPC
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

print(profEN0505_nodup[['Sim','Team']])

totO3_EN0505 = profEN0505_nodup.frac.mean()
totO3_EN1010 = profEN1010_nodup.frac.mean()


filterSP1010 = (filtSP & filtS10 & filtB10)
filterSP0505 = (filtSP & filtS05 & filtB05)

profSP1010 = df.loc[filterSP1010]
profSP0505 = df.loc[filterSP0505]

profSP1010_nodup = profSP1010.drop_duplicates(['Sim', 'Team'])
profSP0505_nodup = profSP0505.drop_duplicates(['Sim', 'Team'])

totO3_SP1010 = profSP1010_nodup.frac.mean()
totO3_SP0505 = profSP0505_nodup.frac.mean()

##################################################################################
################     Pressure PO3 PLOTS        #################################
##################################################################################

####  for all sondes in one category
dft = {}

print('Sim Team', profEN1010_nodup[['Sim','Team']])

simlist = np.asarray(profEN1010.drop_duplicates(['Sim', 'Team'])['Sim'])
teamlist = np.asarray(profEN1010.drop_duplicates(['Sim', 'Team'])['Team'])


#
# errorPlot_ARDif_withtext(adifall, adiferrall, Y, [-3, 3], [1000,5],  '0910 Data',  'test', ytitle, '', '', '',
#                            'ADif_Pair_0910_testall', folderpath ,  True, False)
#
# errorPlot_ARDif_withtext(rdifall, rdiferrall, Y, [-40, 40], [1000,5],  '0910 Data',  '', '', '', '', '',
#                            'RDif_Pair_0910', folderpath, True, False)


## order of the lists [en0505, en1010, sp0505, sp1010]
avgprof_O3S_X, avgprof_O3S_Xerr, Y = Calc_average_profile_pressure([profEN0505, profEN1010, profSP0505, profSP1010],
                                                                   'PO3')
avgprof_O3S_X_dc, avgprof_O3S_Xerr_dc, Y = Calc_average_profile_pressure([profEN0505, profEN1010, profSP0505, profSP1010],
                                                                         'PO3_deconv')
avgprof_O3S_X_dc_sm6, avgprof_O3S_Xerr_dc_sm6, Y = Calc_average_profile_pressure([profEN0505, profEN1010, profSP0505, profSP1010],
                                                                         'PO3_deconv_sm6')
avgprof_O3S_X_dc_sm12, avgprof_O3S_Xerr_dc_sm12, Y = Calc_average_profile_pressure([profEN0505, profEN1010, profSP0505, profSP1010],
                                                                         'PO3_deconv_sm12')
avgprof_O3S_X_dcjma, avgprof_O3S_Xerr_dcjma, Y = Calc_average_profile_pressure([profEN0505, profEN1010, profSP0505, profSP1010],
                                                                               'PO3_deconv_jma')
avgprof_O3S_X_dcjma_sm6, avgprof_O3S_Xerr_dcjma_sm6, Y = Calc_average_profile_pressure([profEN0505, profEN1010, profSP0505, profSP1010],
                                                                               'PO3_deconv_jma_sm6')
avgprof_O3S_X_dcjma_sm12, avgprof_O3S_Xerr_dcjma_sm12, Y = Calc_average_profile_pressure([profEN0505, profEN1010, profSP0505, profSP1010],
                                                                               'PO3_deconv_jma_sm12')

avgprof_O3S_X_dcjma_smb6, avgprof_O3S_Xerr_dcjma_smb6, Y = Calc_average_profile_pressure([profEN0505, profEN1010, profSP0505, profSP1010],
                                                                               'PO3_deconv_smb6_jma')

avgprof_O3S_X_dcjma_smb12, avgprof_O3S_Xerr_dcjma_smb12, Y = Calc_average_profile_pressure([profEN0505, profEN1010, profSP0505, profSP1010],
                                                                               'PO3_deconv_smb12_jma')



avgprof_OPM_X, avgprof_OPM_Xerr, Y = Calc_average_profile_pressure([profEN0505, profEN1010, profSP0505, profSP1010],
                                                                   'PO3_OPM')

dimension = len(Y)
# standard
adif, adiferr, rdif, rdiferr = Calc_Dif(avgprof_O3S_X, avgprof_OPM_X, avgprof_O3S_Xerr, dimension)
# deconvoluted
adif_dc, adiferr_dc, rdif_dc, rdiferr_dc = Calc_Dif(avgprof_O3S_X_dc, avgprof_OPM_X, avgprof_O3S_Xerr_dc, dimension)
#deconvoluted smoothed
adif_dc_sm6, adiferr_dc_sm6, rdif_dc_sm6, rdiferr_dc_sm6 = Calc_Dif(avgprof_O3S_X_dc_sm6, avgprof_OPM_X, avgprof_O3S_Xerr_dc_sm6, dimension)
adif_dc_sm12, adiferr_dc_sm12, rdif_dc_sm12, rdiferr_dc_sm12 = Calc_Dif(avgprof_O3S_X_dc_sm12, avgprof_OPM_X, avgprof_O3S_Xerr_dc_sm12, dimension)
#deconvoluted jma corrected
adif_dcjma, adiferr_dcjma, rdif_dcjma, rdiferr_dcjma = Calc_Dif(avgprof_O3S_X_dcjma, avgprof_OPM_X, avgprof_O3S_Xerr_dcjma, dimension)
#deconvoluted jma corrected smoothed
adif_dcjma_sm6, adiferr_dcjma_sm6, rdif_dcjma_sm6, rdiferr_dcjma_sm6 = Calc_Dif(avgprof_O3S_X_dcjma_sm6, avgprof_OPM_X,
                                                                                avgprof_O3S_Xerr_dcjma_sm6, dimension)
adif_dcjma_sm12, adiferr_dcjma_sm12, rdif_dcjma_sm12, rdiferr_dcjma_sm12 = Calc_Dif(avgprof_O3S_X_dcjma_sm12, avgprof_OPM_X,
                                                                                avgprof_O3S_Xerr_dcjma_sm12, dimension)

#smoothed and then deconvoluted jma corrected
adif_dcjma_smb6, adiferr_dcjma_smb6, rdif_dcjma_smb6, rdiferr_dcjma_smb6 = Calc_Dif(avgprof_O3S_X_dcjma_smb6, avgprof_OPM_X,
                                                                                avgprof_O3S_Xerr_dcjma_smb6, dimension)
adif_dcjma_smb12, adiferr_dcjma_smb12, rdif_dcjma_smb12, rdiferr_dcjma_smb12 = Calc_Dif(avgprof_O3S_X_dcjma_smb12, avgprof_OPM_X,
                                                                                avgprof_O3S_Xerr_dcjma_smb12, dimension)


## current

avgprof_O3S_cur, avgprof_O3S_curerr, Ycur = Calc_average_profileCurrent_pressure([profEN0505, profEN1010, profSP0505, profSP1010],
                                                                   'IM')
avgprof_O3S_curSlow, avgprof_O3S_curSlowerr, Yslow = Calc_average_profileCurrent_pressure([profEN0505, profEN1010, profSP0505, profSP1010],
                                                                   'I_slow_conv')
avgprof_O3S_cur_dc, avgprof_O3S_curerr_dc, Y = Calc_average_profileCurrent_pressure([profEN0505, profEN1010, profSP0505, profSP1010],
                                                                         'I_fast_deconv')
avgprof_OPM_cur, avgprof_OPM_curerr, Y = Calc_average_profileCurrent_pressure([profEN0505, profEN1010, profSP0505, profSP1010],
                                                                   'I_OPM_jma')

dimension = len(Y)

adifcur, adifcurerr, rdifcur, rdifcurerr = Calc_Dif(avgprof_O3S_cur, avgprof_OPM_cur, avgprof_O3S_curerr, dimension)
adifcur_dc, adifcurerr_dc, rdifcur_dc, rdifcurerr_dc = Calc_Dif(avgprof_O3S_cur_dc, avgprof_OPM_cur, avgprof_O3S_curerr_dc, dimension)

dft = {}

size = len(simlist)

allavgprof_O3S_X = [0] * size;
allavgprof_O3S_Xerr = [0] * size
allavgprof_OPM_X = [0] * size;
allavgprof_OPM_Xerr = [0] * size
adifall = [0] * size;
adiferrall = [0] * size
rdifall = [0] * size;
rdiferrall = [0] * size

allavgprof_O3S_Cur = [0] * size;
allavgprof_O3S_Curerr = [0] * size
allavgprof_OPM_Cur = [0] * size;
allavgprof_OPM_Curerr = [0] * size
adifall_cur = [0] * size;
adiferrall_cur = [0] * size
rdifall_cur = [0] * size;
rdiferrall_cur = [0] * size

allavgprof_O3S_Cur_dc = [0] * size;
allavgprof_O3S_Curerr_dc = [0] * size

adifall_cur_dc = [0] * size;
adiferrall_cur_dc = [0] * size
rdifall_cur_dc = [0] * size;
rdiferrall_cur_dc = [0] * size

allavgprof_O3S_X_dcjma = [0] * size;
allavgprof_O3S_Xerr_dcjma = [0] * size
adifall_dcjma = [0] * size;
adiferrall_dcjma = [0] * size
rdifall_dcjma = [0] * size;
rdiferrall_dcjma = [0] * size

allavgprof_O3S_X_dcjma_sm6 = [0] * size;
allavgprof_O3S_Xerr_dcjma_sm6 = [0] * size
adifall_dcjma_sm6 = [0] * size;
adiferrall_dcjma_sm6 = [0] * size
rdifall_dcjma_sm6 = [0] * size;
rdiferrall_dcjma_sm6 = [0] * size

allavgprof_O3S_X_dcjma_sm12 = [0] * size;
allavgprof_O3S_Xerr_dcjma_sm12 = [0] * size
adifall_dcjma_sm12 = [0] * size;
adiferrall_dcjma_sm12 = [0] * size
rdifall_dcjma_sm12 = [0] * size;
rdiferrall_dcjma_sm12 = [0] * size

fig, ax1 = plt.subplots()
plt.xlim([-40, 40])
plt.ylim([1000, 5])
plt.title('EN 1.0%-1.0B')
plt.xlabel('Sonde - OPM (%)')
plt.ylabel('Pressure')
plt.grid(True)
ax1.set_yscale('log')


for j in range(len(simlist)):
    dft[j] = df[(df.Sim == simlist[j]) & (df.Team == teamlist[j])]
    dft[j] = dft[j].reset_index()

    labelsim = str(simlist[j]) + '-' + str(teamlist[j])

    allavgprof_O3S_X[j], allavgprof_O3S_Xerr[j], Y = Calc_average_profile_pressure([dft[j]], 'PO3')
    allavgprof_O3S_X_dcjma[j], allavgprof_O3S_Xerr_dcjma[j], Y = Calc_average_profile_pressure([dft[j]], 'PO3_deconv_jma')
    allavgprof_O3S_X_dcjma_sm6[j], allavgprof_O3S_Xerr_dcjma_sm6[j], Y = Calc_average_profile_pressure([dft[j]], 'PO3_deconv_jma_sm6')
    allavgprof_O3S_X_dcjma_sm12[j], allavgprof_O3S_Xerr_dcjma_sm12[j], Y = Calc_average_profile_pressure([dft[j]], 'PO3_deconv_jma_sm12')
    allavgprof_OPM_X[j], allavgprof_OPM_Xerr[j], Y = Calc_average_profile_pressure([dft[j]], 'PO3_OPM')

    allavgprof_O3S_Cur[j], allavgprof_O3S_Curerr[j], Y = Calc_average_profileCurrent_pressure([dft[j]], 'IM')
    allavgprof_O3S_Cur_dc[j], allavgprof_O3S_Curerr_dc[j], Y = Calc_average_profileCurrent_pressure([dft[j]], 'I_fast_deconv')

    allavgprof_OPM_Cur[j], allavgprof_OPM_Curerr[j], Y = Calc_average_profileCurrent_pressure([dft[j]], 'I_OPM_jma')

    dimension = len(Y)


    adifall_cur[j], adiferrall_cur[j], rdifall_cur[j], rdiferrall_cur[j] = Calc_Dif(allavgprof_O3S_Cur[j], allavgprof_OPM_Cur[j],
                                                                    allavgprof_O3S_Curerr[j], dimension)

    adifall_cur_dc[j], adiferrall_cur_dc[j], rdifall_cur_dc[j], rdiferrall_cur_dc[j] =\
        Calc_Dif(allavgprof_O3S_Cur_dc[j], allavgprof_OPM_Cur[j], allavgprof_O3S_Curerr_dc[j], dimension)

    adifall[j], adiferrall[j], rdifall[j], rdiferrall[j] = Calc_Dif(allavgprof_O3S_X[j], allavgprof_OPM_X[j],
                                                                    allavgprof_O3S_Xerr[j], dimension)
    adifall_dcjma[j], adiferrall_dcjma[j], rdifall_dcjma[j], rdiferrall_dcjma[j] = Calc_Dif(allavgprof_O3S_X_dcjma[j], allavgprof_OPM_X[j],
                                                                    allavgprof_O3S_Xerr_dcjma[j], dimension)
    adifall_dcjma_sm6[j], adiferrall_dcjma_sm6[j], rdifall_dcjma_sm6[j], rdiferrall_dcjma_sm6[j] \
        = Calc_Dif(allavgprof_O3S_X_dcjma_sm6[j], allavgprof_OPM_X[j], allavgprof_O3S_Xerr_dcjma_sm6[j], dimension)

    adifall_dcjma_sm12[j], adiferrall_dcjma_sm12[j], rdifall_dcjma_sm12[j], rdiferrall_dcjma_sm12[j] \
        = Calc_Dif(allavgprof_O3S_X_dcjma_sm12[j], allavgprof_OPM_X[j], allavgprof_O3S_Xerr_dcjma_sm12[j], dimension)

    ax1.errorbar(rdifall[j][0], Y, xerr=rdiferrall[j][0], linewidth=1, elinewidth=0.5, capsize=1, capthick=0.5,
                 label=labelsim)



ax1.errorbar(rdif[1], Y, xerr=rdiferr[1], linewidth=3, elinewidth=2, capsize=3, capthick=2, label='EN 1.0%-1.0B', color = 'black')
ax1.legend(loc='lower left', frameon=True, fontsize='x-small')

plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/' + path + '/' + 'RDifAll' + '.png')
plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/' + path + '/' + 'RDifAll' + '.eps')


fig, ax2 = plt.subplots()
plt.xlim([-3, 3])
plt.ylim([1000, 5])
plt.title('EN 1.0%-1.0B')
plt.xlabel('Sonde - OPM')
plt.ylabel('Pressure')
plt.grid(True)
ax2.set_yscale('log')

for j in range(size):

    ax2.errorbar(adifall[j][0], Y, xerr=adiferrall[j][0], linewidth=1, elinewidth=0.5, capsize=1, capthick=0.5,
                 label=labelsim)

ax2.errorbar(adif[1], Y, xerr=adiferr[1], linewidth=3, elinewidth=2, capsize=3, capthick=2, label='EN 1.0%-1.0B', color = 'black')
ax2.legend(loc='lower left', frameon=True, fontsize='x-small')

plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/' + path + '/' + 'ADifAll' + '.png')
plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/' + path + '/' + 'ADifAll' + '.eps')

## deconvoluted

fig, ax3 = plt.subplots()
plt.xlim([-40, 40])
plt.ylim([1000, 5])
plt.title('EN 1.0%-1.0B Deconv.')
plt.xlabel('Sonde[PO3 JMA] - OPM')
plt.ylabel('Pressure')
plt.grid(True)
ax3.set_yscale('log')

for j in range(size):
    ax3.errorbar(rdifall_dcjma[j][0], Y, xerr=rdiferrall_dcjma[j][0], linewidth=1, elinewidth=0.5, capsize=1, capthick=0.5,
                 label=labelsim)

ax3.errorbar(rdif_dcjma[1], Y, xerr=rdiferr_dcjma[1], linewidth=3, elinewidth=2, capsize=3, capthick=2, label='EN 1.0%-1.0B',
             color='black')
ax3.legend(loc='lower left', frameon=True, fontsize='x-small')

plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/' + path + '/' + 'RDifAll_dcjma' + '.png')
plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/' + path + '/' + 'RDifAll_dcjma' + '.eps')

## deconvoluted sm6

fig, ax4 = plt.subplots()
plt.xlim([-40, 40])
plt.ylim([1000, 5])
plt.title('EN 1.0%-1.0B Deconv Smoothed 6 secs.')
plt.xlabel('Sonde[PO3 JMA] - OPM')
plt.ylabel('Pressure')
plt.grid(True)
ax4.set_yscale('log')

for j in range(size):
    ax4.errorbar(rdifall_dcjma_sm6[j][0], Y, xerr=rdiferrall_dcjma_sm6[j][0], linewidth=1, elinewidth=0.5, capsize=1, capthick=0.5,
                 label=labelsim)

ax4.errorbar(rdif_dcjma_sm6[1], Y, xerr=rdiferr_dcjma_sm6[1], linewidth=3, elinewidth=2, capsize=3, capthick=2, label='EN 1.0%-1.0B',
             color='black')
ax4.legend(loc='lower left', frameon=True, fontsize='x-small')

plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/' + path + '/' + 'RDifAll_dcjma_sm6' + '.png')
plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/' + path + '/' + 'RDifAll_dcjma_sm6' + '.eps')


## deconvoluted sm12

fig, ax5 = plt.subplots()
plt.xlim([-40, 40])
plt.ylim([1000, 5])
plt.title('EN 1.0%-1.0B Deconv Smoothed 12 secs.')
plt.xlabel('Sonde[PO3 JMA] - OPM')
plt.ylabel('Pressure')
plt.grid(True)
ax5.set_yscale('log')

for j in range(size):
    ax5.errorbar(rdifall_dcjma_sm12[j][0], Y, xerr=rdiferrall_dcjma_sm12[j][0], linewidth=1, elinewidth=0.5, capsize=1, capthick=0.5,
                 label=labelsim)

ax5.errorbar(rdif_dcjma_sm12[1], Y, xerr=rdiferr_dcjma_sm12[1], linewidth=3, elinewidth=2, capsize=3, capthick=2, label='EN 1.0%-1.0B',
             color='black')
ax5.legend(loc='lower left', frameon=True, fontsize='x-small')

plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/' + path + '/' + 'RDifAll_dcjma_sm12' + '.png')
plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/' + path + '/' + 'RDifAll_dcjma_sm12' + '.eps')

## deconvoluted sm6

fig, ax6 = plt.subplots()
plt.xlim([-40, 40])
plt.ylim([1000, 5])
plt.title('EN 1.0%-1.0B Current')
plt.xlabel('Sonde[I ECC] - OPM[I JMA]')
plt.ylabel('Pressure')
plt.grid(True)
ax6.set_yscale('log')

for j in range(size):
    ax6.errorbar(rdifall_cur[j][0], Y, xerr=rdiferrall_cur[j][0], linewidth=1, elinewidth=0.5, capsize=1, capthick=0.5,
                 label=labelsim)

ax6.errorbar(rdifcur[1], Y, xerr=rdifcurerr[1], linewidth=3, elinewidth=2, capsize=3, capthick=2, label='EN 1.0%-1.0B',
             color='black')
ax6.legend(loc='lower left', frameon=True, fontsize='x-small')

plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/' + path + '/' + 'Current_RDifAll' + '.png')
plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/' + path + '/' + 'Current_RDifAll' + '.eps')


fig, ax7 = plt.subplots()
plt.xlim([-40, 40])
plt.ylim([1000, 5])
plt.title('EN 1.0%-1.0B Current Deconvoluted')
plt.xlabel('Sonde[I ECC] - OPM[I JMA]')
plt.ylabel('Pressure')
plt.grid(True)
ax7.set_yscale('log')

for j in range(size):
    ax7.errorbar(rdifall_cur_dc[j][0], Y, xerr=rdiferrall_cur_dc[j][0], linewidth=1, elinewidth=0.5, capsize=1, capthick=0.5,
                 label=labelsim)

ax7.errorbar(rdifcur_dc[1], Y, xerr=rdifcurerr_dc[1], linewidth=3, elinewidth=2, capsize=3, capthick=2, label='EN 1.0%-1.0B',
             color='black')
ax7.legend(loc='lower left', frameon=True, fontsize='x-small')

plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/' + path + '/' + 'Current_RDifAll_dc' + '.png')
plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/' + path + '/' + 'Current_RDifAll_dc' + '.eps')

# plt.show()
#
# for j in range(len(simlist)):
#
#
#
#
#     ax2.errorbar(adifall[j][0], Y, xerr=adiferrall[j][0], linewidth=1, elinewidth=0.5, capsize=1, capthick=0.5,
#                  label=labelsim)
#
# ax2.errorbar(adif[1], Y, xerr=adiferr[1], linewidth=3, elinewidth=2, capsize=3, capthick=2, label='EN 1.0%-1.0B', color = 'black')
#
# ax2.legend(loc='lower right', frameon=True, fontsize='x-small')
#
# plt.show()
#
