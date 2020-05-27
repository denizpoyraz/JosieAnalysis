# Functions used for the analysis of Josie17 simulation data
# 16/01/2019

import pandas as pd
import numpy as np
import re
import glob
import math
from math import log
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib.offsetbox import AnchoredText


def errorPlot_ARDif_withtext(xlist, xerrorlist, Y, xra, yra, maintitle, xtitle, ytitle, labelist, O3valuelist, dfnoduplist,
                          plotname, path, logbool, textbool):
    '''

    :param xlist: a list of x values
    :param xerrorlist: a list of x error values
    :param Y:
    :param xra: x range
    :param yra: y range
    :param maintitle:
    :param xtitle:
    :param ytitle:
    :param labelist: a list of the labels
    :param O3valuelist: specific total O3 fractions
    :param dfnoduplist: a list of df_noduplicated(sim), in order to know number of simulations
    :param plotname: how you want to save your plot
    :param path: folder name in Plots folder
    :param logbool: True if you want logarithmic scale
    :param textbool: True if you want an additional text
    :return: just plots
    '''

    d = len(xlist)
    n = [0] * d
    labell = [''] * d
    textl = [''] * d
    tl = [''] * d
    colorl = ['black', 'red', 'blue', 'green']

    ## y locations of the extra text which is drawn for the total O3 values
    texty = [0.23, 0.16, 0.09, 0.02]

    plt.close('all')
    fig, ax = plt.subplots()
    plt.xlim(xra)
    plt.ylim(yra)
    plt.title(maintitle)
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    plt.grid(True)

    # plt.yticks(np.arange(0, 7001, 1000))

    # reference line
    ax.axvline(x=0, color='grey', linestyle='--')
    if logbool: ax.set_yscale('log')

    for i in range(d):
        n[i] = len(dfnoduplist[i])
        labell[i] = labelist[i] + ' ( n =' + str(n[i]) + ')'
        textl[i] = 'tot O3 ratio: ' + str(round(O3valuelist[0], 2))

        ax.errorbar(xlist[i], Y, xerr=xerrorlist[i], label=labell[i], color=colorl[i], linewidth=1, elinewidth=0.5,
                    capsize=1,
                    capthick=0.5)

        if textbool: tl[i] = ax.text(0.05, texty[i], textl[i], color=colorl[i], transform=ax.transAxes)

    # ax.tick_params(axis='both', which='both', direction='in')
    # ax.yaxis.set_ticks_position('both')
    # ax.xaxis.set_ticks_position('both')
    #
    # ax.yaxis.set_minor_locator(AutoMinorLocator(10))
    # ax.xaxis.set_minor_locator(AutoMinorLocator(10))
    # ax.legend(loc='lower right', frameon=True, fontsize='small')

    ax.legend(loc='lower left', frameon=False, fontsize='x-small')

    # plt.show()

    plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/' + path + '/' + plotname + '.png')
    plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/' + path + '/' + plotname + '.eps')
    plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/' + path + '/' + plotname + '.pdf')


    plt.close()
#####################################################



def errorPlot_general(xlist, xerrorlist, Y, xra, yra, maintitle, xtitle, ytitle, labelist, colorlist, plotname, path, logbool, linestylebool, fillbool):
    '''

    :param xlist:
    :param xerrorlist:
    :param Y:
    :param xra:
    :param yra:
    :param maintitle:
    :param xtitle:
    :param ytitle:
    :param labelist:
    :param plotname:
    :param logbool:
    :param linestylebool:
    :return: just plots
    '''


    d = len(xlist)
    n = [0] * d
    labell = [''] * d
    # colorl = ['black', 'red', 'blue', 'green']
    dimension = len(xlist[0])

    plus = [[0] * dimension for i in range(d)]
    minus = [[0] * dimension for i in range(d)]
    plus1 = [[0] * dimension for i in range(d)]
    minus1 = [[0] * dimension for i in range(d)]

    for j in range(d):
        plus[j] = [xlist[j][i] + 3  for i in range(dimension)]
        minus[j] = [xlist[j][i] - 3 for i in range(dimension)]
        plus1[j] = [xlist[j][i] + 1 for i in range(dimension)]
        minus1[j] = [xlist[j][i] - 1 for i in range(dimension)]

    plt.close('all')
    fig, ax = plt.subplots()
    plt.xlim(xra)
    plt.ylim(yra)
    plt.title(maintitle)
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    plt.grid(True)

    lstyle = ['--', ':', '-.', '--', ':', '-.', '--', ':', '-.', '--', ':', '-.', '--', ':', '-.']

    # plt.yticks(np.arange(0, 7001, 1000))

    # reference line
    ax.axvline(x=0, color='grey', linestyle='--')
    if logbool: ax.set_yscale('log')

    for i in range(d):
        labell[i] = labelist[i]
        if not linestylebool:
            ax.errorbar(xlist[i], Y, xerr=xerrorlist[i], label=labell[i], color=colorlist[i], linewidth=1, elinewidth=0.5,capsize=1, capthick=0.5)
        if linestylebool:
            ax.errorbar(xlist[i], Y, xerr=xerrorlist[i], label=labell[i], color=colorlist[i], linewidth=1, elinewidth=0.5,capsize=1, capthick=0.5, linestyle=lstyle[i])
        if fillbool:
          ax.fill_betweenx(Y, minus[0], plus[0], alpha=0.1, facecolor='k', edgecolor= 'lightgrey')
          ax.fill_betweenx(Y, minus1[0], plus1[0], alpha=0.1, facecolor='k', edgecolor= 'lightblue')


    ax.legend(loc='lower right', frameon=True, fontsize='x-small')


    plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/' + path + '/' + plotname + '.png')
    plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/' + path + '/' + plotname + '.eps')
    plt.savefig('/home/poyraden/Analysis/JosieAnalysis/Plots/' + path + '/' + plotname + '.pdf')


    plt.close()
#####################################################




#####################################################
#####################################################

###  the rest of the plot functions need to be updated


def Plot_Profile_PlotsTime(ind, teaml, prof_X, prof_Xerr, OPM_X, OPM_Xerr, Y, xra, yra, xtit, ytit, mtitle, plotname,
                           keyword):
    plt.close('all')
    fig, ax = plt.subplots()
    plt.xlim(xra)
    plt.ylim(yra)
    plt.xlabel(xtit)
    plt.ylabel(ytit)
    plt.title(mtitle)

    if (keyword == 'standard'):
        if (len(ind) == 4):
            ax.errorbar(OPM_X[ind[0]], Y, xerr=OPM_Xerr[ind[0]], label="OPM", color='black', linewidth=2.5,
                        elinewidth=0.5, capsize=1,
                        capthick=0.5, linestyle=':')
            ax.errorbar(prof_X[ind[0]], Y, xerr=prof_Xerr[ind[0]], label="Team " + str(teaml[ind[0]]), color='red',
                        linewidth=1.5, elinewidth=0.5,
                        capsize=1, capthick=0.5, linestyle='--')
            ax.errorbar(prof_X[ind[1]], Y, xerr=prof_Xerr[ind[1]], label="Team " + str(teaml[ind[1]]), color='green',
                        linewidth=1.5, elinewidth=0.5,
                        capsize=1, capthick=0.5, linestyle='-.')
            ax.errorbar(prof_X[ind[2]], Y, xerr=prof_Xerr[ind[2]], label="Team " + str(teaml[ind[2]]), color='blue',
                        linewidth=1.5, elinewidth=0.5,
                        capsize=1, capthick=0.5, linestyle='--')
            ax.errorbar(prof_X[ind[3]], Y, xerr=prof_Xerr[ind[3]], label="Team " + str(teaml[ind[3]]),
                        color='goldenrod', linewidth=1.5,
                        elinewidth=0.5, capsize=1, capthick=0.5, linestyle='-.')

        if (len(ind) == 3):
            ax.errorbar(OPM_X[ind[0]], Y, xerr=OPM_Xerr[ind[0]], label="OPM", color='black', linewidth=2.5,
                        elinewidth=0.5, capsize=1,
                        capthick=0.5, linestyle=':')
            ax.errorbar(prof_X[ind[0]], Y, xerr=prof_Xerr[ind[0]], label="Team " + str(teaml[ind[0]]), color='red',
                        linewidth=1.5, elinewidth=0.5,
                        capsize=1, capthick=0.5, linestyle='--')
            ax.errorbar(prof_X[ind[1]], Y, xerr=prof_Xerr[ind[1]], label="Team " + str(teaml[ind[1]]), color='green',
                        linewidth=1.5, elinewidth=0.5,
                        capsize=1, capthick=0.5, linestyle='-.')
            ax.errorbar(prof_X[ind[2]], Y, xerr=prof_Xerr[ind[2]], label="Team " + str(teaml[ind[2]]), color='blue',
                        linewidth=1.5, elinewidth=0.5,
                        capsize=1, capthick=0.5, linestyle='--')
        if (len(ind) == 2):
            ax.errorbar(OPM_X[ind[0]], Y, xerr=OPM_Xerr[ind[0]], label="OPM", color='black', linewidth=2.5,
                        elinewidth=0.5, capsize=1,
                        capthick=0.5, linestyle=':')
            ax.errorbar(prof_X[ind[0]], Y, xerr=prof_Xerr[ind[0]], label="Team " + str(teaml[ind[0]]), color='red',
                        linewidth=1.5, elinewidth=0.5,
                        capsize=1, capthick=0.5, linestyle='--')
            ax.errorbar(prof_X[ind[1]], Y, xerr=prof_Xerr[ind[1]], label="Team " + str(teaml[ind[1]]), color='green',
                        linewidth=1.5, elinewidth=0.5,
                        capsize=1, capthick=0.5, linestyle='-.')

    ax.legend(loc='lower right', frameon=True, fontsize='small')

    plt.savefig('/home/poyraden/Analysis/Josie_Analysis/Plots/ProfilePlots_withtimecut_v2/' + plotname + '.pdf')
    plt.savefig('/home/poyraden/Analysis/Josie_Analysis/Plots/ProfilePlots_withtimecut_v2/' + plotname + '.eps')


def Plot_Profile_PlotsPair(ind, teaml, prof_X, prof_Xerr, OPM_X, OPM_Xerr, Y, xra, yra, xtit, ytit, mtitle, plotname,
                           keyword):
    plt.close('all')
    fig, ax = plt.subplots()
    plt.xlim(xra)
    plt.ylim(yra)
    plt.xlabel(xtit)
    plt.ylabel(ytit)
    plt.title(mtitle)
    ax.set_yscale('log')

    if (keyword == 'standard'):
        if (len(ind) == 4):
            ax.errorbar(OPM_X[ind[0]], Y, xerr=OPM_Xerr[ind[0]], label="OPM", color='black', linewidth=2.5,
                        elinewidth=0.5, capsize=1,capthick=0.5, linestyle=':')
            ax.errorbar(prof_X[ind[0]], Y, xerr=prof_Xerr[ind[0]], label="Team " + str(teaml[ind[0]]), color='red',
                        linewidth=1.5, elinewidth=0.5,capsize=1, capthick=0.5, linestyle='--')
            ax.errorbar(prof_X[ind[1]], Y, xerr=prof_Xerr[ind[1]], label="Team " + str(teaml[ind[1]]), color='green',
                        linewidth=1.5, elinewidth=0.5,
                        capsize=1, capthick=0.5, linestyle='-.')
            ax.errorbar(prof_X[ind[2]], Y, xerr=prof_Xerr[ind[2]], label="Team " + str(teaml[ind[2]]), color='blue',
                        linewidth=1.5, elinewidth=0.5,
                        capsize=1, capthick=0.5, linestyle='--')
            ax.errorbar(prof_X[ind[3]], Y, xerr=prof_Xerr[ind[3]], label="Team " + str(teaml[ind[3]]),
                        color='goldenrod', linewidth=1.5,
                        elinewidth=0.5, capsize=1, capthick=0.5, linestyle='-.')

        if (len(ind) == 3):
            ax.errorbar(OPM_X[ind[0]], Y, xerr=OPM_Xerr[ind[0]], label="OPM", color='black', linewidth=2.5,
                        elinewidth=0.5, capsize=1,
                        capthick=0.5, linestyle=':')
            ax.errorbar(prof_X[ind[0]], Y, xerr=prof_Xerr[ind[0]], label="Team " + str(teaml[ind[0]]), color='red',
                        linewidth=1.5, elinewidth=0.5,
                        capsize=1, capthick=0.5, linestyle='--')
            ax.errorbar(prof_X[ind[1]], Y, xerr=prof_Xerr[ind[1]], label="Team " + str(teaml[ind[1]]), color='green',
                        linewidth=1.5, elinewidth=0.5,
                        capsize=1, capthick=0.5, linestyle='-.')
            ax.errorbar(prof_X[ind[2]], Y, xerr=prof_Xerr[ind[2]], label="Team " + str(teaml[ind[2]]), color='blue',
                        linewidth=1.5, elinewidth=0.5,
                        capsize=1, capthick=0.5, linestyle='--')
        if (len(ind) == 2):
            ax.errorbar(OPM_X[ind[0]], Y, xerr=OPM_Xerr[ind[0]], label="OPM", color='black', linewidth=2.5,
                        elinewidth=0.5, capsize=1,
                        capthick=0.5, linestyle=':')
            ax.errorbar(prof_X[ind[0]], Y, xerr=prof_Xerr[ind[0]], label="Team " + str(teaml[ind[0]]), color='red',
                        linewidth=1.5, elinewidth=0.5,
                        capsize=1, capthick=0.5, linestyle='--')
            ax.errorbar(prof_X[ind[1]], Y, xerr=prof_Xerr[ind[1]], label="Team " + str(teaml[ind[1]]), color='green',
                        linewidth=1.5, elinewidth=0.5,
                        capsize=1, capthick=0.5, linestyle='-.')

    ax.legend(loc='lower right', frameon=True, fontsize='small')

    plt.savefig('/home/poyraden/Analysis/Josie_Analysis/Plots/ProfilePlots_withtimecut_v2/' + plotname + '.pdf')
    plt.savefig('/home/poyraden/Analysis/Josie_Analysis/Plots/ProfilePlots_withtimecut_v2/' + plotname + '.eps')

def Plot_Simulation_PlotsTime(ind, teaml, X, Y, OPM, xra, yra, xtit, ytit, mtitle, plotname, keyword):

    plt.close('all')
    fig, ax = plt.subplots()
    plt.xlim(xra)
    plt.ylim(yra)
    plt.xlabel(xtit)
    plt.ylabel(ytit)
    plt.title(mtitle)

    if (keyword == 'standard'):
        if (len(ind) == 4):

            ax.plot(X[ind[0]], OPM[ind[0]], label="OPM", color = 'black')
            ax.plot(X[ind[0]], Y[ind[0]], label="Team " +  str(teaml[ind[0]]), color = 'green')
            ax.plot(X[ind[1]], Y[ind[1]], label="Team " +  str(teaml[ind[1]]),color = 'cyan')
            ax.plot(X[ind[2]], Y[ind[2]], label="Team " +  str(teaml[ind[2]]), color = 'tomato')
            ax.plot(X[ind[3]], Y[ind[3]], label="Team " +  str(teaml[ind[3]]), color = 'blue')


        if (len(ind) == 3):
            ax.plot(X[ind[0]], OPM[ind[0]], label="OPM", color = 'black')
            ax.plot(X[ind[0]], Y[ind[0]], label="Team " + str(teaml[ind[0]]), color='green')
            ax.plot(X[ind[1]], Y[ind[1]], label="Team " + str(teaml[ind[1]]), color='cyan')
            ax.plot(X[ind[2]], Y[ind[2]], label="Team " + str(teaml[ind[2]]), color='tomato')

        if (len(ind) == 2):
            ax.plot(X[ind[0]], OPM[ind[0]], label="OPM", color = 'black')
            ax.plot(X[ind[0]], Y[ind[0]], label="Team " + str(teaml[ind[0]]), color='green')
            ax.plot(X[ind[1]], Y[ind[1]], label="Team " + str(teaml[ind[1]]), color='cyan')

    ax.legend(loc='lower right', frameon=True, fontsize='small')

    # plt.show()
    #
    plt.savefig('/home/poyraden/Analysis/Josie_Analysis/Plots/SimulationPlots_0910_v2_pair/' + plotname + '.pdf')
    plt.savefig('/home/poyraden/Analysis/Josie_Analysis/Plots/SimulationPlots_0910_v2_pair/' + plotname + '.eps')


def Plot_Simulation_PlotsPair(ind, teaml, X, Y, OPM, xra, yra, xtit, ytit, mtitle, plotname, keyword):

    plt.close('all')
    fig, ax = plt.subplots()
    plt.xlim(xra)
    plt.ylim(yra)
    plt.xlabel(xtit)
    plt.ylabel(ytit)
    plt.title(mtitle)
    ax.set_xscale('log')


    if (keyword == 'standard'):
        if (len(ind) == 4):

            ax.plot(X[ind[0]], OPM[ind[0]], label="OPM", color = 'black')
            ax.plot(X[ind[0]], Y[ind[0]], label="Team " +  str(teaml[ind[0]]), color = 'green')
            ax.plot(X[ind[1]], Y[ind[1]], label="Team " +  str(teaml[ind[1]]),color = 'cyan')
            ax.plot(X[ind[2]], Y[ind[2]], label="Team " +  str(teaml[ind[2]]), color = 'tomato')
            ax.plot(X[ind[3]], Y[ind[3]], label="Team " +  str(teaml[ind[3]]), color = 'blue')


        if (len(ind) == 3):
            ax.plot(X[ind[0]], OPM[ind[0]], label="OPM", color = 'black')
            ax.plot(X[ind[0]], Y[ind[0]], label="Team " + str(teaml[ind[0]]), color='green')
            ax.plot(X[ind[1]], Y[ind[1]], label="Team " + str(teaml[ind[1]]), color='cyan')
            ax.plot(X[ind[2]], Y[ind[2]], label="Team " + str(teaml[ind[2]]), color='tomato')

        if (len(ind) == 2):
            ax.plot(X[ind[0]], OPM[ind[0]], label="OPM", color = 'black')
            ax.plot(X[ind[0]], Y[ind[0]], label="Team " + str(teaml[ind[0]]), color='green')
            ax.plot(X[ind[1]], Y[ind[1]], label="Team " + str(teaml[ind[1]]), color='cyan')

    ax.legend(loc='lower right', frameon=True, fontsize='small')

    # plt.show()

    plt.savefig('/home/poyraden/Analysis/Josie_Analysis/Plots/SimulationPlots_0910_v2_pair/' + plotname + '.pdf')
    plt.savefig('/home/poyraden/Analysis/Josie_Analysis/Plots/SimulationPlots_0910_v2_pair/' + plotname + '.eps')


def Plot_TimePressure(ind, X, Y, xra, yra, xtit, ytit, mtitle, plotname):

    plt.close('all')
    fig, ax = plt.subplots()
    plt.xlim(xra)
    plt.ylim(yra)
    plt.xlabel(xtit)
    plt.ylabel(ytit)
    plt.title(mtitle)

    ax.plot(X[ind[0]], Y[ind[0]], label=plotname, color='black')
    ax.legend(loc='lower right', frameon=True, fontsize='small')


    # plt.show()
    #
    # plt.savefig('/home/poyraden/Analysis/Josie_Analysis/Plots/SimulationPlots_17_notimecut_pairfixed/' + plotname + '.pdf')
    # plt.savefig('/home/poyraden/Analysis/Josie_Analysis/Plots/SimulationPlots_17_notimecut_pairfixed/' + plotname + '.eps')


####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################

# Plots the two pllots of 2 different data profiles using the absolute difference and relative difference

def Plot_4profile_plots(prof1_X, prof1_Xerr, prof2_X, prof2_Xerr, prof3_X, prof3_Xerr, prof4_X, prof4_Xerr, Y, xra, yra,
                        xtit, ytit, mtitle, plotname, keyword):
    plt.close('all')
    fig, ax = plt.subplots()
    plt.xlim(xra)
    plt.ylim(yra)
    plt.xlabel(xtit)
    plt.ylabel(ytit)
    plt.title(mtitle)

    plt.yticks(np.arange(0, 7001, 1000))
    ax.tick_params(axis='both', which='both', direction='in')
    ax.yaxis.set_ticks_position('both')
    ax.xaxis.set_ticks_position('both')

    ax.yaxis.set_minor_locator(AutoMinorLocator(10))
    ax.xaxis.set_minor_locator(AutoMinorLocator(10))

    if (keyword == '1234'):
        ax.errorbar(prof1_X, Y, xerr=prof1_Xerr, label="Team 1", color='red', linewidth=1.5, elinewidth=0.5,
                    capsize=1, capthick=0.5, linestyle='--')
        ax.errorbar(prof2_X, Y, xerr=prof2_Xerr, label="Team 2", color='green', linewidth=1.5, elinewidth=0.5,
                    capsize=1, capthick=0.5, linestyle='--')
        ax.errorbar(prof3_X, Y, xerr=prof3_Xerr, label="Team 3", color='blue', linewidth=1.5, elinewidth=0.5,
                    capsize=1, capthick=0.5, linestyle='--')
        ax.errorbar(prof4_X, Y, xerr=prof4_Xerr, label="Team 4", color='goldenrod', linewidth=1.5,
                    elinewidth=0.5, capsize=1, capthick=0.5, linestyle='--')

    if (keyword == '5678'):
        ax.errorbar(prof1_X, Y, xerr=prof1_Xerr, label="Team 5", color='crimson', linewidth=1.5, elinewidth=0.5,
                    capsize=1, capthick=0.5, linestyle='--')
        ax.errorbar(prof2_X, Y, xerr=prof2_Xerr, label="Team 6", color='limegreen', linewidth=1.5,
                    elinewidth=0.5, capsize=1, capthick=0.5, linestyle='--')
        ax.errorbar(prof3_X, Y, xerr=prof3_Xerr, label="Team 7", color='dodgerblue', linewidth=1.5,
                    elinewidth=0.5, capsize=1, capthick=0.5, linestyle='--')
        ax.errorbar(prof4_X, Y, xerr=prof4_Xerr, label="Team 8", color='darkorange', linewidth=1.5,
                    elinewidth=0.5, capsize=1, capthick=0.5, linestyle='--')

    # ax.plot(prof1_X, Y, label="Team 1", color = 'green')
    # ax.plot(prof2_X, Y, label="Team 2", color = 'cyan')
    # ax.plot(prof3_X, Y, label="Team 3", color = 'tomato')
    # ax.plot(prof4_X, Y, label="Team 4", color = 'blue')
    ax.legend(loc='lower right', frameon=True, fontsize='small')

    plt.savefig('/home/poyraden/Josie17/Plots/' + plotname + '.pdf')
    plt.savefig('/home/poyraden/Josie17/Plots/' + plotname + '.eps')

    plt.close()


def Plot_5profile_plotsTime(prof1_X, prof1_Xerr, prof2_X, prof2_Xerr, prof3_X, prof3_Xerr, prof4_X, prof4_Xerr, prof5_X,
                            prof5_Xerr, Y, xra, yra, xtit, ytit, mtitle, plotname, keyword):
    plt.close('all')
    fig, ax = plt.subplots()
    plt.xlim(xra)
    plt.ylim(yra)
    plt.xlabel(xtit)
    plt.ylabel(ytit)
    plt.title(mtitle)

    # plt.yticks(np.arange(0, 7001, 1000))
    # ax.tick_params(axis='both', which='both', direction='in')
    # ax.yaxis.set_ticks_position('both')
    # ax.xaxis.set_ticks_position('both')
    #
    # ax.yaxis.set_minor_locator(AutoMinorLocator(10))
    # ax.xaxis.set_minor_locator(AutoMinorLocator(10))

    if (keyword == 'standard'):
        ax.errorbar(prof5_X, Y, xerr=prof5_Xerr, label="OPM", color='black', linewidth=2.5, elinewidth=0.5, capsize=1,
                    capthick=0.5, linestyle=':')
        ax.errorbar(prof1_X, Y, xerr=prof1_Xerr, label="Team 1", color='red', linewidth=1.5, elinewidth=0.5,
                    capsize=1, capthick=0.5, linestyle='--')
        ax.errorbar(prof2_X, Y, xerr=prof2_Xerr, label="Team 2", color='green', linewidth=1.5, elinewidth=0.5,
                    capsize=1, capthick=0.5, linestyle='-.')
        ax.errorbar(prof3_X, Y, xerr=prof3_Xerr, label="Team 3", color='blue', linewidth=1.5, elinewidth=0.5,
                    capsize=1, capthick=0.5, linestyle='--')
        ax.errorbar(prof4_X, Y, xerr=prof4_Xerr, label="Team 4", color='goldenrod', linewidth=1.5,
                    elinewidth=0.5, capsize=1, capthick=0.5, linestyle='-.')
    if (keyword == '5678'):
        ax.errorbar(prof5_X, Y, xerr=prof5_Xerr, label="OPM", color='black', linewidth=2.5, elinewidth=0.5, capsize=1,
                    capthick=0.5, linestyle=':')
        ax.errorbar(prof1_X, Y, xerr=prof1_Xerr, label="Team 5", color='crimson', linewidth=1.5, elinewidth=0.5,
                    capsize=1, capthick=0.5, linestyle='--')
        ax.errorbar(prof2_X, Y, xerr=prof2_Xerr, label="Team 6", color='limegreen', linewidth=1.5,
                    elinewidth=0.5, capsize=1, capthick=0.5, linestyle='-.')
        ax.errorbar(prof3_X, Y, xerr=prof3_Xerr, label="Team 7", color='dodgerblue', linewidth=1.5,
                    elinewidth=0.5, capsize=1, capthick=0.5, linestyle='--')
        ax.errorbar(prof4_X, Y, xerr=prof4_Xerr, label="Team 8", color='darkorange', linewidth=1.5,
                    elinewidth=0.5, capsize=1, capthick=0.5, linestyle='-.')
    else:

        ax.errorbar(prof2_X, Y, xerr=prof2_Xerr, label="No Correction", color='black', linewidth=1.5,
                    elinewidth=0.5, capsize=1, capthick=0.5, linestyle='-.')
        ax.errorbar(prof3_X, Y, xerr=prof3_Xerr, label="Slope Correction", color='red', linewidth=1.5,
                    elinewidth=0.5, capsize=1, capthick=0.5, linestyle='--')
        ax.errorbar(prof4_X, Y, xerr=prof4_Xerr, label="RDif Correction", color='blue', linewidth=1.5,
                    elinewidth=0.5, capsize=1, capthick=0.5, linestyle='-.')
        ax.errorbar(prof5_X, Y, xerr=prof5_Xerr, label="ADif Correction", color='green', linewidth=2.5, elinewidth=0.5,
                    capsize=1,
                    capthick=0.5, linestyle=':')
        ax.errorbar(prof1_X, Y, xerr=prof1_Xerr, label="OPM", color='gold', linewidth=1.5, elinewidth=0.5,
                    capsize=1, capthick=0.5, linestyle=':')

    # ax.plot(prof1_X, Y, label="Team 1", color = 'green')
    # ax.plot(prof2_X, Y, label="Team 2", color = 'cyan')
    # ax.plot(prof3_X, Y, label="Team 3", color = 'tomato')
    # ax.plot(prof4_X, Y, label="Team 4", color = 'blue')
    ax.legend(loc='lower right', frameon=True, fontsize='small')

    plt.savefig('/home/poyraden/Analysis/Josie_Analysis/Plots/ProfilePlots_notimecut/' + plotname + '.pdf')
    plt.savefig('/home/poyraden/Analysis/Josie_Analysis/Plots/ProfilePlots_notimecut/' + plotname + '.eps')

    # plt.show()
    #
    plt.close()


def Plot_5profile_plotsPair(prof1_X, prof1_Xerr, prof2_X, prof2_Xerr, prof3_X, prof3_Xerr, prof4_X, prof4_Xerr, prof5_X,
                            prof5_Xerr, Y, xra, yra, xtit, ytit, mtitle, plotname, keyword):
    plt.close('all')
    fig, ax = plt.subplots()
    plt.xlim(xra)
    plt.ylim(yra)
    plt.xlabel(xtit)
    plt.ylabel(ytit)
    plt.title(mtitle)
    ax.set_yscale('log')

    # plt.yticks(np.arange(0, 7001, 1000))
    # ax.tick_params(axis='both', which='both', direction='in')
    # ax.yaxis.set_ticks_position('both')
    # ax.xaxis.set_ticks_position('both')
    #
    # ax.yaxis.set_minor_locator(AutoMinorLocator(10))
    # ax.xaxis.set_minor_locator(AutoMinorLocator(10))

    if (keyword == 'standard'):
        ax.errorbar(prof5_X, Y, xerr=prof5_Xerr, label="OPM", color='black', linewidth=2.5, elinewidth=0.5, capsize=1,
                    capthick=0.5, linestyle=':')
        ax.errorbar(prof1_X, Y, xerr=prof1_Xerr, label="Team 1", color='red', linewidth=1.5, elinewidth=0.5,
                    capsize=1, capthick=0.5, linestyle='--')
        ax.errorbar(prof2_X, Y, xerr=prof2_Xerr, label="Team 2", color='green', linewidth=1.5, elinewidth=0.5,
                    capsize=1, capthick=0.5, linestyle='-.')
        ax.errorbar(prof3_X, Y, xerr=prof3_Xerr, label="Team 3", color='blue', linewidth=1.5, elinewidth=0.5,
                    capsize=1, capthick=0.5, linestyle='--')
        ax.errorbar(prof4_X, Y, xerr=prof4_Xerr, label="Team 4", color='goldenrod', linewidth=1.5,
                    elinewidth=0.5, capsize=1, capthick=0.5, linestyle='-.')
    if (keyword == '5678'):
        ax.errorbar(prof5_X, Y, xerr=prof5_Xerr, label="OPM", color='black', linewidth=2.5, elinewidth=0.5, capsize=1,
                    capthick=0.5, linestyle=':')
        ax.errorbar(prof1_X, Y, xerr=prof1_Xerr, label="Team 5", color='crimson', linewidth=1.5, elinewidth=0.5,
                    capsize=1, capthick=0.5, linestyle='--')
        ax.errorbar(prof2_X, Y, xerr=prof2_Xerr, label="Team 6", color='limegreen', linewidth=1.5,
                    elinewidth=0.5, capsize=1, capthick=0.5, linestyle='-.')
        ax.errorbar(prof3_X, Y, xerr=prof3_Xerr, label="Team 7", color='dodgerblue', linewidth=1.5,
                    elinewidth=0.5, capsize=1, capthick=0.5, linestyle='--')
        ax.errorbar(prof4_X, Y, xerr=prof4_Xerr, label="Team 8", color='darkorange', linewidth=1.5,
                    elinewidth=0.5, capsize=1, capthick=0.5, linestyle='-.')
    else:

        ax.errorbar(prof2_X, Y, xerr=prof2_Xerr, label="No Correction", color='black', linewidth=1.5,
                    elinewidth=0.5, capsize=1, capthick=0.5, linestyle='-.')
        ax.errorbar(prof3_X, Y, xerr=prof3_Xerr, label="Slope Correction", color='red', linewidth=1.5,
                    elinewidth=0.5, capsize=1, capthick=0.5, linestyle='--')
        ax.errorbar(prof4_X, Y, xerr=prof4_Xerr, label="RDif Correction", color='blue', linewidth=1.5,
                    elinewidth=0.5, capsize=1, capthick=0.5, linestyle='-.')
        ax.errorbar(prof5_X, Y, xerr=prof5_Xerr, label="ADif Correction", color='green', linewidth=2.5, elinewidth=0.5,
                    capsize=1,
                    capthick=0.5, linestyle=':')
        ax.errorbar(prof1_X, Y, xerr=prof1_Xerr, label="OPM", color='gold', linewidth=1.5, elinewidth=0.5,
                    capsize=1, capthick=0.5, linestyle=':')

    # ax.plot(prof1_X, Y, label="Team 1", color = 'green')
    # ax.plot(prof2_X, Y, label="Team 2", color = 'cyan')
    # ax.plot(prof3_X, Y, label="Team 3", color = 'tomato')
    # ax.plot(prof4_X, Y, label="Team 4", color = 'blue')
    ax.legend(loc='lower right', frameon=True, fontsize='small')

    plt.savefig('/home/poyraden/Analysis/Josie_Analysis/Plots/Corrected_lessbin/' + plotname + '.pdf')
    plt.savefig('/home/poyraden/Analysis/Josie_Analysis/Plots/Corrected_lessbin/' + plotname + '.eps')

    # plt.show()
    #
    plt.close()


def Plot_compare_profile_plots(prof1_X, prof1_Xerr, prof2_X,  prof2_Xerr, Y, xra, xtit, ytit, filtx, filty,  totO31value, totO32value, prof1_nodup, prof2_nodup, plotname):

    n1 = len(prof1_nodup)
    n2 = len(prof2_nodup)

    yra = [0,7000]
    labelx = filtx + ' ( n =' + str(n1) + ')'
    labely = filty + '( n =' + str(n2) + ')'

    text1 = 'tot O3 ratio: ' + str(round(totO31value,2))
    text2 = 'tot O3 ratio: ' + str(round(totO32value, 2))

    fig,ax = plt.subplots()
    plt.xlim(xra)
    plt.ylim(yra)
    plt.xlabel(xtit)
    plt.ylabel(ytit)

	# reference line
    ax.axvline(x=0, color='grey', linestyle='--')

    ax.errorbar(prof1_X, Y, xerr = prof1_Xerr, label = labelx,  color='black', linewidth = 1, elinewidth = 0.5, capsize = 1, capthick=0.5)
    ax.errorbar(prof2_X, Y, xerr = prof2_Xerr, label = labely, color='red', linewidth = 1, elinewidth = 0.5, capsize = 1, capthick=0.5)

    plt.yticks(np.arange(0, 7001, 1000))
    ax.tick_params(axis='both', which='both', direction='in')
    ax.yaxis.set_ticks_position('both')
    ax.xaxis.set_ticks_position('both')

    ax.yaxis.set_minor_locator(AutoMinorLocator(10))
    ax.xaxis.set_minor_locator(AutoMinorLocator(10))
    ax.legend(loc='lower right', frameon=True, fontsize = 'small')


    t1 = ax.text(0.05,0.09, text1,  color='black', transform=ax.transAxes)
    t2 = ax.text(0.05,0.02, text2,  color='red', transform=ax.transAxes)


    plt.savefig('/home/poyraden/Josie17/Plots/'+ plotname +'.pdf')
    plt.savefig('/home/poyraden/Josie17/Plots/'+ plotname +'.eps')


################

def Plot_compare_2profile_plots_updated(prof1_X, prof1_Xerr, prof2_X, prof2_Xerr, Y, xra, mtit, xtit, ytit, filtx,
                                        filty, totO31value, totO32value, prof1_nodup, prof2_nodup, plotname):
    n1 = len(prof1_nodup)
    n2 = len(prof2_nodup)

    labelx = filtx + ' ( n =' + str(n1) + ')'
    labely = filty + '( n =' + str(n2) + ')'

    text1 = 'tot O3 ratio: ' + str(round(totO31value, 2))
    text2 = 'tot O3 ratio: ' + str(round(totO32value, 2))

    plt.close('all')

    yra = [0, 7000]
    fig, ax = plt.subplots()
    plt.xlim(xra)
    plt.ylim(yra)
    plt.title(mtit)
    plt.xlabel(xtit)
    plt.ylabel(ytit)
    plt.grid(True)

    # reference line
    ax.axvline(x=0, color='grey', linestyle='--')
    # ax.set_yscale('log')

    ax.errorbar(prof1_X, Y, xerr=prof1_Xerr, label=labelx, color='black', linewidth=1, elinewidth=0.5, capsize=1,
                capthick=0.5)
    ax.errorbar(prof2_X, Y, xerr=prof2_Xerr, label=labely, color='red', linewidth=1, elinewidth=0.5, capsize=1,
                capthick=0.5)

    ax.tick_params(axis='both', which='both', direction='in')
    ax.yaxis.set_ticks_position('both')
    ax.xaxis.set_ticks_position('both')

    ax.yaxis.set_minor_locator(AutoMinorLocator(10))
    ax.xaxis.set_minor_locator(AutoMinorLocator(10))
    ax.legend(loc='lower right', frameon=True, fontsize='small')

    t1 = ax.text(0.05, 0.09, text1, color='black', transform=ax.transAxes)
    t2 = ax.text(0.05, 0.02, text2, color='red', transform=ax.transAxes)

    # plt.savefig('/home/poyraden//Josie17/PlotsTest/' + plotname + '.pdf')
    # plt.savefig('/home/poyraden//Josie17/PlotsTest/' + plotname + '.eps')

    plt.show()
    plt.close()


#####################################################################3

def Plot_compare_2profileplots_Pair(prof1_X, prof1_Xerr, prof2_X, prof2_Xerr, Y, xra, mtit, xtit, ytit, plotname):
    labelx = 'No correction'
    labely = 'Correction'

    plt.close('all')
    yra = [1000, 5]
    fig, ax = plt.subplots()
    plt.xlim(xra)
    plt.ylim(yra)
    plt.title(mtit)
    plt.xlabel(xtit)
    plt.ylabel(ytit)
    plt.grid(True)

    # reference line
    ax.axvline(x=0, color='grey', linestyle='--')
    ax.set_yscale('log')

    ax.errorbar(prof1_X, Y, xerr=prof1_Xerr, label=labelx, color='black', linewidth=1, elinewidth=0.5, capsize=1,
                capthick=0.5)
    ax.errorbar(prof2_X, Y, xerr=prof2_Xerr, label=labely, color='red', linewidth=1, elinewidth=0.5, capsize=1,
                capthick=0.5)

    # ax.tick_params(axis='both', which='both', direction='in')
    # ax.yaxis.set_ticks_position('both')
    # ax.xaxis.set_ticks_position('both')
    #
    # ax.yaxis.set_minor_locator(AutoMinorLocator(10))
    # ax.xaxis.set_minor_locator(AutoMinorLocator(10))
    ax.legend(loc='lower right', frameon=True, fontsize='small')

    # plt.savefig('/home/poyraden//Josie17/Plots/Calibration/Corrected/RDif_lessbin/' + plotname + '.pdf')
    # plt.savefig('/home/poyraden//Josie17/Plots/Calibration/Corrected/RDif_lessbin/' + plotname + '.eps')
    # plt.close()

    # plt.savefig('/Volumes/HD3/KMI/Josie17/Plots/Calibration/Corrected/' + plotname + '.pdf')
    plt.savefig('/home/poyraden/Josie17/Plots/Calibration_1718/Corrected/' + plotname + '.pdf')

    plt.close()


#######################################################################################################################

def Plot_compare_4profile_plots_updated(prof1_X, prof1_Xerr, prof2_X, prof2_Xerr, prof3_X, prof3_Xerr, prof4_X,
                                        prof4_Xerr, Y, xra, mtit, xtit, ytit, filtx, filty, filt3, filt4, totO31value,
                                        totO32value, totO33value, totO34value, prof1_nodup, prof2_nodup, prof3_nodup,
                                        prof4_nodup, plotname):
    n1 = len(prof1_nodup)
    n2 = len(prof2_nodup)
    n3 = len(prof3_nodup)
    n4 = len(prof4_nodup)

    labelx = filtx + ' ( n =' + str(n1) + ')'
    labely = filty + '( n =' + str(n2) + ')'
    label3 = filt3 + '( n =' + str(n3) + ')'
    label4 = filt4 + '( n =' + str(n4) + ')'

    text1 = 'tot O3 ratio: ' + str(round(totO31value, 2))
    text2 = 'tot O3 ratio: ' + str(round(totO32value, 2))
    text3 = 'tot O3 ratio: ' + str(round(totO33value, 2))
    text4 = 'tot O3 ratio: ' + str(round(totO34value, 2))

    # yra = [1000, 6]
    yra = [0, 7000]

    plt.close('all')

    fig, ax = plt.subplots()
    plt.xlim(xra)
    plt.ylim(yra)
    plt.title(mtit)
    plt.xlabel(xtit)
    plt.ylabel(ytit)
    plt.grid(True)

    # plt.yticks(np.arange(0, 7001, 1000))

    # reference line
    ax.axvline(x=0, color='grey', linestyle='--')
    # ax.set_yscale('log')

    ax.errorbar(prof1_X, Y, xerr=prof1_Xerr, label=labelx, color='black', linewidth=1, elinewidth=0.5, capsize=1,
                capthick=0.5)
    ax.errorbar(prof2_X, Y, xerr=prof2_Xerr, label=labely, color='red', linewidth=1, elinewidth=0.5, capsize=1,
                capthick=0.5)
    ax.errorbar(prof3_X, Y, xerr=prof3_Xerr, label=label3, color='blue', linewidth=1, elinewidth=0.5, capsize=1,
                capthick=0.5)
    ax.errorbar(prof4_X, Y, xerr=prof4_Xerr, label=label4, color='green', linewidth=1, elinewidth=0.5, capsize=1,
                capthick=0.5)

    # ax.tick_params(axis='both', which='both', direction='in')
    # ax.yaxis.set_ticks_position('both')
    # ax.xaxis.set_ticks_position('both')

    # ax.yaxis.set_minor_locator(AutoMinorLocator(10))
    # ax.xaxis.set_minor_locator(AutoMinorLocator(10))
    ax.legend(loc='lower right', frameon=True, fontsize='small')

    t1 = ax.text(0.05, 0.23, text1, color='black', transform=ax.transAxes)
    t2 = ax.text(0.05, 0.16, text2, color='red', transform=ax.transAxes)
    t3 = ax.text(0.05, 0.09, text3, color='blue', transform=ax.transAxes)
    t4 = ax.text(0.05, 0.02, text4, color='green', transform=ax.transAxes)

    plt.savefig('//home/poyraden//Josie17/Plots/Calibration_1718/' + plotname + '.pdf')
    plt.savefig('//home/poyraden//Josie17/Plots/Calibration_1718/' + plotname + '.eps')

    plt.close()
########################################################################################

########################################################################################





def Plot_compare_4profile_plots_time(prof1_X, prof1_Xerr, prof2_X, prof2_Xerr, prof3_X, prof3_Xerr, prof4_X,
                                         prof4_Xerr, Y, xra, mtit, xtit, ytit, filtx, filty, filt3, filt4, totO31value,
                                         totO32value, totO33value, totO34value, prof1_nodup, prof2_nodup, prof3_nodup,
                                         prof4_nodup, plotname):
        n1 = len(prof1_nodup)
        n2 = len(prof2_nodup)
        n3 = len(prof3_nodup)
        n4 = len(prof4_nodup)

        labelx = filtx + ' ( n =' + str(n1) + ')'
        labely = filty + '( n =' + str(n2) + ')'
        label3 = filt3 + '( n =' + str(n3) + ')'
        label4 = filt4 + '( n =' + str(n4) + ')'

        text1 = 'tot O3 ratio: ' + str(round(totO31value, 2))
        text2 = 'tot O3 ratio: ' + str(round(totO32value, 2))
        text3 = 'tot O3 ratio: ' + str(round(totO33value, 2))
        text4 = 'tot O3 ratio: ' + str(round(totO34value, 2))

        yra = [0, 9000]

        plt.close('all')
        fig, ax = plt.subplots()
        plt.xlim(xra)
        plt.ylim(yra)
        plt.title(mtit)
        plt.xlabel(xtit)
        plt.ylabel(ytit)
        plt.grid(True)

        # plt.yticks(np.arange(0, 7001, 1000))

        # reference line
        ax.axvline(x=0, color='grey', linestyle='--')

        ax.errorbar(prof1_X, Y, xerr=prof1_Xerr, label=labelx, color='black', linewidth=1, elinewidth=0.5, capsize=1,
                    capthick=0.5)
        ax.errorbar(prof2_X, Y, xerr=prof2_Xerr, label=labely, color='red', linewidth=1, elinewidth=0.5, capsize=1,
                    capthick=0.5)
        ax.errorbar(prof3_X, Y, xerr=prof3_Xerr, label=label3, color='blue', linewidth=1, elinewidth=0.5, capsize=1,
                    capthick=0.5)
        ax.errorbar(prof4_X, Y, xerr=prof4_Xerr, label=label4, color='green', linewidth=1, elinewidth=0.5, capsize=1,
                    capthick=0.5)

        # ax.tick_params(axis='both', which='both', direction='in')
        # ax.yaxis.set_ticks_position('both')
        # ax.xaxis.set_ticks_position('both')

        # ax.yaxis.set_minor_locator(AutoMinorLocator(10))
        # ax.xaxis.set_minor_locator(AutoMinorLocator(10))
        ax.legend(loc='lower right', frameon=True, fontsize='small')

        t1 = ax.text(0.05, 0.23, text1, color='black', transform=ax.transAxes)
        t2 = ax.text(0.05, 0.16, text2, color='red', transform=ax.transAxes)
        t3 = ax.text(0.05, 0.09, text3, color='blue', transform=ax.transAxes)
        t4 = ax.text(0.05, 0.02, text4, color='green', transform=ax.transAxes)

        plt.savefig('/home/poyraden/Analysis/Josie_Analysis/Plots/Difference_Plots_0910/' + plotname + '.pdf')
        plt.savefig('/home/poyraden/Analysis/Josie_Analysis/Plots/Difference_Plots_0910/' + plotname + '.eps')

        plt.close()

    #################################################################################################################


def Plot_compare_8profile_plots_pair(prof1_X, prof1_Xerr, prof2_X, prof2_Xerr, prof3_X, prof3_Xerr, prof4_X,
                                     prof4_Xerr, opm1, opm1err, opm2, opm2err, opm3, opm3err, opm4, opm4err, Y, xra, mtit,
                                     xtit, ytit, filtx, filty, filt3, filt4, filt5, filt6,filt7, filt8,  totO31value,
                                     totO32value, totO33value, totO34value, prof1_nodup, prof2_nodup, prof3_nodup,
                                     prof4_nodup, plotname):
    n1 = len(prof1_nodup)
    n2 = len(prof2_nodup)
    n3 = len(prof3_nodup)
    n4 = len(prof4_nodup)

    labelx = filtx + ' ( n =' + str(n1) + ')'
    labely = filty + '( n =' + str(n2) + ')'
    label3 = filt3 + '( n =' + str(n3) + ')'
    label4 = filt4 + '( n =' + str(n4) + ')'
    label5 = filt5
    label6 = filt6
    label7 = filt7
    label8 = filt8

    text1 = 'tot O3 ratio: ' + str(round(totO31value, 2))
    text2 = 'tot O3 ratio: ' + str(round(totO32value, 2))
    text3 = 'tot O3 ratio: ' + str(round(totO33value, 2))
    text4 = 'tot O3 ratio: ' + str(round(totO34value, 2))

    yra = [1000, 5]

    plt.close('all')
    fig, ax = plt.subplots()
    plt.xlim(xra)
    plt.ylim(yra)
    plt.title(mtit)
    plt.xlabel(xtit)
    plt.ylabel(ytit)
    plt.grid(True)

    # plt.yticks(np.arange(0, 7001, 1000))

    # reference line
    ax.axvline(x=0, color='grey', linestyle='--')
    ax.set_yscale('log')

    ax.errorbar(prof1_X, Y, xerr=prof1_Xerr, label=labelx, color='black', linewidth=1, elinewidth=0.5, capsize=1,
                capthick=0.5)
    ax.errorbar(prof2_X, Y, xerr=prof2_Xerr, label=labely, color='red', linewidth=1, elinewidth=0.5, capsize=1,
                capthick=0.5)
    ax.errorbar(prof3_X, Y, xerr=prof3_Xerr, label=label3, color='blue', linewidth=1, elinewidth=0.5, capsize=1,
                capthick=0.5)
    ax.errorbar(prof4_X, Y, xerr=prof4_Xerr, label=label4, color='green', linewidth=1, elinewidth=0.5, capsize=1,
                capthick=0.5)
    ax.errorbar(opm1, Y, xerr=opm1err, label=label5, color='cyan', linewidth=1.5, elinewidth=0.5, capsize=1,
                capthick=0.5)
    ax.errorbar(opm2, Y, xerr=opm2err, label=label6, color='magenta', linewidth=1.5, elinewidth=0.5, capsize=1,
                capthick=0.5)
    ax.errorbar(opm3, Y, xerr=opm3err, label=label7, color='pink', linewidth=1.5, elinewidth=0.5, capsize=1,
                capthick=0.5)
    ax.errorbar(opm4, Y, xerr=opm4err, label=label8, color='lime', linewidth=1.5, elinewidth=0.5, capsize=1,
                capthick=0.5)
    # ax.tick_params(axis='both', which='both', direction='in')
    # ax.yaxis.set_ticks_position('both')
    # ax.xaxis.set_ticks_position('both')

    # ax.yaxis.set_minor_locator(AutoMinorLocator(10))
    # ax.xaxis.set_minor_locator(AutoMinorLocator(10))
    ax.legend(loc='lower right', frameon=True, fontsize='small')

    # t1 = ax.text(0.05, 0.23, text1, color='black', transform=ax.transAxes)
    # t2 = ax.text(0.05, 0.16, text2, color='red', transform=ax.transAxes)
    # t3 = ax.text(0.05, 0.09, text3, color='blue', transform=ax.transAxes)
    # t4 = ax.text(0.05, 0.02, text4, color='green', transform=ax.transAxes)

    plt.savefig('/home/poyraden/Analysis/Josie_Analysis/Plots/Difference_Plots_0910/' + plotname + '.pdf')
    plt.savefig('/home/poyraden/Analysis/Josie_Analysis/Plots/Difference_Plots_0910/' + plotname + '.eps')

    plt.close()


def Plot_compare_4profile_plots_time(prof1_X, prof1_Xerr, prof2_X, prof2_Xerr, prof3_X, prof3_Xerr, prof4_X,
                                     prof4_Xerr, Y, xra, mtit, xtit, ytit, filtx, filty, filt3, filt4, totO31value,
                                     totO32value, totO33value, totO34value, prof1_nodup, prof2_nodup, prof3_nodup,
                                     prof4_nodup, plotname):
    n1 = len(prof1_nodup)
    n2 = len(prof2_nodup)
    n3 = len(prof3_nodup)
    n4 = len(prof4_nodup)

    labelx = filtx + ' ( n =' + str(n1) + ')'
    labely = filty + '( n =' + str(n2) + ')'
    label3 = filt3 + '( n =' + str(n3) + ')'
    label4 = filt4 + '( n =' + str(n4) + ')'

    text1 = 'tot O3 ratio: ' + str(round(totO31value, 2))
    text2 = 'tot O3 ratio: ' + str(round(totO32value, 2))
    text3 = 'tot O3 ratio: ' + str(round(totO33value, 2))
    text4 = 'tot O3 ratio: ' + str(round(totO34value, 2))

    yra = [0, 9000]

    plt.close('all')
    fig, ax = plt.subplots()
    plt.xlim(xra)
    plt.ylim(yra)
    plt.title(mtit)
    plt.xlabel(xtit)
    plt.ylabel(ytit)
    plt.grid(True)

    # plt.yticks(np.arange(0, 7001, 1000))

    # reference line
    ax.axvline(x=0, color='grey', linestyle='--')

    ax.errorbar(prof1_X, Y, xerr=prof1_Xerr, label=labelx, color='black', linewidth=1, elinewidth=0.5, capsize=1,
                capthick=0.5)
    ax.errorbar(prof2_X, Y, xerr=prof2_Xerr, label=labely, color='red', linewidth=1, elinewidth=0.5, capsize=1,
                capthick=0.5)
    ax.errorbar(prof3_X, Y, xerr=prof3_Xerr, label=label3, color='blue', linewidth=1, elinewidth=0.5, capsize=1,
                capthick=0.5)
    ax.errorbar(prof4_X, Y, xerr=prof4_Xerr, label=label4, color='green', linewidth=1, elinewidth=0.5, capsize=1,
                capthick=0.5)

    # ax.tick_params(axis='both', which='both', direction='in')
    # ax.yaxis.set_ticks_position('both')
    # ax.xaxis.set_ticks_position('both')

    # ax.yaxis.set_minor_locator(AutoMinorLocator(10))
    # ax.xaxis.set_minor_locator(AutoMinorLocator(10))
    ax.legend(loc='lower right', frameon=True, fontsize='small')

    t1 = ax.text(0.05, 0.23, text1, color='black', transform=ax.transAxes)
    t2 = ax.text(0.05, 0.16, text2, color='red', transform=ax.transAxes)
    t3 = ax.text(0.05, 0.09, text3, color='blue', transform=ax.transAxes)
    t4 = ax.text(0.05, 0.02, text4, color='green', transform=ax.transAxes)

    plt.savefig('/home/poyraden/Analysis/Josie_Analysis/Plots/Difference_Plots_0910/' + plotname + '.pdf')
    plt.savefig('/home/poyraden/Analysis/Josie_Analysis/Plots/Difference_Plots_0910/' + plotname + '.eps')

    plt.close()


#################################################################################################################

    ########################################################################################


def Plot_6profile_plots(prof1_X, prof1_Xerr, prof2_X, prof2_Xerr, prof3_X, prof3_Xerr, prof4_X, prof4_Xerr, prof5_X,
                        prof5_Xerr, prof6_X, prof6_Xerr, Y, xra, mtit, xtit, ytit, filtx, filty, filt3, filt4, filt5,
                        filt6, totO31value, totO32value, totO33value, totO34value, totO35value, totO36value,
                        prof1_nodup, prof2_nodup, prof3_nodup, prof4_nodup, prof5_nodup, prof6_nodup, plotname):
    n1 = len(prof1_nodup)
    n2 = len(prof2_nodup)
    n3 = len(prof3_nodup)
    n4 = len(prof4_nodup)
    n5 = len(prof5_nodup)
    n6 = len(prof6_nodup)

    labelx = filtx + ' ( n =' + str(n1) + ')'
    labely = filty + '( n =' + str(n2) + ')'
    label3 = filt3 + '( n =' + str(n3) + ')'
    label4 = filt4 + '( n =' + str(n4) + ')'
    label5 = filt5 + '( n =' + str(n5) + ')'
    label6 = filt6 + '( n =' + str(n6) + ')'

    text1 = 'tot O3 ratio: ' + str(round(totO31value, 2))
    text2 = 'tot O3 ratio: ' + str(round(totO32value, 2))
    text3 = 'tot O3 ratio: ' + str(round(totO33value, 2))
    text4 = 'tot O3 ratio: ' + str(round(totO34value, 2))
    text5 = 'tot O3 ratio: ' + str(round(totO35value, 2))
    text6 = 'tot O3 ratio: ' + str(round(totO36value, 2))

    yra = [1000, 5]

    plt.close('all')
    fig, ax = plt.subplots()
    plt.xlim(xra)
    plt.ylim(yra)
    plt.title(mtit)
    plt.xlabel(xtit)
    plt.ylabel(ytit)
    plt.grid(True)

    # plt.yticks(np.arange(0, 7001, 1000))

    # reference line
    ax.axvline(x=0, color='grey', linestyle='--')
    ax.set_yscale('log')

    ax.errorbar(prof1_X, Y, xerr=prof1_Xerr, label=labelx, color='black', linewidth=1, elinewidth=0.5, capsize=1,
                capthick=0.5)
    ax.errorbar(prof2_X, Y, xerr=prof2_Xerr, label=labely, color='red', linewidth=1, elinewidth=0.5, capsize=1,
                capthick=0.5)
    ax.errorbar(prof3_X, Y, xerr=prof3_Xerr, label=label3, color='magenta', linewidth=1, elinewidth=0.5, capsize=1,
                capthick=0.5)
    ax.errorbar(prof4_X, Y, xerr=prof4_Xerr, label=label4, color='blue', linewidth=1, elinewidth=0.5, capsize=1,
                capthick=0.5)
    ax.errorbar(prof5_X, Y, xerr=prof5_Xerr, label=label5, color='green', linewidth=1, elinewidth=0.5, capsize=1,
                capthick=0.5)
    ax.errorbar(prof6_X, Y, xerr=prof6_Xerr, label=label6, color='purple', linewidth=1, elinewidth=0.5, capsize=1,
                capthick=0.5)

    # ax.tick_params(axis='both', which='both', direction='in')
    # ax.yaxis.set_ticks_position('both')
    # ax.xaxis.set_ticks_position('both')

    # ax.yaxis.set_minor_locator(AutoMinorLocator(10))
    # ax.xaxis.set_minor_locator(AutoMinorLocator(10))
    ax.legend(loc='lower right', frameon=True, fontsize='small')

    t1 = ax.text(0.05, 0.37, text1, color='black', transform=ax.transAxes)
    t2 = ax.text(0.05, 0.30, text2, color='red', transform=ax.transAxes)
    t3 = ax.text(0.05, 0.23, text3, color='blue', transform=ax.transAxes)
    t4 = ax.text(0.05, 0.16, text4, color='green', transform=ax.transAxes)
    t5 = ax.text(0.05, 0.09, text5, color='magenta', transform=ax.transAxes)
    t6 = ax.text(0.05, 0.02, text6, color='purple', transform=ax.transAxes)

    plt.savefig('/home/poyraden/Analysis/Josie_Analysis/Plots/Difference_Plots_0910/' + plotname + '.pdf')
    plt.savefig('/home/poyraden/Analysis/Josie_Analysis/Plots/Difference_Plots_0910/' + plotname + '.eps')

    plt.close()
