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

    # print('in the function')
    # print('r1mean', r1mean)
    # print('r1median', r1median)
    #
    # print('r2mean', r2mean)
    # print('r3mean', r3mean)
    # print('r4mean', r4mean)
    # print('r4median', r4median)

    rmean = [r1mean, r2mean, r3mean, r4mean]
    rstd = [r1std, r2std, r3std, r4std]
    rmedian = [r1median, r2median, r3median, r4median]

    return rmean, rstd, rmedian


######
def ratiofunction_beta_9602(df, sim, team, categorystr):
    r1 = [0] * len(sim);
    r2 = [0] * len(sim);

    r1mean = np.zeros(len(sim));
    r2mean = np.zeros(len(sim));

    r1median = np.zeros(len(sim));
    r2median = np.zeros(len(sim));

    df0 = {}
    df1 = {}
    df2 = {}

    print('len sim', len(sim))

    for j in range(len(sim)):
        # print('simarray', sim[j])
        title = str(sim[j]) + '-' + str(team[j])

        df0[j] = df[(df.Sim == sim[j]) & (df.Team == team[j])]
        df0[j].reset_index(inplace=True)

        rt1 = (df0[j].iloc[0]['R1_Tstop'])
        rt2 = (df0[j].iloc[0]['R2_Tstop'])
        t1 = (df0[j].Tsim < rt1 ) & (df0[j].Tsim >= rt1 - 50)
        t2 = (df0[j].Tsim < rt2 ) & (df0[j].Tsim >= rt2 - 50)
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
        r1median[j] = np.nanmedian(r1[j])
        r2median[j] = np.nanmedian(r2[j])

        # print(j,  c, sc,)
        print(j, sim[j], team[j], rt1, rt2, r1mean[j], r2mean[j] )

    # print('in the function')
    # print('r1mean', r1mean)
    # print('r2mean', r2mean)

    rmean = [r1mean, r2mean]
    rmedian = [r1median, r2median]

    return rmean, rmedian

####

def filter(df):

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

    sim = [sim_en0505, sim_en1010, sim_sp0505, sim_sp1010]
    team = [team_en0505, team_en1010, team_sp0505, team_sp1010]

    return sim, team


#######################################################################################################################
clist =[ 'Tsim', 'Sim', 'Team', 'ENSCI', 'Sol', 'Buf', 'Pair','PO3', 'IM','TPint', 'PO3_OPM', 'I_OPM', 'I_OPM_jma',
         'I_conv_slow',  'PFcor', 'R1_Tstart', 'R1_Tstop', 'R2_Tstart', 'R2_Tstop']

df1 = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_Data_nocut.csv", low_memory=False)
df1 = df1.drop(['Unnamed: 0', 'Unnamed: 0.1', 'ADX', 'ADif', 'ADif_PO3S','Flow','Header_IB1', 'Header_PFcor',
                'Header_PFunc', 'Header_Sim', 'Header_Team', 'IB1', 'I_Pump','O3S', 'OPM', 'PO3_OPM_stp', 'PO3_jma',
                'PO3_stp', 'RDif', 'RDif_PO3S', 'TPext','Tact', 'Tair', 'Tinlet', 'VMRO3', 'VMRO3_OPM', 'Year', 'Z', 'frac']
               , axis=1)

df1 = df1.reindex(columns=clist)
print(list(df1))
# df2 = df1.copy()

df2 = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie9602_Data.csv", low_memory=False)

df2 = df2.drop(['JOSIE_Nr','SST_Nr', 'SondeTypeNr'], axis=1)


# df = df.drop(df[(df.Sim == 140)].index)
# df = df.drop(df[(df.Sim == 147)].index)

# df = df.drop(df[(df.PO3 < 0)].index)
# df = df.drop(df[(df.PO3_OPM < 0)].index)
# df = df[df.ADX == 0]


sim_0910, team_0910 = filter(df1)
sim_9602, team_9602 = filter(df2)

## for 0910
rmean_en0505_0910, rstd_en0505, rmedian_en0505_0910 = ratiofunction_beta(df1, sim_0910[0], team_0910[0], 'EN0505')
rmean_en1010_0910, rstd_en1010, rmedian_en1010_0910 = ratiofunction_beta(df1, sim_0910[1], team_0910[1], 'EN1010')
rmean_sp0505_0910, rstd_sp0505, rmedian_sp0505_0910 = ratiofunction_beta(df1, sim_0910[2], team_0910[2], 'SP0505')
rmean_sp1010_0910, rstd_sp1010, rmedian_sp1010_0910 = ratiofunction_beta(df1, sim_0910[3], team_0910[3], 'SP1010')

## for 9602
rmean_en0505_9602, rmedian_en0505_9602 = ratiofunction_beta_9602(df2, sim_9602[0], team_9602[0], 'EN0505')
rmean_en1010_9602, rmedian_en1010_9602 = ratiofunction_beta_9602(df2, sim_9602[1], team_9602[1], 'EN1010')
rmean_sp0505_9602, rmedian_sp0505_9602 = ratiofunction_beta_9602(df2, sim_9602[2], team_9602[2], 'SP0505')
rmean_sp1010_9602, rmedian_sp1010_9602 = ratiofunction_beta_9602(df2, sim_9602[3], team_9602[3], 'SP1010')


# print('rmean_en0505_9602', rmean_en0505_9602)
# print('rmean_en0505_0910', rmean_en0505_0910)

rmean_en0505 = np.concatenate((rmean_en0505_9602, rmean_en0505_0910),  axis=None)
rmean_en1010 = np.concatenate((rmean_en1010_9602, rmean_en1010_0910),  axis=None)
rmean_sp0505 = np.concatenate((rmean_sp0505_9602, rmean_sp0505_0910),  axis=None)
rmean_sp1010 = np.concatenate((rmean_sp1010_9602, rmean_sp1010_0910),  axis=None)

print('en0505  en1010 sp0505 sp1010')
print(np.nanmedian(rmean_en0505), np.nanmedian(rmean_en1010), np.nanmedian(rmean_sp0505), np.nanmedian(rmean_sp1010))
