import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Beta_Functions import ratiofunction_beta, ratiofunction_beta_9602



#######################################################################################################################

# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_Data_nocut.csv", low_memory=False)
df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie9602_Data.csv", low_memory=False)

# df = df.drop(df[(df.Sim == 140)].index)
# df = df.drop(df[(df.Sim == 147)].index)

# df = df.drop(df[(df.PO3 < 0)].index)
# df = df.drop(df[(df.PO3_OPM < 0)].index)
# # df = df[df.ADX == 0]


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

# ## for 0910
# rmean_en0505, rstd_en0505, rmedian_en0505, rqerr_en0505 = ratiofunction_beta(df, sim_en0505, team_en0505, 'EN0505')
# rmean_en1010, rstd_en1010, rmedian_en1010, rqerr_en1010 = ratiofunction_beta(df, sim_en1010, team_en1010, 'EN1010')
# rmean_sp0505, rstd_sp0505, rmedian_sp0505, rqerr_sp0505 = ratiofunction_beta(df, sim_sp0505, team_sp0505, 'SP0505')
# rmean_sp1010, rstd_sp1010, rmedian_sp1010, rqerr_sp1010 = ratiofunction_beta(df, sim_sp1010, team_sp1010, 'SP1010')

## for 9602
rmean_en0505, rstd_en0505,  rmedian_en0505, rqerr_en0505 = ratiofunction_beta_9602(df, sim_en0505, team_en0505, 'EN0505')
rmean_en1010, rstd_en1010, rmedian_en1010, rqerr_en1010 = ratiofunction_beta_9602(df, sim_en1010, team_en1010, 'EN1010')
rmean_sp0505, rstd_sp0505, rmedian_sp0505, rqerr_sp0505 = ratiofunction_beta_9602(df, sim_sp0505, team_sp0505, 'SP0505')
rmean_sp1010, rstd_sp1010, rmedian_sp1010, rqerr_sp1010 = ratiofunction_beta_9602(df, sim_sp1010, team_sp1010, 'SP1010')


# print('rmean_en0505', rmean_en0505)
# print('rstd_en0505', rstd_en0505)
# print('rmedian_en0505', rmedian_en0505)
# print('rqerr_en0505', rqerr_en0505)

# plotting

# x1 = [0] * len(rmean_en0505[0])
# x1_1 = [1] * len(rmean_en1010[0])
# x1_2 = [2] * len(rmean_sp0505[0])
# x1_3 = [3] * len(rmean_sp1010[0])
#
# xlabels = ['EN 0.5%-0.5B', 'EN 1.0%-1.0B', 'SP 0.5%-0.5B', 'SP 1.0%-1.0B']
#
# x1.extend(x1_1)
# x1.extend(x1_2)
# x1.extend(x1_3)


# # plotting 9602
r1_mean = np.concatenate((rmean_en0505[0], rmean_en1010[0], rmean_sp0505[0], rmean_sp1010[0]), axis=None)
r2_mean = np.concatenate((rmean_en0505[1], rmean_en1010[1], rmean_sp0505[1], rmean_sp1010[1]), axis=None)

r1_median = np.concatenate((rmedian_en0505[0], rmedian_en1010[0], rmedian_sp0505[0], rmedian_sp1010[0]), axis=None)
r2_median = np.concatenate((rmedian_en0505[1], rmedian_en1010[1], rmedian_sp0505[1], rmedian_sp1010[1]), axis=None)

r_en0505_R2_4 = np.concatenate((rmean_en0505[0], rmean_en0505[1]), axis=None)
r_en1010_R2_4 = np.concatenate((rmean_en1010[0], rmean_en1010[1]), axis=None)
r_sp0505_R2_4 = np.concatenate((rmean_sp0505[0], rmean_sp0505[1]), axis=None)
r_sp1010_R2_4 = np.concatenate((rmean_sp1010[0], rmean_sp1010[1]), axis=None)

r_en0505_R2_4_median = np.concatenate((rmedian_en0505[0], rmedian_en0505[1]), axis=None)
r_en1010_R2_4_median = np.concatenate((rmedian_en1010[0], rmedian_en1010[1]), axis=None)
r_sp0505_R2_4_median = np.concatenate((rmedian_sp0505[0], rmedian_sp0505[1]), axis=None)
r_sp1010_R2_4_median = np.concatenate((rmedian_sp1010[0], rmedian_sp1010[1]), axis=None)

# print('r_en0505_R2_4', r_en0505_R2_4)
# print('median',      r_en0505_R2_4_median)
#
#
# colors = ("dodgerblue",  "red", 'green')
# groups = ("Tsim R1", "Tsim R2")
#
# # # Create plot
# # fig, ax = plt.subplots()
# #
# # #
# # ax.scatter(x1, r1_mean, alpha=0.8, c=colors[0], marker="o", label=groups[0])
# # ax.scatter(x1, r2_mean, alpha=0.8, c=colors[1], marker='v', edgecolors='none', label=groups[1])
# # # ax.scatter(x1, r3_mean, alpha=0.8, c=colors[2], marker="<", edgecolors='none', label=groups[2])
# # # ax.scatter(x1, r4_mean, alpha=0.8, c=colors[3], marker=">", edgecolors='none', label=groups[3])
# # # data_to_plot = [r_en0505_R2_4, r_en1010_R2_4, r_sp0505_R2_4, r_sp1010_R2_4]
# # r_en0505_R2_4 = r_en0505_R2_4[~np.isnan(r_en0505_R2_4)]
# # r_en1010_R2_4 = r_en1010_R2_4[~np.isnan(r_en1010_R2_4)]
# # r_sp0505_R2_4 = r_sp0505_R2_4[~np.isnan(r_sp0505_R2_4)]
# # r_sp1010_R2_4 = r_sp1010_R2_4[~np.isnan(r_sp1010_R2_4)]
# #
# # data_to_plot = [r_en0505_R2_4, r_en1010_R2_4, r_sp0505_R2_4, r_sp1010_R2_4]
# # ax.boxplot(data_to_plot,   positions=[0,1,2,3])
# # plt.ylabel('I ECC/ 0.10 * I OPM(cor. JMA) conv. slow')
# # plt.title('1996-2002 data')
# # plt.ylim(0, 2)
# # ax.set_xticks(np.arange(len(xlabels)))
# # ax.set_xticklabels(xlabels)
# #
# # # plt.title('Matplot scatter plot')
# # plt.legend(loc='upper right')
# # plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Ratio_Conv/RatioPlot_9602.png')
# # plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Ratio_Conv/RatioPlot_9602.eps')
# # plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Ratio_Conv/RatioPlot_9602.pdf')
# #
# # plt.show()
#
# print('r_en0505_R2_4, r_en1010_R2_4, r_sp0505_R2_4, r_sp1010_R2_4')
# print('mean', np.nanmean(r_en0505_R2_4), np.nanmean(r_en1010_R2_4), np.nanmean(r_sp0505_R2_4), np.nanmean(r_sp1010_R2_4))
# print('median', np.nanmedian(r_en0505_R2_4), np.nanmedian(r_en1010_R2_4), np.nanmedian(r_sp0505_R2_4), np.nanmedian(r_sp1010_R2_4))

## 96 02 data
#### median 0.6754185008005833 0.6564234362859472 0.4461621624277383 0.675864792982012
## 0910 data
## median 0.23211791775753718 0.5326908763844327 0.20759831872428983 0.5276937040805872

## all data
## 0.311820951952146 0.6209623264594483 0.24907889408991635 0.6241351914335151


# ## plotting 0910
# r1_mean = np.concatenate((rmean_en0505[0], rmean_en1010[0], rmean_sp0505[0], rmean_sp1010[0]), axis=None)
# r2_mean = np.concatenate((rmean_en0505[1], rmean_en1010[1], rmean_sp0505[1], rmean_sp1010[1]), axis=None)
# r3_mean = np.concatenate((rmean_en0505[2], rmean_en1010[2], rmean_sp0505[2], rmean_sp1010[2]), axis=None)
# r4_mean = np.concatenate((rmean_en0505[3], rmean_en1010[3], rmean_sp0505[3], rmean_sp1010[3]), axis=None)
#
# r1_median = np.concatenate((rmedian_en0505[0], rmedian_en1010[0], rmedian_sp0505[0], rmedian_sp1010[0]), axis=None)
# r2_median = np.concatenate((rmedian_en0505[1], rmedian_en1010[1], rmedian_sp0505[1], rmedian_sp1010[1]), axis=None)
# r3_median = np.concatenate((rmedian_en0505[2], rmedian_en1010[2], rmedian_sp0505[2], rmedian_sp1010[2]), axis=None)
# r4_median = np.concatenate((rmedian_en0505[3], rmedian_en1010[3], rmedian_sp0505[3], rmedian_sp1010[3]), axis=None)
#
# r_en0505_R1_4 = np.concatenate((rmean_en0505[0], rmean_en0505[1], rmean_en0505[2], rmean_en0505[3]), axis=None)
# r_en1010_R1_4 = np.concatenate((rmean_en1010[0], rmean_en1010[1], rmean_en1010[2], rmean_en1010[3]), axis=None)
# r_sp0505_R1_4 = np.concatenate((rmean_sp0505[0], rmean_sp0505[1], rmean_sp0505[2], rmean_sp0505[3]), axis=None)
# r_sp1010_R1_4 = np.concatenate((rmean_sp1010[0], rmean_sp1010[1], rmean_sp1010[3], rmean_sp1010[3]), axis=None)
#
# r_en0505_R2_4 = np.concatenate((rmean_en0505[1], rmean_en0505[2], rmean_en0505[3]), axis=None)
# r_en1010_R2_4 = np.concatenate((rmean_en1010[1], rmean_en1010[2], rmean_en1010[3]), axis=None)
# r_sp0505_R2_4 = np.concatenate((rmean_sp0505[1], rmean_sp0505[2], rmean_sp0505[3]), axis=None)
# r_sp1010_R2_4 = np.concatenate((rmean_sp1010[1], rmean_sp1010[2], rmean_sp1010[3]), axis=None)
#
# r_en0505_R2_4_median = np.concatenate((rmedian_en0505[1], rmedian_en0505[2], rmedian_en0505[3]), axis=None)
# r_en1010_R2_4_median = np.concatenate((rmedian_en1010[1], rmedian_en1010[2], rmedian_en1010[3]), axis=None)
# r_sp0505_R2_4_median = np.concatenate((rmedian_sp0505[1], rmedian_sp0505[2], rmedian_sp0505[3]), axis=None)
# r_sp1010_R2_4_median = np.concatenate((rmedian_sp1010[1], rmedian_sp1010[2], rmedian_sp1010[3]), axis=None)


# colors = ("dodgerblue", "blue", "red", 'green')
# groups = ("Tsim 2100-2400", "Tsim 4100-4400", "Tsim 6100-6400", 'Tsim 8100-8400')
#
# # Create plot
# fig = plt.figure()
# ax = fig.add_subplot(1, 1, 1)
#
# ax.scatter(x1, r1_mean, alpha=0.8, c=colors[0], marker="o", label=groups[0])
# ax.scatter(x1, r2_mean, alpha=0.8, c=colors[1], marker='v', edgecolors='none', label=groups[1])
# ax.scatter(x1, r3_mean, alpha=0.8, c=colors[2], marker="<", edgecolors='none', label=groups[2])
# ax.scatter(x1, r4_mean, alpha=0.8, c=colors[3], marker=">", edgecolors='none', label=groups[3])
# data_to_plot = [r_en0505_R1_4, r_en1010_R1_4, r_sp0505_R1_4, r_sp1010_R1_4]
# ax.boxplot(data_to_plot, positions=[0,1,2,3])
#
# x0 = [0]
# x11 = [1]
# x2 = [2]
# x3 = [3]
#
#
# plt.ylabel('I ECC/ 0.10 * I OPM(cor. JMA) conv. slow')
# plt.title('0910 data')
# plt.ylim(0, 1)
# ax.set_xticks(np.arange(len(xlabels)))
# ax.set_xticklabels(xlabels)
#
# # plt.title('Matplot scatter plot')
# plt.legend(loc='best')
# plt.show()

# fig = plt.figure()
# ax2 = fig.add_subplot(1, 1, 1)
# groups2 = ( "Tsim 4100-4400", "Tsim 6100-6400", 'Tsim 8100-8400')
# # ax2.scatter(x1, r1, alpha=0.8, c=colors[0], marker="o", label=groups[0])
# ax2.scatter(x1, r2_mean, alpha=0.8, c=colors[1], marker='v', edgecolors='none', label=groups[1])
# ax2.scatter(x1, r3_mean, alpha=0.8, c=colors[2], marker="<", edgecolors='none', label=groups[2])
# ax2.scatter(x1, r4_mean, alpha=0.8, c=colors[3], marker=">", edgecolors='none', label=groups[3])
# r_en0505_R2_4 = r_en0505_R2_4[~np.isnan(r_en0505_R2_4)]
# r_en1010_R2_4 = r_en1010_R2_4[~np.isnan(r_en1010_R2_4)]
# r_sp0505_R2_4 = r_sp0505_R2_4[~np.isnan(r_sp0505_R2_4)]
# r_sp1010_R2_4 = r_sp1010_R2_4[~np.isnan(r_sp1010_R2_4)]
# data_to_plot = [r_en0505_R2_4, r_en1010_R2_4, r_sp0505_R2_4, r_sp1010_R2_4]
# ax2.boxplot(data_to_plot, positions=[0,1,2,3])

# ax2.errorbar(x0, np.nanmean(r_en0505_R2_4), yerr=np.std(r_en0505_R2_4), color='gold', elinewidth=1, capsize=1, capthick=0.5,
#             marker='s', markersize=10, alpha=0.9, label='mean')
# ax2.errorbar(x11, np.nanmean(r_en1010_R2_4), yerr=np.std(r_en1010_R2_4), color='gold', elinewidth=1, capsize=1, capthick=0.5,
#             marker='s', markersize=10, alpha=0.9)
# ax2.errorbar(x2, np.nanmean(r_sp0505_R2_4), yerr=np.std(r_sp0505_R2_4), color='gold', elinewidth=1, capsize=1, capthick=0.5,
#             marker='s', markersize=10, alpha=0.9)
# ax2.errorbar(x3, np.nanmean(r_sp1010_R2_4), yerr=np.std(r_sp1010_R2_4), color='gold', elinewidth=1, capsize=1, capthick=0.5,
#             marker='s', markersize=10, alpha=0.9)



# print('median', np.nanmedian(r_en0505_R2_4), np.nanmedian(r_en1010_R2_4), np.nanmedian(r_sp0505_R2_4), np.nanmedian(r_sp1010_R2_4))

# filem = open('../Latex/0910_Beta_Medians_latex_table.txt', "w")
#
# filem.write('Median EN0505 (R2-R4)' + str(np.nanmedian(r_en0505_R2_4))  + '\n')
# filem.write('Median EN1010 (R2-R4)' + str(np.nanmedian(r_en1010_R2_4))  + '\n')
# filem.write('Median SP0505 (R2-R4)' + str(np.nanmedian(r_sp0505_R2_4))  + '\n')
# filem.write('Median SP1010 (R2-R4)' + str(np.nanmedian(r_sp1010_R2_4))  + '\n')
# filem.write('Now usuing medians rather than mean' + '\n')
# filem.write('Median EN0505 (R2-R4)' + str(np.nanmedian(r_en0505_R2_4_median))  + '\n')
# filem.write('Median EN1010 (R2-R4)' + str(np.nanmedian(r_en1010_R2_4_median))  + '\n')
# filem.write('Median SP0505 (R2-R4)' + str(np.nanmedian(r_sp0505_R2_4_median))  + '\n')
# filem.write('Median SP1010 (R2-R4)' + str(np.nanmedian(r_sp1010_R2_4_median))  + '\n')
# filem.close()
#
