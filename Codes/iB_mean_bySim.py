import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import NullFormatter
from Analyse_Functions import cuts2017, cuts0910, polyfit




# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_Data_nocut_tempfixed.csv", low_memory=False)
df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_Data_nocut_tempfixed.csv", low_memory=False)
# print(list(df))

# df = cuts0910(df)

# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie9602_Data.csv", low_memory=False)

## week 1 : 171, 172, 173, 174, 177  , 182, 183, 184, 185, 191
#
# week1 = [171, 172, 173, 174, 177, 182, 183, 184, 185, 191]
# week2 = [175, 176, 178, 179, 180, 181, 186, 187, 188, 189, 190]
#
# # ## week1 2017
# #
# df = df.drop(df[(df.Sim == 175) | (df.Sim == 176) | (df.Sim == 178) | (df.Sim == 179) | (df.Sim == 180) | (df.Sim == 181)
#              | (df.Sim == 186) | (df.Sim == 187) | (df.Sim == 188) | (df.Sim == 189) | (df.Sim == 190) ].index)
#
# #week 2 2017
# df = df.drop(df[(df.Sim == 171) | (df.Sim == 172) | (df.Sim == 173) | (df.Sim == 174) | (df.Sim == 177) | (df.Sim == 182)
#              | (df.Sim == 183) | (df.Sim == 184) | (df.Sim == 185) | (df.Sim == 191) ].index)
#
# df = df.drop(df[(df.iB0 < -1) ].index)
# df = df.drop(df[(df.iB1 < -1) ].index)
# df = df.drop(df[(df.iB2 < -1) ].index)
#
# df = df.drop(df[(df.iB0 > 1) ].index)
# df = df.drop(df[(df.iB1 > 1) ].index)
# df = df.drop(df[(df.iB2 > 1) ].index)

df = df.drop(df[(df.PO3 < 0)].index)
df = df.drop(df[(df.PO3_OPM < 0)].index)




# print('0910', list(df))
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
df = df[df.Sim < 186]
df = df.drop(df[(df.Sim == 175) & (df.Team == 1)].index)
df = df.drop(df[(df.Sim == 172) & (df.Team == 2)].index)
df = df.drop(df[(df.Sim == 175) & (df.Team == 3)].index)
df = df.drop(df[(df.Sim == 175) & (df.Team == 4)].index)
df = df.drop(df[(df.Sim == 175) & (df.Team == 2)].index)
df = df.drop(df[(df.Sim == 179) & (df.Team == 2)].index)

df['DeltaP'] = df['Pw'] - df['Pair']
dfp = df[df.DeltaP > 0]

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
filterEN1010 = (filtEN & filtS10 & filtB01)

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
filterSP0505 = (filtSP & filtS10 & filtB01)

profSP1010 = df.loc[filterSP1010]
profSP0505 = df.loc[filterSP0505]
profSP1010_dp = dfp.loc[filterSP1010]
profSP0505_dp = dfp.loc[filterSP0505]
profSP1010_nodup = profSP1010.drop_duplicates(['Sim', 'Team'])
profSP0505_nodup = profSP0505.drop_duplicates(['Sim', 'Team'])
df_nodup = df.drop_duplicates(['Sim', 'Team'])

dft = {}
dftp = {}

dftl20 = {}
dft20 = {}
dft15 = {}
dft10 = {}
dft5 = {}

df['TPintC'] = df['TPint'] - 273
df['TPextC'] = df['TPext'] - 273
df['TcellC'] = df['Tcell'] - 273


filter_20 = (df.Pair <= 20) & (df.Pair > 19)
filter_15 = (df.Pair <= 15) & (df.Pair > 14)
filter_10 = (df.Pair <= 10) & (df.Pair > 9)
filter_5 = (df.Pair <= 9) & (df.Pair > 6)
# filter_5 = (df.Pair <= 6) & (df.Pair >= 5)
filter_less20 = (df.Pair <= 20)


en0505_20 = [0] * len(profEN0505_nodup.Sim.tolist())
en0505_15 = [0] * len(profEN0505_nodup.Sim.tolist())
en0505_10 = [0] * len(profEN0505_nodup.Sim.tolist())
en0505_5 = [0] * len(profEN0505_nodup.Sim.tolist())
en0505_mass = [0] * len(profEN0505_nodup.Sim.tolist())
en0505_intmass = [0] * len(profEN0505_nodup.Sim.tolist())
en0505_mass20 = [0] * len(profEN0505_nodup.Sim.tolist())
en0505_intdp = [0] * len(profEN0505_nodup.Sim.tolist())



## EN0505
for j in range(len(profEN0505_nodup.Sim.tolist())):

    dft[j] = df[(df.Sim == profEN0505_nodup.Sim.tolist()[j]) & (df.Team == profEN0505_nodup.Team.tolist()[j])]
    dftp[j] = dfp[(dfp.Sim == profEN0505_nodup.Sim.tolist()[j]) & (dfp.Team == profEN0505_nodup.Team.tolist()[j])]

    dft20[j] = df[(df.Sim == profEN0505_nodup.Sim.tolist()[j]) & (df.Team == profEN0505_nodup.Team.tolist()[j]) & filter_20]
    dft15[j] = df[(df.Sim == profEN0505_nodup.Sim.tolist()[j]) & (df.Team == profEN0505_nodup.Team.tolist()[j]) & filter_15]
    dft10[j] = df[(df.Sim == profEN0505_nodup.Sim.tolist()[j]) & (df.Team == profEN0505_nodup.Team.tolist()[j]) & filter_10]
    dft5[j] = df[(df.Sim == profEN0505_nodup.Sim.tolist()[j]) & (df.Team == profEN0505_nodup.Team.tolist()[j]) & filter_5]
    dftl20[j] = df[(df.Sim == profEN0505_nodup.Sim.tolist()[j]) & (df.Team == profEN0505_nodup.Team.tolist()[j]) & filter_less20]

    en0505_intmass[j] = np.trapz(dft[j].massloss, x=dft[j].Tsim)
    en0505_mass20[j] = np.trapz(dftl20[j].massloss, x=dftl20[j].Tsim)
    en0505_intdp[j] = np.trapz(dftp[j].DeltaP, x=dftp[j].Tsim)


    en0505_20[j] = np.nanmean(dft20[j]['TcellC'])
    en0505_15[j] = np.nanmean(dft15[j]['TcellC'])
    en0505_10[j] = np.nanmean(dft10[j]['TcellC'])
    en0505_5[j] = np.nanmean(dft5[j]['TcellC'])
    en0505_mass[j] = np.nanmean(dft[j]['PostTestSolution_Lost_gr'])
    # en0505_mass[j] = np.nanmean(dft[j]['Diff'])

    ### 2017 PostTestSolution_Lost_gr

print('size', len(profEN0505_nodup), len(profEN1010_nodup), len(profSP0505_nodup), len(profSP1010_nodup))

print('EN0505 mass', np.nanmean(en0505_mass), np.nanstd(en0505_mass), en0505_mass)
print('EN0505 integraded mass', np.nanmean(en0505_intmass), np.nanstd(en0505_intmass), en0505_intmass)
print('EN0505 integraded mass less 20', np.nanmean(en0505_mass20), np.nanstd(en0505_mass20), en0505_mass20)
print('EN0505 integrated delta P mean', np.nanmean(en0505_intdp), np.nanstd(en0505_intdp), en0505_intdp)
print('EN0505 integrated delta P median', np.nanmedian(en0505_intdp), np.nanstd(en0505_intdp), en0505_intdp)



print('20 C', np.nanmean(en0505_20), np.nanstd(en0505_20), en0505_20)
print('15 C', np.nanmean(en0505_15), np.nanstd(en0505_15), en0505_15)
print('10 C', np.nanmean(en0505_10), np.nanstd(en0505_10), en0505_10)
print('5 C', np.nanmean(en0505_5), np.nanstd(en0505_5), en0505_5)

fig, axs = plt.subplots(2, 2, sharey=True, tight_layout=True)
axs[0, 0].hist(en0505_20)
axs[0, 0].set_title('EN 0.5%-0.5B 20hPa')
axs[0, 1].hist(en0505_15)
axs[0, 1].set_title('EN 0.5%-0.5B 15hPa')
axs[1, 0].hist(en0505_10)
axs[1, 0].set_title('EN 0.5%-0.5B 10hPa')
axs[1, 1].hist(en0505_5)
axs[1, 1].set_title('EN 0.5%-0.5B 5hPa')

plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/Hist2017_EN0505_bysim.png')
plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/Hist2017_EN0505_bysim.pdf')
plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/Hist2017_EN0505_bysim.eps')

######################################################################################################

EN1010_20 = [0] * len(profEN1010_nodup.Sim.tolist())
EN1010_15 = [0] * len(profEN1010_nodup.Sim.tolist())
EN1010_10 = [0] * len(profEN1010_nodup.Sim.tolist())
EN1010_5 = [0] * len(profEN1010_nodup.Sim.tolist())
EN1010_mass = [0] * len(profEN1010_nodup.Sim.tolist())
EN1010_intmass = [0] * len(profEN1010_nodup.Sim.tolist())
EN1010_mass20 = [0] * len(profEN1010_nodup.Sim.tolist())
EN1010_intdp = [0] * len(profEN1010_nodup.Sim.tolist())



## EN1001
for j in range(len(profEN1010_nodup.Sim.tolist())):

    dft[j] = df[(df.Sim == profEN1010_nodup.Sim.tolist()[j]) & (df.Team == profEN1010_nodup.Team.tolist()[j])]
    dftp[j] = dfp[(dfp.Sim == profEN1010_nodup.Sim.tolist()[j]) & (dfp.Team == profEN1010_nodup.Team.tolist()[j])]

    dft20[j] = df[
        (df.Sim == profEN1010_nodup.Sim.tolist()[j]) & (df.Team == profEN1010_nodup.Team.tolist()[j]) & filter_20]
    dft15[j] = df[
        (df.Sim == profEN1010_nodup.Sim.tolist()[j]) & (df.Team == profEN1010_nodup.Team.tolist()[j]) & filter_15]
    dft10[j] = df[
        (df.Sim == profEN1010_nodup.Sim.tolist()[j]) & (df.Team == profEN1010_nodup.Team.tolist()[j]) & filter_10]
    dft5[j] = df[
        (df.Sim == profEN1010_nodup.Sim.tolist()[j]) & (df.Team == profEN1010_nodup.Team.tolist()[j]) & filter_5]
    dftl20[j] = df[
        (df.Sim == profEN1010_nodup.Sim.tolist()[j]) & (df.Team == profEN1010_nodup.Team.tolist()[j]) & filter_less20]

    EN1010_intmass[j] = np.trapz(dft[j].massloss, x=dft[j].Tsim)
    EN1010_mass20[j] = np.trapz(dftl20[j].massloss, x=dftl20[j].Tsim)

    EN1010_20[j] = np.nanmean(dft20[j]['TcellC'])
    EN1010_15[j] = np.nanmean(dft15[j]['TcellC'])
    EN1010_10[j] = np.nanmean(dft10[j]['TcellC'])
    EN1010_5[j] = np.nanmean(dft5[j]['TcellC'])
    # EN1010_mass[j] = np.nanmean(dft[j]['Diff'])
    EN1010_mass[j] = np.nanmean(dft[j]['PostTestSolution_Lost_gr'])
    # EN1010_intdp[j] = np.trapz(dftp[j].DeltaP, x=dftp[j].Tsim)



print('EN1010 mass', np.nanmean(EN1010_mass),np.nanstd(EN1010_mass),  EN1010_mass)
print('EN1010 integrated mass', np.nanmean(EN1010_intmass),np.nanstd(EN1010_intmass),  EN1010_intmass)
print('EN1010 mass20', np.nanmean(EN1010_mass20),np.nanstd(EN1010_mass20),  EN1010_mass20)
print('EN1010 int DeltaP mean', np.nanmean(EN1010_intdp),np.nanstd(EN1010_intdp),  EN1010_intdp)
print('EN1010 int DeltaP median', np.nanmedian(EN1010_intdp),np.nanstd(EN1010_intdp),  EN1010_intdp)

print('20 C', np.nanmean(EN1010_20), np.nanstd(EN1010_20), EN1010_20)
print('15 C', np.nanmean(EN1010_15),np.nanstd(EN1010_15), EN1010_15)
print('10 C', np.nanmean(EN1010_10), np.nanstd(EN1010_10),  EN1010_10)
print('5 C', np.nanmean(EN1010_5), np.nanstd(EN1010_5), EN1010_5)

fig, axs = plt.subplots(2, 2, sharey=True, tight_layout=True)
axs[0,0].hist(EN1010_20)
axs[0,0].set_title('EN 1.0%-0.1B 20hPa')
axs[0,1].hist(EN1010_15)
axs[0,1].set_title('EN 1.0%-0.1B 15hPa')
axs[1,0].hist(EN1010_10)
axs[1,0].set_title('EN 1.0%-0.1B 10hPa')
axs[1,1].hist(EN1010_5)
axs[1,1].set_title('EN 1.0%-0.1B 5hPa')


# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/Hist2017_EN1010_bysim.png')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/Hist2017_EN1010_bysim.pdf')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/Hist2017_EN1010_bysim.eps')

plt.show()

##################################################################################################

sp0505_20 = [0] * len(profSP0505_nodup.Sim.tolist())
sp0505_15 = [0] * len(profSP0505_nodup.Sim.tolist())
sp0505_10 = [0] * len(profSP0505_nodup.Sim.tolist())
sp0505_5 = [0] * len(profSP0505_nodup.Sim.tolist())
sp0505_mass = [0] * len(profSP0505_nodup.Sim.tolist())
sp0505_intmass = [0] * len(profSP0505_nodup.Sim.tolist())
sp0505_mass20 = [0] * len(profSP0505_nodup.Sim.tolist())
sp0505_intdp = [0] * len(profSP0505_nodup.Sim.tolist())


## SP0505
for j in range(len(profSP0505_nodup.Sim.tolist())):
    dft[j] = df[(df.Sim == profSP0505_nodup.Sim.tolist()[j]) & (df.Team == profSP0505_nodup.Team.tolist()[j])]
    dftp[j] = dfp[(dfp.Sim == profSP0505_nodup.Sim.tolist()[j]) & (dfp.Team == profSP0505_nodup.Team.tolist()[j])]

    dft20[j] = df[
        (df.Sim == profSP0505_nodup.Sim.tolist()[j]) & (df.Team == profSP0505_nodup.Team.tolist()[j]) & filter_20]
    dft15[j] = df[
        (df.Sim == profSP0505_nodup.Sim.tolist()[j]) & (df.Team == profSP0505_nodup.Team.tolist()[j]) & filter_15]
    dft10[j] = df[
        (df.Sim == profSP0505_nodup.Sim.tolist()[j]) & (df.Team == profSP0505_nodup.Team.tolist()[j]) & filter_10]
    dft5[j] = df[
        (df.Sim == profSP0505_nodup.Sim.tolist()[j]) & (df.Team == profSP0505_nodup.Team.tolist()[j]) & filter_5]
    dftl20[j] = df[
        (df.Sim == profSP0505_nodup.Sim.tolist()[j]) & (df.Team == profSP0505_nodup.Team.tolist()[j]) & filter_less20]

    sp0505_intmass[j] = np.trapz(dft[j].massloss, x=dft[j].Tsim)
    sp0505_mass20[j] = np.trapz(dftl20[j].massloss, x=dftl20[j].Tsim)

    sp0505_20[j] = np.nanmean(dft20[j]['TcellC'])
    sp0505_15[j] = np.nanmean(dft15[j]['TcellC'])
    sp0505_10[j] = np.nanmean(dft10[j]['TcellC'])
    sp0505_5[j] = np.nanmean(dft5[j]['TcellC'])
    # sp0505_mass[j] = np.nanmean(dft[j]['Diff'])
    # sp0505_mass[j] = np.nanmean(dft[j]['PostTestSolution_Lost_gr'])
    # sp0505_intdp[j] = np.trapz(dftp[j].DeltaP, x=dftp[j].Tsim)


print('SP0505 mass', np.nanmean(sp0505_mass), np.nanstd(sp0505_mass), sp0505_mass)
print('SP0505 integrated mass', np.nanmean(sp0505_intmass), np.nanstd(sp0505_intmass), sp0505_intmass)
print('SP0505  mass 20', np.nanmean(sp0505_mass20), np.nanstd(sp0505_mass20), sp0505_mass20)
print('SP0505 int deltaP mean', np.nanmean(sp0505_intdp), np.nanstd(sp0505_intdp), sp0505_intdp)
print('SP0505 int deltaP meadin', np.nanmedian(sp0505_intdp), np.nanstd(sp0505_intdp), sp0505_intdp)

print('20 C', np.nanmean(sp0505_20), np.nanstd(sp0505_20), sp0505_20)
print('15 C', np.nanmean(sp0505_15), np.nanstd(sp0505_15), sp0505_15)
print('10 C', np.nanmean(sp0505_10), np.nanstd(sp0505_10), sp0505_10)
print('5 C', np.nanmean(sp0505_5), np.nanstd(sp0505_5), sp0505_5)

fig, axs = plt.subplots(2, 2, sharey=True, tight_layout=True)
axs[0, 0].hist(sp0505_20)
axs[0, 0].set_title('SP 0.5%-0.5B 20hPa')
axs[0, 1].hist(sp0505_15)
axs[0, 1].set_title('SP 0.5%-0.5B 15hPa')
axs[1, 0].hist(sp0505_10)
axs[1, 0].set_title('SP 0.5%-0.5B 10hPa')
axs[1, 1].hist(sp0505_5)
axs[1, 1].set_title('SP 0.5%-0.5B 5hPa')

# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/Hist2017_SP0505_bysim.png')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/Hist2017_SP0505_bysim.pdf')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/Hist2017_SP0505_bysim.eps')

######################################################################################################

##################################################################################################

sp1010_20 = [0] * len(profSP1010_nodup.Sim.tolist())
sp1010_15 = [0] * len(profSP1010_nodup.Sim.tolist())
sp1010_10 = [0] * len(profSP1010_nodup.Sim.tolist())
sp1010_5 = [0] * len(profSP1010_nodup.Sim.tolist())
sp1010_mass = [0] * len(profSP1010_nodup.Sim.tolist())
sp1010_intmass = [0] * len(profSP1010_nodup.Sim.tolist())
sp1010_mass20 = [0] * len(profSP1010_nodup.Sim.tolist())
sp1010_intdp = [0] * len(profSP1010_nodup.Sim.tolist())


## SP1010
for j in range(len(profSP1010_nodup.Sim.tolist())):
    dft[j] = df[(df.Sim == profSP1010_nodup.Sim.tolist()[j]) & (df.Team == profSP1010_nodup.Team.tolist()[j])]
    dftp[j] = dfp[(dfp.Sim == profSP1010_nodup.Sim.tolist()[j]) & (dfp.Team == profSP1010_nodup.Team.tolist()[j])]

    dft20[j] = df[
        (df.Sim == profSP1010_nodup.Sim.tolist()[j]) & (df.Team == profSP1010_nodup.Team.tolist()[j]) & filter_20]
    dft15[j] = df[
        (df.Sim == profSP1010_nodup.Sim.tolist()[j]) & (df.Team == profSP1010_nodup.Team.tolist()[j]) & filter_15]
    dft10[j] = df[
        (df.Sim == profSP1010_nodup.Sim.tolist()[j]) & (df.Team == profSP1010_nodup.Team.tolist()[j]) & filter_10]
    dft5[j] = df[
        (df.Sim == profSP1010_nodup.Sim.tolist()[j]) & (df.Team == profSP1010_nodup.Team.tolist()[j]) & filter_5]
    dftl20[j] = df[
        (df.Sim == profSP1010_nodup.Sim.tolist()[j]) & (df.Team == profSP1010_nodup.Team.tolist()[j]) & filter_less20]

    sp1010_intmass[j] = np.trapz(dft[j].massloss, x=dft[j].Tsim)
    sp1010_mass20[j] = np.trapz(dftl20[j].massloss, x=dftl20[j].Tsim)
    sp1010_intdp[j] = np.trapz(dftp[j].DeltaP, x=dftp[j].Tsim)


    sp1010_20[j] = np.nanmean(dft20[j]['TcellC'])
    sp1010_15[j] = np.nanmean(dft15[j]['TcellC'])
    sp1010_10[j] = np.nanmean(dft10[j]['TcellC'])
    sp1010_5[j] = np.nanmean(dft5[j]['TcellC'])
    # sp1010_mass[j] = np.nanmean(dft[j]['Diff'])
    sp1010_mass[j] = np.nanmean(dft[j]['PostTestSolution_Lost_gr'])

print('SP1010 mass', np.nanmean(sp1010_mass), np.nanstd(sp1010_mass), sp1010_mass)
print('SP1010 integrated mass', np.nanmean(sp1010_intmass), np.nanstd(sp1010_intmass), sp1010_intmass)
print('SP1010 mass 20', np.nanmean(sp1010_mass20), np.nanstd(sp1010_mass20), sp1010_mass20)
print('SP1010 int dp mean', np.nanmean(sp1010_intdp), np.nanstd(sp1010_intdp), sp1010_intdp)
print('SP1010 int dp median', np.nanmedian(sp1010_intdp), np.nanstd(sp1010_intdp), sp1010_intdp)

print('20 C', np.nanmean(sp1010_20), np.nanstd(sp1010_20), sp1010_20)
print('15 C', np.nanmean(sp1010_15), np.nanstd(sp1010_15), sp1010_15)
print('10 C', np.nanmean(sp1010_10), np.nanstd(sp1010_10), sp1010_10)
print('5 C', np.nanmean(sp1010_5), np.nanstd(sp1010_5), sp1010_5)

fig, axs = plt.subplots(2, 2, sharey=True, tight_layout=True)
axs[0, 0].hist(sp1010_20)
axs[0, 0].set_title('SP 1.0%-1.0B 20hPa')
axs[0, 1].hist(sp1010_15)
axs[0, 1].set_title('SP 1.0%-1.0B 15hPa')
axs[1, 0].hist(sp1010_10)
axs[1, 0].set_title('SP 1.0%-1.0B 10hPa')
axs[1, 1].hist(sp1010_5)
axs[1, 1].set_title('SP 1.0%-1.0B 5hPa')

# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/Hist2017_SP1010_bysim.png')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/Hist2017_SP1010_bysim.pdf')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/Hist2017_SP1010_bysim.eps')

######################################################################################################




# #2017
# print('EN1001', 'EN1010', 'SP1001', 'SP1010')
## mass difference
# print('EN0505', 'EN1010', 'SP0505', 'SP1010')
# print(len(profEN0505_nodup), len(profEN1010_nodup), len(profSP0505_nodup), len(profSP1010_nodup))
# print('mean Diff', np.nanmean(profEN0505_nodup['Diff']), np.nanmean(profEN1010_nodup['Diff']), np.nanmean(profSP0505_nodup['Diff']), np.nanmean(profSP1010_nodup['Diff']), )
# print('std Diff', np.nanstd(profEN0505_nodup['Diff']), np.nanstd(profEN1010_nodup['Diff']), np.nanstd(profSP0505_nodup['Diff']), np.nanstd(profSP1010_nodup['Diff']), )
# print('median Diff', np.median(profEN0505_nodup['Diff']), np.median(profEN1010_nodup['Diff']), np.median(profSP0505_nodup['Diff']), np.median(profSP1010_nodup['Diff']), )
# #
#


# # print('EN0505', 'EN1010', 'SP0505', 'SP1010')
# #2017
# print('EN1001', 'EN1010', 'SP1001', 'SP1010')

# print(profEN0505_nodup[['Sim', 'Team', 'iB0']])
# print(profEN1010_nodup[['Sim', 'Team', 'iB0']])
# print(profSP0505_nodup[['Sim', 'Team', 'iB0']])
# print(profSP1010_nodup[['Sim', 'Team', 'iB0']])
#
#
#
# #
# print(len(profEN0505_nodup), len(profEN1010_nodup), len(profSP0505_nodup), len(profSP1010_nodup))
# print('mean iB0', np.nanmean(profEN0505_nodup['iB0']), np.nanmean(profEN1010_nodup['iB0']), np.nanmean(profSP0505_nodup['iB0']), np.nanmean(profSP1010_nodup['iB0']), )
# print('std iB0', np.nanstd(profEN0505_nodup['iB0']), np.nanstd(profEN1010_nodup['iB0']), np.nanstd(profSP0505_nodup['iB0']), np.nanstd(profSP1010_nodup['iB0']), )
# print('median iB0', np.median(profEN0505_nodup['iB0']), np.median(profEN1010_nodup['iB0']), np.median(profSP0505_nodup['iB0']), np.median(profSP1010_nodup['iB0']), )
#
# print('mean iB1', np.nanmean(profEN0505_nodup['iB1']), np.nanmean(profEN1010_nodup['iB1']), np.nanmean(profSP0505_nodup['iB1']), np.nanmean(profSP1010_nodup['iB1']), )
# print('std iB1', np.nanstd(profEN0505_nodup['iB1']), np.nanstd(profEN1010_nodup['iB1']), np.nanstd(profSP0505_nodup['iB1']), np.nanstd(profSP1010_nodup['iB1']), )
# print('median iB1', np.median(profEN0505_nodup['iB1']), np.median(profEN1010_nodup['iB1']), np.median(profSP0505_nodup['iB1']), np.median(profSP1010_nodup['iB1']), )
#
# print('mean iB2', np.nanmean(profEN0505_nodup['iB2']), np.nanmean(profEN1010_nodup['iB2']), np.nanmean(profSP0505_nodup['iB2']), np.nanmean(profSP1010_nodup['iB2']), )
# print('std iB2', np.nanstd(profEN0505_nodup['iB2']), np.nanstd(profEN1010_nodup['iB2']), np.nanstd(profSP0505_nodup['iB2']), np.nanstd(profSP1010_nodup['iB2']), )
#
# print('median iB2', np.median(profEN0505_nodup['iB2']), np.median(profEN1010_nodup['iB2']), np.median(profSP0505_nodup['iB2']), np.median(profSP1010_nodup['iB2']), )
#
# print('mean std median iB0 all', np.nanmean(df_nodup['iB0']),  np.nanstd(df_nodup['iB0']),  np.median(df_nodup['iB0'])  )
#
#
# ## temperature:
#
# df['TPintC'] = df['TPint'] - 273
#
# # filter_20 = (df.Pair <= 20) & (df.Pair > 15)
# # filter_15 = (df.Pair <= 15) & (df.Pair > 10)
# # filter_10 = (df.Pair <= 10) & (df.Pair > 5)
#
# filter_20 = (df.Pair <= 20) & (df.Pair > 19)
# filter_15 = (df.Pair <= 15) & (df.Pair > 14)
# filter_10 = (df.Pair <= 10) & (df.Pair > 9)
# filter_5 = (df.Pair <= 9) & (df.Pair > 6)
#
#
#
# # filterSP0505_20 = (filtSP & filtS05 & filtB05  & filter_20)
# # filterSP0505_15 = (filtSP & filtS05 & filtB05  & filter_15)
# # filterSP0505_10 = (filtSP & filtS05 & filtB05  & filter_10)
# # filterSP0505_5 = (filtSP & filtS05 & filtB05 & filter_5)
#
# filterSP0505_20 = (filtSP & filtS10 & filtB01  & filter_20)
# filterSP0505_15 = (filtSP & filtS10 & filtB01  & filter_15)
# filterSP0505_10 = (filtSP & filtS10 & filtB01  & filter_10)
# filterSP0505_5 = (filtSP & filtS10 & filtB01 & filter_5)
#
#
# filterSP1010_20 = (filtSP & filtS10 & filtB10 & filter_20)
# filterSP1010_15 = (filtSP & filtS10 & filtB10 & filter_15)
# filterSP1010_10 = (filtSP & filtS10 & filtB10 & filter_10)
# filterSP1010_5 = (filtSP & filtS10 & filtB10 & filter_5)
#
#
# filterEN0505_20 = (filtEN & filtS05 & filtB05  & filter_20)
# filterEN0505_15 = (filtEN & filtS05 & filtB05  & filter_15)
# filterEN0505_10 = (filtEN & filtS05 & filtB05  & filter_10)
# filterEN0505_5 = (filtEN & filtS05 & filtB05  & filter_5)
#
# #
# # filterEN1010_20 = (filtEN & filtS10 & filtB10 & filter_20)
# # filterEN1010_15 = (filtEN & filtS10 & filtB10 & filter_15)
# # filterEN1010_10 = (filtEN & filtS10 & filtB10 & filter_10)
# # filterEN1010_5 = (filtEN & filtS10 & filtB10 & filter_5)
#
#
# filterEN1010_20 = (filtEN & filtS10 & filtB01 & filter_20)
# filterEN1010_15 = (filtEN & filtS10 & filtB01 & filter_15)
# filterEN1010_10 = (filtEN & filtS10 & filtB01 & filter_10)
# filterEN1010_5 = (filtEN & filtS10 & filtB01 & filter_5)
#
#
# print('EN0505', 'EN1010', 'SP0505', 'SP1010')
# #
# print('20 mean', np.nanmean(df.loc[filterEN0505_20]['TPintC']), np.nanmean(df.loc[filterEN1010_20]['TPintC']), np.nanmean(df.loc[filterSP0505_20]['TPintC']), np.nanmean(df.loc[filterSP1010_20]['TPintC']), )
# print('20 std', np.nanstd(df.loc[filterEN0505_20]['TPintC']), np.nanstd(df.loc[filterEN1010_20]['TPintC']), np.nanstd(df.loc[filterSP0505_20]['TPintC']), np.nanstd(df.loc[filterSP1010_20]['TPintC']), )
# print('20 median', np.median(df.loc[filterEN0505_20]['TPintC']), np.median(df.loc[filterEN1010_20]['TPintC']), np.median(df.loc[filterSP0505_20]['TPintC']), np.median(df.loc[filterSP1010_20]['TPintC']), )
#
# print('15 mean', np.nanmean(df.loc[filterEN0505_15]['TPintC']), np.nanmean(df.loc[filterEN1010_15]['TPintC']), np.nanmean(df.loc[filterSP0505_15]['TPintC']), np.nanmean(df.loc[filterSP1010_15]['TPintC']), )
# print('15 std', np.nanstd(df.loc[filterEN0505_15]['TPintC']), np.nanstd(df.loc[filterEN1010_15]['TPintC']), np.nanstd(df.loc[filterSP0505_15]['TPintC']), np.nanstd(df.loc[filterSP1010_15]['TPintC']), )
# print('15 median', np.median(df.loc[filterEN0505_15]['TPintC']), np.median(df.loc[filterEN1010_15]['TPintC']), np.median(df.loc[filterSP0505_15]['TPintC']), np.median(df.loc[filterSP1010_15]['TPintC']), )
#
# print('10 mean', np.nanmean(df.loc[filterEN0505_10]['TPintC']), np.nanmean(df.loc[filterEN1010_10]['TPintC']), np.nanmean(df.loc[filterSP0505_10]['TPintC']), np.nanmean(df.loc[filterSP1010_10]['TPintC']), )
# print('10 std', np.nanstd(df.loc[filterEN0505_10]['TPintC']), np.nanstd(df.loc[filterEN1010_10]['TPintC']), np.nanstd(df.loc[filterSP0505_10]['TPintC']), np.nanstd(df.loc[filterSP1010_10]['TPintC']), )
# print('10 median', np.median(df.loc[filterEN0505_10]['TPintC']), np.median(df.loc[filterEN1010_10]['TPintC']), np.median(df.loc[filterSP0505_10]['TPintC']), np.median(df.loc[filterSP1010_10]['TPintC']), )
#
# print('5 mean', np.nanmean(df.loc[filterEN0505_5]['TPintC']), np.nanmean(df.loc[filterEN1010_5]['TPintC']), np.nanmean(df.loc[filterSP0505_5]['TPintC']), np.nanmean(df.loc[filterSP1010_5]['TPintC']), )
# print('5 std', np.nanstd(df.loc[filterEN0505_5]['TPintC']), np.nanstd(df.loc[filterEN1010_5]['TPintC']), np.nanstd(df.loc[filterSP0505_5]['TPintC']), np.nanstd(df.loc[filterSP1010_5]['TPintC']), )
# print('5 median', np.median(df.loc[filterEN0505_5]['TPintC']), np.median(df.loc[filterEN1010_5]['TPintC']), np.median(df.loc[filterSP0505_5]['TPintC']), np.median(df.loc[filterSP1010_5]['TPintC']), )
#
#
#
# fig, axs = plt.subplots(2, 2, sharey=True, tight_layout=True)
# axs[0,0].hist(df.loc[filterEN0505_20]['TPintC'])
# axs[0,0].set_title('EN 0.5%-0.5B 20hPa')
# axs[0,1].hist(df.loc[filterEN0505_15]['TPintC'])
# axs[0,1].set_title('EN 0.5%-0.5B 15hPa')
# axs[1,0].hist(df.loc[filterEN0505_10]['TPintC'])
# axs[1,0].set_title('EN 0.5%-0.5B 10hPa')
# axs[1,1].hist(df.loc[filterEN0505_5]['TPintC'])
# axs[1,1].set_title('EN 0.5%-0.5B 5hPa')
#
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/Hist2017_EN0505.png')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/Hist2017_EN0505.pdf')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/Hist2017_EN0505.eps')
#
# plt.show()
#
#
# fig, axs1 = plt.subplots(2, 2, sharey=True, tight_layout=True)
# axs1[0,0].hist(df.loc[filterEN1010_20]['TPintC'])
# axs1[0,0].set_title('EN 1.0%-0.1B 20hPa')
# axs1[0,1].hist(df.loc[filterEN1010_15]['TPintC'])
# axs1[0,1].set_title('EN 1.0%-0.1B 15hPa')
# axs1[1,0].hist(df.loc[filterEN1010_10]['TPintC'])
# axs1[1,0].set_title('EN 1.0%-0.1B 10hPa')
# axs1[1,1].hist(df.loc[filterEN1010_5]['TPintC'])
# axs1[1,1].set_title('EN 1.0%-0.1B 5hPa')
#
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/Hist2017_EN1001.png')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/Hist2017_EN1001.pdf')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/Hist2017_EN1001.eps')
#
#
# fig, axs2 = plt.subplots(2, 2, sharey=True, tight_layout=True)
# axs2[0,0].hist(df.loc[filterSP0505_20]['TPintC'])
# axs2[0,0].set_title('SP 1.0%-0.1B 20hPa')
# axs2[0,1].hist(df.loc[filterSP0505_15]['TPintC'])
# axs2[0,1].set_title('SP 1.0%-0.1B 15hPa')
# axs2[1,0].hist(df.loc[filterSP0505_10]['TPintC'])
# axs2[1,0].set_title('SP 1.0%-0.1B 10hPa')
# axs2[1,1].hist(df.loc[filterSP0505_5]['TPintC'])
# axs2[1,1].set_title('SP 1.0%-0.1B 5hPa')
#
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/Hist2017_SP1001.png')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/Hist2017_SP1001.pdf')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/Hist2017_SP1001.eps')
#
#
# fig, axs2 = plt.subplots(2, 2, sharey=True, tight_layout=True)
# axs2[0,0].hist(df.loc[filterSP1010_20]['TPintC'])
# axs2[0,0].set_title('SP 1.0%-1.0B 20hPa')
# axs2[0,1].hist(df.loc[filterSP1010_15]['TPintC'])
# axs2[0,1].set_title('SP 1.0%-1.0B 15hPa')
# axs2[1,0].hist(df.loc[filterSP1010_10]['TPintC'])
# axs2[1,0].set_title('SP 1.0%-1.0B 10hPa')
# axs2[1,1].hist(df.loc[filterSP1010_5]['TPintC'])
# axs2[1,1].set_title('SP 1.0%-1.0B 5hPa')
#
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/Hist2017_SP1010.png')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/Hist2017_SP1010.pdf')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/Hist2017_SP1010.eps')
#
# # ax2.set_ylabel(r'TSim')
# # ax2.set_xlabel('Temp C')
#
# plt.show()
# #
# # fig = plt.figure()
# # plt.ylabel('I ECC/ 0.10 * I OPM(cor. JMA) conv. slow')
# # plt.title('0910 data')
# # ax2 = fig.add_subplot(1, 1, 1)
# #
# # groups2 = ( "Tsim 4100-4400", "Tsim 6100-6400", 'Tsim 8100-8400')
# # # ax2.scatter(x1, r1, alpha=0.8, c=colors[0], marker="o", label=groups[0])
# #
# # r_en0505_R2_4 = r_en0505_R2_4[~np.isnan(r_en0505_R2_4)]
# # r_en1010_R2_4 = r_en1010_R2_4[~np.isnan(r_en1010_R2_4)]
# # r_sp0505_R2_4 = r_sp0505_R2_4[~np.isnan(r_sp0505_R2_4)]
# # r_sp1010_R2_4 = r_sp1010_R2_4[~np.isnan(r_sp1010_R2_4)]
# # data_to_plot = [r_en0505_R2_4, r_en1010_R2_4, r_sp0505_R2_4, r_sp1010_R2_4]
# # ax2.boxplot(data_to_plot, positions=[0,1,2,3])
# # ax2.set_xticks(np.arange(len(xlabels)))
# # ax2.set_xticklabels(xlabels)
#
#
# nullfmt = NullFormatter()         # no labels
#
# # definitions for the axes
# left, width = 0.1, 0.65
# bottom, height = 0.1, 0.65
# bottom_h = left_h = left + width + 0.02
#
# rect_scatter = [left, bottom, width, height]
# rect_histx = [left, bottom_h, width, 0.2]
# rect_histy = [left_h, bottom, 0.2, height]
