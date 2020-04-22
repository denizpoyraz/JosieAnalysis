import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def ratiofunction_beta(df, sim, team, categorystr):
    r1 = [0] * len(sim);
    r2 = [0] * len(sim);
    r3 = [0] * len(sim);
    r4 = [0] * len(sim)

    r1mean = np.zeros(len(sim));
    r2mean = np.zeros(len(sim));
    r3mean = np.zeros(len(sim));
    r4mean = np.zeros(len(sim))
    r1std = np.zeros(len(sim));
    r2std = np.zeros(len(sim));
    r3std = np.zeros(len(sim));
    r4std = np.zeros(len(sim))
    r1median = np.zeros(len(sim));
    r2median = np.zeros(len(sim));
    r3median = np.zeros(len(sim));
    r4median = np.zeros(len(sim))
    qerr_r1 = np.zeros(len(sim))
    qerr_r2 = np.zeros(len(sim))
    qerr_r3 = np.zeros(len(sim))
    qerr_r4 = np.zeros(len(sim))

    df0 = {}
    df1 = {}
    df2 = {}
    df3 = {}
    df4 = {}

    for j in range(len(sim)):
        # print('simarray', sim[j])
        title = str(sim[j]) + '-' + str(team[j])

        r1_down = 2350;
        r1_up = 2400;
        r2_down = 4350;
        r2_up = 4400;
        r3_down = 6350;
        r3_up = 6400;
        r4_down = 8350;
        r4_up = 8400

        t1 = (df.Tsim >= r1_down) & (df.Tsim < r1_up)
        t2 = (df.Tsim >= r2_down) & (df.Tsim < r2_up)
        t3 = (df.Tsim >= r3_down) & (df.Tsim < r3_up)
        t4 = (df.Tsim >= r4_down) & (df.Tsim < r4_up)

        df1[j] = df[(df.Sim == sim[j]) & (df.Team == team[j]) & t1]
        df2[j] = df[(df.Sim == sim[j]) & (df.Team == team[j]) & t2]
        df3[j] = df[(df.Sim == sim[j]) & (df.Team == team[j]) & t3]
        df4[j] = df[(df.Sim == sim[j]) & (df.Team == team[j]) & t4]

        r1[j] = np.array((df1[j].IM / (0.10 * df1[j].I_conv_slow)).tolist())
        r2[j] = np.array((df2[j].IM / (0.10 * df2[j].I_conv_slow)).tolist())
        r3[j] = np.array((df3[j].IM / (0.10 * df3[j].I_conv_slow)).tolist())
        r4[j] = np.array((df4[j].IM / (0.10 * df4[j].I_conv_slow)).tolist())

        # print(j, np.nanmean(r1[j]))

        r1mean[j] = np.nanmean(r1[j])
        r1std[j] = np.nanstd(r1[j])
        r2mean[j] = np.nanmean(r2[j])
        r2std[j] = np.nanstd(r2[j])
        r3mean[j] = np.nanmean(r3[j])
        r3std[j] = np.nanstd(r3[j])
        r4mean[j] = np.nanmean(r4[j])
        r4std[j] = np.nanstd(r4[j])

        r1median[j] = np.nanmedian(r1[j])
        r2median[j] = np.nanmedian(r2[j])
        r3median[j] = np.nanmedian(r3[j])
        r4median[j] = np.nanmedian(r4[j])

        qerr_r1[j] = (np.nanquantile(r1[j], 0.75) - np.nanquantile(r1[j], 0.25)) / (2 * 0.6745)
        qerr_r2[j] = (np.nanquantile(r2[j], 0.75) - np.nanquantile(r2[j], 0.25)) / (2 * 0.6745)
        qerr_r3[j] = (np.nanquantile(r3[j], 0.75) - np.nanquantile(r3[j], 0.25)) / (2 * 0.6745)
        qerr_r4[j] = (np.nanquantile(r4[j], 0.75) - np.nanquantile(r4[j], 0.25)) / (2 * 0.6745)


    print('in the function')
    print('r1mean', r1mean)
    print('r1median', r1median)

    print('r2mean', r2mean)
    print('r3mean', r3mean)
    print('r4mean', r4mean)
    print('r4median', r4median)

    rmean = [r1mean, r2mean, r3mean, r4mean]
    rstd = [r1std, r2std, r3std, r4std]
    rmedian = [r1median, r2median, r3median, r4median]
    qerr = [qerr_r1, qerr_r2, qerr_r3, qerr_r4]

    return rmean, rstd, rmedian, qerr


######
def ratiofunction_beta_9602(df, sim, team, categorystr):

    r1 = [0] * len(sim);
    r2 = [0] * len(sim);

    r1mean = np.zeros(len(sim));
    r2mean = np.zeros(len(sim));
    r1std = np.zeros(len(sim));
    r2std = np.zeros(len(sim));

    r1median = np.zeros(len(sim))
    r2median = np.zeros(len(sim))
    qerr_r1 = np.zeros(len(sim))
    qerr_r2 = np.zeros(len(sim))

    df0 = {}
    df1 = {}
    df2 = {}

    file = open('../Latex/9602_TimeConstant_' + categorystr + "latex_table.txt", "w")
    file.write(categorystr + '\n')

    print('len sim', len(sim))

    for j in range(len(sim)):
        # print('simarray', sim[j])
        title = str(sim[j]) + '-' + str(team[j])

        df0[j] = df[(df.Sim == sim[j]) & (df.Team == team[j])]
        df0[j].reset_index(inplace=True)
        year = (df0[j].iloc[0]['JOSIE_Nr'])

        rt1 = (df0[j].iloc[0]['R1_Tstop'])
        rt2 = (df0[j].iloc[0]['R2_Tstop'])
        t1 = (df0[j].Tsim < rt1 ) & (df0[j].Tsim >= rt1 - 15)
        t2 = (df0[j].Tsim < rt2 ) & (df0[j].Tsim >= rt2 - 15)
        #
        df1[j] = df0[j][t1]
        df2[j] = df0[j][t2]
        # c = df1[j].IM .tolist()
        # sc = ( df1[j].I_conv_slow.tolist())

        r1[j] =  np.array((df1[j].IM / (0.10 * df1[j].I_conv_slow)).tolist())
        r2[j] =  np.array((df2[j].IM / (0.10 * df2[j].I_conv_slow)).tolist())
        #
        r1mean[j] = np.nanmean(r1[j])
        r2mean[j] = np.nanmean(r2[j])
        r1std[j] = np.nanstd(r1[j])
        r2std[j] = np.nanstd(r2[j])
        r1median[j] = np.nanmedian(r1[j])
        r2median[j] = np.nanmedian(r2[j])
        qerr_r1[j] = (np.nanquantile(r1[j], 0.75) - np.nanquantile(r1[j], 0.25)) / (2 * 0.6745)
        qerr_r2[j] = (np.nanquantile(r2[j], 0.75) - np.nanquantile(r2[j], 0.25)) / (2 * 0.6745)

        lr1 = str(round(r1mean[j], 2)) + '\pm ' + str(round(r1std[j], 2))
        lr2 = str(round(r2mean[j], 2)) + '\pm ' + str(round(r2std[j], 2))
        lr3 = str(round(r1median[j], 2)) + '\pm ' + str(round(qerr_r1[j], 2))
        lr4 = str(round(r2median[j], 2)) + '\pm ' + str(round(qerr_r2[j], 2))

        mat = '$'

        file.write('\hline' + '\n')
        file.write(mat + str(int(year)) + '-' + title + mat + ' & ' + mat + lr1 + mat + ' & ' + mat + lr2 + mat + ' & ' + mat + lr3 + mat +
                   ' & ' + mat + lr4 + mat + r'\\' + '\n')

    rmean = [r1mean, r2mean]
    rstd = [r1std, r2std]
    rmedian = [r1median, r2median]
    rqerr = [qerr_r1, qerr_r2]

    qerr_1 = (np.nanquantile(r1median, 0.75) - np.nanquantile(r1median, 0.25)) / (2 * 0.6745)
    qerr_2 = (np.nanquantile(r2median, 0.75) - np.nanquantile(r2median, 0.25)) / (2 * 0.6745)

    file.write('\hline' + '\n')
    file.write('\hline' + '\n')
    file.write('Mean & ' + mat + str(round(np.nanmean(r1mean), 2)) + '\pm ' + str(round(np.nanstd(r1mean), 2)) + mat + ' & ' +
               mat + str(round(np.nanmean(r2mean), 2)) + '\pm ' + str(round(np.nanstd(r2mean), 2)) + mat  + r'\\' + '\n')
    file.write('Median  & ' + mat + str(round(np.nanmedian(r1mean), 2)) + '\pm ' + str(round(qerr_1, 2)) + mat + ' & ' +
               mat + str(round(np.nanmedian(r2mean), 2)) + '\pm ' + str(round(qerr_2, 2)) + mat  + r'\\' + '\n')
    file.write('\hline' + '\n')
    file.write('\hline' + '\n')
    file.write('Mean R1-R2 &' + mat + str(round(np.nanmean(rmean), 2)) + '\pm ' + str(round(np.nanstd(rmean), 2)) + mat + ' & '+ r'\\' + '\n')
    file.write('Median R1-R2 &' + mat + str(round(np.nanmedian(rmedian), 2)) + '\pm ' + str(round(np.nanstd(rmedian), 2)) + mat + ' & '+ r'\\' + '\n')

    file.close()



    return rmean, rstd, rmedian, rqerr


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
# rmean_en0505, rstd_en0505, rmedian_en0505 = ratiofunction_beta(df, sim_en0505, team_en0505, 'EN0505')
# rmean_en1010, rstd_en1010, rmedian_en1010 = ratiofunction_beta(df, sim_en1010, team_en1010, 'EN1010')
# rmean_sp0505, rstd_sp0505, rmedian_sp0505 = ratiofunction_beta(df, sim_sp0505, team_sp0505, 'SP0505')
# rmean_sp1010, rstd_sp1010, rmedian_sp1010= ratiofunction_beta(df, sim_sp1010, team_sp1010, 'SP1010')

# rmean_en0505, rstd_en0505, rmedian_en0505, rqerr_en0505 = ratiofunction_beta(df, sim_en0505, team_en0505, 'EN0505')
# rmean_en1010, rstd_en1010, rmedian_en1010, rqerr_en1010 = ratiofunction_beta(df, sim_en1010, team_en1010, 'EN1010')
# rmean_sp0505, rstd_sp0505, rmedian_sp0505, rqerr_sp0505 = ratiofunction_beta(df, sim_sp0505, team_sp0505, 'SP0505')
# rmean_sp1010, rstd_sp1010, rmedian_sp1010, rqerr_sp1010 = ratiofunction_beta(df, sim_sp1010, team_sp1010, 'SP1010')

## for 9602
# rmean_en0505, rmedian_en0505 = ratiofunction_beta_9602(df, sim_en0505, team_en0505, 'EN0505')
# rmean_en1010, rmedian_en1010 = ratiofunction_beta_9602(df, sim_en1010, team_en1010, 'EN1010')
# rmean_sp0505, rmedian_sp0505 = ratiofunction_beta_9602(df, sim_sp0505, team_sp0505, 'SP0505')
# rmean_sp1010, rmedian_sp1010 = ratiofunction_beta_9602(df, sim_sp1010, team_sp1010, 'SP1010')

rmean_en0505, rstd_en0505,  rmedian_en0505, rqerr_en0505 = ratiofunction_beta_9602(df, sim_en0505, team_en0505, 'EN0505')
rmean_en1010, rstd_en1010, rmedian_en1010, rqerr_en1010 = ratiofunction_beta_9602(df, sim_en1010, team_en1010, 'EN1010')
rmean_sp0505, rstd_sp0505, rmedian_sp0505, rqerr_sp0505 = ratiofunction_beta_9602(df, sim_sp0505, team_sp0505, 'SP0505')
rmean_sp1010, rstd_sp1010, rmedian_sp1010, rqerr_sp1010 = ratiofunction_beta_9602(df, sim_sp1010, team_sp1010, 'SP1010')


# print('rmean_en0505', rmean_en0505)
# print('rstd_en0505', rstd_en0505)
# print('rmedian_en0505', rmedian_en0505)
# print('rqerr_en0505', rqerr_en0505)

# plotting

x1 = [0] * len(rmean_en0505[0])
x1_1 = [1] * len(rmean_en1010[0])
x1_2 = [2] * len(rmean_sp0505[0])
x1_3 = [3] * len(rmean_sp1010[0])

xlabels = ['EN 0.5%-0.5B', 'EN 1.0%-1.0B', 'SP 0.5%-0.5B', 'SP 1.0%-1.0B']

x1.extend(x1_1)
x1.extend(x1_2)
x1.extend(x1_3)


# plotting 9602
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

print('r_en0505_R2_4', r_en0505_R2_4)
print('median',      r_en0505_R2_4_median)
#

colors = ("dodgerblue",  "red", 'green')
groups = ("Tsim R1", "Tsim R2")

# # Create plot
fig, ax = plt.subplots()

#
ax.scatter(x1, r1_mean, alpha=0.8, c=colors[0], marker="o", label=groups[0])
ax.scatter(x1, r2_mean, alpha=0.8, c=colors[1], marker='v', edgecolors='none', label=groups[1])
# ax.scatter(x1, r3_mean, alpha=0.8, c=colors[2], marker="<", edgecolors='none', label=groups[2])
# ax.scatter(x1, r4_mean, alpha=0.8, c=colors[3], marker=">", edgecolors='none', label=groups[3])
# data_to_plot = [r_en0505_R2_4, r_en1010_R2_4, r_sp0505_R2_4, r_sp1010_R2_4]
r_en0505_R2_4 = r_en0505_R2_4[~np.isnan(r_en0505_R2_4)]
r_en1010_R2_4 = r_en1010_R2_4[~np.isnan(r_en1010_R2_4)]
r_sp0505_R2_4 = r_sp0505_R2_4[~np.isnan(r_sp0505_R2_4)]
r_sp1010_R2_4 = r_sp1010_R2_4[~np.isnan(r_sp1010_R2_4)]

data_to_plot = [r_en0505_R2_4, r_en1010_R2_4, r_sp0505_R2_4, r_sp1010_R2_4]
ax.boxplot(data_to_plot,   positions=[0,1,2,3])
plt.ylabel('I ECC/ 0.10 * I OPM(cor. JMA) conv. slow')
plt.title('1996-2002 data')
plt.ylim(0, 2)
ax.set_xticks(np.arange(len(xlabels)))
ax.set_xticklabels(xlabels)

# plt.title('Matplot scatter plot')
plt.legend(loc='upper right')
plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Ratio_Conv/RatioPlot_9602.png')
plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Ratio_Conv/RatioPlot_9602.eps')
plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Ratio_Conv/RatioPlot_9602.pdf')

plt.show()

print('r_en0505_R2_4, r_en1010_R2_4, r_sp0505_R2_4, r_sp1010_R2_4')
print('mean', np.nanmean(r_en0505_R2_4), np.nanmean(r_en1010_R2_4), np.nanmean(r_sp0505_R2_4), np.nanmean(r_sp1010_R2_4))
print('median', np.nanmedian(r_en0505_R2_4), np.nanmedian(r_en1010_R2_4), np.nanmedian(r_sp0505_R2_4), np.nanmedian(r_sp1010_R2_4))

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
#
#
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



print('median', np.nanmedian(r_en0505_R2_4), np.nanmedian(r_en1010_R2_4), np.nanmedian(r_sp0505_R2_4), np.nanmedian(r_sp1010_R2_4))

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
