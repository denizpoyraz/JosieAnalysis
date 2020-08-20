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


# dfr = df.copy()

### now make this data set in equal time 1s
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


dfr = df.resample('4S', on='TS').mean().interpolate()
dfr = dfr.reset_index()

for i in range(len(dfr)):
    date_time = datetime.datetime.strptime(str(dfr.at[i, 'TS']), "%Y-%m-%d %H:%M:%S")
    a_timedelta = date_time - datetime.datetime(1970, 1, 1)
    seconds = a_timedelta.total_seconds()
    dfr.at[i, 'nTime'] = seconds


dfr.to_csv("/home/poyraden/Analysis/Homogenization_Analysis/Files/Costa_Rica/Proccessed/costarica_20100212_8secs.csv")

dfr['iB0'] = 0.020
dfr['PFcor'] = 27.7

## now do the convolution to dfr
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

size = len(dfr)

Islow = [0] * size
Islow_conv = [0] * size
Islow_conv_test = [0] * size

Islow_conv_w = [0] * size


Ifast = [0] * size
Ifast_deconv = [0] * size
Ifastminib0 = [0] * size
Ifastminib0_deconv = [0] * size


Ifast_deconv_hv = [0] * size
Ifastminib0_deconv_hv = [0] * size
Ifast_deconv_hs = [0] * size
Ifastminib0_deconv_hs = [0] * size


beta = 0.03
af = 1

nsample = len(dfr)

freq = 3
amp = 1
dfr['signal'] =  np.sin(2 * np.pi / 300 * dfr['nTime'])
sample = 800

noise = 0.00002 * np.random.normal(600,1333,1333)
# noise = 0.0008*np.asarray(np.random(range(0,1000)))


dfr['noisy_signal'] = dfr['signal'] + noise





dfr.at[0, 'iB0'] = 0.020
dfr.at[0, 'PFcor'] = 100 / 27.7
dfr.at[0, 'TPumpK'] = dfr.at[0, 'TPump'] + 273

dfr.at[1, 'iB0'] = 0.020
dfr.at[2, 'PFcor'] = 100 / 27.7
dfr.at[3, 'TPumpK'] = dfr.at[0, 'TPump'] + 273

Islow[0] = beta * dfr.at[0, 'noisy_signal']
Islow[1] = beta * dfr.at[1, 'noisy_signal']

print('ONE ', Islow[0], Islow[1] )


Islow_conv[0] = 0
Islow_conv[1] = Islow[1] - (Islow[1] - Islow_conv[0]) * np.exp(-(4) / tslow)

Islow_conv_w[1] = Islow[0] - (Islow[0] - Islow_conv_w[0]) * np.exp(-(4) / tslow)

print('TWO ', Islow_conv[0],  Islow_conv[1])

# for i in range(1,4):
for i in range(1, size - 1):

    t1 = dfr.at[i+1, 'nTime']
    t2 = dfr.at[i, 'nTime']
    # print(t1, t2)

    Xs = np.exp(-(t1 - t2) / tslow)
    Xf = np.exp(-(t1 - t2) / tfast)


    # ###########  for 2000 data
    dfr.at[i,'iB0'] = 0.020
    dfr.at[i, 'PFcor'] = 100 / 27.7
    dfr.at[i, 'TPumpK'] = dfr.at[i, 'TPump'] + 273

    Islow[i] = beta * dfr.at[i, 'noisy_signal']
    Islow[i+1] = beta * dfr.at[i+1, 'noisy_signal']

    Islow_conv[i+1] = Islow[i+1] - (Islow[i+1] - Islow_conv[i]) * Xs
    Islow_conv_w[i+1] = Islow[i] - (Islow[i] - Islow_conv_w[i]) * Xs

    Ifast[i+1] = af * (dfr.at[i+1, 'noisy_signal'] - Islow_conv[i+1])
    Ifast[i] = af * (dfr.at[i, 'noisy_signal'] - Islow_conv[i])

    Ifastminib0[i+1] = af * (dfr.at[i+1, 'noisy_signal'] - Islow_conv[i+1] - dfr.at[i+1, 'iB0'])

    Ifast_deconv[i+1] = (Ifast[i+1] - Ifast[i] * Xf) / (1 - Xf)
    Ifastminib0_deconv[i+1] = (Ifastminib0[i+1] - Ifastminib0[i] * Xf) / (1 - Xf)

    Ifast_deconv_hv[i+1] = Ifast[i+1] + (tfast/(t1 - t2) * (Ifast[i+1] - Ifast[i]))
    Ifastminib0_deconv_hv[i+1] = Ifastminib0[i+1] + (tfast/(t1 - t2) * (Ifastminib0[i+1] - Ifastminib0[i]))

    Ifast_deconv_hs[i+1] = Ifast[i] + (tfast / (t1 - t2) * (Ifast[i+1] - Ifast[i]))
    Ifastminib0_deconv_hs[i+1] = Ifastminib0[i] + (tfast / (t1 - t2) * (Ifastminib0[i+1] - Ifastminib0[i]))




dfr['I_slow'] = Islow
dfr['I_slow_conv'] = Islow_conv
dfr['I_slow_conv_w'] = Islow_conv_w

dfr['I_fast'] = Ifast
dfr['Ifast_minib0'] = Ifastminib0
dfr['Ifast_deconv'] = Ifast_deconv
dfr['Ifast_minib0_deconv'] = Ifastminib0_deconv


dfr['I_fast_sm8'] = dfr['I_fast'].rolling(window=4 * 1).mean()
dfr['Ifast_minib0_sm8'] = dfr['Ifast_minib0'].rolling(window=4 * 1).mean()
dfr['Ifast_deconv_sm8'] = dfr['Ifast_deconv'].rolling(window=4 * 1).mean()
dfr['Ifast_minib0_deconv_sm8'] = dfr['Ifast_minib0_deconv'].rolling(window=4 * 1).mean()


dfr['Ifast_deconv_hv'] = Ifast_deconv_hv
dfr['Ifast_minib0_deconv_hv'] = Ifastminib0_deconv_hv
dfr['Ifast_deconv_hs'] = Ifast_deconv_hs
dfr['Ifast_minib0_deconv_hs'] = Ifastminib0_deconv_hs


dfr['Ifast_deconv_hv_sm8'] = dfr['Ifast_deconv_hv'].rolling(window=4 * 1).mean()
dfr['Ifast_minib0_deconv_hv_sm8'] = dfr['Ifast_minib0_deconv_hv'].rolling(window=4 * 1).mean()
dfr['Ifast_deconv_hs_sm8'] = dfr['Ifast_deconv_hs'].rolling(window=4 * 1).mean()
dfr['Ifast_minib0_deconv_hs_sm8'] = dfr['Ifast_minib0_deconv_hs'].rolling(window=4 * 1).mean()

## now pressure


for k in range(len(dfr)):
    ## jma corrections
    for p in range(len(JMA) - 1):
        if (dfr.at[k, 'Press'] >= Pval[p + 1]) & (dfr.at[k, 'Press'] < Pval[p]):
            dfr.at[k, 'PO3_minib0_deconv_jma_sm8'] = 0.043085 * dfr.at[k, 'TPumpK'] * dfr.at[
                k, 'Ifast_minib0_deconv_sm8'] / \
                                                        (dfr.at[k, 'PFcor'] * JMA[p])
            dfr.at[k, 'PO3_minib0_deconv_jma'] = 0.043085 * dfr.at[k, 'TPumpK'] * dfr.at[
                k, 'Ifast_minib0_deconv'] / \
                                                    (dfr.at[k, 'PFcor'] * JMA[p])
            dfr.at[k, 'PO3_jma'] = 0.043085 * dfr.at[k, 'TPumpK'] * (dfr.at[k, 'O3CellI'] - dfr.at[k, 'iB0'] ) / \
                                                 (dfr.at[k, 'PFcor'] * JMA[p])

    if (dfr.at[k, 'Press'] <= Pval[14]):
        dfr.at[k, 'PO3_minib0_deconv_jma_sm8'] = 0.043085 * dfr.at[k, 'TPumpK'] * dfr.at[
            k, 'Ifast_minib0_deconv_sm8'] / \
                                                    (dfr.at[k, 'PFcor'] * JMA[14])
        dfr.at[k, 'PO3_minib0_deconv_jma'] = 0.043085 * dfr.at[k, 'TPumpK'] * dfr.at[k, 'Ifast_minib0_deconv'] / \
                                                (dfr.at[k, 'PFcor'] * JMA[14])
        dfr.at[k, 'PO3_jma'] = 0.043085 * dfr.at[k, 'TPumpK'] * (dfr.at[k, 'O3CellI'] - dfr.at[k, 'iB0']) / \
                               (dfr.at[k, 'PFcor'] * JMA[14])

    ## komhyr corrections
    for p in range(len(komhyr_en) - 1):

        if (dfr.at[k, 'Press'] >= Pval_komhyr[p + 1]) & (dfr.at[k, 'Press'] < Pval_komhyr[p]):
            # print(p, Pval[p + 1], Pval[p ])
            dfr.at[k, 'PO3_minib0_deconv_komhyr_sm8'] = (dfr.at[k, 'TPumpK'] * 0.043085 * dfr.at[
                k, 'Ifast_minib0_deconv_sm8']) / \
                                                           (dfr.at[k, 'PFcor'] * komhyr_en[p])
            dfr.at[k, 'PO3_minib0_deconv_komhyr'] = (dfr.at[k, 'TPumpK'] * 0.043085 * dfr.at[
                k, 'Ifast_minib0_deconv']) / \
                                                           (dfr.at[k, 'PFcor'] * komhyr_en[p])

            dfr.at[k, 'PO3_ifast'] = (dfr.at[k, 'TPumpK'] * 0.043085 * dfr.at[k, 'I_fast']) / \
                                     (dfr.at[k, 'PFcor'] * komhyr_en[p])

            dfr.at[k, 'PO3_ifast_deconv'] = (dfr.at[k, 'TPumpK'] * 0.043085 * dfr.at[k, 'Ifast_deconv_sm8']) / \
                                     (dfr.at[k, 'PFcor'] * komhyr_en[p])

            dfr.at[k, 'PO3_komhyr'] = (dfr.at[k, 'TPumpK'] * 0.043085 * (dfr.at[k, 'O3CellI'] - dfr.at[k, 'iB0'] )) / \
                                            (dfr.at[k, 'PFcor'] * komhyr_en[p])



    if (dfr.at[k, 'Press'] <= Pval_komhyr[7]):

        dfr.at[k, 'PO3_minib0_deconv_komhyr_sm8'] = (dfr.at[k, 'TPumpK'] * 0.043085 * dfr.at[
            k, 'Ifast_minib0_deconv_sm8']) / \
                                                       (dfr.at[k, 'PFcor'] * komhyr_en[7])
        dfr.at[k, 'PO3_minib0_deconv_komhyr'] = (dfr.at[k, 'TPumpK'] * 0.043085 * dfr.at[
            k, 'Ifast_minib0_deconv']) / \
                                                   (dfr.at[k, 'PFcor'] * komhyr_en[7])

        dfr.at[k, 'PO3_ifast'] = (dfr.at[k, 'TPumpK'] * 0.043085 * dfr.at[k, 'I_fast']) / \
                                 (dfr.at[k, 'PFcor'] * komhyr_en[7])

        dfr.at[k, 'PO3_ifast_deconv'] = (dfr.at[k, 'TPumpK'] * 0.043085 * dfr.at[k, 'Ifast_deconv_sm8']) / \
                                        (dfr.at[k, 'PFcor'] * komhyr_en[7])

        dfr.at[k, 'PO3_komhyr'] = (dfr.at[k, 'TPumpK'] * 0.043085 * (dfr.at[k, 'O3CellI'] - dfr.at[k, 'iB0'] )) / \
                                  (dfr.at[k, 'PFcor'] * komhyr_en[7])


dfr['PO3'] = (dfr['TPumpK'] * 0.043085 * (dfr['O3CellI'] - dfr['iB0'] )) / \
                          (dfr['PFcor'] )

dfr['ppmv_ifast'] = dfr['PO3_ifast'] * 0.001 / (dfr['Press'] * 100) * 1000000
dfr['ppmv_ifast_deconv'] = dfr['PO3_ifast_deconv'] * 0.001 / (dfr['Press'] * 100) * 1000000

dfr['ppmv_po3'] = dfr['O3_mPa'] * 0.001 / (dfr['Press'] * 100) * 1000000
dfr['ppmv_ifast_minib0_deconv_kom_sm8'] = dfr['PO3_minib0_deconv_komhyr_sm8'] * 0.001 / (dfr['Press'] * 100) * 1000000


dfr.to_csv("/home/poyraden/Analysis/Homogenization_Analysis/Files/Costa_Rica/Proccessed/costarica_20100212_8secs_convoluted.csv")

##now plot

# gs = gridspec.GridSpec(1, 3)
#
# dfr.TsimMin = dfr.nTime / 60
#
# # ax2 = plt.subplot()  # create the first subplot that will ALWAYS be there
# ax2 = plt.subplot(gs[:, :2])  # create the first subplot that will ALWAYS be there
#
# ax2.set_xlabel(r'Current ($\mu$A)')
# ax2.set_ylabel('Alt. (km)')
# # ax2.set_xlabel(r'ppmv')
#
#
# plt.plot(dfr.I_slow_conv, dfr.GeopAlt,  label='I slow conv')
# plt.plot(dfr.I_slow_conv_w, dfr.GeopAlt,  label='I slow conv wrong')
#
# plt.plot(dfr.Ifast_deconv_sm8, dfr.GeopAlt,  label='I fast deconv current method')
# #
# plt.plot(dfr.Ifast_deconv_hv_sm8, dfr.GeopAlt,  label='I fast deconv HV')
# plt.plot(dfr.Ifast_deconv_hs_sm8, dfr.GeopAlt,  label='I fast deconv HS')
# # #
#
#
# # # # plt.title(ptitle)
# plt.legend(loc='best', fontsize='small')
# # #
# ax2 = plt.subplot(gs[:, 2])  # create the first subplot that will ALWAYS be there
# # #
# # dfr['rdif'] = (dfr['Ifast_deconv_sm8'] - dfr['Ifast_deconv_hs_sm8']) * 100 / (dfr['Ifast_deconv_hs_sm8'])
# # # dfr['rdif'] = (dfr['Ifast_deconv_hv_sm8'] - dfr['Ifast_deconv_hs_sm8']) * 100 / (dfr['Ifast_deconv_hs_sm8'])
# dfr['rdif'] = (dfr['I_slow_conv_w'] - dfr['I_slow_conv']) * 100 / (dfr['I_slow_conv'])
#
# #
# # # ax2.set_xlabel(r'Rdif HV - HS / HS')
# ax2.set_xlabel(r'Rdif')
# #
# #
# #
# plt.plot(dfr.rdif, dfr.GeopAlt,  label='rdif')
#
# # plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Costa_Rica/HV_HS.eps')
# # plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Costa_Rica/HV_HS.png')
# plt.show()


ax1 = plt.subplot()  # create the first subplot that will ALWAYS be there
#
ax1.set_xlabel(r'Tsim')
# ax1.set_ylabel('Alt. (km)')
# ax1.set_xlabel(r'ppmv')


plt.plot(dfr.nTime, dfr.noisy_signal,  label='noisy_signal')
plt.plot(dfr.nTime, dfr.Ifast_deconv_sm8,  label='noisy_signal deconv')

plt.legend(loc='best', fontsize='small')
plt.grid()

plt.show()



