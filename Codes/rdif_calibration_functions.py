import pandas as pd
import numpy as np
import re
import glob
import math
from math import log
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib.offsetbox import AnchoredText

from Josie_Functions import Calc_average_profile, Calc_average_profile_Pair
from Josie_Functions import Calc_RDif
from Josie_Functions import meanfunction


###############################################################################
def correct_Rdif(dfm, Rdif, Ys):
    corr = [0] * len(Rdif)
    for ir in range(len(Rdif)):
        # corr[ir] = 1 - Rdif[ir] / 100
        corr[ir] = Rdif[ir] / 100 + 1

        if ((dfm.Pair <= Ys[ir]) & (dfm.Pair > Ys[ir + 1])):
            return dfm.PO3 / corr[ir]
            # return  corr[ir] / dfm.PO3


##########################

def correct_Adif(dfm, Adif, Ys):
    corr = [0] * len(Adif)
    for ir in range(len(Adif)):
        # print(ir, Rdif[ir])
        corr[ir] = Adif[ir]
        if ((dfm.Pair <= Ys[ir]) & (dfm.Pair > Ys[ir + 1])):
            # print(ir, Ys[ir],tmp)
            return dfm.PO3  - corr[ir]


#####################################################################################
# def correctedPlot_PerCategory(category, rdiff,yf,  dfm, pltitle, plname ):
# def correctedPlot_PerCategory(dfm, rdiff,yf,  pltitle, plname ):
def correctedPlot_PerCategory(x1, x2, x3, yy, pltitle, plname):
    fig, ax = plt.subplots()
    plt.xlim(0, 30)
    plt.ylim(1000, 5)
    plt.title(pltitle)
    plt.xlabel('PO3 (hPa)')
    plt.ylabel(r'Pair (mPa)')
    ax.set_yscale('log')

    x3 = np.asarray(x3)

    plt.plot(x1, yy, '-.', label='OPM', linewidth=2.0)
    plt.plot(x2, yy, '-.', label='Sonde', linewidth=2.0)
    plt.plot(np.squeeze(x3), yy, '-.', label='Sonde with correction', linewidth=2.0)
    ax.legend(loc='upper right', frameon=True, fontsize='small')

    plt.savefig('/home/poyraden/Josie17/Plots/Calibration_1718/RdifCorrected_wOPM_' + plname + '.pdf')
    plt.savefig('/home/poyraden/Josie17/Plots/Calibration_1718/RdifCorrected_wOPM_' + plname + '.eps')


##########################################################
def correctedPlot_AllCategory(x1, x2, x3, x4, xc1, xc2, xc3, xc4, yy, pltitle, plname):
    Y = yy

    fig, ax = plt.subplots()
    plt.xlim(0, 30)
    plt.ylim(1000, 5)
    plt.title('Not Corrected')
    plt.xlabel('PO3 (hPa)')
    plt.ylabel(r'Pair (mPa)')
    ax.set_yscale('log')

    plt.plot(x1, yy, '-.', label='SP 1.0%-1.0B', linewidth=2.0)
    plt.plot(x2, yy, '-.', label='SP 1.0%-0.1B', linewidth=2.0)
    plt.plot(x3, yy, '-.', label='EN 1.0%-0.1B', linewidth=2.0)
    plt.plot(x4, yy, '-.', label='EN 0.5%-0.5B', linewidth=2.0)

    ax.legend(loc='upper right', frameon=True, fontsize='small')

    plt.savefig('/home/poyraden/Josie17/Plots/Calibration_1718/NOTCorrected_All_RDif_' + plname + '.pdf')
    plt.savefig('/home/poyraden/Josie17/Plots/Calibration_1718/NOTCorrected_All_RDif_' + plname + '.eps')

    fig, ax1 = plt.subplots()
    plt.xlim(0, 30)
    plt.ylim(1000, 5)
    plt.title('Corrected')
    plt.xlabel('PO3 (hPa)')
    plt.ylabel(r'Pair (mPa)')
    ax1.set_yscale('log')

    plt.plot(np.squeeze(xc1), Y, '-.', label='SP 1.0%-1.0B', linewidth=2.0)
    plt.plot(np.squeeze(xc2), Y, '-.', label='SP 1.0%-0.1B', linewidth=2.0)
    plt.plot(np.squeeze(xc3), Y, '-.', label='EN 1.0%-0.1B', linewidth=2.0)
    plt.plot(np.squeeze(xc4), Y, '-.', label='EN 0.5%-0.5B', linewidth=2.0)

    ax1.legend(loc='upper right', frameon=True, fontsize='small')

    plt.savefig('/home/poyraden/Josie17/Plots/Calibration_1718/Corrected_All_RDif_' + plname + '.pdf')
    plt.savefig('/home/poyraden/Josie17/Plots/Calibration_1718/Corrected_All_RDif_' + plname + '.eps')


###########################################################################################################
def plot_2difPlots(r1, r1err, r2, r2err, a1, a1err, a2, a2err, yy, pltitle, plname):
    Y = yy

    fig, ax1 = plt.subplots()
    plt.xlim(-20, 20)
    plt.ylim(1000, 5)
    plt.title(pltitle)
    plt.ylabel('PO3 (hPa)')
    plt.xlabel(r'Sonde1 - Sonde2 (%)')
    ax1.axvline(x=0, color='grey', linestyle='--')
    ax1.set_yscale('log')

    ax1.errorbar(r1, Y, xerr=r1err, label='No Correction', linewidth=1, elinewidth=0.5, capsize=1, capthick=0.5)
    ax1.errorbar(r2, Y, xerr=r2err, label='Correction', linewidth=1, elinewidth=0.5, capsize=1, capthick=0.5)
    ax1.legend(loc='upper right', frameon=True, fontsize='small')
    plt.savefig('/home/poyraden/Josie17/Plots/Calibration_1718/RDifCorrected_RDif_' + plname + '.pdf')
    plt.savefig('/home/poyraden/Josie17/Plots/Calibration_1718/RDifCorrected_RDif_' + plname + '.eps')

    fig, ax2 = plt.subplots()
    plt.xlim(-3, 3)
    plt.ylim(1000, 5)
    plt.title(pltitle)
    plt.ylabel('PO3 (hPa)')
    plt.xlabel(r'Sonde1 - Sonde2 (%)')
    ax2.set_yscale('log')
    ax2.axvline(x=0, color='grey', linestyle='--')

    ax2.errorbar(a1, Y, xerr=a1err, label='No Correction', linewidth=1, elinewidth=0.5, capsize=1, capthick=0.5)
    ax2.errorbar(a2, Y, xerr=a2err, label='Correction', linewidth=1, elinewidth=0.5, capsize=1, capthick=0.5)
    ax2.legend(loc='upper right', frameon=True, fontsize='small')
    plt.savefig('/home/poyraden/Josie17/Plots/Calibration_1718/RDifCorrected_ADif_' + plname + '.pdf')
    plt.savefig('/home/poyraden/Josie17/Plots/Calibration_1718/RdifCorrected_ADif_' + plname + '.eps')

########################################################################################################################
