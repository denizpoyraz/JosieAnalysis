import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from numpy.polynomial import polynomial as P
import matplotlib.gridspec as gridspec

from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt

import pickle
from Josie_Functions import Calc_average_profileCurrent_pressure, Calc_average_profile_time, Calc_average_profile_Pair, Calc_average_profile_pressure
from Analyse_Functions import cuts2017, cuts0910, polyfit

# plothost(avgprof_tpint[0], avgprof_tpext[0],  avgprof_tpboil[0],  avgprof_tpcell[0], adif_cell[0], Y,  mtitle0, stitle0)


def plothost(hostarr1, hostarr2, hostarr3, hostarr32, hostarr4, twinarr1, twinarr2, Y,  mtitle, stitle ):
# def plothost(hostarr1, hostarr2, hostarr3, twinarr1, twinarr2, Y, mtitle, stitle):
# def plothost(hostarr1, hostarr2,  twinarr1, twinarr2, Y, mtitle, stitle):
    #
    host = host_subplot(111, axes_class=AA.Axes)
    plt.subplots_adjust(bottom=0.27)

    par1 = host.twiny()
    par2 = host.twiny()
    # par3 = host.twiny()


    new_fixed_axis = par1.get_grid_helper().new_fixed_axis
    par1.axis["bottom"] = new_fixed_axis(loc="bottom",
                                         axes=par1,
                                         offset=(0, -30))
    par2.axis["bottom"] = new_fixed_axis(loc="bottom",
                                         axes=par2,
                                         offset=(0, -60))
    # par3.axis["bottom"] = new_fixed_axis(loc="bottom",
    #                                      axes=par3,
    #                                      offset=(0, -60))

    par2.axis["bottom"].toggle(all=True)

    host.set_ylabel("Pressure")
    host.set_xlabel("Temp (C)")
    host.set_title(mtitle)
    # host.set_title("SP 1.0%-1.0B")
    host.set_xlim(0, 35)
    host.set_ylim(30, 0)
    # host.set_yscale('log')

    # # par1.set_xlabel("TBoil - TCell/ TCell [%]")
    par2.set_xlabel("Pw - Pair")
    # par3.set_xlabel("TBoil (C)")

    # par1.set_xlabel("TPint - TPext/ TPext [%]")
    # par1.set_xlabel("TPint - TCell/ TCell [%]")
    par1.set_xlabel("TBoil - TCell")

    par1.set_xlim(-20,10)
    # par2.set_xlabel("TPint - TPext")
    # par2.set_xlabel("TPint - TCell")

    par2.set_xlim(-15,10)
    # par3.set_xlabel("TBoil (C)")
    # # par1.set_xlabel("TPint - TCell/ TCell [%]")
    # par2.set_xlabel("TPint - TCell")

# plothost(avgprof_tpint[0], avgprof_tpext[0],  rdif[0], adif[0], Y, mtitle0, stitle0)
# plothost(avgprof_tpint[0], avgprof_tpext[0],  avgprof_tpboil[0],  avgprof_tpcell[0], adif_cell[0], Y,  mtitle0, stitle0)



    # p4, = par1.plot(twinarr1, Y, label="RDif")
    # p4, = par1.plot(twinarr1, Y, label="TBoil")

    p5, = par1.plot(twinarr2, Y, label="TCell - TBoil")


    p4, = par2.plot(twinarr1, Y, label="Pw - Pair")

    p1, = host.plot(hostarr1, Y, label="TPint ")
    # p2, = host.plot(hostarr2, Y, label="TCell ")
    p2, = host.plot(hostarr2, Y, label="TPext ")

    p3, = host.plot(hostarr3, Y, label="TBoil")
    #
    p32, = host.plot(hostarr32, Y, label="TCell gen.")


    p6, = host.plot(hostarr4, Y, label="Pw")



# host.legend()
    host.legend(ncol=4, loc='upper center')

    # host.axis["bottom"].label.set_color(p1.get_color())
    par1.axis["bottom"].label.set_color(p5.get_color())
    par2.axis["bottom"].label.set_color(p4.get_color())
    # par3.axis["bottom"].label.set_color(p3.get_color())

    plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/pwfixed_DeltaP_' + stitle + '.png')
    plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/pwfixed_DeltaP_' + stitle + '.pdf')
    plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature_fixed/pwfixed_DeltaP_' + stitle + '.eps')

    plt.show()

    plt.draw()


# df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_Data_nocut_tempfixed_paper.csv", low_memory=False)
#
# df = cuts2017(df)
# df = df[df.Sim > 185]
# df = df[df.Sim < 186]


# df['DeltaP'] = df['Pw'] - df['Pair']

# df = df[df.Sim < 186]
# #
df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_Data_nocut_tempfixed_paper.csv", low_memory=False)

df['DeltaP'] = df['Pw'] - df['Pair']
df = cuts0910(df)
# # df = df[df.Year == 2009]
# df = df[df.Year == 2010]

# df = df.drop(df[(df.Sim == 166) & (df.Team == 1)].index)

dfp = df[df.DeltaP > 0]
dfp  = df

#
#
df['TPintC'] = df['TPext'] - 273
df['TPextC'] = df['TPint'] - 273
df['TPintK'] = df['TPext']
df['TPextK'] = df['TPint']
df['TcellC'] = df['Tcell'] - 273
df['TboilK'] = df['Tboil'] + 273
#
#

### filter for each sonde solution

filtEN = df.ENSCI == 1
filtSP = df.ENSCI == 0

filtS10 = df.Sol == 1
filtS05 = df.Sol == 0.5

filtB10 = df.Buf == 1.0
filtB05 = df.Buf == 0.5
filtB01 = df.Buf == 0.1

filterEN0505 = (filtEN & filtS05 & filtB05)
filterEN1010 = (filtEN & filtS10 & filtB10)
#2017
# filterEN1010 = (filtEN & filtS10 & filtB01)

###
profEN0505 = df.loc[filterEN0505]
profEN1010 = df.loc[filterEN1010]
profEN0505_dp = dfp.loc[filterEN0505]
profEN1010_dp = dfp.loc[filterEN1010]
profEN0505_nodup = profEN0505.drop_duplicates(['Sim', 'Team'])
profEN1010_nodup = profEN1010.drop_duplicates(['Sim', 'Team'])
###
filterSP1010 = (filtSP & filtS10 & filtB10)
filterSP0505 = (filtSP & filtS05 & filtB05)
#2017
# filterSP0505 = (filtSP & filtS10 & filtB01)

profSP1010 = df.loc[filterSP1010]
profSP0505 = df.loc[filterSP0505]
profSP1010_dp = dfp.loc[filterSP1010]
profSP0505_dp = dfp.loc[filterSP0505]
profSP1010_nodup = profSP1010.drop_duplicates(['Sim', 'Team'])
profSP0505_nodup = profSP0505.drop_duplicates(['Sim', 'Team'])

# prof = [profEN0505, profEN1010, profSP0505, profSP1010]

#
#
avgprof_tpint, avgprof_tpint_err, Y = Calc_average_profile_pressure([profEN0505, profEN1010, profSP0505, profSP1010], 'TPintC')
avgprof_tpext, avgprof_tpext_err, Y = Calc_average_profile_pressure([profEN0505, profEN1010, profSP0505, profSP1010], 'TPextC')
avgprof_tpcell, avgprof_tpcell_err, Y = Calc_average_profile_pressure([profEN0505, profEN1010, profSP0505, profSP1010], 'TcellC')
avgprof_tpboil, avgprof_tpboil_err, Y = Calc_average_profile_pressure([profEN0505, profEN1010, profSP0505, profSP1010], 'Tboil')

avgprof_deltap, avgprof_deltap_err, Yp = Calc_average_profile_pressure([profEN0505_dp, profEN1010_dp, profSP0505_dp, profSP1010_dp], 'DeltaP')
avgprof_pw, avgprof_pw_err, Yp = Calc_average_profile_pressure([profEN0505_dp, profEN1010_dp, profSP0505_dp, profSP1010_dp], 'Pw')


avgprof_tpintK, avgprof_tpintK_err, Y = Calc_average_profile_pressure([profEN0505, profEN1010, profSP0505, profSP1010], 'TPintK')
avgprof_tpextK, avgprof_tpextK_err, Y = Calc_average_profile_pressure([profEN0505, profEN1010, profSP0505, profSP1010], 'TPextK')
avgprof_tpcellK, avgprof_tpcellK_err, Y = Calc_average_profile_pressure([profEN0505, profEN1010, profSP0505, profSP1010], 'Tcell')
avgprof_tpboilK, avgprof_tpboilK_err, Y = Calc_average_profile_pressure([profEN0505, profEN1010, profSP0505, profSP1010], 'TboilK')



adif = [0] * 4
adiferr = [0] * 4
rdif = [0] * 4
rdiferr = [0] * 4

adif_cell = [0] * 4
adif_cellerr = [0] * 4
rdif_cell = [0] * 4
rdif_cellerr = [0] * 4


#
for k in range(4):

    adif[k] = [i - j for i,j in zip(avgprof_tpint[k], avgprof_tpext[k])]
    adiferr[k] = [np.sqrt(i*i + j*j) for i,j in zip(avgprof_tpint_err[k], avgprof_tpext_err[k])]

    rdif[k] = [(i - j)/j * 100 for i, j in zip(avgprof_tpintK[k], avgprof_tpextK[k])]
    rdiferr[k] = [np.sqrt((ie * ie)/(i*i) + (je * je)/(j*j)) for ie, je, i, j
                  in zip(avgprof_tpintK_err[k], avgprof_tpextK_err[k], avgprof_tpintK[k], avgprof_tpextK[k])]

    adif_cell[k] = [i - j for i, j in zip(avgprof_tpcell[k], avgprof_tpboil[k])]
    adif_cellerr[k] = [np.sqrt(i * i + j * j) for i, j in zip(avgprof_tpcell_err[k], avgprof_tpboil_err[k])]

    rdif_cell[k] = [(j - i) / i * 100 for i, j in zip(avgprof_tpcellK[k], avgprof_tpboilK[k])]
    rdif_cellerr[k] = [np.sqrt((ie * ie) / (i * i) + (je * je) / (j * j)) for ie, je, i, j
                  in zip(avgprof_tpcellK_err[k], avgprof_tpboilK_err[k], avgprof_tpcellK[k], avgprof_tpboilK[k])]


###  part a

mtitle0 = '0910 EN 0.5%-0.5B'
stitle0 = '0910_EN0505_RADif_sr'

mtitle1 = '0910 EN 1.0%-0.1B'
stitle1 = '0910_EN1001_RADif_sr'

# mtitle1 = '0910 EN 1.0%-1.0B'
# stitle1 = '0910_EN1010_RADif_sr'
#
mtitle2 = '0910 SP 0.5%-0.5B'
stitle2 = '0910_SP0505_RADif_sr'
#
# mtitle2 = '0910 SP 1.0%-0.1B'
# stitle2 = '0910_SP1001_RADif_sr'

mtitle3 = '0910 SP 1.0%-1.0B'
stitle3 = '0910_SP1010_RADif_sr'

# p1, = host.plot(avgprof_tpint[0], Y, label="TPint ")
# p2, = host.plot(avgprof_tpext[0], Y, label="TPext ")
# p3, = host.plot(avgprof_tpcell[0], Y, label="TPext generated ")
# p4, = par1.plot(rdif[0], Y, label="RDif")
# p5, = par2.plot(adif[0], Y, label="ADif")

# plothost(avgprof_tpint[0], avgprof_tpext[0],  avgprof_tpcell[0], rdif[0], adif[0], Y, mtitle0, stitle0)
# plothost(avgprof_tpint[1], avgprof_tpext[1],  avgprof_tpcell[1], rdif[1], adif[1], Y, mtitle1, stitle1)
# plothost(avgprof_tpint[2], avgprof_tpext[2],  avgprof_tpcell[2], rdif[2], adif[2], Y, mtitle2, stitle2)
# plothost(avgprof_tpint[3], avgprof_tpext[3],  avgprof_tpcell[3], rdif[3], adif[3], Y, mtitle3, stitle3)

# plothost(avgprof_tpint[0], avgprof_tpext[0],  rdif[0], adif[0], Y, mtitle0, stitle0)
# plothost(avgprof_tpint[1], avgprof_tpext[1], rdif[1], adif[1], Y, mtitle1, stitle1)
# plothost(avgprof_tpint[2], avgprof_tpext[2],   rdif[2], adif[2], Y, mtitle2, stitle2)
# plothost(avgprof_tpint[3], avgprof_tpext[3],   rdif[3], adif[3], Y, mtitle3, stitle3)

plothost(avgprof_tpint[0], avgprof_tpext[0],  avgprof_tpboil[0],  avgprof_tpcell[0], avgprof_pw[0],  avgprof_deltap[0], adif_cell[0], Y,  mtitle0, stitle0)
plothost(avgprof_tpint[1], avgprof_tpext[1],  avgprof_tpboil[1],  avgprof_tpcell[1], avgprof_pw[1], avgprof_deltap[1], adif_cell[1], Y,  mtitle1, stitle1)
plothost(avgprof_tpint[2], avgprof_tpext[2],  avgprof_tpboil[2],  avgprof_tpcell[2], avgprof_pw[2], avgprof_deltap[2], adif_cell[2], Y,  mtitle2, stitle2)
plothost(avgprof_tpint[3], avgprof_tpext[3],  avgprof_tpboil[3],  avgprof_tpcell[3], avgprof_pw[3], avgprof_deltap[3], adif_cell[3], Y,  mtitle3, stitle3)

# plothost(avgprof_tpint[1], avgprof_tpext[1], avgprof_tpboil[1], avgprof_tpcell[1],  adif_cell[1], Y, mtitle1, stitle1)
# plothost(avgprof_tpint[2], avgprof_tpext[2], avgprof_tpboil[2],  avgprof_tpcell[2],  adif_cell[2], Y, mtitle2, stitle2)
# plothost(avgprof_tpint[3], avgprof_tpext[3], avgprof_tpboil[3], avgprof_tpcell[3], adif_cell[3], Y, mtitle3, stitle3)

# host = host_subplot(111, axes_class=AA.Axes)
# plt.subplots_adjust(bottom=0.30)
#
# par1 = host.twiny()
# par2 = host.twiny()
#
# new_fixed_axis = par1.get_grid_helper().new_fixed_axis
# par1.axis["bottom"] = new_fixed_axis(loc="bottom",
#                                     axes=par1,
#                                     offset=(0, -30))
# par2.axis["bottom"] = new_fixed_axis(loc="bottom",
#                                     axes=par2,
#                                     offset=(0, -60))
#
# par1.axis["bottom"].toggle(all=True)
#
# host.set_ylabel("Pressure")
# host.set_xlabel("Temp (C)")
# host.set_title(mtitle0)
# # host.set_title("SP 1.0%-1.0B")
# host.set_ylim(1000, 3)
# host.set_yscale('log')
#
#
# par1.set_xlabel("TCell - TBoil/ TBoil [%]")
# par2.set_xlabel("TCell - TBoil.")
#
# p1, = host.plot(avgprof_tpint[0], Y, label="TPint ")
# p2, = host.plot(avgprof_tpext[0], Y, label="TPext ")
# p3, = host.plot(avgprof_tpcell[0], Y, label="TPext generated ")
# p4, = par1.plot(rdif[0], Y, label="RDif")
# p5, = par2.plot(adif[0], Y, label="ADif")
#
#
# # host.legend()
# host.legend(ncol=4, loc='upper center')
#
#
# host.axis["bottom"].label.set_color(p1.get_color())
# par1.axis["bottom"].label.set_color(p3.get_color())
# par2.axis["bottom"].label.set_color(p4.get_color())
#
# plt.draw()
#
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/' + stitle0 + '.png')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/' + stitle0 + '.pdf')
# plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/Temperature/' + stitle0 + '.eps')
#
# plt.show()



#
# avgprof_tpint_sp, avgprof_tpint_sp_err, Y = Calc_average_profile_pressure([dfsp], 'TPintC')
# avgprof_tpext_sp, avgprof_tpext_sp_err, Y = Calc_average_profile_pressure([dfsp], 'TPextC')
#
# avgprofgen_tpint_pre, avgprofgen_tpint_pre_err, Y = Calc_average_profile_pressure([dfgen], 'TPintC')
# avgprofgen_tpext_pre, avgprofgen_tpext_pre_err, Y = Calc_average_profile_pressure([dfgen], 'TPextC')
#
# # print('avgprofgen_tpint_pre', avgprofgen_tpint_pre)
# # print('avgprofgen_tpext_pre', avgprofgen_tpext_pre)
# #
# adifall_en = [i - j for i,j in zip(avgprof_tpint_en[0], avgprof_tpext_en[0])]
# adifall_en_err = [np.sqrt(i*i + j*j) for i,j in zip(avgprof_tpint_en_err[0], avgprof_tpext_en_err[0])]
#
# adifall_sp = [i - j for i,j in zip(avgprof_tpint_sp[0], avgprof_tpext_sp[0])]
# adifall_sp_err = [np.sqrt(i*i + j*j) for i,j in zip(avgprof_tpint_sp_err[0], avgprof_tpext_sp_err[0])]
#
# # rdifall = [(i - j)/i * 100  for i, j in zip(avgprof_tpint_pre[0], avgprof_tpext_pre[0])]
# # rdifall_err = [np.sqrt((ie * ie)/(i*i) + (je * je)/(j*j)) for ie, je, i, j
# #                  in zip(avgprof_tpint_pre_err[0], avgprof_tpext_pre_err[0], avgprof_tpint_pre_err[0], avgprof_tpext_pre_err[0])]
#
# ##fit
#
# p_enf, p_spf = polyfit(df)
#
# print('p_enf[0]', p_enf[0], p_enf[14])
#
# print('Y', Y)
# print('p(Y)', p_enf(Y) )
# # c_en, stats_en = np.polyfit(Y, adifall_en, 15)
# # c_sp, stats_sp = np.polyfit(Y, adifall_sp, 15)
# # print('c_en', c_en)
# # print('c_sp', c_sp)
# # p2 = np.poly1d(np.polyfit(Y, adifall, 12))
# # p3 = np.poly1d(np.polyfit(Y, adifall, 13))
# # p4 = np.poly1d(np.polyfit(Y, adifall, 14))
# # p5 = np.poly1d(np.polyfit(Y, adifall, 15))
#
#
