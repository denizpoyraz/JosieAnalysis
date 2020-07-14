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


df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_deconv_beta0_tempfixed_paper.csv", low_memory=False)

# dft/ = {}

simlist = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Sim'])
teamlist = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Team'])

for j in range(len(simlist)):

    r1_min = 2100;
    r1_max = 2400;
    r2_min = 4100;
    r2_max = 4400;
    r3_min = 6100;
    r3_max = 6400;
    r4_min = 8100;
    r4_max = 8400

    if simlist[j] == 140:
        r1_min = 2450;
        r1_max = 2750;
        r2_min = 4450;
        r2_max = 4750;
        r3_min = 6450;
        r3_max = 6750;
        r4_min = 8450;
        r4_max = 8750

    dft = df[(df.Sim == simlist[j]) & (df.Team == teamlist[j])]
    title = str(simlist[j]) + '_' + str(teamlist[j])

    #
    # time_r1_b = np.array(dft[j][(dft[j].Tsim > r1_min) & (dft[j].Tsim < r1_max)].Tsim.tolist())
    # time_r1 = time_r1_b = r1_min
    # current_r1 = np.array(dft[(dft[j].Tsim > r1_min) & (dft[j].Tsim < r2_min)].Ifast_minib0.tolist())

    time_r1_b, time_r1, current_r1 = make_rangearray(dft, r1_min, r1_max)
    time_r2_b, time_r2, current_r2 = make_rangearray(dft, r2_min, r2_max)
    time_r3_b, time_r3, current_r3 = make_rangearray(dft, r3_min, r3_max)
    time_r4_b, time_r4, current_r4 = make_rangearray(dft, r4_min, r4_max)

    mod = Model(fit_func)
    # pars = mod.make_params(A=0.5, tfast=20)
    mod.set_param_hint('A', value=1, min=0, max=20)
    mod.set_param_hint('tfast', value=20, min=10, max=40)

    out1 = mod.fit(current_r1, t=time_r1)
    out2 = mod.fit(current_r2, t=time_r2)
    out3 = mod.fit(current_r3, t=time_r3)
    out4 = mod.fit(current_r4, t=time_r4)

    print(title, out1.params['A'].value, out2.params['A'].value, out3.params['A'].value, out4.params['A'].value, )
    print( out1.params['tfast'].value, out2.params['tfast'].value, out3.params['tfast'].value, out4.params['tfast'].value, )

    fig, ax = plt.subplots()

    plt.title(title)

    plt.plot(dft[(dft.Tsim > 1500) & (dft.Tsim < 9000)].Tsim, dft[(dft.Tsim > 1500) & (dft.Tsim < 9000)].Ifast_minib0)
    plt.plot(time_r1_b, out1.best_fit, 'r--', label='fit R1')
    plt.plot(time_r2_b, out2.best_fit, 'r--', label='fit R2')
    plt.plot(time_r3_b, out3.best_fit, 'r--', label='fit R3')
    plt.plot(time_r4_b, out4.best_fit, 'r--', label='fit R4')

    plt.show()
    plt.close()
