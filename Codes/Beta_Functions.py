import numpy as np
import pandas as pd

def ratiofunction_beta(df, sim, team, categorystr, boolibo, slow, fast):

    ##modifications made for timzescan, i slow conv used for beta calculation will be calculated in this function!

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

    dft = {}
    df1 = {}
    df2 = {}
    df3 = {}
    df4 = {}

    # df['iB0'] = 0.014

    file = open('../Latex/0910_TimeConstant_beta0' + categorystr + "1607_table.txt", "w")
    file.write(categorystr + '\n')
    file.write('\hline' + '\n')

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

        if sim[j] == 140:
            r1_down = 2700;
            r1_up = 2740;
            r2_down = 4700;
            r2_up = 4740;
            r3_down = 6700;
            r3_up = 6740;
            r4_down = 8700;
            r4_up = 8740


        dft[j] = df[(df.Sim == sim[j]) & (df.Team == team[j])]
        dft[j].reset_index(inplace=True)

        # t1 = (dft[j].Tsim >= r1_down) & (dft[j].Tsim < r1_up)
        # t2 = (dft[j].Tsim >= r2_down) & (dft[j].Tsim < r2_up)
        # t3 = (dft[j].Tsim >= r3_down) & (dft[j].Tsim < r3_up)
        # t4 = (dft[j].Tsim >= r4_down) & (dft[j].Tsim < r4_up)

        # zeroindex = int(np.mean(dft[j] .index))


        size = len(dft[j])
        Ums_i = [0] * size
        # Ua_i = [0] * size

        Ums_i[0] = dft[j].at[0, 'IM']

        ## only convolute slow part of the signal, which is needed for beta calculation
        for i in range(size - 1):
            # Ua_i = dft[j]['I_OPM_jma'].iloc[i + 1, ]
            Ua_i = dft[j].at[i+1, 'I_OPM_jma']
            t1 = dft[j].at[i + 1, 'Tsim']
            t2 = dft[j].at[i, 'Tsim']
            Xs = np.exp(-(t1 - t2) / slow)
            Xf = np.exp(-(t1 - t2) / fast)
            Ums_i[i + 1] = Ua_i - (Ua_i - Ums_i[i]) * Xs

        dft[j]['I_conv_slow_jma'] = Ums_i

        df1[j] = dft[j][(dft[j].Tsim >= r1_down) & (dft[j].Tsim < r1_up)]
        df2[j] = dft[j][(dft[j].Tsim >= r2_down) & (dft[j].Tsim < r2_up)]
        df3[j] = dft[j][(dft[j].Tsim >= r3_down) & (dft[j].Tsim < r3_up)]
        df4[j] = dft[j][(dft[j].Tsim >= r4_down) & (dft[j].Tsim < r4_up)]

        if not boolibo:

            r1[j] = np.array((df1[j].IM / (0.10 * df1[j].I_conv_slow_jma)).tolist())
            r2[j] = np.array((df2[j].IM / (0.10 * df2[j].I_conv_slow_jma)).tolist())
            r3[j] = np.array((df3[j].IM / (0.10 * df3[j].I_conv_slow_jma)).tolist())
            r4[j] = np.array((df4[j].IM / (0.10 * df4[j].I_conv_slow_jma)).tolist())

        if  boolibo:

            r1[j] = np.array(( (df1[j].IM - df1[j].iB0) / (0.10 * df1[j].I_conv_slow_jma)).tolist())
            r2[j] = np.array(( (df2[j].IM - df2[j].iB0) / (0.10 * df2[j].I_conv_slow_jma)).tolist())
            r3[j] = np.array(( (df3[j].IM - df3[j].iB0) / (0.10 * df3[j].I_conv_slow_jma)).tolist())
            r4[j] = np.array(( (df4[j].IM - df4[j].iB0) / (0.10 * df4[j].I_conv_slow_jma)).tolist())
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

        lr1 = str(round(r1mean[j], 2)) + '\pm ' + str(round(r1std[j], 2))
        lr2 = str(round(r2mean[j], 2)) + '\pm ' + str(round(r2std[j], 2))
        lr3 = str(round(r3mean[j], 2)) + '\pm ' + str(round(r3std[j], 2))
        lr4 = str(round(r4mean[j], 2)) + '\pm ' + str(round(r4std[j], 2))
        lr5 = str(round(r1median[j], 2)) + '\pm ' + str(round(qerr_r1[j], 2))
        lr6 = str(round(r2median[j], 2)) + '\pm ' + str(round(qerr_r2[j], 2))
        lr7 = str(round(r3median[j], 2)) + '\pm ' + str(round(qerr_r3[j], 2))
        lr8 = str(round(r4median[j], 2)) + '\pm ' + str(round(qerr_r4[j], 2))

        mat = '$'
        end = '&'

        file.write( mat + title + mat + end +  mat + lr1 + mat + ' & ' + mat + lr2 + mat + ' & ' + mat + lr3 + mat +' & ' + mat + lr4 + mat + r'\\' + '\n')
        # file.write( mat + title + mat + end + 'Median' + end + mat + lr5 + mat + ' & ' + mat + lr6 + mat + ' & ' + mat + lr7 + mat +' & ' + mat + lr8 + mat + r'\\' + '\n')

    rmean = [r1mean, r2mean, r3mean, r4mean]
    rstd = [r1std, r2std, r3std, r4std]
    rmedian = [r1median, r2median, r3median, r4median]

    qerr_1 = (np.nanquantile(r1median, 0.75) - np.nanquantile(r1median, 0.25)) / (2 * 0.6745)
    qerr_2 = (np.nanquantile(r2median, 0.75) - np.nanquantile(r2median, 0.25)) / (2 * 0.6745)
    qerr_3 = (np.nanquantile(r3median, 0.75) - np.nanquantile(r3median, 0.25)) / (2 * 0.6745)
    qerr_4 = (np.nanquantile(r4median, 0.75) - np.nanquantile(r4median, 0.25)) / (2 * 0.6745)

    qerr = [qerr_1, qerr_2, qerr_3, qerr_4]

    mederr = (np.nanquantile(rmedian[1:4], 0.75) - np.nanquantile(rmedian[1:4], 0.25)) / (2 * 0.6745)

    print('median error', mederr)

    print('qerr', qerr)

    # print('Test mean', len(rmean[0]))
    # print('Test median', len(rmedian[0]))

    file.write('\hline' + '\n')
    file.write('\hline' + '\n')
    file.write(
        'Mean & ' + mat + str(round(np.nanmean(r1mean), 2)) + '\pm ' + str(round(np.nanstd(r1mean), 2)) + mat + ' & ' +
        mat + str(round(np.nanmean(r2mean), 2)) + '\pm ' + str(round(np.nanstd(r2mean), 2)) + mat + ' & ' +
        mat + str(round(np.nanmean(r3mean), 2)) + '\pm ' + str(round(np.nanstd(r3mean), 2)) + mat + ' & ' +
        mat + str(round(np.nanmean(r4mean), 2)) + '\pm ' + str(round(np.nanstd(r4mean), 2)) + mat +  r'\\' + '\n')
    # file.write('Median  & ' + mat + str(np.round(np.nanmedian(r1median), 2)) + '\pm ' + str(np.round(qerr_r1, 2)) + mat + ' & ')
    # # +
    # #            mat + str(round(np.nanmedian(r2median), 2)) + '\pm ' + str(round(qerr_r2, 2)) + mat +
    # #            str(round(np.nanmedian(r3median), 2)) + '\pm ' + str(round(qerr_r3, 2)) + mat + ' & ' + mat +
    # #            str(round(np.nanmedian(r4median), 2)) + '\pm ' + str(round(qerr_r4, 2)) + mat + r'\\' + '\n')
    # # file.write('\hline' + '\n')
    file.write('Median & ' + mat + str(round(np.nanmedian(r1median), 2)) + '\pm ' + str(round(qerr_1, 2)) + mat + ' & ' +
mat + str(round(np.nanmedian(r2median), 2)) + '\pm ' + str(round(qerr_2, 2)) + mat + ' & ' +
        mat + str(round(np.nanmedian(r3median), 2)) + '\pm ' + str(round(qerr_3, 2)) + mat + ' & ' +
        mat + str(round(np.nanmedian(r4median), 2)) + '\pm ' + str(round(qerr_4, 2)) + mat + r'\\' + '\n')

    file.write('\hline' + '\n')
    file.write('Mean R2-R4 &' + mat + str(round(np.nanmean(rmean[1:4]), 2)) + '\pm ' + str(
        round(np.nanstd(rmean[1:4]), 2)) + mat + ' & ' + r'\\' + '\n')
    file.write('Median R2-R4 &' + mat + str(round(np.nanmedian(rmedian[1:4]), 2)) + '\pm ' + str(
        round(mederr, 2)) + mat + ' & ' + r'\\' + '\n')

    return rmean, rstd, rmedian, qerr


######
def ratiofunction_beta_9602(df, sim, team, categorystr, boolib0, slow, fast):

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

    dft = {}
    df1 = {}
    df2 = {}

    df['iB0'] = 0.014

    Pval_komhyr = np.array([1000, 199, 59, 30, 20, 10, 7, 5])
    komhyr_sp_tmp = np.array([1, 1.007, 1.018, 1.022, 1.032, 1.055, 1.070, 1.092])
    komhyr_en_tmp = np.array([1, 1.007, 1.018, 1.029, 1.041, 1.066, 1.087, 1.124])

    komhyr_sp = [1 / i for i in komhyr_sp_tmp]
    komhyr_en = [1 / i for i in komhyr_en_tmp]

    file = open('../Latex/9602_TimeConstant_' + categorystr + "5secslatex_table.txt", "w")
    file.write(categorystr + '\n')

    print('len sim', len(sim))

    for j in range(len(sim)):
        # print('simarray', sim[j])
        title = str(sim[j]) + '-' + str(team[j])

        dftj = df[(df.Sim == sim[j]) & (df.Team == team[j])]
        dftj.reset_index(inplace=True)


        size = len(dftj)
        Ums_i = [0] * size
        Ua_i = [0] * size
        Ums_i[0] = dftj.at[0, 'IM']

        ## only convolute slow part of the signal, which is needed for beta calculation
        for k in range(size - 1):

            ## komhyr corrections
            for p in range(len(komhyr_en) - 1):

                if dftj.at[k, 'ENSCI'] == 1:
                    if (dftj.at[k, 'Pair'] >= Pval_komhyr[p + 1]) & (dftj.at[k, 'Pair'] < Pval_komhyr[p]):
                        # print(p, Pval[p + 1], Pval[p ])
                        dftj.at[k, 'I_OPM_komhyr'] = dftj.at[k, 'PO3_OPM'] * dftj.at[k, 'PFcor'] * komhyr_en[p] / \
                                                   (dftj.at[k, 'TPint'] * 0.043085)
                if dftj.at[k, 'ENSCI'] == 0:
                    if (dftj.at[k, 'Pair'] >= Pval_komhyr[p + 1]) & (dftj.at[k, 'Pair'] < Pval_komhyr[p]):
                        # print(p, Pval[p + 1], Pval[p ])
                        dftj.at[k, 'I_OPM_komhyr'] = dftj.at[k, 'PO3_OPM'] * dftj.at[k, 'PFcor'] * komhyr_sp[p] / \
                                                   (dftj.at[k, 'TPint'] * 0.043085)

            if (dftj.at[k, 'Pair'] <= Pval_komhyr[7]):

                if dftj.at[k, 'ENSCI'] == 1:
                    dftj.at[k, 'I_OPM_komhyr'] = dftj.at[k, 'PO3_OPM'] * dftj.at[k, 'PFcor'] * komhyr_en[7] / \
                                               (dftj.at[k, 'TPint'] * 0.043085)
                if dftj.at[k, 'ENSCI'] == 0:
                    dftj.at[k, 'I_OPM_komhyr'] = dftj.at[k, 'PO3_OPM'] * dftj.at[k, 'PFcor'] * komhyr_sp[7] / \
                                               (dftj.at[k, 'TPint'] * 0.043085)

            size = len(dftj)
            Ums_i = [0] * size
            Ua_i = [0] * size
            Ums_i[0] = dftj.at[0, 'IM']

            ## only convolute slow part of the signal, which is needed for beta calculation
        for ik in range(size - 1):


            Ua_i = dftj.at[ik + 1, 'I_OPM_jma']
            t1 = dftj.at[ik + 1, 'Tsim']
            t2 = dftj.at[ik, 'Tsim']
            Xs = np.exp(-(t1 - t2) / slow)
            Xf = np.exp(-(t1 - t2) / fast)
            Ums_i[ik + 1] = Ua_i - (Ua_i - Ums_i[ik]) * Xs

        dftj['I_conv_slow_jma'] = Ums_i

        year = (dftj.iloc[0]['JOSIE_Nr'])

        rt1 = (dftj.iloc[0]['R1_Tstop'])
        rt2 = (dftj.iloc[0]['R2_Tstop'])
        if sim[j] == 90: rt1 = 1050
        t1 = (dftj.Tsim <= rt1 ) & (dftj.Tsim >= rt1 - 5)
        t2 = (dftj.Tsim <= rt2 ) & (dftj.Tsim >= rt2 - 5)
        #
        df1[j] = dftj[t1]
        df2[j] = dftj[t2]
        # c = df1[j].IM .tolist()
        # sc = ( df1[j].I_conv_slow.tolist())

        if not boolib0:
            r1[j] = np.array((df1[j].IM / (0.10 * df1[j].I_conv_slow_jma)).tolist())
            r2[j] = np.array((df2[j].IM / (0.10 * df2[j].I_conv_slow_jma)).tolist())


        if boolib0:
            r1[j] = np.array(((df1[j].IM - df1[j].iB0) / (0.10 * df1[j].I_conv_slow_jma)).tolist())
            r2[j] = np.array(((df2[j].IM - df2[j].iB0) / (0.10 * df2[j].I_conv_slow_jma)).tolist())

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

        file.write(mat + str(int(year)) + '-' + title + mat + ' & ' + mat + lr1 + mat + ' & ' + mat + lr2 + mat + ' & ' + mat + lr3 + mat +
                   ' & ' + mat + lr4 + mat + r'\\' + '\n')

    rmean = [r1mean, r2mean]
    rstd = [r1std, r2std]
    rmedian = [r1median, r2median]
    rqerr = [qerr_r1, qerr_r2]

    qerr_1 = (np.nanquantile(r1median, 0.75) - np.nanquantile(r1median, 0.25)) / (2 * 0.6745)
    qerr_2 = (np.nanquantile(r2median, 0.75) - np.nanquantile(r2median, 0.25)) / (2 * 0.6745)

    mederr = (np.nanquantile(rmedian, 0.75) - np.nanquantile(rmedian, 0.25)) / (2 * 0.6745)


    file.write('\hline' + '\n')
    file.write('\hline' + '\n')
    file.write('Mean & ' + mat + str(round(np.nanmean(r1mean), 2)) + '\pm ' + str(round(np.nanstd(r1mean), 2)) + mat + ' & ' +
               mat + str(round(np.nanmean(r2mean), 2)) + '\pm ' + str(round(np.nanstd(r2mean), 2)) + mat  + r'\\' + '\n')
    file.write('Median  & ' + mat + str(round(np.nanmedian(r1median), 2)) + '\pm ' + str(round(qerr_1, 2)) + mat + ' & ' +
               mat + str(round(np.nanmedian(r2median), 2)) + '\pm ' + str(round(qerr_2, 2)) + mat  + r'\\' + '\n')
    file.write('\hline' + '\n')
    file.write('\hline' + '\n')
    file.write('Mean R1-R2 &' + mat + str(round(np.nanmean(rmean), 2)) + '\pm ' + str(round(np.nanstd(rmean), 2)) + mat + ' & '+ r'\\' + '\n')
    file.write('Median R1-R2 &' + mat + str(round(np.nanmedian(rmedian), 2)) + '\pm ' + str(round(mederr, 2)) + mat + ' & '+ r'\\' + '\n')

    file.close()



    return rmean, rstd, rmedian, rqerr
