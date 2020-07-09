import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from numpy.polynomial import polynomial as P
import matplotlib.gridspec as gridspec

from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt

import pickle
from Josie_Functions import Calc_average_profileCurrent_pressure, Calc_average_profile_time, Calc_average_profile_Pair, Calc_average_profile_pressure

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

def polyfit(dfp):

    dfp = cuts2017(dfp)

    dfp['TPintC'] = dfp['TPext'] - 273
    dfp['TPextC'] = dfp['TPint'] - 273
    dfp['TPintK'] = dfp['TPext']
    dfp['TPextK'] = dfp['TPint']

    dfp = dfp[dfp.Sim > 185]

    dfen = dfp[dfp.ENSCI == 1]
    dfsp = dfp[dfp.ENSCI == 0]

    avgprof_tpint_en, avgprof_tpint_en_err, Y = Calc_average_profile_pressure([dfen], 'TPintC')
    avgprof_tpext_en, avgprof_tpext_en_err, Y = Calc_average_profile_pressure([dfen], 'TPextC')

    avgprof_tpint_sp, avgprof_tpint_sp_err, Y = Calc_average_profile_pressure([dfsp], 'TPintC')
    avgprof_tpext_sp, avgprof_tpext_sp_err, Y = Calc_average_profile_pressure([dfsp], 'TPextC')

    adifall_en = [i - j for i, j in zip(avgprof_tpint_en[0], avgprof_tpext_en[0])]
    adifall_en_err = [np.sqrt(i * i + j * j) for i, j in zip(avgprof_tpint_en_err[0], avgprof_tpext_en_err[0])]

    adifall_sp = [i - j for i, j in zip(avgprof_tpint_sp[0], avgprof_tpext_sp[0])]
    adifall_sp_err = [np.sqrt(i * i + j * j) for i, j in zip(avgprof_tpint_sp_err[0], avgprof_tpext_sp_err[0])]

    p_en = np.poly1d(np.polyfit(Y, adifall_en, 15))
    p_sp = np.poly1d(np.polyfit(Y, adifall_sp, 15))

    # print('Y', Y)
    # print('p_en', p_en)

    return p_en, p_sp




df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv.csv", low_memory=False)

df = cuts2017(df)

dfgen = df[df.Sim < 186]


df['TPintC'] = df['TPext'] - 273
df['TPextC'] = df['TPint'] - 273
df['TPintK'] = df['TPext']
df['TPextK'] = df['TPint']

dfgen['TPintC'] = dfgen['TPext'] - 273
dfgen['TPextC'] = dfgen['TPint'] - 273
dfgen['TPintK'] = dfgen['TPext']
dfgen['TPextK'] = dfgen['TPint']


dfone = df[(df.Sim == 173) & (df.Team ==1) & (df.Pair > 0)]
dfone['TPintC'] = dfone['TPext'] - 273
dfone['TPextC'] = dfone['TPint'] - 273


df = df[df.Sim > 185]

dfen = df[df.ENSCI == 1]
dfsp = df[df.ENSCI == 0]


print(list(dfgen))

simlist = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Sim'])
teamlist = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Team'])
# adx = np.asarray(df.drop_duplicates(['Sim', 'Team'])['ADX'])
sol = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Sol'].tolist())
buff = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Buf'])
ensci = np.asarray(df.drop_duplicates(['Sim', 'Team'])['ENSCI'])

dft = {}
# TPint, TPext

# for j in range(len(simlist)):
#
#
#     if ensci[j] == 0:
#         sondestr = 'SPC'
#     else:
#         sondestr = 'ENSCI'
#     # if adx[j] == 1:
#     #     adxstr = 'ADX'
#     # else:
#     #     adxstr = ''
#     if sol[j] == 2.0: solstr = '2p0'
#     if sol[j] == 1.0: solstr = '1p0'
#     if sol[j] == 0.5: solstr = '0p5'
#
#     if buff[j] == 0.1: bufstr = '0p1'
#     if buff[j] == 0.5: bufstr = '0p5'
#     if buff[j] == 1.0: bufstr = '1p0'
#
#     title = str(simlist[j]) + '_' + str(teamlist[j])
#             # + '_' + adxstr + sondestr + solstr + '-' + bufstr + 'B'
#     type = sondestr + ' ' + str(sol[j]) + '\% - ' + str(buff[j]) + 'B'
#     sp = str(simlist[j]) + '-' + str(teamlist[j])
#     ptitle = sp + ' ' + sondestr + ' ' + str(sol[j]) + '% - ' + str(buff[j]) + 'B'
#     print(title)
#
#     dft[j] = df[(df.Sim == simlist[j]) & (df.Team == teamlist[j])]
#     dft[j] = dft[j].reset_index()
#
#     # gs = gridspec.GridSpec(1, 2)
#
#
#     # ax2 = plt.subplot(gs[:, :1])
#     fig, ax2 = plt.subplots()
#
#     ax2.set_ylabel(r'TSim')
#     ax2.set_xlabel('Temp C')
#     plt.plot(dft[j].TPint-273, dft[j].Tsim,label='TPint')
#     plt.plot(dft[j].TPext-273, dft[j].Tsim, label='TPext')
#     plt.plot(dft[j].TPext- dft[j].TPint, dft[j].Tsim, label='TPext - TPint',  linestyle="--")
#
#
#     # ax2.set_ylabel(r'Pressure (mPa)')
#     # ax2.set_xticklabels([])
#     # ax2.set_xlabel('Tsim (secs)')
#     # plt.plot(dft[j].Tsim, 0.1 * dft[j].I_conv_slow, label='0.1 * I slow conv. ', color='#d62728')
#     plt.title(ptitle)
#     plt.legend(loc='upper right', fontsize='small')
#
#     plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/Sim_' + title + '.eps')
#     plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/Sim_' + title + '.png')
#
#     plt.show()
#     plt.close('all)')

###############################################



## for all simulations greater than 185

avgprof_tpint_en, avgprof_tpint_en_err, Y = Calc_average_profile_pressure([dfen], 'TPintC')
avgprof_tpext_en, avgprof_tpext_en_err, Y = Calc_average_profile_pressure([dfen], 'TPextC')

avgprof_tpint_sp, avgprof_tpint_sp_err, Y = Calc_average_profile_pressure([dfsp], 'TPintC')
avgprof_tpext_sp, avgprof_tpext_sp_err, Y = Calc_average_profile_pressure([dfsp], 'TPextC')

avgprofgen_tpint_pre, avgprofgen_tpint_pre_err, Y = Calc_average_profile_pressure([dfgen], 'TPintC')
avgprofgen_tpext_pre, avgprofgen_tpext_pre_err, Y = Calc_average_profile_pressure([dfgen], 'TPextC')

# print('avgprofgen_tpint_pre', avgprofgen_tpint_pre)
# print('avgprofgen_tpext_pre', avgprofgen_tpext_pre)
#
adifall_en = [i - j for i,j in zip(avgprof_tpint_en[0], avgprof_tpext_en[0])]
adifall_en_err = [np.sqrt(i*i + j*j) for i,j in zip(avgprof_tpint_en_err[0], avgprof_tpext_en_err[0])]

adifall_sp = [i - j for i,j in zip(avgprof_tpint_sp[0], avgprof_tpext_sp[0])]
adifall_sp_err = [np.sqrt(i*i + j*j) for i,j in zip(avgprof_tpint_sp_err[0], avgprof_tpext_sp_err[0])]

# rdifall = [(i - j)/i * 100  for i, j in zip(avgprof_tpint_pre[0], avgprof_tpext_pre[0])]
# rdifall_err = [np.sqrt((ie * ie)/(i*i) + (je * je)/(j*j)) for ie, je, i, j
#                  in zip(avgprof_tpint_pre_err[0], avgprof_tpext_pre_err[0], avgprof_tpint_pre_err[0], avgprof_tpext_pre_err[0])]

##fit

p_enf, p_spf = polyfit(df)

print('p_enf[0]', p_enf[0], p_enf[14])

print('Y', Y)
print('p(Y)', p_enf(Y) )
# c_en, stats_en = np.polyfit(Y, adifall_en, 15)
# c_sp, stats_sp = np.polyfit(Y, adifall_sp, 15)
# print('c_en', c_en)
# print('c_sp', c_sp)
# p2 = np.poly1d(np.polyfit(Y, adifall, 12))
# p3 = np.poly1d(np.polyfit(Y, adifall, 13))
# p4 = np.poly1d(np.polyfit(Y, adifall, 14))
# p5 = np.poly1d(np.polyfit(Y, adifall, 15))


fig, ax = plt.subplots()
# plt.xlim(xra)
# plt.xlim(1000,5)
# plt.ylabel('Temp C')
# plt.xlabel('P Air')
# ax.set_xscale('log')

plt.ylim(1000,5)
# plt.xlim(10,30)

plt.xlabel('Temp C')
plt.ylabel('P Air')
ax.set_yscale('log')

# ax.errorbar(avgprof_tpint_pre[0], Y, xerr=avgprof_tpint_pre_err[0], label='TPint', color='red', linewidth=1, elinewidth=0.5,
#             capsize=1, capthick=0.5)
# ax.errorbar(avgprof_tpext_pre[0], Y, xerr=avgprof_tpext_pre_err[0], label='TPext', color='blue', linewidth=1, elinewidth=0.5,
#             capsize=1, capthick=0.5, linestyle = '--')
# ax.errorbar( Y, adifall,  yerr=adifall_err, label=' TPint - TPext ', color='black', linewidth=1, elinewidth=0.5,
#             capsize=1, capthick=0.5, linestyle = ':')

plt.plot( adifall_en, Y,  label = 'adif ensci')
plt.plot( p_enf(Y), Y, label = 'fit ensci')
plt.plot(avgprof_tpext_en[0], Y, label = 'TP Cell ensci')
plt.plot(avgprof_tpint_en[0] - p_enf(Y), Y, label = 'TP Cell generated ensci ')

plt.plot( adifall_sp, Y,  label = 'adif sp')
plt.plot( p_spf(Y), Y, label = 'fit sp')
plt.plot(avgprof_tpext_sp[0], Y, label = 'TP Cell sp')
plt.plot(avgprof_tpint_sp[0] - p_spf(Y), Y, label = 'TP Cell generated sp ')

# plt.plot(adifall, Y,  label = 'adif')
# plt.plot( p(Y), Y,  label = 'fit')
# plt.plot(avgprofgen_tpint_pre[0], Y,  label = 'TP int')
#
# plt.plot(avgprofgen_tpint_pre[0] - p(Y), Y,  label = 'TP Cell generated')



# plt.plot(df.Pair, df.TPintC, label ='TPint')
# plt.plot(df.Pair, df.TPextC, label ='TPext')
# plt.plot(df.Pair, df.TPext - p(df.Pair), label = 'fit')



ax.legend(loc='upper right ', frameon=False, fontsize='small')

# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/' + titlelist[l] + '.png')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/' + titlelist[l] + '.eps')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/' + titlelist[l] + '.pdf')
plt.show()


# ### per sonde and solution type
#
# filtEN = df.ENSCI == 1
# filtSP = df.ENSCI == 0
#
# filtS10 = df.Sol == 1
# filtS05 = df.Sol == 0.5
#
# filtB10 = df.Buf == 1.0
# filtB05 = df.Buf == 0.5
# filtB01 = df.Buf == 0.1
#
# filterEN0505 = (filtEN & filtS05 & filtB05)
# # & (df.Sim == 184) & (df.Team == 8))
# filterEN1010 = (filtEN & filtS10 & filtB10)
# filterEN1001 = (filtEN & filtS10 & filtB01)
#
# profEN0505 = df.loc[filterEN0505]
# profEN1010 = df.loc[filterEN1010]
# profEN1001 = df.loc[filterEN1001]
#
# profEN0505_nodup = profEN0505.drop_duplicates(['Sim', 'Team'])
# profEN1010_nodup = profEN1010.drop_duplicates(['Sim', 'Team'])
# profEN1001_nodup = profEN1001.drop_duplicates(['Sim', 'Team'])
#
# print(profEN0505_nodup[['Sim','Team']])
#
# totO3_EN0505 = profEN0505_nodup.frac.mean()
# totO3_EN1010 = profEN1010_nodup.frac.mean()
# totO3_EN1001 = profEN1001_nodup.frac.mean()
#
# filterSP1010 = (filtSP & filtS10 & filtB10)
# filterSP0505 = (filtSP & filtS05 & filtB05)
# filterSP1001 = (filtSP & filtS10 & filtB01)
#
# profSP1010 = df.loc[filterSP1010]
# profSP0505 = df.loc[filterSP0505]
# profSP1001 = df.loc[filterSP1001]
#
# profSP1010_nodup = profSP1010.drop_duplicates(['Sim', 'Team'])
# profSP0505_nodup = profSP0505.drop_duplicates(['Sim', 'Team'])
# profSP1001_nodup = profSP1001.drop_duplicates(['Sim', 'Team'])
#
# totO3_SP1010 = profSP1010_nodup.frac.mean()
# totO3_SP0505 = profSP0505_nodup.frac.mean()
# totO3_SP1001 = profSP1001_nodup.frac.mean()
#
#
# labellist = ['EN 0.5%-0.5B ','EN 1.0%-0.1B', 'SP 1.0%-0.1B', 'SP 1.0%-1.0B' ]
# titlelist = ['En0505', 'EN1001', 'SP1001', 'SP1010']
# # def Calc_average_profile_time(dataframelist, xcolumn, ybin, tmin, tmax ):
#
#
#
#
# avgprofAll_tpint, avgprofAll_tpint_err, Yt = Calc_average_profile_time([profEN0505, profEN1001, profSP1001, profSP1010], 'TPintC', 200, 0, 7000)
# avgprofAll_tpext, avgprofAll_tpext_err, Yt = Calc_average_profile_time([profEN0505, profEN1001, profSP1001, profSP1010], 'TPextC', 200, 0, 7000)
#
# avgprofAll_tpint_pre, avgprofAll_tpint_pre_err, Y = Calc_average_profile_pressure([profEN0505, profEN1001, profSP1001, profSP1010], 'TPintC')
# avgprofAll_tpext_pre, avgprofAll_tpext_pre_err, Y = Calc_average_profile_pressure([profEN0505, profEN1001, profSP1001, profSP1010], 'TPextC')
#
#
# adif = [0] * 4
# adiferr = [0] * 4
# adifpre = [0] * 4
# adifpreerr = [0] * 4
#
# rdif = [0] * 4
# rdiferr = [0] * 4
# rdifpre = [0] * 4
# rdifpreerr = [0] * 4
#
# for k in range(4):
#     adif[k] = [j - i for i,j in zip(avgprofAll_tpext[k], avgprofAll_tpint[k])]
#     adiferr[k] = [np.sqrt(i*i + j*j) for i,j in zip(avgprofAll_tpint_err[k], avgprofAll_tpext_err[k])]
#
#     adifpre[k] = [j - i for i,j in zip(avgprofAll_tpext_pre[k], avgprofAll_tpint_pre[k])]
#     adifpreerr[k] = [np.sqrt(i*i + j*j) for i,j in zip(avgprofAll_tpint_pre_err[k], avgprofAll_tpext_pre_err[k])]
#
#     rdif[k] = [(j - i)/j * 100 for i, j in zip(avgprofAll_tpext[k], avgprofAll_tpint[k])]
#     rdiferr[k] = [np.sqrt((ie * ie)/(i*i) + (je * je)/(j*j)) for ie, je, i, j  in zip(avgprofAll_tpint_err[k], avgprofAll_tpext_err[k], avgprofAll_tpint[k], avgprofAll_tpext[k])]
#
#     rdifpre[k] = [(j - i)/j * 100  for i, j in zip(avgprofAll_tpext_pre[k], avgprofAll_tpint_pre[k])]
#     rdifpreerr[k] = [np.sqrt((ie * ie)/(i*i) + (je * je)/(j*j)) for ie, je, i, j
#                      in zip(avgprofAll_tpint_pre_err[k], avgprofAll_tpext_pre_err[k], avgprofAll_tpint_pre[k], avgprofAll_tpext_pre[k])]
#
#
# print(avgprofAll_tpint[0])
# print(avgprofAll_tpint_err[0])
#
# print(adif[0])
# print(adiferr[0])
# #
# # for l in range(4):
# #
# #     fig, ax = plt.subplots()
# #     # plt.xlim(xra)
# #     # plt.ylim(yra)
# #     plt.title(labellist[l])
# #     plt.xlabel('Temp C')
# #     plt.ylabel('TSim')
# #
# #     ax.errorbar(avgprofAll_tpint[l], Y, xerr=avgprofAll_tpint_err[l], label='TPint', color='red', linewidth=1, elinewidth=0.5,
# #                 capsize=1, capthick=0.5)
# #     ax.errorbar(avgprofAll_tpext[l], Y, xerr=avgprofAll_tpext_err[l], label='TPext', color='blue', linewidth=1, elinewidth=0.5,
# #                 capsize=1, capthick=0.5, linestyle = '--')
# #     ax.errorbar(adif[l], Y, xerr=adiferr[l], label=' TPext - TPext ', color='black', linewidth=1, elinewidth=0.5,
# #                 capsize=1, capthick=0.5, linestyle = ':')
# #
# #     ax.legend(loc='upper right ', frameon=False, fontsize='small')
# #
# #     plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/' + titlelist[l] + '.png')
# #     plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/' + titlelist[l] + '.eps')
# #     plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/' + titlelist[l] + '.pdf')
# #
# #     plt.show()
# #
# # for l in range(0,4):
# #
# #     fig, ax = plt.subplots()
# #     # plt.xlim(xra)
# #     plt.ylim(1000, 5)
# #     ax.set_yscale('log')
# #     plt.title(labellist[l])
# #     plt.xlabel('Temp C')
# #     plt.ylabel('Pressure')
# #
# #     ax.errorbar(avgprofAll_tpint_pre[l], Y, xerr=avgprofAll_tpint_pre_err[l], label='TPint', color='red', linewidth=1, elinewidth=0.5,
# #                 capsize=1, capthick=0.5)
# #     ax.errorbar(avgprofAll_tpext_pre[l], Y, xerr=avgprofAll_tpext_pre_err[l], label='TPext', color='blue', linewidth=1, elinewidth=0.5,
# #                 capsize=1, capthick=0.5, linestyle = '--')
# #     ax.errorbar(adifpre[l], Y, xerr=adifpreerr[l], label=' TPext - TPext ', color='black', linewidth=1, elinewidth=0.5,
# #                 capsize=1, capthick=0.5, linestyle = ':')
# #
# #     ax.legend(loc='upper right ', frameon=False, fontsize='small')
# #
# #     plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/Pressure_' + titlelist[l] + '.png')
# #     plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/Pressure_' + titlelist[l] + '.eps')
# #     plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/Pressure_' + titlelist[l] + '.pdf')
# #
# #     plt.show()
#
#
#
# host = host_subplot(111, axes_class=AA.Axes)
# plt.subplots_adjust(bottom=0.30)
#
# par1 = host.twiny()
# par2 = host.twiny()
#
# new_fixed_axis = par1.get_grid_helper().new_fixed_axis
# par1.axis["bottom"] = new_fixed_axis(loc="bottom",
#                                     axes=par1,
#                                     offset=(0, -30))
# par2.axis["bottom"] = new_fixed_axis(loc="bottom",
#                                     axes=par2,
#                                     offset=(0, -60))
#
# par1.axis["bottom"].toggle(all=True)
#
# host.set_ylabel("Pressure")
# host.set_xlabel("Temp (C)")
# host.set_title("SP 1.0%-1.0B")
# host.set_ylim(1000, 3)
# host.set_yscale('log')
#
#
# par1.set_xlabel("TPint - TPext/ TPint")
# par2.set_xlabel("TPint - TPext.")
#
# p1, = host.plot(avgprofAll_tpint_pre[3], Y, label="TPint ")
# p2, = host.plot(avgprofAll_tpext_pre[3], Y, label="TPext ")
#
# p3, = par1.plot(rdifpre[3], Y, label="Rdif")
# p4, = par2.plot(adifpre[3], Y, label="Adif")
#
# # p1, = host.plot(avgprofAll_tpint[0], Yt, label="TPint ")
# # p2, = host.plot(avgprofAll_tpext[0], Yt, label="TPext ")
# #
# # p3, = par1.plot(rdif[0], Yt, label="Rdif")
# # p4, = par2.plot(adif[0], Yt, label="Adif")
#
# # par1.set_xlim(0, 4)
# # par1.set_xlim(1000, 0)
#
# # host.legend()
# host.legend(ncol=4, loc='upper center')
#
#
# host.axis["bottom"].label.set_color(p1.get_color())
# par1.axis["bottom"].label.set_color(p3.get_color())
# par2.axis["bottom"].label.set_color(p4.get_color())
#
# plt.draw()
#
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/SP1010_Tpump.png')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/SP1010_Tpump.eps')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/SP1010_Tpump.pdf')
# plt.show()

#
# fig, ax = plt.subplots()
# plt.plot(avgprofAll_tpint[0], Yt, label="TPint ")
# plt.plot(avgprofAll_tpext[0], Yt, label="TPext ")
#
# # # plt.plot(rdif[0], Yt, label="Rdif")
# plt.plot(adif[0], Yt, label="Adif")
# 
# plt.show()
