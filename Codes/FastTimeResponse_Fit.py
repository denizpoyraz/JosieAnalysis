import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
import numpy as np
from lmfit import Model

def fit_func(t, A, tfast):
    return A * np.exp(-t/tfast)

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
    plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/TimeResponseFit/' + title + '_' + rangestr + '.png')
    # plt.show()
    plt.close()




def mainfunction(dff, simlistf, teamlistf, filef, category, boolpersim):

    A1array = [0] * len(simlistf)
    A2array = [0] * len(simlistf)
    A3array = [0] * len(simlistf)
    A4array = [0] * len(simlistf)

    tf1array = [0] * len(simlistf)
    tf2array = [0] * len(simlistf)
    tf3array = [0] * len(simlistf)
    tf4array = [0] * len(simlistf)

    measured_mass = [0] * len(simlistf)
    integrated_mass = [0] * len(simlistf)

    filef.write(category + '\n')



    for j in range(len(simlistf)):

        r1_min = 2103;
        r1_max = 2403;
        r2_min = 4103;
        r2_max = 4403;
        r3_min = 6103;
        r3_max = 6403;
        r4_min = 8103;
        r4_max = 8410

        if simlistf[j] == 140:
            r1_min = 2450; r1_max = 2750; r2_min = 4450; r2_max = 4750; r3_min = 6450; r3_max = 6750; r4_min = 8450; r4_max = 8750
        if simlistf[j] == 161:
            r1_min = 2160; r1_max = 2460; r2_min = 4150; r2_max = 4450; r3_min = 6160; r3_max = 6460; r4_min = 8150; r4_max = 8460
        if (simlistf[j] == 167) | (simlistf[j] == 164):
            r1_min = 2130; r1_max = 2460; r2_min = 4130; r2_max = 4450;  r3_min = 6130;  r3_max = 6460; r4_min = 8130; r4_max = 8460
        if simlistf[j] == 162:
            r1_min = 2165; r1_max = 2465; r2_min = 4150; r2_max = 4450;  r3_min = 6165;  r3_max = 6460; r4_min = 8165; r4_max = 8460
        if simlistf[j] == 166:
            r1_min = 2260; r1_max = 2465; r2_min = 4260; r2_max = 4450;  r3_min = 6260;  r3_max = 6460; r4_min = 8260; r4_max = 8460
        if simlistf[j] == 163:
            r1_min = 2150; r1_max = 2450; r2_min = 4150; r2_max = 4450;  r3_min = 6150;  r3_max = 6460; r4_min = 8150; r4_max = 8460


        dft = dff[(dff.Sim == simlistf[j]) & (dff.Team == teamlistf[j])]
        title = str(simlistf[j]) + '-' + str(teamlistf[j])

        measured_mass[j] = round(np.nanmean(dft['Diff']),2)
        integrated_mass[j] = round(np.trapz(dft.massloss, x=dft.Tsim),2)

        time_r1_b, time_r1, current_r1 = make_rangearray(dft, r1_min, r1_max)
        time_r2_b, time_r2, current_r2 = make_rangearray(dft, r2_min, r2_max)
        time_r3_b, time_r3, current_r3 = make_rangearray(dft, r3_min, r3_max)
        time_r4_b, time_r4, current_r4 = make_rangearray(dft, r4_min, r4_max)

        mod = Model(fit_func)
        # pars = mod.make_params(A=0.5, tfast=20)
        mod.set_param_hint('A', value=1, min=0, max=20)
        mod.set_param_hint('tfast', value=20, min=15, max=35)

        out1 = mod.fit(current_r1, t=time_r1)
        out2 = mod.fit(current_r2, t=time_r2)
        out3 = mod.fit(current_r3, t=time_r3)
        out4 = mod.fit(current_r4, t=time_r4)

        A1array[j] = round(out1.params['A'].value,2)
        A2array[j] = round(out2.params['A'].value,2)
        A3array[j] = round(out3.params['A'].value,2)
        A4array[j] = round(out4.params['A'].value,2)

        tf1array[j] = round(out1.params['tfast'].value,2)
        tf2array[j] = round(out2.params['tfast'].value,2)
        tf3array[j] = round(out3.params['tfast'].value,2)
        tf4array[j] = round(out4.params['tfast'].value,2)

        mat = '$'
        end = ' & '

        if boolpersim:

            # filef.write('\hline' + '\n')
            # filef.write(mat + title + mat + end + 'A' + mat + end + mat +  str(A1array[j]) + mat + ' & ' + mat +  str(A2array[j]) + mat + ' & ' + mat +
            #            str(A3array[j]) + mat + ' & ' + mat +  str(A4array[j]) + mat + r'\\' + '\n')
            filef.write(mat + title + mat   + end + mat +  str(tf1array[j]) + mat + end + mat +  str(tf2array[j]) + mat + end + mat +
                       str(tf3array[j]) + mat + end + mat +  str(tf4array[j]) + mat +  end + mat + str(measured_mass[j]) + mat + end
            + mat + str(integrated_mass[j]) + mat + r'\\' + '\n')


        # if (simlistf[j] == 148) | (simlistf[j] == 144) | (simlistf[j] == 164):

        plot_eachrange(dft, r1_min, r1_max, time_r1_b, out1, title, 'R1')
        plot_eachrange(dft, r2_min, r2_max, time_r2_b, out2, title, 'R2')
        plot_eachrange(dft, r3_min, r3_max, time_r3_b, out3, title, 'R3')
        plot_eachrange(dft, r4_min, r4_max, time_r4_b, out4, title, 'R4')

    Aarray = [A1array, A2array, A3array, A4array]
    tarray = [tf1array, tf2array, tf3array, tf4array]

    meanA = round(np.nanmean(Aarray),2)
    meant = round(np.nanmean(tarray),2)
    stdA = round(np.nanstd(Aarray),2)
    stdt = round(np.nanstd(tarray),2)
    medianA = round(np.nanmedian(Aarray),2)
    mediant = round(np.nanmedian(tarray),2)
    medianmeas = round(np.nanmedian(measured_mass),2)
    medianint = round(np.nanmedian(integrated_mass),2)
    meanmeas = round(np.nanmean(measured_mass), 2)
    meanint = round(np.nanmean(integrated_mass), 2)

    # print('test', medianint, medianmeas)

    filef.write('\hline' + '\n')
    filef.write( 'mean ' + ' ' + end + mat + str(round(np.nanmean(tf1array),2)) + mat + ' &  ' + mat + str(round(np.nanmean(tf2array),2)) + mat + ' & ' + mat +
        str(round(np.nanmean(tf3array),2)) + mat +  ' & ' + mat + str(round(np.nanmean(tf4array),2)) + mat + end + mat + str(meanmeas) + mat + end + mat
    + str(meanint) + mat + r'\\' + '\n')
    filef.write('median ' + ' ' + end + mat + str(round(np.nanmedian(tf1array),2)) + mat + ' &  ' + mat + str(round(
        np.nanmedian(tf2array),2)) + mat + ' & ' + mat +
                str(round(np.nanmedian(tf3array),2)) + mat + ' & ' + mat + str(round(np.nanmedian(tf4array),2)) + mat
                + end + mat + str(medianmeas) + mat + end + mat + str(medianint) + mat + r'\\' + '\n')
    filef.write( 'mean ' + ' ' + end + mat + str(meant) + mat + ' $\pm$ ' + mat + str(stdt) + mat+ r'\\' + '\n')
    filef.write( 'median ' + ' ' + end + mat + str(mediant) + mat + r'\\' + '\n')

    # return meanA, meant, medianA, mediant, stdA, stdt
    print(meant, mediant, stdt)


df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_deconv_beta0_tempfixed_paper.csv", low_memory=False)

df = df[df.ADX == 0]

df = df.drop(df[(df.Sim == 147) & (df.Team == 3)].index)
df = df.drop(df[(df.Sim == 158) & (df.Team == 1)].index)
df = df.drop(df[(df.Sim == 158) & (df.Team == 2)].index)
df = df.drop(df[(df.Sim == 160) & (df.Team == 4)].index)
df = df.drop(df[(df.Sim == 165) & (df.Team == 4)].index)
## new
df = df.drop(df[(df.Sim == 167) & (df.Team == 4)].index)


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

#
# file = open('0910_TimeResponse_Fit_en0505.txt', "w")
# file.write('EN 0.5%-0.5B' + '\n')
# mainfunction(df, sim_en0505, team_en0505, file, 'EN 0.5%-0.5B', 1)
# file.close()
# #
# file = open('0910_TimeResponse_Fit_en1010.txt', "w")
# file.write('EN 1.0%-1.0B' + '\n')
# mainfunction(df, sim_en1010, team_en1010, file, 'EN 1.0%-1.0B', 1)
# file.close()
#
# file = open('0910_TimeResponse_Fit_sp0505.txt', "w")
# file.write('SP 0.5%-0.5B' + '\n')
# mainfunction(df, sim_sp0505, team_sp0505, file, 'SP 0.5%-0.5B', 1)
# file.close()
#
# file = open('0910_TimeResponse_Fit_sp01010.txt', "w")
# file.write('SP 1.0%-1.0B' + '\n')
# mainfunction(df, sim_sp1010, team_sp1010, file, 'SP 1.0%-1.0B', 1)
# file.close()
#
file = open('0910_TimeResponse_Fit.txt', "w")
mainfunction(df, simlist, teamlist, file, 'all', 0)
file.close()

#



