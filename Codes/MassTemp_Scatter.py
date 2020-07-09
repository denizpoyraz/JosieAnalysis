import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.integrate import quad

from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt
from Josie_Functions import Calc_average_profileCurrent_pressure, Calc_average_profile_time, Calc_average_profile_Pair, Calc_average_profile_pressure


def integrand(Pw, Rw, Tempc,  etap, Phip):

    return Pw/(Rw * Tempc) * etap * Phip

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



df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv_tempfixed.csv", low_memory=False)

print(list(df))

# df = cuts2017(df)

df = df.drop(df[(df.iB0 < -1) ].index)
df = df.drop(df[(df.iB1 < -1) ].index)
df = df.drop(df[(df.iB2 < -1) ].index)

df = df.drop(df[(df.iB0 > 1) ].index)
df = df.drop(df[(df.iB1 > 1) ].index)
df = df.drop(df[(df.iB2 > 1) ].index)

df = df.drop(df[(df.PO3 < 0)].index)
df = df.drop(df[(df.PO3_OPM < 0)].index)

# print('2017', list(df))
#
# 0910 beta0 cuts
df = df.drop(df[(df.Sim == 147) & (df.Team == 3)].index)
df = df.drop(df[(df.Sim == 158) & (df.Team == 1)].index)
df = df.drop(df[(df.Sim == 158) & (df.Team == 2)].index)
df = df.drop(df[(df.Sim == 160) & (df.Team == 4)].index)
df = df.drop(df[(df.Sim == 165) & (df.Team == 4)].index)
# df = df[df.ADX == 0]


# df = df.drop(df[(df.Diff < -1)].index)
## [175, 172, 175, 175, 175, 179]
## [1, 2, 3, 4, 2, 2]
df = df.drop(df[(df.Sim == 175) & (df.Team == 1)].index)
df = df.drop(df[(df.Sim == 172) & (df.Team == 2)].index)
df = df.drop(df[(df.Sim == 175) & (df.Team == 3)].index)
df = df.drop(df[(df.Sim == 175) & (df.Team == 4)].index)
df = df.drop(df[(df.Sim == 175) & (df.Team == 2)].index)
df = df.drop(df[(df.Sim == 179) & (df.Team == 2)].index)



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
df_nodup = df.drop_duplicates(['Sim', 'Team'])

dft = {}


print('en0505', len(profEN0505_nodup.Sim.tolist()))
nt = 50
cumsum_en0505 = [0] * len(profEN0505_nodup.Sim.tolist())
nsim_en0505 = len(profEN0505_nodup.Sim.tolist())
list_en0505 =  []
mean_en0505 = [0] * nt
cumsum_en1010 = [0] * len(profEN1010_nodup.Sim.tolist())
nsim_en1010 = len(profEN1010_nodup.Sim.tolist())
list_en1010 =  []
mean_en1010 = [0] * nt

cumsum_sp0505 = [0] * len(profSP0505_nodup.Sim.tolist())
nsim_sp0505 = len(profSP0505_nodup.Sim.tolist())
list_sp0505 =  []
mean_sp0505 = [0] * nt
cumsum_sp1010 = [0] * len(profSP1010_nodup.Sim.tolist())
nsim_sp1010 = len(profSP1010_nodup.Sim.tolist())
list_sp1010 =  []
mean_sp1010 = [0] * nt



for tt in range(nt):
    list_en0505.append([])
    list_en1010.append([])
    list_sp0505.append([])
    list_sp1010.append([])

#
#
# fig, ax1 = plt.subplots()
#
# ## EN0505
# for j in range(len(profEN0505_nodup.Sim.tolist())):
#
#     title = str(profEN0505_nodup.Sim.tolist()[j]) + '_' + str(profEN0505_nodup.Team.tolist()[j])
#     dft[j] = df[(df.Sim == profEN0505_nodup.Sim.tolist()[j]) & (df.Team == profEN0505_nodup.Team.tolist()[j])]
#     dft[j] = dft[j].reset_index()
#     # cumsum_en0505[j] = dft[j].massloss.cumsum() * 2
#
#     plt.plot(dft[j].Tsim, dft[j].massloss.cumsum() * 2, label=title)
#
#     dft[j]['cumsum'] = dft[j].massloss.cumsum() * 2
#     cumsum_en0505[j], avgprofAll_tpint_err, Y = Calc_average_profile_time([dft[j]], 'cumsum', 200, 0, 10000)
#
#
# for t in range(len(Y)):
#     for jj in range(nsim_en0505):
#         list_en0505[t].append(cumsum_en0505[jj][0][t])
#     mean_en0505[t] = np.nanmean(list_en0505[t])
#
# plt.plot(Y, mean_en0505, label = 'mean', color = 'black', linewidth = 2)
#
# ax1.legend(loc='lower right', frameon=True, fontsize='small')
# plt.title("0910 EN 0.5%-0.5B")
# plt.ylabel("mass loss in grs")
# plt.xlabel('Time')
# plt.xlim([0,13000])
#
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/0910_EN0505_massloss.png')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/0910_EN0505_massloss.eps')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/0910_EN0505_massloss.pdf')
#
# plt.show()
#
# fig, ax2 = plt.subplots()
#
# ## en1010
# for j in range(len(profEN1010_nodup.Sim.tolist())):
#
#     title = str(profEN1010_nodup.Sim.tolist()[j]) + '_' + str(profEN1010_nodup.Team.tolist()[j])
#     dft[j] = df[(df.Sim == profEN1010_nodup.Sim.tolist()[j]) & (df.Team == profEN1010_nodup.Team.tolist()[j])]
#     dft[j] = dft[j].reset_index()
#     # cumsum_en0505[j] = dft[j].massloss.cumsum() * 2
#
#     plt.plot(dft[j].Tsim, dft[j].massloss.cumsum() * 2, label=title)
#
#     dft[j]['cumsum'] = dft[j].massloss.cumsum() * 2
#     cumsum_en1010[j], avgprofAll_tpint_err, Y = Calc_average_profile_time([dft[j]], 'cumsum', 200, 0, 10000)
#
#
# for t in range(len(Y)):
#     for jj in range(nsim_en1010):
#         list_en1010[t].append(cumsum_en1010[jj][0][t])
#     mean_en1010[t] = np.nanmean(list_en1010[t])
#
# plt.plot(Y, mean_en1010, label = 'mean', color = 'black', linewidth = 2)
#
# ax2.legend(loc='lower right', frameon=True, fontsize='small')
# plt.title("0910 EN 1.0%-0.1B")
# plt.ylabel("mass loss in grs")
# plt.xlabel('Time')
# plt.xlim([0,13000])
#
#
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/0910_EN1010_massloss.png')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/0910_EN1010_massloss.eps')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/0910_EN1010_massloss.pdf')
#
# plt.show()
#
#
#
#
#
# fig, ax3 = plt.subplots()
#
# ## EN0505
# for j in range(len(profSP0505_nodup.Sim.tolist())):
#
#     title = str(profSP0505_nodup.Sim.tolist()[j]) + '_' + str(profSP0505_nodup.Team.tolist()[j])
#     dft[j] = df[(df.Sim == profSP0505_nodup.Sim.tolist()[j]) & (df.Team == profSP0505_nodup.Team.tolist()[j])]
#     dft[j] = dft[j].reset_index()
#     # cumsum_sp0505[j] = dft[j].massloss.cumsum() * 2
#
#     plt.plot(dft[j].Tsim, dft[j].massloss.cumsum() * 2, label=title)
#
#     dft[j]['cumsum'] = dft[j].massloss.cumsum() * 2
#     cumsum_sp0505[j], avgprofAll_tpint_err, Y = Calc_average_profile_time([dft[j]], 'cumsum', 200, 0, 10000)
#
#
# for t in range(len(Y)):
#     for jj in range(nsim_sp0505):
#         list_sp0505[t].append(cumsum_sp0505[jj][0][t])
#     mean_sp0505[t] = np.nanmean(list_sp0505[t])
#
# plt.plot(Y, mean_sp0505, label = 'mean', color = 'black', linewidth = 2)
#
# ax3.legend(loc='lower right', frameon=True, fontsize='small')
# plt.title("0910 SP 1.0%-0.1B")
# plt.ylabel("mass loss in grs")
# plt.xlabel('Time')
# plt.xlim([0,13000])
#
#
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/0910_SP0505_massloss.png')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/0910_SP0505_massloss.eps')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/0910_SP0505_massloss.pdf')
#
# plt.show()
#
# fig, ax4 = plt.subplots()
#
# ## en1010
# for j in range(len(profSP1010_nodup.Sim.tolist())):
#
#     title = str(profSP1010_nodup.Sim.tolist()[j]) + '_' + str(profSP1010_nodup.Team.tolist()[j])
#     dft[j] = df[(df.Sim == profSP1010_nodup.Sim.tolist()[j]) & (df.Team == profSP1010_nodup.Team.tolist()[j])]
#     dft[j] = dft[j].reset_index()
#     # cumsum_sp0505[j] = dft[j].massloss.cumsum() * 2
#
#     plt.plot(dft[j].Tsim, dft[j].massloss.cumsum() * 2, label=title)
#
#     dft[j]['cumsum'] = dft[j].massloss.cumsum() * 2
#     cumsum_sp1010[j], avgprofAll_tpint_err, Y = Calc_average_profile_time([dft[j]], 'cumsum', 200, 0, 10000)
#
#
# for t in range(len(Y)):
#     for jj in range(nsim_sp1010):
#         list_sp1010[t].append(cumsum_sp1010[jj][0][t])
#     mean_sp1010[t] = np.nanmean(list_sp1010[t])
#
# plt.plot(Y, mean_sp1010, label = 'mean', color = 'black', linewidth = 2)
#
# ax4.legend(loc='lower right', frameon=True, fontsize='small')
# plt.title("0910 SP 1.0%-1.0B")
# plt.ylabel("mass loss in grs")
# plt.xlabel('Time')
# plt.xlim([0,13000])
#
#
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/0910_SP1010_massloss.png')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/0910_SP1010_massloss.eps')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/0910_SP1010_massloss.pdf')
#
# plt.show()



#####################33  indivudal plots
# 
dft = df[(df.Sim == 183) & (df.Team == 5)]

host = host_subplot(111, axes_class=AA.Axes)
plt.subplots_adjust(bottom=0.30)

par1 = host.twiny()
par2 = host.twiny()

new_fixed_axis = par2.get_grid_helper().new_fixed_axis
par2.axis["bottom"] = new_fixed_axis(loc="bottom",
                                    axes=par2,
                                    offset=(0, -30))
par1.axis["bottom"] = new_fixed_axis(loc="bottom",
                                    axes=par1,
                                    offset=(0, -60))

par2.axis["bottom"].toggle(all=True)

host.set_ylabel("Mass Loss in gr")
host.set_xlabel("Time Sim.")
host.set_title("183_5 SP 1.0%-1.0B")
# host_set_yrange(0, 0.4)

par1.set_xlabel("Pressure")
par2.set_xlabel("TPint")

p1, = host.plot(dft.Tsim, dft.massloss.cumsum()*2, label="Time ")
p2, = par1.plot(dft.Pair, dft.massloss.cumsum()*2, label="Pressure")
p3, = par2.plot(dft.TPext, dft.massloss.cumsum()*2,  label="TPint")

# par1.set_xlim(0, 4)
par1.set_xlim(1000, 0)

# host.legend()
host.legend(ncol=3, loc='upper center')


host.axis["bottom"].label.set_color(p1.get_color())
par1.axis["bottom"].label.set_color(p2.get_color())
par2.axis["bottom"].label.set_color(p3.get_color())

plt.draw()

plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/2017_SP1010_183_massloss.png')
plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/2017_SP1010_183_massloss.eps')
plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/2017_SP1010_183_massloss.pdf')
plt.show()





# for t2 in range(len(Yp)):
#     for jj2 in range(nsim_en0505):
#         list_en0505p[t2].append(cumsum_en0505p[jj2][0][t2])
#     mean_en0505p[t2] = np.nanmean(list_en0505p[t2])
#
# print('mean_en0505p', mean_en0505p)
#
# #         # plt.show()
# plt.plot(Yp, mean_en0505p, label = 'mean')
# plt.show()


# ## pressure
# nnp = 19
# cumsum_en0505p = [0] * len(profEN0505_nodup.Sim.tolist())
# list_en0505p =  []
# mean_en0505p = [0] * nt
#
# for tp in range(nnp):
#     list_en0505p.append([])
