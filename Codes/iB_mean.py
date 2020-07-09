import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import NullFormatter




df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_deconv_tempfixed.csv", low_memory=False)
# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv_ml.csv", low_memory=False)

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
df = df.drop(df[(df.iB0 < -1) ].index)
df = df.drop(df[(df.iB1 < -1) ].index)
df = df.drop(df[(df.iB2 < -1) ].index)

df = df.drop(df[(df.iB0 > 1) ].index)
df = df.drop(df[(df.iB1 > 1) ].index)
df = df.drop(df[(df.iB2 > 1) ].index)



# print('0910', list(df))
#
# # beta0 cuts
df = df.drop(df[(df.Sim == 147) & (df.Team == 3)].index)
df = df.drop(df[(df.Sim == 158) & (df.Team == 1)].index)
df = df.drop(df[(df.Sim == 158) & (df.Team == 2)].index)
df = df.drop(df[(df.Sim == 160) & (df.Team == 4)].index)
df = df.drop(df[(df.Sim == 165) & (df.Team == 4)].index)
# #
df = df.drop(df[(df.PO3 < 0)].index)
df = df.drop(df[(df.PO3_OPM < 0)].index)

# df = df.drop(df[(df.PostTestSolution_Lost_gr < -1)].index)
## [175, 172, 175, 175, 175, 179]
## [1, 2, 3, 4, 2, 2]
df = df.drop(df[(df.Sim == 175) & (df.Team == 1)].index)
df = df.drop(df[(df.Sim == 172) & (df.Team == 2)].index)
df = df.drop(df[(df.Sim == 175) & (df.Team == 3)].index)
df = df.drop(df[(df.Sim == 175) & (df.Team == 4)].index)
df = df.drop(df[(df.Sim == 175) & (df.Team == 2)].index)
df = df.drop(df[(df.Sim == 179) & (df.Team == 2)].index)


#
# df = df[df.ADX == 0]



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




# #2017
# print('EN1001', 'EN1010', 'SP1001', 'SP1010')
## mass difference
# print('EN0505', 'EN1010', 'SP0505', 'SP1010')
# print(len(profEN0505_nodup), len(profEN1010_nodup), len(profSP0505_nodup), len(profSP1010_nodup))
# print('mean PostTestSolution_Lost_gr', np.mean(profEN0505_nodup['PostTestSolution_Lost_gr']), np.mean(profEN1010_nodup['PostTestSolution_Lost_gr']), np.mean(profSP0505_nodup['PostTestSolution_Lost_gr']), np.mean(profSP1010_nodup['PostTestSolution_Lost_gr']), )
# print('std PostTestSolution_Lost_gr', np.std(profEN0505_nodup['PostTestSolution_Lost_gr']), np.std(profEN1010_nodup['PostTestSolution_Lost_gr']), np.std(profSP0505_nodup['PostTestSolution_Lost_gr']), np.std(profSP1010_nodup['PostTestSolution_Lost_gr']), )
# print('median PostTestSolution_Lost_gr', np.median(profEN0505_nodup['PostTestSolution_Lost_gr']), np.median(profEN1010_nodup['PostTestSolution_Lost_gr']), np.median(profSP0505_nodup['PostTestSolution_Lost_gr']), np.median(profSP1010_nodup['PostTestSolution_Lost_gr']), )
# #
#

EN0505_totalmlc = np.trapz(profEN0505.massloss, x=profEN0505.Tsim)
print(EN0505_totalmlc)

print('EN0505', 'EN1010', 'SP0505', 'SP1010')
print(len(profEN0505_nodup), len(profEN1010_nodup), len(profSP0505_nodup), len(profSP1010_nodup))
print('mean PostTestSolution_Lost_gr', np.mean(profEN0505_nodup['Diff']), np.mean(profEN1010_nodup['Diff']), np.mean(profSP0505_nodup['Diff']), np.mean(profSP1010_nodup['Diff']), )
print('std Diff', np.std(profEN0505_nodup['Diff']), np.std(profEN1010_nodup['Diff']), np.std(profSP0505_nodup['Diff']), np.std(profSP1010_nodup['Diff']), )
print('median Diff', np.median(profEN0505_nodup['Diff']), np.median(profEN1010_nodup['Diff']), np.median(profSP0505_nodup['Diff']), np.median(profSP1010_nodup['Diff']), )
#



# # print('EN0505', 'EN1010', 'SP0505', 'SP1010')
# #2017
# print('EN1001', 'EN1010', 'SP1001', 'SP1010')
#
# print(profEN0505_nodup[['Sim', 'Team', 'iB0']])
# print(profEN1010_nodup[['Sim', 'Team', 'iB0']])
# print(profSP0505_nodup[['Sim', 'Team', 'iB0']])
# print(profSP1010_nodup[['Sim', 'Team', 'iB0']])



#
print(len(profEN0505_nodup), len(profEN1010_nodup), len(profSP0505_nodup), len(profSP1010_nodup))
print('mean iB0', np.mean(profEN0505_nodup['iB0']), np.mean(profEN1010_nodup['iB0']), np.mean(profSP0505_nodup['iB0']), np.mean(profSP1010_nodup['iB0']), )
print('std iB0', np.std(profEN0505_nodup['iB0']), np.std(profEN1010_nodup['iB0']), np.std(profSP0505_nodup['iB0']), np.std(profSP1010_nodup['iB0']), )
print('median iB0', np.median(profEN0505_nodup['iB0']), np.median(profEN1010_nodup['iB0']), np.median(profSP0505_nodup['iB0']), np.median(profSP1010_nodup['iB0']), )

print('mean iB1', np.mean(profEN0505_nodup['iB1']), np.mean(profEN1010_nodup['iB1']), np.mean(profSP0505_nodup['iB1']), np.mean(profSP1010_nodup['iB1']), )
print('std iB1', np.std(profEN0505_nodup['iB1']), np.std(profEN1010_nodup['iB1']), np.std(profSP0505_nodup['iB1']), np.std(profSP1010_nodup['iB1']), )
print('median iB1', np.median(profEN0505_nodup['iB1']), np.median(profEN1010_nodup['iB1']), np.median(profSP0505_nodup['iB1']), np.median(profSP1010_nodup['iB1']), )

print('mean iB2', np.mean(profEN0505_nodup['iB2']), np.mean(profEN1010_nodup['iB2']), np.mean(profSP0505_nodup['iB2']), np.mean(profSP1010_nodup['iB2']), )
print('std iB2', np.std(profEN0505_nodup['iB2']), np.std(profEN1010_nodup['iB2']), np.std(profSP0505_nodup['iB2']), np.std(profSP1010_nodup['iB2']), )

print('median iB2', np.median(profEN0505_nodup['iB2']), np.median(profEN1010_nodup['iB2']), np.median(profSP0505_nodup['iB2']), np.median(profSP1010_nodup['iB2']), )

print('mean std median iB0 all', np.mean(df_nodup['iB0']),  np.std(df_nodup['iB0']),  np.median(df_nodup['iB0'])  )


## temperature:

df['TPintC'] = df['TPint'] - 273

# filter_20 = (df.Pair <= 20) & (df.Pair > 15)
# filter_15 = (df.Pair <= 15) & (df.Pair > 10)
# filter_10 = (df.Pair <= 10) & (df.Pair > 5)

filter_20 = (df.Pair <= 20) & (df.Pair > 19)
filter_15 = (df.Pair <= 15) & (df.Pair > 14)
filter_10 = (df.Pair <= 10) & (df.Pair > 9)
filter_5 = (df.Pair <= 6) & (df.Pair >= 5)
# filter_5 = (df.Pair <= 9) & (df.Pair > 6)
filter_20_5 = (df.Pair <= 20) & (df.Pair > 5)



filterSP0505_20 = (filtSP & filtS05 & filtB05  & filter_20)
filterSP0505_15 = (filtSP & filtS05 & filtB05  & filter_15)
filterSP0505_10 = (filtSP & filtS05 & filtB05  & filter_10)
filterSP0505_5 = (filtSP & filtS05 & filtB05 & filter_5)

filterSP0505_20_5 = (filtSP & filtS05 & filtB05  & filter_20_5)

#
# filterSP0505_20 = (filtSP & filtS10 & filtB01  & filter_20)
# filterSP0505_15 = (filtSP & filtS10 & filtB01  & filter_15)
# filterSP0505_10 = (filtSP & filtS10 & filtB01  & filter_10)
# filterSP0505_5 = (filtSP & filtS10 & filtB01 & filter_5)
# filterSP0505_20_5 = (filtSP & filtS10 & filtB01 & filter_20_5)


filterSP1010_20 = (filtSP & filtS10 & filtB10 & filter_20)
filterSP1010_15 = (filtSP & filtS10 & filtB10 & filter_15)
filterSP1010_10 = (filtSP & filtS10 & filtB10 & filter_10)
filterSP1010_5 = (filtSP & filtS10 & filtB10 & filter_5)
filterSP1010_20_5 = (filtSP & filtS10 & filtB10 & filter_20_5)


filterEN0505_20 = (filtEN & filtS05 & filtB05  & filter_20)
filterEN0505_15 = (filtEN & filtS05 & filtB05  & filter_15)
filterEN0505_10 = (filtEN & filtS05 & filtB05  & filter_10)
filterEN0505_5 = (filtEN & filtS05 & filtB05  & filter_5)
filterEN0505_20_5 = (filtEN & filtS05 & filtB05  & filter_20_5)

#
filterEN1010_20 = (filtEN & filtS10 & filtB10 & filter_20)
filterEN1010_15 = (filtEN & filtS10 & filtB10 & filter_15)
filterEN1010_10 = (filtEN & filtS10 & filtB10 & filter_10)
filterEN1010_5 = (filtEN & filtS10 & filtB10 & filter_5)
filterEN1010_20_5 = (filtEN & filtS10 & filtB10 & filter_20_5)


#
# filterEN1010_20 = (filtEN & filtS10 & filtB01 & filter_20)
# filterEN1010_15 = (filtEN & filtS10 & filtB01 & filter_15)
# filterEN1010_10 = (filtEN & filtS10 & filtB01 & filter_10)
# filterEN1010_5 = (filtEN & filtS10 & filtB01 & filter_5)
# filterEN1010_20_5 = (filtEN & filtS10 & filtB01 & filter_20_5)


print('EN0505', 'EN1010', 'SP0505', 'SP1010')
#
print('20 mean', np.mean(df.loc[filterEN0505_20]['TPintC']), np.mean(df.loc[filterEN1010_20]['TPintC']), np.mean(df.loc[filterSP0505_20]['TPintC']), np.mean(df.loc[filterSP1010_20]['TPintC']), )
print('20 std', np.std(df.loc[filterEN0505_20]['TPintC']), np.std(df.loc[filterEN1010_20]['TPintC']), np.std(df.loc[filterSP0505_20]['TPintC']), np.std(df.loc[filterSP1010_20]['TPintC']), )
print('20 median', np.median(df.loc[filterEN0505_20]['TPintC']), np.median(df.loc[filterEN1010_20]['TPintC']), np.median(df.loc[filterSP0505_20]['TPintC']), np.median(df.loc[filterSP1010_20]['TPintC']), )

print('15 mean', np.mean(df.loc[filterEN0505_15]['TPintC']), np.mean(df.loc[filterEN1010_15]['TPintC']), np.mean(df.loc[filterSP0505_15]['TPintC']), np.mean(df.loc[filterSP1010_15]['TPintC']), )
print('15 std', np.std(df.loc[filterEN0505_15]['TPintC']), np.std(df.loc[filterEN1010_15]['TPintC']), np.std(df.loc[filterSP0505_15]['TPintC']), np.std(df.loc[filterSP1010_15]['TPintC']), )
print('15 median', np.median(df.loc[filterEN0505_15]['TPintC']), np.median(df.loc[filterEN1010_15]['TPintC']), np.median(df.loc[filterSP0505_15]['TPintC']), np.median(df.loc[filterSP1010_15]['TPintC']), )

print('10 mean', np.mean(df.loc[filterEN0505_10]['TPintC']), np.mean(df.loc[filterEN1010_10]['TPintC']), np.mean(df.loc[filterSP0505_10]['TPintC']), np.mean(df.loc[filterSP1010_10]['TPintC']), )
print('10 std', np.std(df.loc[filterEN0505_10]['TPintC']), np.std(df.loc[filterEN1010_10]['TPintC']), np.std(df.loc[filterSP0505_10]['TPintC']), np.std(df.loc[filterSP1010_10]['TPintC']), )
print('10 median', np.median(df.loc[filterEN0505_10]['TPintC']), np.median(df.loc[filterEN1010_10]['TPintC']), np.median(df.loc[filterSP0505_10]['TPintC']), np.median(df.loc[filterSP1010_10]['TPintC']), )

print('5 mean', np.mean(df.loc[filterEN0505_5]['TPintC']), np.mean(df.loc[filterEN1010_5]['TPintC']), np.mean(df.loc[filterSP0505_5]['TPintC']), np.mean(df.loc[filterSP1010_5]['TPintC']), )
print('5 std', np.std(df.loc[filterEN0505_5]['TPintC']), np.std(df.loc[filterEN1010_5]['TPintC']), np.std(df.loc[filterSP0505_5]['TPintC']), np.std(df.loc[filterSP1010_5]['TPintC']), )
print('5 median', np.median(df.loc[filterEN0505_5]['TPintC']), np.median(df.loc[filterEN1010_5]['TPintC']), np.median(df.loc[filterSP0505_5]['TPintC']), np.median(df.loc[filterSP1010_5]['TPintC']), )


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
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/Hist2017_EN0505.png')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/Hist2017_EN0505.pdf')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/Hist2017_EN0505.eps')
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
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/Hist2017_EN1001.png')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/Hist2017_EN1001.pdf')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/Hist2017_EN1001.eps')
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
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/Hist2017_SP1001.png')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/Hist2017_SP1001.pdf')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/Hist2017_SP1001.eps')
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
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/Hist2017_SP1010.png')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/Hist2017_SP1010.pdf')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/Hist2017_SP1010.eps')
#
# # ax2.set_ylabel(r'TSim')
# # ax2.set_xlabel('Temp C')
#
# plt.show()
#
# fig = plt.figure()
# plt.ylabel('I ECC/ 0.10 * I OPM(cor. JMA) conv. slow')
# plt.title('0910 data')
# ax2 = fig.add_subplot(1, 1, 1)
#
# groups2 = ( "Tsim 4100-4400", "Tsim 6100-6400", 'Tsim 8100-8400')
# # ax2.scatter(x1, r1, alpha=0.8, c=colors[0], marker="o", label=groups[0])
#
# r_en0505_R2_4 = r_en0505_R2_4[~np.isnan(r_en0505_R2_4)]
# r_en1010_R2_4 = r_en1010_R2_4[~np.isnan(r_en1010_R2_4)]
# r_sp0505_R2_4 = r_sp0505_R2_4[~np.isnan(r_sp0505_R2_4)]
# r_sp1010_R2_4 = r_sp1010_R2_4[~np.isnan(r_sp1010_R2_4)]
# data_to_plot = [r_en0505_R2_4, r_en1010_R2_4, r_sp0505_R2_4, r_sp1010_R2_4]
# ax2.boxplot(data_to_plot, positions=[0,1,2,3])
# ax2.set_xticks(np.arange(len(xlabels)))
# ax2.set_xticklabels(xlabels)

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
#
# plt.figure(1, figsize=(8, 8))
#
# axScatter = plt.axes(rect_scatter)
# axHistx = plt.axes(rect_histx)
# axHisty = plt.axes(rect_histy)
#
# axScatter.scatter(df.loc[filterSP1010_20_5]['TPintC'], df.loc[filterSP1010_20_5]['massloss'] )

plt.hist(df.loc[filterSP1010_20_5]['massloss'])


plt.show()
