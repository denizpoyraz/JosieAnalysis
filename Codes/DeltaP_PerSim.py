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
from Analyse_Functions import cuts2017, cuts0910, polyfit


# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_Data_nocut_tempfixed.csv", low_memory=False)
#
# df = cuts2017(df)
# # df = df[df.Sim > 185]
# df = df[df.Sim < 186]


# df['DeltaP'] = df['Pw'] - df['Pair']

# df = df[df.Sim < 186]
#
df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_Data_nocut_tempfixed.csv", low_memory=False)

df['DeltaP'] = df['Pw'] - df['Pair']
df = cuts0910(df)
# df = df[df.Year == 2009]
# df = df[df.Year == 2010]
dfp = df[df.Pair >= 0]

# df = df.drop(df[(df.Sim == 166) & (df.Team == 1)].index)

# dfp = df[df.DeltaP > 0]
# dfp = df

#
#
df['TPintC'] = df['TPext'] - 273
df['TPextC'] = df['TPint'] - 273
df['TPintK'] = df['TPext']
df['TPextK'] = df['TPint']
df['TcellC'] = df['Tcell'] - 273
df['TboilK'] = df['Tboil'] + 273
#
#

### filter for each sonde solution

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
profEN0505_dp = dfp.loc[filterEN0505]
profEN1010_dp = dfp.loc[filterEN1010]
profEN0505_nodup = profEN0505.drop_duplicates(['Sim', 'Team'])
profEN1010_nodup = profEN1010.drop_duplicates(['Sim', 'Team'])
###
filterSP1010 = (filtSP & filtS10 & filtB10)
filterSP0505 = (filtSP & filtS05 & filtB05)
#2017
# filterSP0505 = (filtSP & filtS10 & filtB01)

profSP1010 = df.loc[filterSP1010]
profSP0505 = df.loc[filterSP0505]
profSP1010_dp = dfp.loc[filterSP1010]
profSP0505_dp = dfp.loc[filterSP0505]
profSP1010_nodup = profSP1010.drop_duplicates(['Sim', 'Team'])
profSP0505_nodup = profSP0505.drop_duplicates(['Sim', 'Team'])

avgprof_deltap_all, avgprof_deltap_all_err, Yp = Calc_average_profile_pressure([profEN0505_dp, profEN1010_dp, profSP0505_dp, profSP1010_dp], 'DeltaP')
# avgprof_deltap_all, avgprof_deltap_all_err, Yp = Calc_average_profile_pressure([profEN0505_dp, profEN1010_dp, profSP0505_dp, profSP1010_dp], 'Pw')


print('en0505 all', avgprof_deltap_all[0])

dft = {}

size = len(profEN0505_nodup)

avgprof_deltap = [0] * size
avgprof_deltap_err = [0] * size
title = [''] * size

print('sim' , profEN0505_nodup.Sim.tolist())
print('team' , profEN0505_nodup.Team.tolist())

## en0505
for j in range(len(profEN0505_nodup)):

    dft[j] = dfp[(dfp.Sim == profEN0505_nodup.Sim.tolist()[j]) & (dfp.Team == profEN0505_nodup.Team.tolist()[j])]

    title[j] = str(profEN0505_nodup.Sim.tolist()[j]) + '_' + str(profEN0505_nodup.Team.tolist()[j])


    avgprof_deltap[j], avgprof_deltap_err[j], Yp = Calc_average_profile_pressure([dft[j]], 'DeltaP')

    print(j, avgprof_deltap[j])

fig, ax1 = plt.subplots()
# plt.xlim([-40, 40])
plt.ylim([1000, 5])
plt.xlim([-5, 40])
plt.title(' 2010 DeltaP > 0 EN 0.5%-0.5B')
plt.xlabel('Pw - Pair ')
plt.ylabel('Pressure')
plt.grid(True)
ax1.set_yscale('log')

for i in range(size):

    ax1.plot(avgprof_deltap[i][0], Yp,  linewidth=1.5, label=title[i])

ax1.plot(avgprof_deltap_all[0], Yp, linewidth=1, label='EN 0.5%-0.5B', color = 'black')
ax1.legend(loc='best', frameon=True, fontsize='x-small')

# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/DeltaP_2010_DeltaPg0_EN0505.png')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/DeltaP_2010_DeltaPg0_EN0505.pdf')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/DeltaP_2010_DeltaPg0_EN0505.eps')

plt.show()

dft = {}
size = len(profEN1010_nodup)
avgprof_deltap = [0] * size
avgprof_deltap_err = [0] * size
title = [''] * size

## en1010
for j in range(len(profEN1010_nodup)):

    dft[j] = dfp[(dfp.Sim == profEN1010_nodup.Sim.tolist()[j]) & (dfp.Team == profEN1010_nodup.Team.tolist()[j])]

    title[j] = str(profEN1010_nodup.Sim.tolist()[j]) + '_' + str(profEN1010_nodup.Team.tolist()[j])


    avgprof_deltap[j], avgprof_deltap_err[j], Yp = Calc_average_profile_pressure([dft[j]], 'DeltaP')

fig, ax2 = plt.subplots()
# plt.xlim([-40, 40])
plt.ylim([1000, 5])
plt.xlim([-5, 40])
plt.title(' 2010 DeltaP > 0 EN 1.0%-1.0B')
plt.xlabel('Pw - Pair ')
plt.ylabel('Pressure')
plt.grid(True)
ax2.set_yscale('log')

for i in range(size):

    ax2.plot(avgprof_deltap[i][0], Yp,  linewidth=1.5, label=title[i])

ax2.plot(avgprof_deltap_all[1], Yp, linewidth=1, label='EN1.0%-1.0B', color = 'black')
ax2.legend(loc='best', frameon=True, fontsize='x-small')

# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/DeltaP_2010_DeltaPg0_EN1010.png')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/DeltaP_2010_DeltaPg0_EN1010.pdf')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/DeltaP_2010_DeltaPg0_EN1010.eps')

plt.show()

##
dft = {}
size = len(profSP0505_nodup)
avgprof_deltap = [0] * size
avgprof_deltap_err = [0] * size
title = [''] * size

## en1010
for j in range(len(profSP0505_nodup)):

    dft[j] = dfp[(dfp.Sim == profSP0505_nodup.Sim.tolist()[j]) & (dfp.Team == profSP0505_nodup.Team.tolist()[j])]

    title[j] = str(profSP0505_nodup.Sim.tolist()[j]) + '_' + str(profSP0505_nodup.Team.tolist()[j])


    avgprof_deltap[j], avgprof_deltap_err[j], Yp = Calc_average_profile_pressure([dft[j]], 'DeltaP')

fig, ax3 = plt.subplots()
# plt.xlim([-40, 40])
plt.ylim([1000, 5])
plt.xlim([-5, 40])
plt.title(' 2010 DeltaP > 0 SP 0.5%-0.5B')
plt.xlabel('Pw - Pair ')
plt.ylabel('Pressure')
plt.grid(True)
ax3.set_yscale('log')

for i in range(size):

    ax3.plot(avgprof_deltap[i][0], Yp,  linewidth=1.5, label=title[i])

ax3.plot(avgprof_deltap_all[2], Yp, linewidth=1, label='SP 0.5%-0.5B', color = 'black')
ax3.legend(loc='best', frameon=True, fontsize='x-small')
#
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/DeltaP_2010_DeltaPg0_SP0505.png')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/DeltaP_2010_DeltaPg0_SP0505.pdf')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/DeltaP_2010_DeltaPg0_SP0505.eps')

plt.show()


##
dft = {}
size = len(profSP1010_nodup)
avgprof_deltap = [0] * size
avgprof_deltap_err = [0] * size
title = [''] * size

## en1010
for j in range(len(profSP1010_nodup)):

    dft[j] = dfp[(dfp.Sim == profSP1010_nodup.Sim.tolist()[j]) & (dfp.Team == profSP1010_nodup.Team.tolist()[j])]

    title[j] = str(profSP1010_nodup.Sim.tolist()[j]) + '_' + str(profSP1010_nodup.Team.tolist()[j])

    avgprof_deltap[j], avgprof_deltap_err[j], Yp = Calc_average_profile_pressure([dft[j]], 'DeltaP')
    print('sp1010', j, title[j], avgprof_deltap[j] )

print('all', avgprof_deltap_all[3])
fig, ax4 = plt.subplots()
plt.xlim([-5, 40])
plt.ylim([1000, 5])
plt.title(' 2010 DeltaP > 0 SP 1.0%-1.0B')
plt.xlabel('Pw - Pair ')
plt.ylabel('Pressure')
plt.grid(True)
ax4.set_yscale('log')

for i in range(size):

    ax4.plot(avgprof_deltap[i][0], Yp,  linewidth=1.5, label=title[i])

ax4.plot(avgprof_deltap_all[3], Yp, linewidth=3, label='SP 1.0%-1.0B', color = 'black')
ax4.legend(loc='best', frameon=True, fontsize='x-small')

# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/DeltaP_2010_DeltaPg0_SP1010.png')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/DeltaP_2010_DeltaPg0_SP1010.pdf')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/DeltaP_2010_DeltaPg0_SP1010.eps')

plt.show()


