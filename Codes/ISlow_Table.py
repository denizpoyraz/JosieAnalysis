import numpy as np
import pandas as pd

def mederr(med):
    err = (np.nanquantile(med, 0.75) - np.nanquantile(med, 0.25)) / (2 * 0.6745)
    return err


def table_islow(df, sim, team, categorystr):

    file = open('../Latex/ISlow/0910_ISlow_One_' + categorystr + "_.txt", "w")
    file.write(categorystr + '\n')
    file.write('\hline' + '\n')
    file2 = open('../Latex/ISlow/0910_ISlow_Two_v2_' + categorystr + "_.txt", "w")
    file2.write(categorystr + '\n')
    file2.write('\hline' + '\n')
    file3 = open('../Latex/ISlow/0910_ISlow_Three_v2_' + categorystr + "_.txt", "w")
    file3.write(categorystr + '\n')
    file3.write('\hline' + '\n')

    iB0 = np.zeros(len(sim));
    iB1 = np.zeros(len(sim));
    Y1 = np.zeros(len(sim));
    Y2ep = np.zeros(len(sim));
    Y2bs = np.zeros(len(sim))
    Y2mY1 = np.zeros(len(sim));
    Y3 = np.zeros(len(sim));
    Y3D = np.zeros(len(sim));
    Y4 = np.zeros(len(sim));
    Y4mY3 = np.zeros(len(sim));
    Y5 = np.zeros(len(sim));
    iB2 = np.zeros(len(sim));
    Y6 = np.zeros(len(sim));
    Y5mY6 = np.zeros(len(sim))
    t_decay = np.zeros(len(sim))
    t3 = np.zeros(len(sim))

    for j in range(len(sim)):
        dft = df[(df.Sim == sim[j]) & (df.Team == team[j])]
        # dft = dft.reset_index(inplace=True)

        size = len(dft)
        title = str(sim[j]) + '-' + str(team[j])


        t_prep_end = dft[(dft.TimeTag == 'Prep')].Tsim.max()
        t_sim_begin = dft[(dft.TimeTag == 'Sim')].Tsim.min()
        t3[j] = t_sim_begin - t_prep_end
        t_decay[j] = dft.at[dft.first_valid_index(), 'decay_time']
        t_ib2 = t_sim_begin + 7 * 60

        iB0[j] = dft.at[dft.first_valid_index(), 'iB0']
        iB1[j] = dft.at[dft.first_valid_index(), 'iB1']
        Y1[j] = iB1[j] - iB0[j]
        Y2ep[j] = dft[dft.Tsim == t_prep_end].I_slow_conv.tolist()[0]
        Y2bs[j] = dft[dft.Tsim == t_sim_begin].I_slow_conv.tolist()[0]
        Y2mY1[j] = Y2ep[j] - Y1[j]
        Y3[j] = (Y1[j]) * np.exp(-t3[j] / (25 * 60))
        Y3D[j] = (Y1[j]) * np.exp(-t_decay[j] / (25 * 60))
        Y4[j] = dft[dft.Tsim == t_sim_begin].I_slow_conv.tolist()[0]
        Y4mY3[j] = Y4[j] - Y3[j]
        Y5[j] = dft[dft.Tsim == t_ib2].I_slow_conv.tolist()[0]
        iB2[j] = dft.at[dft.first_valid_index(), 'iB2']
        Y6[j] = iB2[j] - iB0[j]
        Y5mY6[j] = Y5[j] - Y6[j]

        mat = '$'
        end = '&'

        # file.write(
        #     mat + title + mat + end + mat + str(round(iB0[j],3)) + mat + end + mat + str(round(iB1[j],3)) + mat + end + mat + str(round(Y1[
        #         j],3)) + mat + end + mat + str(round(Y2ep[j],3)) + mat + end + mat + str(round(Y2bs[j],3)) + mat + end + mat + str(round(Y2mY1[
        #         j],3)) + mat + r'\\' + '\n')
        # file2.write(
        #     mat + title + mat + end + mat + str(round(Y3[j], 3)) + mat + end + mat + str(
        #         round(Y3D[j], 3)) + mat + end + mat + str(round(Y4[j], 3)) + mat + end + mat + str(
        #         round(Y4mY3[j], 3)) + mat + end + mat + str(round(Y5[j], 3)) + mat + end + mat
        #     + str(round(iB2[j], 3)) + mat + end + mat + str(round(Y6[j], 3))+ mat + end + mat + str(round(Y5mY6[j], 3)) + mat +  r'\\' + '\n')
        ##v2 tables
        file2.write(
            mat + title + mat + end + mat + str(round(Y3[j], 3)) + mat + end + mat + str(
                round(Y3D[j], 3)) + mat + end + mat + str(round(Y4[j], 3)) + mat + end + mat + str(
                round(Y4mY3[j], 3)) + mat + end + mat + str(t3[j]) + mat + end + mat + str(t_decay[j]) + mat + r'\\' + '\n')

        file3.write( mat + title + mat + end + mat +str(round(Y5[j], 3)) + mat + end + mat
            + str(round(iB2[j], 3)) + mat + end + mat + str(round(Y6[j], 3)) + mat + end + mat + str(
                round(Y5mY6[j], 3)) + mat + r'\\' + '\n')


    print(iB0, np.nanmedian(iB0), np.nanmean(iB0))

    mat = '$'
    end = '&'

    # file.write('\hline' + '\n')
    # file.write('\hline' + '\n')
    # file.write(
    #     'Mean & ' + mat + str(round(np.nanmean(iB0), 3)) + '\pm ' + str(round(np.nanstd(iB0), 3)) + mat + end
    #     + mat + str(round(np.nanmean(iB1), 3)) + '\pm ' + str(round(np.nanstd(iB1), 3)) + mat + end
    #     + mat + str(round(np.nanmean(Y1), 3)) + '\pm ' + str(round(np.nanstd(Y1), 3)) + mat + end
    #     + mat + str(round(np.nanmean(Y2ep), 3)) + '\pm ' + str(round(np.nanstd(Y2ep), 3)) + mat + end
    #     + mat + str(round(np.nanmean(Y2bs), 3)) + '\pm ' + str(round(np.nanstd(Y2bs), 3)) + mat + end
    #     + mat + str(round(np.nanmean(Y2mY1), 3)) + '\pm ' + str(round(np.nanstd(Y2mY1), 3)) + mat + r'\\' + '\n')
    # file.write('\hline' + '\n')
    # file.write('\hline' + '\n')
    # file.write(
    #     'Median & ' + mat + str(round(np.nanmedian(iB0), 3)) + '\pm ' + str(
    #         round(np.nanquantile(iB0, 0.25), 3)) + ',' + str(round(np.nanquantile(iB0, 0.75), 3)) + mat + end
    #     + mat + str(round(np.nanmedian(iB1), 3)) + '\pm ' + str(round(np.nanquantile(iB1, 0.25), 3)) + ',' + str(
    #         round(np.nanquantile(iB1, 0.75), 3)) + mat + end
    #     + mat + str(round(np.nanmedian(Y1), 3)) + '\pm ' + str(round(np.nanquantile(Y1, 0.25), 3)) + ',' + str(
    #         round(np.nanquantile(Y1, 0.75), 3)) + mat + end
    #     + mat + str(round(np.nanmedian(Y2ep), 3)) + '\pm ' + str(round(np.nanquantile(Y2ep, 0.25), 3)) + ',' + str(
    #         round(np.nanquantile(Y2ep, 0.75), 3)) + mat + end
    #     + mat + str(round(np.nanmedian(Y2bs), 3)) + '\pm ' + str(round(np.nanquantile(Y2bs, 0.25), 3)) + ',' + str(
    #         round(np.nanquantile(Y2bs, 0.75), 3)) + mat + end
    #     + mat + str(round(np.nanmedian(Y2mY1), 3)) + '\pm ' + str(round(np.nanquantile(Y2mY1, 0.25), 3)) + ',' + str(
    #         round(np.nanquantile(Y2mY1, 0.75), 3)) + mat + r'\\' + '\n')

    # file2.write('\hline' + '\n')
    # file2.write('\hline' + '\n')
    # file2.write(
    #     'Mean & ' + mat + str(round(np.nanmean(Y3), 3)) + '\pm ' + str(round(np.nanstd(Y3), 3)) + mat + end
    #     + mat + str(round(np.nanmean(Y3D), 3)) + '\pm ' + str(round(np.nanstd(Y3D), 3)) + mat + end
    #     + mat + str(round(np.nanmean(Y4), 3)) + '\pm ' + str(round(np.nanstd(Y4), 3)) + mat + end
    #     + mat + str(round(np.nanmean(Y4mY3), 3)) + '\pm ' + str(round(np.nanstd(Y4mY3), 3)) + mat + end
    #     + mat + str(round(np.nanmean(Y5), 3)) + '\pm ' + str(round(np.nanstd(Y5), 3)) + mat + end
    #     + mat + str(round(np.nanmean(iB2), 3)) + '\pm ' + str(round(np.nanstd(iB2), 3)) + mat + end
    #     + mat + str(round(np.nanmean(Y6), 3)) + '\pm ' + str(round(np.nanstd(Y6), 3)) + mat + end
    #     + mat + str(round(np.nanmean(Y5mY6), 3)) + '\pm ' + str(round(np.nanstd(Y5mY6), 3)) + mat + r'\\' + '\n')
    # file2.write('\hline' + '\n')
    # file2.write('\hline' + '\n')
    # file2.write(
    #     'Median & ' + mat + str(round(np.nanmedian(Y3), 3)) + '\pm ' + str(
    #         round(np.nanquantile(Y3, 0.25), 3)) + ',' + str(round(np.nanquantile(Y3, 0.75), 3)) + mat + end
    #     + mat + str(round(np.nanmedian(Y3D), 3)) + '\pm ' + str(round(np.nanquantile(Y3D, 0.25), 3)) + ',' + str(
    #         round(np.nanquantile(Y3D, 0.75), 3)) + mat + end
    #     + mat + str(round(np.nanmedian(Y4), 3)) + '\pm ' + str(round(np.nanquantile(Y4, 0.25), 3)) + ',' + str(
    #         round(np.nanquantile(Y4, 0.75), 3)) + mat + end
    #     + mat + str(round(np.nanmedian(Y4mY3), 3)) + '\pm ' + str(round(np.nanquantile(Y4mY3, 0.25), 3)) + ',' + str(
    #         round(np.nanquantile(Y4mY3, 0.75), 3)) + mat + end
    #     + mat + str(round(np.nanmedian(Y5), 3)) + '\pm ' + str(round(np.nanquantile(Y5, 0.25), 3)) + ',' + str(
    #         round(np.nanquantile(Y5, 0.75), 3)) + mat + end
    #     + mat + str(round(np.nanmedian(iB2), 3)) + '\pm ' + str(round(np.nanquantile(iB2, 0.25), 3)) + ',' + str(
    #         round(np.nanquantile(iB2, 0.75), 3)) + mat + end
    #     + mat + str(round(np.nanmedian(Y6), 3)) + '\pm ' + str(round(np.nanquantile(Y6, 0.25), 3)) + ',' + str(
    #         round(np.nanquantile(Y6, 0.75), 3)) + mat + end
    #     + mat + str(round(np.nanmedian(Y5mY6), 3)) + '\pm ' + str(round(np.nanquantile(Y5mY6, 0.25), 3)) + ',' + str(
    #         round(np.nanquantile(Y5mY6, 0.75), 3)) + mat + r'\\' + '\n')
    # file2.write('\hline' + '\n')
    ##v2 tables
    file2.write('\hline' + '\n')
    file2.write('\hline' + '\n')
    file2.write(
        'Mean & ' + mat + str(round(np.nanmean(Y3), 3)) + '\pm ' + str(round(np.nanstd(Y3), 3)) + mat + end
        + mat + str(round(np.nanmean(Y3D), 3)) + '\pm ' + str(round(np.nanstd(Y3D), 3)) + mat + end
        + mat + str(round(np.nanmean(Y4), 3)) + '\pm ' + str(round(np.nanstd(Y4), 3)) + mat + end
        + mat + str(round(np.nanmean(Y4mY3), 3)) + '\pm ' + str(round(np.nanstd(Y4mY3), 3)) + mat + end
        + mat + str(round(np.nanmean(t3), 3)) + '\pm ' + str(round(np.nanstd(t3), 3)) + mat + end
        + mat + str(round(np.nanmean(t_decay), 3)) + '\pm ' + str(round(np.nanstd(t_decay), 3)) + mat  + r'\\' + '\n')

    file2.write('\hline' + '\n')
    file2.write('\hline' + '\n')
    file2.write(
        'Median & ' + mat + str(round(np.nanmedian(Y3), 3)) + '\pm ' + str(
            round(np.nanquantile(Y3, 0.25), 3)) + ',' + str(round(np.nanquantile(Y3, 0.75), 3)) + mat + end
        + mat + str(round(np.nanmedian(Y3D), 3)) + '\pm ' + str(round(np.nanquantile(Y3D, 0.25), 3)) + ',' + str(
            round(np.nanquantile(Y3D, 0.75), 3)) + mat + end
        + mat + str(round(np.nanmedian(Y4), 3)) + '\pm ' + str(round(np.nanquantile(Y4, 0.25), 3)) + ',' + str(
            round(np.nanquantile(Y4, 0.75), 3)) + mat + end
        + mat + str(round(np.nanmedian(Y4mY3), 3)) + '\pm ' + str(round(np.nanquantile(Y4mY3, 0.25), 3)) + ',' + str(
            round(np.nanquantile(Y4mY3, 0.75), 3)) + mat + end
        + mat + str(round(np.nanmedian(t3), 3)) + '\pm ' + str(round(np.nanquantile(t3, 0.25), 3)) + ',' + str(
            round(np.nanquantile(t3, 0.75), 3)) + mat + end
        + mat + str(round(np.nanmedian(t_decay), 3)) + '\pm ' + str(round(np.nanquantile(t_decay, 0.25), 3)) + ',' + str(
            round(np.nanquantile(t_decay, 0.75), 3)) + mat + r'\\' + '\n')

    file3.write('\hline' + '\n')
    file3.write('\hline' + '\n')
    file3.write('Mean &'
    + mat + str(round(np.nanmean(Y5), 3)) + '\pm ' + str(round(np.nanstd(Y5), 3)) + mat + end
    + mat + str(round(np.nanmean(iB2), 3)) + '\pm ' + str(round(np.nanstd(iB2), 3)) + mat + end
    + mat + str(round(np.nanmean(Y6), 3)) + '\pm ' + str(round(np.nanstd(Y6), 3)) + mat + end
    + mat + str(round(np.nanmean(Y5mY6), 3)) + '\pm ' + str(round(np.nanstd(Y5mY6), 3)) + mat + r'\\' + '\n')

    file3.write('\hline' + '\n')
    file3.write('\hline' + '\n')
    file3.write('Median &'
    + mat + str(round(np.nanmedian(Y5), 3)) + '\pm ' + str(round(np.nanquantile(Y5, 0.25), 3)) + ',' + str(
        round(np.nanquantile(Y5, 0.75), 3)) + mat + end
    + mat + str(round(np.nanmedian(iB2), 3)) + '\pm ' + str(round(np.nanquantile(iB2, 0.25), 3)) + ',' + str(
        round(np.nanquantile(iB2, 0.75), 3)) + mat + end
    + mat + str(round(np.nanmedian(Y6), 3)) + '\pm ' + str(round(np.nanquantile(Y6, 0.25), 3)) + ',' + str(
        round(np.nanquantile(Y6, 0.75), 3)) + mat + end
    + mat + str(round(np.nanmedian(Y5mY6), 3)) + '\pm ' + str(round(np.nanquantile(Y5mY6, 0.25), 3)) + ',' + str(
        round(np.nanquantile(Y5mY6, 0.75), 3)) + mat + r'\\' + '\n')


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


dfa = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_Deconv_preparationadded_all.csv", low_memory=False) #all data
dfs = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_Deconv_preparationadded_mino_t.csv", low_memory=False) #simulation data

dfa = dfa[dfa.ADX == 0]

dfa = dfa.drop(dfa[(dfa.Sim == 147) & (dfa.Team == 3)].index)
dfa = dfa.drop(dfa[(dfa.Sim == 158) & (dfa.Team == 1)].index)
dfa = dfa.drop(dfa[(dfa.Sim == 158) & (dfa.Team == 2)].index)
dfa = dfa.drop(dfa[(dfa.Sim == 160) & (dfa.Team == 4)].index)
dfa = dfa.drop(dfa[(dfa.Sim == 165) & (dfa.Team == 4)].index)

dfs = dfs[dfs.ADX == 0]

dfs = dfs.drop(dfs[(dfs.Sim == 147) & (dfs.Team == 3)].index)
dfs = dfs.drop(dfs[(dfs.Sim == 158) & (dfs.Team == 1)].index)
dfs = dfs.drop(dfs[(dfs.Sim == 158) & (dfs.Team == 2)].index)
dfs = dfs.drop(dfs[(dfs.Sim == 160) & (dfs.Team == 4)].index)
dfs = dfs.drop(dfs[(dfs.Sim == 165) & (dfs.Team == 4)].index)

sim_0910, team_0910 = filter(dfa)

# ratiofunction_beta(df, sim, team, categorystr, boolibo, slow, fast):
# ratiofunction_beta(df1, sim_0910[0], team_0910[0], 'EN0505', 1, tslow, tfast)


table_islow(dfa, sim_0910[0], team_0910[0], 'EN0505')
table_islow(dfa, sim_0910[1], team_0910[1], 'EN1010')
table_islow(dfa, sim_0910[2], team_0910[2], 'SP0505')
table_islow(dfa, sim_0910[3], team_0910[3], 'SP1010')




