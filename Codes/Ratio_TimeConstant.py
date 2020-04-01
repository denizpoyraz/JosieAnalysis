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

        # print(j, np.mean(r1[j]))

        r1mean[j] = np.mean(r1[j])
        r1std[j] = np.std(r1[j])
        r2mean[j] = np.mean(r2[j])
        r2std[j] = np.std(r2[j])
        r3mean[j] = np.mean(r3[j])
        r3std[j] = np.std(r3[j])
        r4mean[j] = np.mean(r4[j])
        r4std[j] = np.std(r4[j])

        r1median[j] = np.median(r1[j])
        r2median[j] = np.median(r2[j])
        r3median[j] = np.median(r3[j])
        r4median[j] = np.median(r4[j])

    print('in the function')
    print('r1mean', r1mean)
    print('r2mean',r2mean)
    print('r3mean', r3mean)
    print('r4mean', r4mean)

    rmean = [r1mean, r2mean, r3mean, r4mean]
    rstd = [r1std, r2std, r3std, r4std]
    rmedian = [r1median, r2median, r3median, r4median]

    return rmean, rstd, rmedian


#######################################################################################################################

# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2009_Data_nocut.csv", low_memory=False)
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

rmean_en0505, rstd_en0505, rmedian_en0505 = ratiofunction_beta(df, sim_en0505, team_en0505, 'EN0505')
rmean_en1010, rstd_en1010, rmedian_en1010 = ratiofunction_beta(df, sim_en1010, team_en1010, 'EN1010')
rmean_sp0505, rstd_sp0505, rmedian_sp0505 = ratiofunction_beta(df, sim_sp0505, team_sp0505, 'SP0505')
rmean_sp1010, rstd_sp1010, rmedian_sp1010= ratiofunction_beta(df, sim_sp1010, team_sp1010, 'SPsp1010')


# plotting

x1 = [0] * len(rmean_en0505[0])
x1_1 = [1] * len(rmean_en1010[0])
x1_2 = [2] * len(rmean_sp0505[0])
x1_3 = [3] * len(rmean_sp1010[0])

xlabels = ['EN 0.5%-0.5B', 'EN 1.0%-1.0B', 'SP 0.5%-0.5B', 'SP 1.0%-1.0B']

x1.extend(x1_1)
x1.extend(x1_2)
x1.extend(x1_3)

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


colors = ("dodgerblue", "blue", "red", 'green')
groups = ("Tsim 2100-2400", "Tsim 4100-4400", "Tsim 6100-6400", 'Tsim 8100-8400')

# Create plot
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

ax.scatter(x1, r1_mean, alpha=0.8, c=colors[0], marker="o", label=groups[0])
ax.scatter(x1, r2_mean, alpha=0.8, c=colors[1], marker='v', edgecolors='none', label=groups[1])
ax.scatter(x1, r3_mean, alpha=0.8, c=colors[2], marker="<", edgecolors='none', label=groups[2])
ax.scatter(x1, r4_mean, alpha=0.8, c=colors[3], marker=">", edgecolors='none', label=groups[3])
data_to_plot = [r_en0505_R1_4, r_en1010_R1_4, r_sp0505_R1_4, r_sp1010_R1_4]
ax.boxplot(data_to_plot, positions=[0,1,2,3])

x0 = [0]
x11 = [1]
x2 = [2]
x3 = [3]


plt.ylabel('I ECC/ 0.10 * I OPM(cor. JMA) conv. slow')
plt.title('0910 data')
plt.ylim(0, 1)
ax.set_xticks(np.arange(len(xlabels)))
ax.set_xticklabels(xlabels)

# plt.title('Matplot scatter plot')
plt.legend(loc='best')
plt.show()

fig = plt.figure()
ax2 = fig.add_subplot(1, 1, 1)
groups2 = ( "Tsim 4100-4400", "Tsim 6100-6400", 'Tsim 8100-8400')
# ax2.scatter(x1, r1, alpha=0.8, c=colors[0], marker="o", label=groups[0])
ax2.scatter(x1, r2_mean, alpha=0.8, c=colors[1], marker='v', edgecolors='none', label=groups[1])
ax2.scatter(x1, r3_mean, alpha=0.8, c=colors[2], marker="<", edgecolors='none', label=groups[2])
ax2.scatter(x1, r4_mean, alpha=0.8, c=colors[3], marker=">", edgecolors='none', label=groups[3])
data_to_plot = [r_en0505_R2_4, r_en1010_R2_4, r_sp0505_R2_4, r_sp1010_R2_4]
ax2.boxplot(data_to_plot, positions=[0,1,2,3])

x0 = [0]
x11 = [1]
x2 = [2]
x3 = [3]
# ax2.errorbar(x0, np.mean(r_en0505_R2_4), yerr=np.std(r_en0505_R2_4), color='gold', elinewidth=1, capsize=1, capthick=0.5,
#             marker='s', markersize=10, alpha=0.9, label='mean')
# ax2.errorbar(x11, np.mean(r_en1010_R2_4), yerr=np.std(r_en1010_R2_4), color='gold', elinewidth=1, capsize=1, capthick=0.5,
#             marker='s', markersize=10, alpha=0.9)
# ax2.errorbar(x2, np.mean(r_sp0505_R2_4), yerr=np.std(r_sp0505_R2_4), color='gold', elinewidth=1, capsize=1, capthick=0.5,
#             marker='s', markersize=10, alpha=0.9)
# ax2.errorbar(x3, np.mean(r_sp1010_R2_4), yerr=np.std(r_sp1010_R2_4), color='gold', elinewidth=1, capsize=1, capthick=0.5,
#             marker='s', markersize=10, alpha=0.9)

plt.ylabel('I ECC/ 0.10 * I OPM(cor. JMA) conv. slow')
plt.title('0910 data ')
plt.ylim(0, 1)
ax2.set_xticks(np.arange(len(xlabels)))
ax2.set_xticklabels(xlabels)

# plt.title('Matplot scatter plot')
plt.legend(loc='best')
plt.show()

filem = open('../Latex/0910_Beta_Medians_latex_table.txt', "w")

filem.write('Median EN0505 (R2-R4)' + str(np.median(r_en0505_R2_4))  + '\n')
filem.write('Median EN1010 (R2-R4)' + str(np.median(r_en1010_R2_4))  + '\n')
filem.write('Median SP0505 (R2-R4)' + str(np.median(r_sp0505_R2_4))  + '\n')
filem.write('Median SP1010 (R2-R4)' + str(np.median(r_sp1010_R2_4))  + '\n')
filem.write('Now usuing medians rather than mean' + '\n')
filem.write('Median EN0505 (R2-R4)' + str(np.median(r_en0505_R2_4_median))  + '\n')
filem.write('Median EN1010 (R2-R4)' + str(np.median(r_en1010_R2_4_median))  + '\n')
filem.write('Median SP0505 (R2-R4)' + str(np.median(r_sp0505_R2_4_median))  + '\n')
filem.write('Median SP1010 (R2-R4)' + str(np.median(r_sp1010_R2_4_median))  + '\n')
filem.close()
