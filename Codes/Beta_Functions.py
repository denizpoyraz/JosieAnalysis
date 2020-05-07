import numpy as np
import pandas as pd

def ratiofunction_beta(df, sim, team, categorystr, boolibo):

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

    df['iB0'] = 0.014

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

        if not boolibo:

            r1[j] = np.array((df1[j].IM / (0.10 * df1[j].I_conv_slow)).tolist())
            r2[j] = np.array((df2[j].IM / (0.10 * df2[j].I_conv_slow)).tolist())
            r3[j] = np.array((df3[j].IM / (0.10 * df3[j].I_conv_slow)).tolist())
            r4[j] = np.array((df4[j].IM / (0.10 * df4[j].I_conv_slow)).tolist())

        if  boolibo:

            r1[j] = np.array(( (df1[j].IM - df1[j].iB0) / (0.10 * df1[j].I_conv_slow)).tolist())
            r2[j] = np.array(( (df2[j].IM - df2[j].iB0) / (0.10 * df2[j].I_conv_slow)).tolist())
            r3[j] = np.array(( (df3[j].IM - df3[j].iB0) / (0.10 * df3[j].I_conv_slow)).tolist())
            r4[j] = np.array(( (df4[j].IM - df4[j].iB0) / (0.10 * df4[j].I_conv_slow)).tolist())
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
    qerr = [qerr_r1, qerr_r2, qerr_r3, qerr_r4]

    return rmean, rstd, rmedian, qerr


######
def ratiofunction_beta_9602(df, sim, team, categorystr, boolib0):

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

    df['iB0'] = 0.014


    file = open('../Latex/9602_TimeConstant_' + categorystr + "5secslatex_table.txt", "w")
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
        if sim[j] == 90: rt1 = 1050
        t1 = (df0[j].Tsim <= rt1 ) & (df0[j].Tsim >= rt1 - 5)
        t2 = (df0[j].Tsim <= rt2 ) & (df0[j].Tsim >= rt2 - 5)
        #
        df1[j] = df0[j][t1]
        df2[j] = df0[j][t2]
        # c = df1[j].IM .tolist()
        # sc = ( df1[j].I_conv_slow.tolist())

        if not boolib0:
            r1[j] = np.array((df1[j].IM / (0.10 * df1[j].I_conv_slow)).tolist())
            r2[j] = np.array((df2[j].IM / (0.10 * df2[j].I_conv_slow)).tolist())


        if boolib0:
            r1[j] = np.array(((df1[j].IM - df1[j].iB0) / (0.10 * df1[j].I_conv_slow)).tolist())
            r2[j] = np.array(((df2[j].IM - df2[j].iB0) / (0.10 * df2[j].I_conv_slow)).tolist())




        # print(sim[j],team[j], 'Ratio', r1[j], r2[j])
        # print(sim[j], team[j], 'Curent', df1[j].IM.tolist(), df1[j].I_conv_slow.tolist() )
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
