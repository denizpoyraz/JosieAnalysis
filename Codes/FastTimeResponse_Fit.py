import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
import numpy as np
from lmfit import Model

def fit_func(t, A, tfast):
    return A * np.exp(-t/tfast)

def fit_func_wc(t, A, tfast, C):
    return A * np.exp(-t/tfast) + C

def  make_rangearray(dff, t1, t2):

    time_r_b = np.array(dff[(dff.Tsim > t1) & (dff.Tsim < t2)].Tsim.tolist())
    time_r = time_r_b - t1
    current_r = np.array(dff[(dff.Tsim > t1) & (dff.Tsim < t2)].Ifast_minib0.tolist())

    return time_r_b, time_r, current_r

def plot_eachrange(dff, rmin, rmax, timeb, fitout,  title, rangestr):

    fig, ax = plt.subplots()
    plt.title(title)
    # plt.plot(dft[(dft.Tsim > 1500) & (dft.Tsim < 9000)].Tsim, dft[(dft.Tsim > 1500) & (dft.Tsim < 9000)].Ifast_minib0)
    plt.xlim([rmin - 200, rmax + 200])
    plt.plot(dff.Tsim, dff.Ifast_minib0, label='Ifast - iB0')
    plt.plot(timeb, fitout.best_fit, 'r--', label= 'fit ' + rangestr )
    ax.legend(loc='best', frameon=False, fontsize='small')

    # plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/TimeResponseFit/' + title + '_' + rangestr + '.png')
    # plt.show()
    plt.close()


def mainfunction(dff, simlistf, teamlistf, filef, category, boolpersim):

    timeconstant = 1

    A1array = [0] * len(simlistf)
    A2array = [0] * len(simlistf)
    A3array = [0] * len(simlistf)
    A4array = [0] * len(simlistf)

    tf1array = [0] * len(simlistf)
    tf2array = [0] * len(simlistf)
    tf3array = [0] * len(simlistf)
    tf4array = [0] * len(simlistf)
    tf1array_err = [0] * len(simlistf)
    tf2array_err = [0] * len(simlistf)
    tf3array_err = [0] * len(simlistf)
    tf4array_err = [0] * len(simlistf)

    C1array = [0] * len(simlistf)
    C2array = [0] * len(simlistf)
    C3array = [0] * len(simlistf)
    C4array = [0] * len(simlistf)

    C1array_err = [0] * len(simlistf)
    C2array_err = [0] * len(simlistf)
    C3array_err = [0] * len(simlistf)
    C4array_err = [0] * len(simlistf)

    measured_mass = [0] * len(simlistf)
    integrated_mass = [0] * len(simlistf)

    filef.write(category + '\n')

    fix = 10
    nsec = 60

    for j in range(len(simlistf)):

        r1_min = 2103 +fix;
        r1_max = r1_min+nsec;
        r2_min = 4103+fix;
        r2_max = r2_min+nsec;
        r3_min = 6103+fix;
        r3_max = r3_min+nsec;
        r4_min = 8103+fix;
        r4_max = r4_min+nsec

        if simlistf[j] == 140:
            r1_min = 2450; r1_max = r1_min+nsec; r2_min = 4450; r2_max = r2_min+nsec; r3_min = 6450; r3_max = r3_min+nsec; r4_min = 8450; r4_max = r4_min+nsec
        if simlistf[j] == 143:
            r1_min = 2103 +fix; r1_max = r1_min+nsec; r2_min = 4103 +fix; r2_max = r2_min+nsec; r3_min = 6103 +fix; r3_max = r3_min+nsec; r4_min = 8103 +fix; r4_max = r4_min+nsec
        if simlistf[j] == 161:
            r1_min = 2160; r1_max = r1_min+nsec; r2_min = 4150; r2_max = r2_min+nsec; r3_min = 6160; r3_max = r3_min+nsec; r4_min = 8150; r4_max = r4_min+nsec
        if (simlistf[j] == 167) | (simlistf[j] == 164):
            r1_min = 2130; r1_max = r1_min+nsec; r2_min = 4130; r2_max = r2_min+nsec;  r3_min = 6130;  r3_max = r3_min+nsec; r4_min = 8130; r4_max = r4_min+nsec
        if simlistf[j] == 162:
            r1_min = 2165; r1_max = r1_min+nsec; r2_min = 4150; r2_max = r2_min+nsec;  r3_min = 6165;  r3_max = r3_min+nsec; r4_min = 8165; r4_max = r4_min+nsec
        if simlistf[j] == 166:
            r1_min = 2260; r1_max = r1_min+nsec; r2_min = 4260; r2_max = r2_min+nsec;  r3_min = 6260;  r3_max = r3_min+nsec; r4_min = 8260; r4_max = r4_min+nsec
        if simlistf[j] == 163:
            r1_min = 2150; r1_max = r1_min+nsec; r2_min = 4150; r2_max = r2_min+nsec;  r3_min = 6150;  r3_max = r3_min+nsec; r4_min = 8150; r4_max = r4_min+nsec


        dft = dff[(dff.Sim == simlistf[j]) & (dff.Team == teamlistf[j])]
        title = str(simlistf[j]) + '-' + str(teamlistf[j])

        measured_mass[j] = round(np.nanmean(dft['Diff']),2)
        # EN1010_mass[j] = np.nanmean(dft[j]['Diff'])
        # EN1010_mass[j] = np.nanmean(dft[j]['PostTestSolution_Lost_gr'])
        integrated_mass[j] = round(np.trapz(dft.massloss, x=dft.Tsim),2)

        time_r1_b, time_r1, current_r1 = make_rangearray(dft, r1_min, r1_max)
        time_r2_b, time_r2, current_r2 = make_rangearray(dft, r2_min, r2_max)
        time_r3_b, time_r3, current_r3 = make_rangearray(dft, r3_min, r3_max)
        time_r4_b, time_r4, current_r4 = make_rangearray(dft, r4_min, r4_max)

        mod0 = Model(fit_func)
        mod = Model(fit_func)
        # mod = Model(fit_func_wc)
        # pars = mod.make_params(A=0.5, tfast=20)
        mod.set_param_hint('A', value=1, min=0, max=20)
        mod.set_param_hint('tfast', value=20, min=15, max=35)
        # mod.set_param_hint('C', value=0.05, min=-0.1, max=1)
        
        mod0.set_param_hint('A', value=1, min=0, max=20)
        mod0.set_param_hint('tfast', value=20, min=15, max=35)

        out1 = mod.fit(current_r1, t=time_r1)
        out2 = mod.fit(current_r2, t=time_r2)
        out3 = mod.fit(current_r3, t=time_r3)
        out4 = mod.fit(current_r4, t=time_r4)
        
        out1_0 = mod0.fit(current_r1, t=time_r1)
        out2_0 = mod0.fit(current_r2, t=time_r2)
        out3_0 = mod0.fit(current_r3, t=time_r3)
        out4_0 = mod0.fit(current_r4, t=time_r4)

        A1array[j] = round(out1.params['A'].value,2)
        A2array[j] = round(out2.params['A'].value,2)
        A3array[j] = round(out3.params['A'].value,2)
        A4array[j] = round(out4.params['A'].value,2)

        tf1array[j] = round(out1.params['tfast'].value,2)
        tf2array[j] = round(out2.params['tfast'].value,2)
        tf3array[j] = round(out3.params['tfast'].value,2)
        tf4array[j] = round(out4.params['tfast'].value,2)


        # print(j, title)
        tf1array_err[j] = round(out1.params['tfast'].stderr,2)
        tf2array_err[j] = round(out2.params['tfast'].stderr,2)
        tf3array_err[j] = round(out3.params['tfast'].stderr,2)
        tf4array_err[j] = round(out4.params['tfast'].stderr,2)

        # # stderr
        # C1array[j] = round(out1.params['C'].value,4)
        # C2array[j] = round(out2.params['C'].value,4)
        # C3array[j] = round(out3.params['C'].value,4)
        # C4array[j] = round(out4.params['C'].value,4)
        # C1array_err[j] = round(out1.params['C'].value,4)
        # C2array_err[j] = round(out2.params['C'].value,4)
        # C3array_err[j] = round(out3.params['C'].value,4)
        # C4array_err[j] = round(out4.params['C'].value,4)

        # print(title)
        # print(current_r2)
        # print(A1array[j], tf1array[j], C1array[j] , dft[(dft.Tsim < r1_min + 2) & (dft.Tsim > r1_min-2)].Ifast_minib0.tolist()[0])
        # print(A2array[j], tf2array[j], C2array[j], dft[(dft.Tsim < r2_min + 2) & (dft.Tsim > r2_min-2)].Ifast_minib0.tolist()[0])
        # print(A3array[j], tf3array[j], C3array[j], dft[(dft.Tsim < r3_min + 2) & (dft.Tsim > r3_min-2)].Ifast_minib0.tolist()[0])
        # print(A4array[j], tf4array[j], C4array[j], dft[(dft.Tsim < r4_min + 2) & (dft.Tsim > r4_min-2)].Ifast_minib0.tolist()[0])


        # print(j, title, ' ', C1array[j], ' ',  C2array[j], ' ' ,C3array[j], ' ' , C4array[j])
        # print(j, title, ' C ' , round(out1.params['C'].value,2), ' error ', round(out1.params['C'].stderr,2), ' chi2 ', round(out1.chisqr,2), ' ',
        #       ' red chi2 ', round(out1.redchi,2))

        # print(j, title, round(out1_0.redchi,2), ' ', round(out2_0.redchi,2), ' ', round(out3_0.redchi,2), ' ', round(out4_0.redchi,2) )
        # print(j, title, round(out1.redchi,2), ' ', round(out2.redchi,2), ' ', round(out3.redchi,2), ' ', round(out4.redchi,2) )


        mat = '$'
        end = ' & '
        pm = '\pm'

        if boolpersim:

            if timeconstant:

                filef.write(mat + title + mat   + end + mat +  str(tf1array[j]) + pm + str(tf1array_err[j]) + mat + end + mat +
                            str(tf2array[j])  + pm + str(tf2array_err[j]) + mat + end + mat +
                           str(tf3array[j])  + pm + str(tf3array_err[j])  + mat + end + mat +
                            str(tf4array[j]) + pm + str(tf4array_err[j]) + mat  + r'\\' + '\n')

            if not timeconstant:

                filef.write(mat + title + mat   + end + mat +  str(C1array[j]) + pm + str(C1array_err[j]) + mat + end + mat +
                            str(C2array[j])  + pm + str(C2array_err[j]) + mat + end + mat +
                           str(C3array[j])  + pm + str(C3array_err[j])  + mat + end + mat +
                            str(C4array[j]) + pm + str(C4array_err[j]) + mat  + r'\\' + '\n')


        # if (simlistf[j] == 148) | (simlistf[j] == 144) | (simlistf[j] == 164):

        plot_eachrange(dft, r1_min, r1_max, time_r1_b, out1, title, 'R1')
        plot_eachrange(dft, r2_min, r2_max, time_r2_b, out2, title, 'R2')
        plot_eachrange(dft, r3_min, r3_max, time_r3_b, out3, title, 'R3')
        plot_eachrange(dft, r4_min, r4_max, time_r4_b, out4, title, 'R4')

    Aarray = [A1array, A2array, A3array, A4array]
    tarray = [tf1array, tf2array, tf3array, tf4array]
    Carray = [C1array, C2array, C3array, C4array]

    meanA = round(np.nanmean(Aarray),2)
    meant = round(np.nanmean(tarray),2)
    meanC = round(np.nanmean(Carray),4)

    stdA = round(np.nanstd(Aarray),2)
    stdt = round(np.nanstd(tarray),2)
    stdC = round(np.nanstd(tarray),4)
    medianA = round(np.nanmedian(Aarray),2)
    mediant = round(np.nanmedian(tarray),2)
    medianmeas = round(np.nanmedian(measured_mass),2)
    medianint = round(np.nanmedian(integrated_mass),2)
    meanmeas = round(np.nanmean(measured_mass), 2)
    meanint = round(np.nanmean(integrated_mass), 2)
    medianC = round(np.nanmedian(Carray),4)

    # print('test', medianint, medianmeas)

    if timeconstant:

        filef.write('\hline' + '\n')
        filef.write( 'mean ' + ' ' + end + mat + str(round(np.nanmean(tf1array),2)) + mat + ' &  ' + mat + str(round(np.nanmean(tf2array),2)) + mat + ' & ' + mat +
            str(round(np.nanmean(tf3array),2)) + mat + ' & ' + mat + str(round(np.nanmean(tf4array),2)) + mat + r'\\' + '\n')
        filef.write('median ' + ' ' + end + mat + str(round(np.nanmedian(tf1array),2)) + mat + ' &  ' + mat + str(round(
            np.nanmedian(tf2array),2)) + mat + ' & ' + mat +
                    str(round(np.nanmedian(tf3array),2)) + mat + ' & ' + mat + str(round(np.nanmedian(tf4array),2)) +  mat + r'\\' + '\n')
        filef.write( 'mean ' + ' ' + end + mat + str(meant) + mat + ' $\pm$ ' + mat + str(stdt) + mat+ r'\\' + '\n')
        filef.write( 'median ' + ' ' + end + mat + str(mediant) + mat + r'\\' + '\n')


    if not timeconstant:

        filef.write('\hline' + '\n')
        filef.write('mean ' + ' ' + end + mat + str(round(np.nanmean(C1array), 4)) + mat + ' &  ' + mat + str(
            round(np.nanmean(C2array), 4)) + mat + ' & ' + mat +
                    str(round(np.nanmean(C3array), 4)) + mat + ' & ' + mat + str(
            round(np.nanmean(C4array), 4)) + mat + r'\\' + '\n')
        filef.write('median ' + ' ' + end + mat + str(round(np.nanmedian(C1array), 4)) + mat + ' &  ' + mat + str(round(
            np.nanmedian(C2array), 4)) + mat + ' & ' + mat +
                    str(round(np.nanmedian(C3array), 4)) + mat + ' & ' + mat + str(
            round(np.nanmedian(C4array), 4)) + mat + r'\\' + '\n')
        filef.write('mean ' + ' ' + end + mat + str(meanC) + mat + ' $\pm$ ' + mat + str(stdC) + mat + r'\\' + '\n')
        filef.write('median ' + ' ' + end + mat + str(medianC) + mat + r'\\' + '\n')

    # return meanA, meant, medianA, mediant, stdA, stdt
    # print(meant, mediant, medianC, stdt)


df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_deconv_beta0_tempfixed_paper.csv", low_memory=False)

df = df[df.ADX == 0]

df = df.drop(df[(df.Sim == 147) & (df.Team == 3)].index)
df = df.drop(df[(df.Sim == 158) & (df.Team == 1)].index)
df = df.drop(df[(df.Sim == 158) & (df.Team == 2)].index)
df = df.drop(df[(df.Sim == 160) & (df.Team == 4)].index)
df = df.drop(df[(df.Sim == 165) & (df.Team == 4)].index)
## new
df = df.drop(df[(df.Sim == 167) & (df.Team == 4)].index)

df = df[(df.Year == 2010)]


# dft/ = {}

simlist = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Sim'])
teamlist = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Team'])

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

# #
file = open('tables/10_TimeResponse_Fit_10_60_seconds_en0505.txt', "w")
# # file = open('10_TimeResponse_Fit_10_60_seconds_constantterm_en0505.txt', "w")
#
file.write('EN 0.5%-0.5B' + '\n')
mainfunction(df, sim_en0505, team_en0505, file, 'EN 0.5%-0.5B', 1)
file.close()
# # # #
file = open('tables/10_TimeResponse_Fit_10_60_seconds_en1010.txt', "w")
file.write('EN 1.0%-1.0B' + '\n')
mainfunction(df, sim_en1010, team_en1010, file, 'EN 1.0%-1.0B', 1)
file.close()

file = open('tables/10_TimeResponse_Fit_10_60_seconds_sp0505.txt', "w")
file.write('SP 0.5%-0.5B' + '\n')
mainfunction(df, sim_sp0505, team_sp0505, file, 'SP 0.5%-0.5B', 1)
file.close()

file = open('tables/10_TimeResponse_Fit_10_60_seconds_sp01010.txt', "w")
file.write('SP 1.0%-1.0B' + '\n')
mainfunction(df, sim_sp1010, team_sp1010, file, 'SP 1.0%-1.0B', 1)
file.close()
#
file = open('tables/10_TimeResponse_Fit_10_60_seconds.txt', "w")
mainfunction(df, simlist, teamlist, file, 'all', 0)
file.close()





