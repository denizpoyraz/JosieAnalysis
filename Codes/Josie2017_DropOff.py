import pandas as pd
import numpy as np
import glob
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt
from makeDF_Functions import calculate_O3frac17
from Analyse_Functions import polyfit
from Josie_PlotFunctions import Plot_Simulation_PlotsTime

def plothost(hostarr1, hostarr2, twinarr1, Y,  mtitle, stitle ):
# def plothost(hostarr1, hostarr2, hostarr3, twinarr1, twinarr2, Y, mtitle, stitle):
# def plothost(hostarr1, hostarr2,  twinarr1, twinarr2, Y, mtitle, stitle):
    #
    plt.close('all')

    host = host_subplot(111, axes_class=AA.Axes)
    plt.subplots_adjust(bottom=0.27)

    par1 = host.twiny()
    # par2 = host.twiny()
    # par3 = host.twiny()


    new_fixed_axis = par1.get_grid_helper().new_fixed_axis
    par1.axis["bottom"] = new_fixed_axis(loc="bottom",
                                         axes=par1,
                                         offset=(0, -30))
    # par2.axis["bottom"] = new_fixed_axis(loc="bottom",
    #                                      axes=par2,
    #                                      offset=(0, -60))
    # par3.axis["bottom"] = new_fixed_axis(loc="bottom",
    #                                      axes=par3,
    #                                      offset=(0, -60))

    par1.axis["bottom"].toggle(all=True)

    host.set_ylabel("Time")
    host.set_xlabel("Temp (C)")
    host.set_title(mtitle)
    # host.set_title("SP 1.0%-1.0B")
    host.set_xlim(0, 35)
    host.set_ylim(0, 7000)
    # host.set_yscale('log')

    # # par1.set_xlabel("TBoil - TCell/ TCell [%]")
    par1.set_xlabel(r"P$_{saturation}$ - Pair")
    # par2.set_xlabel("Pw")
    par1.set_xlim(-20,10)
    # par2.set_xlim(-15,10)
    # p4, = par1.plot(twinarr1, Y, label="TBoil")
    p5, = par1.plot(twinarr1, Y, label=r"P$_{saturation}$ - Pair")

    p3, = host.plot(hostarr1, Y, label="TCell gen.")
    p4, = host.plot(hostarr2, Y, label="TBoil")

    host.legend(ncol=4, loc='lower center')

    # host.axis["bottom"].label.set_color(p1.get_color())
    # par1.axis["bottom"].label.set_color(p4.get_color())
    par1.axis["bottom"].label.set_color(p5.get_color())
    # par3.axis["bottom"].label.set_color(p3.get_color())

    plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/ENSCI_DropOff/DeltaP_' + stitle + '.png')
    # plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/ENSCI_DropOff/DeltaP_' + stitle + '.pdf')
    plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/ENSCI_DropOff/DeltaP_' + stitle + '.eps')
    # plt.show()

    plt.close('all')

df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_Data_nocut_1607.csv", low_memory=False)

df['DeltaP'] = df['Pw'] - df['Pair']
# df = cuts0910(df)
# # df = df[df.Year == 2009]
# df = df[df.Year == 2010]

# df = df.drop(df[(df.Sim == 166) & (df.Team == 1)].index)

# dfp = df[df.DeltaP > 0]
# dfp  = df

## filter for each sonde solution
sim = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Sim'].tolist())
team = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Team'].tolist())
sol = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Sol'].tolist())
buff = np.asarray(df.drop_duplicates(['Sim', 'Team'])['Buf'])
ensci = np.asarray(df.drop_duplicates(['Sim', 'Team'])['ENSCI'])

# dfsim = df.drop_duplicates(['Sim'])
# simlist = dfsim.Sim.tolist()
nsim = len(sim)

print(list(df))

dft = {}

TempBoil = [0] * nsim
TempCell = [0] * nsim
Pair = [0] * nsim
Time = [0] * nsim
Pw = [0] * nsim
DeltaP = [0] * nsim
Current = [0] * nsim

ssttitle = [''] * nsim

print(sim)
print(team)

for j in range(nsim):

    if ensci[j] == 0:
        sondestr = 'SPC'
    else:
        sondestr = 'ENSCI'

    if sol[j] == 2.0: solstr = '2p0'
    if sol[j] == 1.0: solstr = '1p0'
    if sol[j] == 0.5: solstr = '0p5'

    if buff[j] == 0.1: bufstr = '0p1'
    if buff[j] == 0.5: bufstr = '0p5'
    if buff[j] == 1.0: bufstr = '1p0'

    ssttitle[j] = str(sim[j]) + '_' + str(team[j])  + ' ' + sondestr + ' ' + str(sol[j]) + '% - ' + str(buff[j]) + 'B'
    figname = str(sim[j]) + '_' + str(team[j])
    print(ssttitle[j], figname)


    dft[j] = df[(df.Sim == sim[j]) & (df.Team == team[j])]

    TempBoil[j] = dft[j].Tboil.tolist()
    TempCell[j] = dft[j].TcellC.tolist()
    Pw[j] = dft[j].Pw.tolist()
    DeltaP[j] = (dft[j].Pw - dft[j].Pair).tolist()
    Current[j] = dft[j].IM.tolist()

    Pair[j] = dft[j].Pair.tolist()
    Time[j] = dft[j].Tsim.tolist()

    plothost(TempCell[j], TempBoil[j], DeltaP[j], Time[j], ssttitle[j], figname)

#
# print('TBoil', TempBoil[2])
#
# for s,t in zip(sim,team):
#     ind = np.where(sim == s)[0]
#     indt = np.where(team == t)[0]
#
#     print(s, t, ind, indt)
#     tind = 999
#     if ind == indt:
#         tind = ind
#
#     print('tind', tind)
#     titlestr = 'Simulation ' + str(s)
#     plotstr = 'ProfileSimulationTime_' + str(s)
#     plotstr_pair = 'ProfileSimulationPressure_' + str(s)
#     # print(s, titlestr, plotstr)
#
#     # if(s == 140):
#     #
#     # Plot_Simulation_PlotsTime(ind, ssttitle,  TempCell, TempBoil, Time, [0, 35],  [0, 7000],  'Temp (C)', 'Elapsed Time (sec)'
#     #                          , titlestr, plotstr, 'two')
#
#     # Plot_Simulation_PlotsTime(ind, ssttitle,  Current, TempBoil, Time, [0, 8],  [0, 7000],  'Temp (C)', 'Elapsed Time (sec)'
#     #                          , titlestr, plotstr, 'standard')
#     # print('TBoil', TempBoil[ind[0]])
#     # print('time', Time[ind[0]])
#
#     # plothost(ind, TempCell[ind[0]], TempBoil[ind[0]], DeltaP[ind[0]], Time[ind[0]], titlestr, titlestr)
