import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
from Convolution_Functions import convolution

Pval = np.array([1000, 730, 535, 382, 267, 185, 126, 85, 58, 39, 26.5, 18.1, 12.1, 8.3, 6])
JMA = np.array([0.999705941, 0.997216654, 0.995162562, 0.992733959, 0.989710199, 0.985943645, 0.981029252, 0.974634364,
                0.966705137, 0.956132227, 0.942864263, 0.9260478, 0.903069813, 0.87528384, 0.84516337])

Pval_komhyr = np.array([1000, 199, 59, 30, 20, 10, 7, 5])
komhyr_sp_tmp = np.array([1, 1.007, 1.018, 1.022, 1.032, 1.055, 1.070, 1.092])
komhyr_en_tmp = np.array([1, 1.007, 1.018, 1.029, 1.041, 1.066, 1.087, 1.124])

komhyr_sp = [1/i for i in komhyr_sp_tmp]
komhyr_en = [1/i for i in komhyr_en_tmp]

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

# df['PO3'] = (df['TPumpK'] * 0.043085 * (df['O3CellI'] - df['iB0'] )) / (df['PFcor'] )

### now make this data set in equal time 1s
df = df.drop_duplicates(subset=['Time'], keep='first')
df = df.reset_index()
#
df['TS'] = pd.to_datetime(df.Time, unit = 's')

dfr = df.resample('4S', on='TS').mean().interpolate()
dfo = dfr.reset_index()

dfo['nTime'] = (dfo['TS'] - datetime.datetime(1970,1,1)).dt.total_seconds()
#
#
#
# dfo.to_csv("/home/poyraden/Analysis/Homogenization_Analysis/Files/Costa_Rica/Proccessed/costarica_20100212_4secs.csv")



## now do the convolution to dfo

tslow = 25 * 60
tfast = 20

beta = 0.03
af = 1

dfo['iB0'] = 0.020
dfo['PFcor'] = 100 / 27.7
dfo['TPumpK'] = dfo.at[0, 'TPump'] + 273
dfo['IminusiB0'] = dfo['O3CellI'] - dfo['iB0']

Islow_f, Islow_conv_f, Ifast_f, Ifast_deconv_f,  Ifastminib0_f, Ifastminib0_deconv_f = convolution(dfo, 'O3_ppmv', 'O3_ppmv', 'nTime', 0.03, 1)

Islow, Islow_conv, Ifast, Ifast_deconv,  Ifastminib0, Ifastminib0_deconv = convolution(dfo, 'O3CellI', 'O3CellI', 'nTime', 0.03, 1)
Islow_mib0, Islow_conv_mib0, Ifast_mib0, Ifast_deconv_mib0,  Ifastminib0_mib0, Ifastminib0_deconv_mib0 = convolution(dfo, 'IminusiB0', 'O3CellI', 'nTime', 0.03, 1)


dfo['Islow_f'] = Islow_f
dfo['Islow_conv_f'] = Islow_conv_f
dfo['Ifast_f'] = Ifast_f
dfo['Ifast_deconv_f'] = Ifast_deconv_f
dfo['Ifastminib0_f'] = Ifastminib0_f
dfo['Ifastminib0_deconv_f'] = Ifastminib0_deconv_f

dfo['Islow'] = Islow
dfo['Islow_conv'] = Islow_conv
dfo['Ifast'] = Ifast
dfo['Ifast_deconv'] = Ifast_deconv
dfo['Ifastminib0'] = Ifastminib0
dfo['Ifastminib0_deconv'] = Ifastminib0_deconv

dfo['Islow_mib0'] = Islow_mib0
dfo['Islow_conv_mib0'] = Islow_conv_mib0
dfo['Ifast_mib0'] = Ifast_mib0
dfo['Ifast_deconv_mib0'] = Ifast_deconv_mib0
dfo['Ifastminib0_mib0'] = Ifastminib0_mib0
dfo['Ifastminib0_deconv_mib0'] = Ifastminib0_deconv_mib0

##now convert current to pressure and than to ppm

for k in range(len(dfo)):
    ## jma corrections
    for p in range(len(JMA) - 1):
        if (dfo.at[k, 'Press'] >= Pval[p + 1]) & (dfo.at[k, 'Press'] < Pval[p]):
            dfo.at[k, 'PO3_minib0_deconv_jma'] = 0.043085 * dfo.at[k, 'TPumpK'] * dfo.at[
                k, 'Ifastminib0_deconv'] / \
                                                        (dfo.at[k, 'PFcor'] * JMA[p])
            dfo.at[k, 'PO3_deconv_jma'] = 0.043085 * dfo.at[k, 'TPumpK'] * dfo.at[
                k, 'Ifast_deconv'] / \
                                                    (dfo.at[k, 'PFcor'] * JMA[p])
            dfo.at[k, 'PO3_jma'] = 0.043085 * dfo.at[k, 'TPumpK'] * (dfo.at[k, 'O3CellI'] - dfo.at[k, 'iB0'] ) / \
                                                 (dfo.at[k, 'PFcor'] * JMA[p])

    if (dfo.at[k, 'Press'] <= Pval[14]):
        dfo.at[k, 'PO3_minib0_deconv_jma'] = 0.043085 * dfo.at[k, 'TPumpK'] * dfo.at[
            k, 'Ifastminib0_deconv'] / \
                                                    (dfo.at[k, 'PFcor'] * JMA[14])
        dfo.at[k, 'PO3_deconv_jma'] = 0.043085 * dfo.at[k, 'TPumpK'] * dfo.at[k, 'Ifast_deconv'] / \
                                                (dfo.at[k, 'PFcor'] * JMA[14])
        dfo.at[k, 'PO3_jma'] = 0.043085 * dfo.at[k, 'TPumpK'] * (dfo.at[k, 'O3CellI'] - dfo.at[k, 'iB0']) / \
                               (dfo.at[k, 'PFcor'] * JMA[14])

    ## komhyr corrections
    for p in range(len(komhyr_en) - 1):

        if (dfo.at[k, 'Press'] >= Pval_komhyr[p + 1]) & (dfo.at[k, 'Press'] < Pval_komhyr[p]):
            # print(p, Pval[p + 1], Pval[p ])
            dfo.at[k, 'PO3_minib0_deconv_komhyr'] = (dfo.at[k, 'TPumpK'] * 0.043085 * dfo.at[
                k, 'Ifastminib0_deconv']) / \
                                                           (dfo.at[k, 'PFcor'] * komhyr_en[p])
            dfo.at[k, 'PO3_deconv_komhyr'] = (dfo.at[k, 'TPumpK'] * 0.043085 * dfo.at[
                k, 'Ifast_deconv']) / \
                                                           (dfo.at[k, 'PFcor'] * komhyr_en[p])

            dfo.at[k, 'PO3_ifast_komhyr'] = (dfo.at[k, 'TPumpK'] * 0.043085 * dfo.at[k, 'Ifast']) / \
                                     (dfo.at[k, 'PFcor'] * komhyr_en[p])

            dfo.at[k, 'PO3_komhyr'] = (dfo.at[k, 'TPumpK'] * 0.043085 * (dfo.at[k, 'O3CellI'] - dfo.at[k, 'iB0'] )) / \
                                            (dfo.at[k, 'PFcor'] * komhyr_en[p])


    if (dfo.at[k, 'Press'] <= Pval_komhyr[7]):

        dfo.at[k, 'PO3_minib0_deconv_komhyr'] = (dfo.at[k, 'TPumpK'] * 0.043085 * dfo.at[
            k, 'Ifastminib0_deconv']) / \
                                                       (dfo.at[k, 'PFcor'] * komhyr_en[7])
        dfo.at[k, 'PO3_deconv_komhyr'] = (dfo.at[k, 'TPumpK'] * 0.043085 * dfo.at[
            k, 'Ifastminib0_deconv']) / \
                                                   (dfo.at[k, 'PFcor'] * komhyr_en[7])

        dfo.at[k, 'PO3_ifast_deconv'] = (dfo.at[k, 'TPumpK'] * 0.043085 * dfo.at[k, 'Ifast_deconv_sm8']) / \
                                        (dfo.at[k, 'PFcor'] * komhyr_en[7])

        dfo.at[k, 'PO3_komhyr'] = (dfo.at[k, 'TPumpK'] * 0.043085 * (dfo.at[k, 'O3CellI'] - dfo.at[k, 'iB0'] )) / \
                                  (dfo.at[k, 'PFcor'] * komhyr_en[7])

    dfo.at[k, 'PO3_minib0_deconv'] = (dfo.at[k, 'TPumpK'] * 0.043085 * dfo.at[
        k, 'Ifastminib0_deconv']) / \
                                            (dfo.at[k, 'PFcor'] )
    dfo.at[k, 'PO3_deconv'] = (dfo.at[k, 'TPumpK'] * 0.043085 * dfo.at[
        k, 'Ifast_deconv']) / \
                                     (dfo.at[k, 'PFcor'])


dfo['PO3'] = (dfo['TPumpK'] * 0.043085 * (dfo['O3CellI'] - dfo['iB0'] )) / \
                          (dfo['PFcor'] )

dfo.at[k, 'PO3_ifast'] = (dfo.at[k, 'TPumpK'] * 0.043085 * dfo.at[k, 'Ifast']) / \
                                     (dfo.at[k, 'PFcor'] )

dfo['ppmv_ifast'] = dfo['PO3_ifast'] * 0.001 / (dfo['Press'] * 100) * 1000000

dfo['ppmv_ifast_komhyr'] = dfo['PO3_ifast_komhyr'] * 0.001 / (dfo['Press'] * 100) * 1000000
dfo['ppmv_ifast_deconv_komhyr'] = dfo['PO3_deconv_komhyr'] * 0.001 / (dfo['Press'] * 100) * 1000000
dfo['ppmv_Ifastminib0_deconv_komhyr'] = dfo['PO3_minib0_deconv_komhyr'] * 0.001 / (dfo['Press'] * 100) * 1000000

dfo['ppmv_ifast_jma'] = dfo['PO3_ifast'] * 0.001 / (dfo['Press'] * 100) * 1000000
dfo['ppmv_ifast_deconv_jma'] = dfo['PO3_deconv_jma'] * 0.001 / (dfo['Press'] * 100) * 1000000
dfo['ppmv_Ifastminib0_deconv_jma'] = dfo['PO3_minib0_deconv_jma'] * 0.001 / (dfo['Press'] * 100) * 1000000

dfo['ppmv_ifast_deconv'] = dfo['PO3_deconv'] * 0.001 / (dfo['Press'] * 100) * 1000000
dfo['ppmv_Ifastminib0_deconv'] = dfo['PO3_minib0_deconv'] * 0.001 / (dfo['Press'] * 100) * 1000000

dfo['ppmv_po3'] = dfo['O3_mPa'] * 0.001 / (dfo['Press'] * 100) * 1000000
# dfo['ppmv_Ifastminib0_deconv_kom'] = dfo['PO3_minib0_deconv_komhyr_sm8'] * 0.001 / (dfo['Press'] * 100) * 1000000



# dfo.to_csv("/home/poyraden/Analysis/Homogenization_Analysis/Files/Costa_Rica/Proccessed/costarica_20100212_4secs_convoluted.csv")

print(len(dfo))
# ax1 = plt.subplot()  # create the first subplot that will ALWAYS be there
#

fig = plt.figure()
# set height ratios for sublots
gs = gridspec.GridSpec(1, 2, width_ratios=[2, 1])

# fig, ax1 = plt.subplots()
plt.title('Costa Rica 12 February 2010')
ax1 = plt.subplot(gs[0])

ax1.set_ylabel('Alt. (km)')
ax1.set_xlabel(r'ppmv')
# ax1.set_xlabel(r'Current ($\mu$A)')

# ax1.set_xlim(0.01, 0.055)
# ax1.set_ylim(10, 15)

# plt.plot(dfo.O3CellI, dfo.GeopAlt,  label='ECC', linewidth=2.5)
# plt.plot(dfo.Ifastminib0_deconv_mib0.rolling(window=3, center=True).mean(), dfo.GeopAlt,  label=' Fast min ib0 deconv. smoothed 13 seconds ( slow = I - ib0)')
# plt.plot(dfo.Ifastminib0_deconv.rolling(window=3, center=True).mean(), dfo.GeopAlt,  label=' Fast min ib0 deconv. smoothed 13 seconds')
# plt.plot(dfo.Ifast_deconv.rolling(window=3, center=True).mean(), dfo.GeopAlt,  label=' Fast deconv. smoothed 13 seconds')

plt.plot(dfo.ppmv_po3, dfo.GeopAlt,  label='ECC', linewidth=1.5)
# plt.plot(dfo.ppmv_ifast_komhyr.rolling(window=1, center=True).mean(), dfo.GeopAlt,  label=' Fast reaction')
plt.plot(dfo.ppmv_ifast_deconv_komhyr.rolling(window=13, center=True).mean(), dfo.GeopAlt,  label='ECC corrected')
# plt.plot(dfo.Ifast_deconv.rolling(window=3, center=True).mean(), dfo.GeopAlt,  label=' Fast deconv. smoothed 13 seconds')

# dif = df.Time.diff()
# plt.hist(dif, density=False, bins=60)  # `density=False` would make counts
# plt.xlim(0, 10)
# ax1.set_xlabel('Time Intervals (sec.)')
# #
#
# ax1.tick_params(axis='x', which='minor', bottom=True, top=True)
# ax1.xaxis.set_major_locator(MultipleLocator(0.01))
# ax1.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
# # For the minor ticks, use no labels; default NullFormatter.
# ax1.xaxis.set_minor_locator(MultipleLocator(0.001))
#
# ax1.tick_params(axis='y', which='minor', left=True, right=True)
# ax1.yaxis.set_major_locator(MultipleLocator(1))
# ax1.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
# # For the minor ticks, use no labels; default NullFormatter.
# ax1.yaxis.set_minor_locator(MultipleLocator(0.2))

# ax1.set_xscale('log')

plt.legend(loc='left top', fontsize='small')
#
ax2 = plt.subplot(gs[1])
# plt.plot(dfa.I, dfa.km, label = 'Ascent', linewidth = 3 )
ax2.axvline(x=0, color='grey', linestyle='--')

ax2.set_xlim(-40, 40)
ax2.set_xlabel('RDif Corr. - Original (%)')

dfo['ifdsm'] = dfo.ppmv_ifast_deconv_komhyr.rolling(window=13, center=True).mean()
# dfo['ifdsm'] = dfo.Ifast_deconv_f.rolling(window=13, center=True, win_type='gaussian').mean(std=4)

dfo['rdif'] = (dfo.ifdsm - dfo.ppmv_po3) / dfo.ppmv_po3 * 100

plt.plot(dfo.rdif.rolling(window=10, center=True).mean(), dfo.GeopAlt,  label='Rdif (Ifast_deconv - I)[%]')

# title = 'CR_4secData_ifast_comparison'
#

# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Costa_Rica/' + title + '.eps')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Costa_Rica/' + title + '.png')
plt.show()


############################################################################################3

##now plot

# gs = gridspec.GridSpec(1, 3)
#
# dfo.TsimMin = dfo.nTime / 60
#
# ax2 = plt.subplot()  # create the first subplot that will ALWAYS be there
# ax2 = plt.subplot(gs[:, :2])  # create the first subplot that will ALWAYS be there
#
# ax2.set_xlabel(r'Current ($\mu$A)')
# ax2.set_ylabel('Alt. (km)')
# # ax2.set_xlabel(r'ppmv')
# print('what')
#
# plt.plot(dfo.Islow_conv_f, dfo.GeopAlt,  label='I slow conv')
# plt.plot(dfo.O3_ppmv, dfo.GeopAlt,  label='ECC', linewidth=2.5)
# plt.plot(dfo.Ifast_f.rolling(window=1, center=True).mean(), dfo.GeopAlt,  label=' Fast ', linewidth=2.5)
# plt.plot(dfo.Ifast_f.rolling(window=13, center=True).mean(), dfo.GeopAlt,  label=' Fast smoothed',  linewidth=2.5)
#
# plt.plot(dfo.Ifast_deconv_f.rolling(window=13, center=True).mean(), dfo.GeopAlt,  label=' Fast deconv. smoothed')
# plt.plot(dfo.Ifast_deconv_f.rolling(window=12, win_type='gaussian').mean(std=3), dfo.GeopAlt,  label=' Fast deconv. gaus. smoothed')

# # plt.plot(dfo.Ifast_deconv_hv_sm8, dfo.GeopAlt,  label='I fast deconv HV')
# # plt.plot(dfo.Ifast_deconv_hs_sm8, dfo.GeopAlt,  label='I fast deconv HS')
# #
#
#
# # # # plt.title(ptitle)
# plt.legend(loc='best', fontsize='small')
# # #
# ax2 = plt.subplot(gs[:, 2])  # create the first subplot that will ALWAYS be there
# #
# dfo['rdif'] = (dfo['Ifast_deconv_sm8'] - dfo['Ifast_deconv_hs_sm8']) * 100 / (dfo['Ifast_deconv_hs_sm8'])
# # dfo['rdif'] = (dfo['Ifast_deconv_hv_sm8'] - dfo['Ifast_deconv_hs_sm8']) * 100 / (dfo['Ifast_deconv_hs_sm8'])
#
# # ax2.set_xlabel(r'Rdif HV - HS / HS')
# ax2.set_xlabel(r'Rdif Current - HS / HS')
#
#
#
# plt.plot(dfo.rdif, dfo.GeopAlt,  label='rdif')

# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Costa_Rica/HV_HS.eps')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Costa_Rica/HV_HS.png')

#


## now pressure

#
# for k in range(len(dfo)):
#     ## jma corrections
#     for p in range(len(JMA) - 1):
#         if (dfo.at[k, 'Press'] >= Pval[p + 1]) & (dfo.at[k, 'Press'] < Pval[p]):
#             dfo.at[k, 'PO3_minib0_deconv_jma_sm8'] = 0.043085 * dfo.at[k, 'TPumpK'] * dfo.at[
#                 k, 'Ifast_minib0_deconv_sm8'] / \
#                                                         (dfo.at[k, 'PFcor'] * JMA[p])
#             dfo.at[k, 'PO3_minib0_deconv_jma'] = 0.043085 * dfo.at[k, 'TPumpK'] * dfo.at[
#                 k, 'Ifast_minib0_deconv'] / \
#                                                     (dfo.at[k, 'PFcor'] * JMA[p])
#             dfo.at[k, 'PO3_jma'] = 0.043085 * dfo.at[k, 'TPumpK'] * (dfo.at[k, 'O3CellI'] - dfo.at[k, 'iB0'] ) / \
#                                                  (dfo.at[k, 'PFcor'] * JMA[p])
#
#     if (dfo.at[k, 'Press'] <= Pval[14]):
#         dfo.at[k, 'PO3_minib0_deconv_jma_sm8'] = 0.043085 * dfo.at[k, 'TPumpK'] * dfo.at[
#             k, 'Ifast_minib0_deconv_sm8'] / \
#                                                     (dfo.at[k, 'PFcor'] * JMA[14])
#         dfo.at[k, 'PO3_minib0_deconv_jma'] = 0.043085 * dfo.at[k, 'TPumpK'] * dfo.at[k, 'Ifast_minib0_deconv'] / \
#                                                 (dfo.at[k, 'PFcor'] * JMA[14])
#         dfo.at[k, 'PO3_jma'] = 0.043085 * dfo.at[k, 'TPumpK'] * (dfo.at[k, 'O3CellI'] - dfo.at[k, 'iB0']) / \
#                                (dfo.at[k, 'PFcor'] * JMA[14])
#
#     ## komhyr corrections
#     for p in range(len(komhyr_en) - 1):
#
#         if (dfo.at[k, 'Press'] >= Pval_komhyr[p + 1]) & (dfo.at[k, 'Press'] < Pval_komhyr[p]):
#             # print(p, Pval[p + 1], Pval[p ])
#             dfo.at[k, 'PO3_minib0_deconv_komhyr_sm8'] = (dfo.at[k, 'TPumpK'] * 0.043085 * dfo.at[
#                 k, 'Ifast_minib0_deconv_sm8']) / \
#                                                            (dfo.at[k, 'PFcor'] * komhyr_en[p])
#             dfo.at[k, 'PO3_minib0_deconv_komhyr'] = (dfo.at[k, 'TPumpK'] * 0.043085 * dfo.at[
#                 k, 'Ifast_minib0_deconv']) / \
#                                                            (dfo.at[k, 'PFcor'] * komhyr_en[p])
#
#             dfo.at[k, 'PO3_ifast'] = (dfo.at[k, 'TPumpK'] * 0.043085 * dfo.at[k, 'I_fast']) / \
#                                      (dfo.at[k, 'PFcor'] * komhyr_en[p])
#
#             dfo.at[k, 'PO3_ifast_deconv'] = (dfo.at[k, 'TPumpK'] * 0.043085 * dfo.at[k, 'Ifast_deconv_sm8']) / \
#                                      (dfo.at[k, 'PFcor'] * komhyr_en[p])
#
#             dfo.at[k, 'PO3_komhyr'] = (dfo.at[k, 'TPumpK'] * 0.043085 * (dfo.at[k, 'O3CellI'] - dfo.at[k, 'iB0'] )) / \
#                                             (dfo.at[k, 'PFcor'] * komhyr_en[p])
#
#
#
#     if (dfo.at[k, 'Press'] <= Pval_komhyr[7]):
#
#         dfo.at[k, 'PO3_minib0_deconv_komhyr_sm8'] = (dfo.at[k, 'TPumpK'] * 0.043085 * dfo.at[
#             k, 'Ifast_minib0_deconv_sm8']) / \
#                                                        (dfo.at[k, 'PFcor'] * komhyr_en[7])
#         dfo.at[k, 'PO3_minib0_deconv_komhyr'] = (dfo.at[k, 'TPumpK'] * 0.043085 * dfo.at[
#             k, 'Ifast_minib0_deconv']) / \
#                                                    (dfo.at[k, 'PFcor'] * komhyr_en[7])
#
#         dfo.at[k, 'PO3_ifast'] = (dfo.at[k, 'TPumpK'] * 0.043085 * dfo.at[k, 'I_fast']) / \
#                                  (dfo.at[k, 'PFcor'] * komhyr_en[7])
#
#         dfo.at[k, 'PO3_ifast_deconv'] = (dfo.at[k, 'TPumpK'] * 0.043085 * dfo.at[k, 'Ifast_deconv_sm8']) / \
#                                         (dfo.at[k, 'PFcor'] * komhyr_en[7])
#
#         dfo.at[k, 'PO3_komhyr'] = (dfo.at[k, 'TPumpK'] * 0.043085 * (dfo.at[k, 'O3CellI'] - dfo.at[k, 'iB0'] )) / \
#                                   (dfo.at[k, 'PFcor'] * komhyr_en[7])
#
#
# dfo['PO3'] = (dfo['TPumpK'] * 0.043085 * (dfo['O3CellI'] - dfo['iB0'] )) / \
#                           (dfo['PFcor'] )
#
# dfo['ppmv_ifast'] = dfo['PO3_ifast'] * 0.001 / (dfo['Press'] * 100) * 1000000
# dfo['ppmv_ifast_deconv'] = dfo['PO3_ifast_deconv'] * 0.001 / (dfo['Press'] * 100) * 1000000
#
# dfo['ppmv_po3'] = dfo['O3_mPa'] * 0.001 / (dfo['Press'] * 100) * 1000000
# dfo['ppmv_ifast_minib0_deconv_kom_sm8'] = dfo['PO3_minib0_deconv_komhyr_sm8'] * 0.001 / (dfo['Press'] * 100) * 1000000


#
# for i in range(2, size - step):
#
#     t1 = dfo.at[i+step, 'nTime']
#     t2 = dfo.at[i, 'nTime']
#     # print(t1, t2)
#
#     Xs = np.exp(-(t1 - t2) / tslow)
#     Xf = np.exp(-(t1 - t2) / tfast)
#
#
#     # ###########  for 2000 data
#     dfo.at[i,'iB0'] = 0.020
#     dfo.at[i, 'PFcor'] = 100 / 27.7
#     dfo.at[i, 'TPumpK'] = dfo.at[i, 'TPump'] + 273
#
#     Islow[i] = beta * dfo.at[i, 'O3CellI']
#     # Islow[1] = beta * dfo.at[1, 'O3CellI']
#     #
#     # Islow_conv[0] = 0
#     # Islow_conv[1] = Islow[1] - (Islow[1] - Islow_conv[0]) * Xs
#
#     # Islow[0] = beta * dfo.at[0, 'O3CellI']
#
#     # Islow_conv_test[0] = (1 - Xs) * Islow[0] + Xs * Islow_conv_test[0]
#     # print('islow 0', Islow[0], Islow[1], Islow_conv_test[0])
#
#     # Islow_conv[1] = Islow[1] - (Islow[1] ) * Xs
#
#
#     Islow_conv[i+step] = Islow[i+step] - (Islow[i+step] - Islow_conv[i]) * Xs
#     # Islow_conv[i+step] = Islow[i] - (Islow[i] - Islow_conv[i]) * Xs
#
#     Islow_conv_test[i+step] = (1 - Xs) * Islow[i+step] + Xs * Islow_conv_test[i]
#     #
#     # print(i+step, 'Islow_conv', Islow[i+step], Islow_conv[i+step], Islow_conv_test[i+step])
#     # Islow_conv[i + 1] = Islow[i] - (Islow[i] - Islow_conv[i]) * Xs
#     # print(i+step, 'Islow_conv', Islow_conv[i+step])
#
#
#     Ifast[i+step] = af * (dfo.at[i+step, 'O3CellI'] - Islow_conv[i+step])
#     Ifastminib0[i+step] = af * (dfo.at[i+step, 'O3CellI'] - Islow_conv[i+step] - dfo.at[i+step, 'iB0'])
#
#     Ifast_deconv[i+step] = (Ifast[i+step] - Ifast[i] * Xf) / (1 - Xf)
#     Ifastminib0_deconv[i+step] = (Ifastminib0[i+step] - Ifastminib0[i] * Xf) / (1 - Xf)
#
#     Ifast_deconv_hv[i+step] = Ifast[i+step] + (tfast/(t1 - t2) * (Ifast[i+step] - Ifast[i]))
#     Ifastminib0_deconv_hv[i+step] = Ifastminib0[i+step] + (tfast/(t1 - t2) * (Ifastminib0[i+step] - Ifastminib0[i]))
#
#     Ifast_deconv_hs[i+step] = Ifast[i] + (tfast / (t1 - t2) * (Ifast[i+step] - Ifast[i]))
#     Ifastminib0_deconv_hs[i+step] = Ifastminib0[i] + (tfast / (t1 - t2) * (Ifastminib0[i+step] - Ifastminib0[i]))

#

#
