import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.gridspec as gridspec

columnString = "Time Press GeopAlt Temp RH O3_mPa O3_ppmv O3_DU Wind_Dir Wind_Spd TPump O3CellI GPS_Lon GPS_Lat GPS_Alt"
columnStr = columnString.split(" ")
print(columnStr)


filename = "/home/poyraden/Analysis/Homogenization_Analysis/Files/Costa_Rica/costarica_20100212T13_SHADOZV06.dat"

df = pd.read_csv(filename, sep="\s+", engine="python", skiprows=37, names=columnStr)






df.to_csv("/home/poyraden/Analysis/Homogenization_Analysis/Files/Costa_Rica/Proccessed/costarica_20100212.csv")


dfo = df.copy()

### now make this data set in equal time steps
df = df.drop_duplicates(subset=['Time'], keep='first')
df = df.reset_index()

df['iB0'] = 0.020
df['PFcor'] = 100 / 27.7

Pval = np.array([1000, 730, 535, 382, 267, 185, 126, 85, 58, 39, 26.5, 18.1, 12.1, 8.3, 6])
JMA = np.array([0.999705941, 0.997216654, 0.995162562, 0.992733959, 0.989710199, 0.985943645, 0.981029252, 0.974634364,
                0.966705137, 0.956132227, 0.942864263, 0.9260478, 0.903069813, 0.87528384, 0.84516337])

Pval_komhyr = np.array([1000, 199, 59, 30, 20, 10, 7, 5])
komhyr_sp_tmp = np.array([1, 1.007, 1.018, 1.022, 1.032, 1.055, 1.070, 1.092])
komhyr_en_tmp = np.array([1, 1.007, 1.018, 1.029, 1.041, 1.066, 1.087, 1.124])

komhyr_sp = [1/i for i in komhyr_sp_tmp]
komhyr_en = [1/i for i in komhyr_en_tmp]

# df['PO3'] = (df['TPumpK'] * 0.043085 * (df['O3CellI'] - df['iB0'] )) / (df['PFcor'] )



sec_series = np.array(df['Time'].tolist())

ts = np.zeros(len(sec_series))

for dj in range(len(sec_series)):
    tmp = pd.Timestamp(sec_series[dj], unit='s')
    nt = pd.Timestamp(sec_series[dj], unit='s').time()
    date_time = datetime.datetime.strptime(str(nt), "%H:%M:%S")
    a_timedelta = date_time - datetime.datetime(1900, 1, 1)
    seconds = a_timedelta.total_seconds()
    df.at[dj, 'TS'] = tmp


dfo = df.resample('4S', on='TS').mean().interpolate()
dfo = dfo.reset_index()

for i in range(len(dfo)):
    date_time = datetime.datetime.strptime(str(dfo.at[i, 'TS']), "%Y-%m-%d %H:%M:%S")
    a_timedelta = date_time - datetime.datetime(1970, 1, 1)
    seconds = a_timedelta.total_seconds()
    dfo.at[i, 'nTime'] = seconds



dfo.to_csv("/home/poyraden/Analysis/Homogenization_Analysis/Files/Costa_Rica/Proccessed/costarica_20100212_8secs.csv")

dfo['iB0'] = 0.020
dfo['PFcor'] = 27.7

## now do the convolution to dfo
## jma corrections
Pval = np.array([1000, 730, 535, 382, 267, 185, 126, 85, 58, 39, 26.5, 18.1, 12.1, 8.3, 6])
JMA = np.array([0.999705941, 0.997216654, 0.995162562, 0.992733959, 0.989710199, 0.985943645, 0.981029252, 0.974634364,
                0.966705137, 0.956132227, 0.942864263, 0.9260478, 0.903069813, 0.87528384, 0.84516337])

Pval_komhyr = np.array([1000, 199, 59, 30, 20, 10, 7, 5])
komhyr_sp_tmp = np.array([1, 1.007, 1.018, 1.022, 1.032, 1.055, 1.070, 1.092])
komhyr_en_tmp = np.array([1, 1.007, 1.018, 1.029, 1.041, 1.066, 1.087, 1.124])

komhyr_sp = [1/i for i in komhyr_sp_tmp]
komhyr_en = [1/i for i in komhyr_en_tmp]


tslow = 25 * 60
tfast = 20

size = len(dfo)

Islow = [0] * size
Islow_conv = [0] * size
Islow_conv_test = [0] * size

Ifast = [0] * size
Ifast_deconv = [0] * size
Ifastminib0 = [0] * size
Ifastminib0_deconv = [0] * size


Ifast_deconv_hv = [0] * size
Ifastminib0_deconv_hv = [0] * size
Ifast_deconv_hs = [0] * size
Ifastminib0_deconv_hs = [0] * size

step = 1

beta = 0.03
af = 1
# Islow[0] = beta * dfo.at[0, 'O3CellI']
# Islow[1] = beta * dfo.at[1, 'O3CellI']

# dfo.at[0,'iB0'] = 0.020
# dfo.at[0, 'PFcor'] = 100 / 27.7
# dfo.at[0, 'TPumpK'] = dfo.at[i, 'TPump'] + 273

# Islow_conv_test[0] = 0.001
dfo.at[0, 'iB0'] = 0.020
dfo.at[0, 'PFcor'] = 100 / 27.7
dfo.at[0, 'TPumpK'] = dfo.at[0, 'TPump'] + 273

Islow[0] = beta * dfo.at[0, 'O3CellI']
Islow[1] = beta * dfo.at[1, 'O3CellI']

print('ONE ', Islow[0], Islow[1] )


Islow_conv[0] = 0
Islow_conv[1] = Islow[1] - (Islow[1] - Islow_conv[0]) * np.exp(-(4) / tslow)

print('TWO ', Islow_conv[0],  Islow_conv[1])

for i in range(2, size - step):


    t1 = dfo.at[i+step, 'nTime']
    t2 = dfo.at[i, 'nTime']
    # print(t1, t2)

    Xs = np.exp(-(t1 - t2) / tslow)
    Xf = np.exp(-(t1 - t2) / tfast)


    # ###########  for 2000 data
    dfo.at[i,'iB0'] = 0.020
    dfo.at[i, 'PFcor'] = 100 / 27.7
    dfo.at[i, 'TPumpK'] = dfo.at[i, 'TPump'] + 273

    Islow[i] = beta * dfo.at[i, 'O3CellI']
    # Islow[1] = beta * dfo.at[1, 'O3CellI']
    #
    # Islow_conv[0] = 0
    # Islow_conv[1] = Islow[1] - (Islow[1] - Islow_conv[0]) * Xs

    # Islow[0] = beta * dfo.at[0, 'O3CellI']

    # Islow_conv_test[0] = (1 - Xs) * Islow[0] + Xs * Islow_conv_test[0]
    # print('islow 0', Islow[0], Islow[1], Islow_conv_test[0])

    # Islow_conv[1] = Islow[1] - (Islow[1] ) * Xs


    Islow_conv[i+step] = Islow[i+step] - (Islow[i+step] - Islow_conv[i]) * Xs
    # Islow_conv[i+step] = Islow[i] - (Islow[i] - Islow_conv[i]) * Xs

    Islow_conv_test[i+step] = (1 - Xs) * Islow[i+step] + Xs * Islow_conv_test[i]
    #
    # print(i+step, 'Islow_conv', Islow[i+step], Islow_conv[i+step], Islow_conv_test[i+step])
    # Islow_conv[i + 1] = Islow[i] - (Islow[i] - Islow_conv[i]) * Xs
    # print(i+step, 'Islow_conv', Islow_conv[i+step])


    Ifast[i+step] = af * (dfo.at[i+step, 'O3CellI'] - Islow_conv[i+step])
    Ifastminib0[i+step] = af * (dfo.at[i+step, 'O3CellI'] - Islow_conv[i+step] - dfo.at[i+step, 'iB0'])

    Ifast_deconv[i+step] = (Ifast[i+step] - Ifast[i] * Xf) / (1 - Xf)
    Ifastminib0_deconv[i+step] = (Ifastminib0[i+step] - Ifastminib0[i] * Xf) / (1 - Xf)

    Ifast_deconv_hv[i+step] = Ifast[i+step] + (tfast/(t1 - t2) * (Ifast[i+step] - Ifast[i]))
    Ifastminib0_deconv_hv[i+step] = Ifastminib0[i+step] + (tfast/(t1 - t2) * (Ifastminib0[i+step] - Ifastminib0[i]))

    Ifast_deconv_hs[i+step] = Ifast[i] + (tfast / (t1 - t2) * (Ifast[i+step] - Ifast[i]))
    Ifastminib0_deconv_hs[i+step] = Ifastminib0[i] + (tfast / (t1 - t2) * (Ifastminib0[i+step] - Ifastminib0[i]))




dfo['I_slow'] = Islow
dfo['I_slow_conv'] = Islow_conv
dfo['I_slow_conv_test'] = Islow_conv_test

dfo['I_fast'] = Ifast
dfo['Ifast_minib0'] = Ifastminib0
dfo['Ifast_deconv'] = Ifast_deconv
dfo['Ifast_minib0_deconv'] = Ifastminib0_deconv


dfo['I_fast_sm8'] = dfo['I_fast'].rolling(window=4 * step).mean()
dfo['Ifast_minib0_sm8'] = dfo['Ifast_minib0'].rolling(window=4 * step).mean()
dfo['Ifast_deconv_sm8'] = dfo['Ifast_deconv'].rolling(window=4 * step).mean()
dfo['Ifast_minib0_deconv_sm8'] = dfo['Ifast_minib0_deconv'].rolling(window=4 * step).mean()


dfo['Ifast_deconv_hv'] = Ifast_deconv_hv
dfo['Ifast_minib0_deconv_hv'] = Ifastminib0_deconv_hv
dfo['Ifast_deconv_hs'] = Ifast_deconv_hs
dfo['Ifast_minib0_deconv_hs'] = Ifastminib0_deconv_hs


dfo['Ifast_deconv_hv_sm8'] = dfo['Ifast_deconv_hv'].rolling(window=4 * step).mean()
dfo['Ifast_minib0_deconv_hv_sm8'] = dfo['Ifast_minib0_deconv_hv'].rolling(window=4 * step).mean()
dfo['Ifast_deconv_hs_sm8'] = dfo['Ifast_deconv_hs'].rolling(window=4 * step).mean()
dfo['Ifast_minib0_deconv_hs_sm8'] = dfo['Ifast_minib0_deconv_hs'].rolling(window=4 * step).mean()

## now pressure


for k in range(len(dfo)):
    ## jma corrections
    for p in range(len(JMA) - 1):
        if (dfo.at[k, 'Press'] >= Pval[p + 1]) & (dfo.at[k, 'Press'] < Pval[p]):
            dfo.at[k, 'PO3_minib0_deconv_jma_sm8'] = 0.043085 * dfo.at[k, 'TPumpK'] * dfo.at[
                k, 'Ifast_minib0_deconv_sm8'] / \
                                                        (dfo.at[k, 'PFcor'] * JMA[p])
            dfo.at[k, 'PO3_minib0_deconv_jma'] = 0.043085 * dfo.at[k, 'TPumpK'] * dfo.at[
                k, 'Ifast_minib0_deconv'] / \
                                                    (dfo.at[k, 'PFcor'] * JMA[p])
            dfo.at[k, 'PO3_jma'] = 0.043085 * dfo.at[k, 'TPumpK'] * (dfo.at[k, 'O3CellI'] - dfo.at[k, 'iB0'] ) / \
                                                 (dfo.at[k, 'PFcor'] * JMA[p])

    if (dfo.at[k, 'Press'] <= Pval[14]):
        dfo.at[k, 'PO3_minib0_deconv_jma_sm8'] = 0.043085 * dfo.at[k, 'TPumpK'] * dfo.at[
            k, 'Ifast_minib0_deconv_sm8'] / \
                                                    (dfo.at[k, 'PFcor'] * JMA[14])
        dfo.at[k, 'PO3_minib0_deconv_jma'] = 0.043085 * dfo.at[k, 'TPumpK'] * dfo.at[k, 'Ifast_minib0_deconv'] / \
                                                (dfo.at[k, 'PFcor'] * JMA[14])
        dfo.at[k, 'PO3_jma'] = 0.043085 * dfo.at[k, 'TPumpK'] * (dfo.at[k, 'O3CellI'] - dfo.at[k, 'iB0']) / \
                               (dfo.at[k, 'PFcor'] * JMA[14])

    ## komhyr corrections
    for p in range(len(komhyr_en) - 1):

        if (dfo.at[k, 'Press'] >= Pval_komhyr[p + 1]) & (dfo.at[k, 'Press'] < Pval_komhyr[p]):
            # print(p, Pval[p + 1], Pval[p ])
            dfo.at[k, 'PO3_minib0_deconv_komhyr_sm8'] = (dfo.at[k, 'TPumpK'] * 0.043085 * dfo.at[
                k, 'Ifast_minib0_deconv_sm8']) / \
                                                           (dfo.at[k, 'PFcor'] * komhyr_en[p])
            dfo.at[k, 'PO3_minib0_deconv_komhyr'] = (dfo.at[k, 'TPumpK'] * 0.043085 * dfo.at[
                k, 'Ifast_minib0_deconv']) / \
                                                           (dfo.at[k, 'PFcor'] * komhyr_en[p])

            dfo.at[k, 'PO3_ifast'] = (dfo.at[k, 'TPumpK'] * 0.043085 * dfo.at[k, 'I_fast']) / \
                                     (dfo.at[k, 'PFcor'] * komhyr_en[p])

            dfo.at[k, 'PO3_ifast_deconv'] = (dfo.at[k, 'TPumpK'] * 0.043085 * dfo.at[k, 'Ifast_deconv_sm8']) / \
                                     (dfo.at[k, 'PFcor'] * komhyr_en[p])

            dfo.at[k, 'PO3_komhyr'] = (dfo.at[k, 'TPumpK'] * 0.043085 * (dfo.at[k, 'O3CellI'] - dfo.at[k, 'iB0'] )) / \
                                            (dfo.at[k, 'PFcor'] * komhyr_en[p])



    if (dfo.at[k, 'Press'] <= Pval_komhyr[7]):

        dfo.at[k, 'PO3_minib0_deconv_komhyr_sm8'] = (dfo.at[k, 'TPumpK'] * 0.043085 * dfo.at[
            k, 'Ifast_minib0_deconv_sm8']) / \
                                                       (dfo.at[k, 'PFcor'] * komhyr_en[7])
        dfo.at[k, 'PO3_minib0_deconv_komhyr'] = (dfo.at[k, 'TPumpK'] * 0.043085 * dfo.at[
            k, 'Ifast_minib0_deconv']) / \
                                                   (dfo.at[k, 'PFcor'] * komhyr_en[7])

        dfo.at[k, 'PO3_ifast'] = (dfo.at[k, 'TPumpK'] * 0.043085 * dfo.at[k, 'I_fast']) / \
                                 (dfo.at[k, 'PFcor'] * komhyr_en[7])

        dfo.at[k, 'PO3_ifast_deconv'] = (dfo.at[k, 'TPumpK'] * 0.043085 * dfo.at[k, 'Ifast_deconv_sm8']) / \
                                        (dfo.at[k, 'PFcor'] * komhyr_en[7])

        dfo.at[k, 'PO3_komhyr'] = (dfo.at[k, 'TPumpK'] * 0.043085 * (dfo.at[k, 'O3CellI'] - dfo.at[k, 'iB0'] )) / \
                                  (dfo.at[k, 'PFcor'] * komhyr_en[7])


dfo['PO3'] = (dfo['TPumpK'] * 0.043085 * (dfo['O3CellI'] - dfo['iB0'] )) / \
                          (dfo['PFcor'] )

dfo['ppmv_ifast'] = dfo['PO3_ifast'] * 0.001 / (dfo['Press'] * 100) * 1000000
dfo['ppmv_ifast_deconv'] = dfo['PO3_ifast_deconv'] * 0.001 / (dfo['Press'] * 100) * 1000000

dfo['ppmv_po3'] = dfo['O3_mPa'] * 0.001 / (dfo['Press'] * 100) * 1000000
dfo['ppmv_ifast_minib0_deconv_kom_sm8'] = dfo['PO3_minib0_deconv_komhyr_sm8'] * 0.001 / (dfo['Press'] * 100) * 1000000


dfo.to_csv("/home/poyraden/Analysis/Homogenization_Analysis/Files/Costa_Rica/Proccessed/costarica_20100212_8secs_convoluted.csv")

##now plot

gs = gridspec.GridSpec(1, 3)

dfo.TsimMin = dfo.nTime / 60

# ax2 = plt.subplot()  # create the first subplot that will ALWAYS be there
ax2 = plt.subplot(gs[:, :2])  # create the first subplot that will ALWAYS be there

ax2.set_xlabel(r'Current ($\mu$A)')
ax2.set_ylabel('Alt. (km)')
# ax2.set_xlabel(r'ppmv')


plt.plot(dfo.I_slow_conv, dfo.GeopAlt,  label='I slow conv')

plt.plot(dfo.Ifast_deconv_sm8, dfo.GeopAlt,  label='I fast deconv current method')

plt.plot(dfo.Ifast_deconv_hv_sm8, dfo.GeopAlt,  label='I fast deconv HV')
plt.plot(dfo.Ifast_deconv_hs_sm8, dfo.GeopAlt,  label='I fast deconv HS')
#


# # # plt.title(ptitle)
plt.legend(loc='best', fontsize='small')
# #
ax2 = plt.subplot(gs[:, 2])  # create the first subplot that will ALWAYS be there
#
dfo['rdif'] = (dfo['Ifast_deconv_sm8'] - dfo['Ifast_deconv_hs_sm8']) * 100 / (dfo['Ifast_deconv_hs_sm8'])
# dfo['rdif'] = (dfo['Ifast_deconv_hv_sm8'] - dfo['Ifast_deconv_hs_sm8']) * 100 / (dfo['Ifast_deconv_hs_sm8'])

# ax2.set_xlabel(r'Rdif HV - HS / HS')
ax2.set_xlabel(r'Rdif Current - HS / HS')



plt.plot(dfo.rdif, dfo.GeopAlt,  label='rdif')

# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Costa_Rica/HV_HS.eps')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Costa_Rica/HV_HS.png')
# plt.show()


ax1 = plt.subplot()  # create the first subplot that will ALWAYS be there
#
ax1.set_xlabel(r'Current ($\mu$A)')
# ax1.set_ylabel('Alt. (km)')
ax1.set_xlabel(r'ppmv')


plt.plot(df.O3_ppmv, df.GeopAlt,  label='I ECC')

# plt.show()



