import pandas as pd
import numpy as np
import re
import glob
import math
from math import log
from makeDF_Functions import calculate_O3frac

from Analyse_Functions import polyfit


##########  part for TP Cell:


df17 = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv.csv", low_memory=False)

p_en, p_sp = polyfit(df17)



#######################################################################

## 17/06 correction for TPint and TPext exchange

slow = 25 * 60  # 25 minutes in seconds
fast = 25  # 25seconds

# Read the metadata file
dfmeta = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Josie10_MetaData.csv")
# dfmeta = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Josie10_MetaData.csv")
dfmeta_ib = pd.read_excel("/home/poyraden/Analysis/JOSIEfiles/ib_2010.xlsx")
dfmeta_m = pd.read_excel("/home/poyraden/Analysis/JOSIEfiles/2010_mass.xlsx")




# all files
## use pathlib jspr
# allFiles = glob.glob("/home/poyraden/Analysis/JOSIEfiles/JOSIE-2010-Data-ReProc/*.O3R")
allFiles = glob.glob("/home/poyraden/Analysis/JOSIEfiles/JOSIE-2010-Data-ReProc/*.O3R")


list_data = []

#Some declarations

columnString = "Tact Tsim Pair Tair Tinlet IM TPint TPext PFcor I_Pump PO3 VMRO3 PO3_OPM VMRO3_OPM ADif_PO3S RDif_PO3S Z"
columnStr = columnString.split(" ")


column_metaString = "Year Sim Team Code Flow IB1 Cor Sol Buf ADX"
columnMeta  = ['Year', 'Sim', 'Team', 'Code', 'Flow', 'IB1', 'Cor', 'ENSCI' , 'Sol', 'Buf', 'ADX']
columnMeta_ib = ['Simib', 'Teamib', 'Yearib', 'iB0', 'iB1', 'iB2']
columnMeta_m = ['Simm', 'Teamm', 'Mspre', 'Mspost', 'Diff']

Pval = np.array([1000, 730, 535, 382, 267, 185, 126, 85, 58, 39, 26.5, 18.1, 12.1, 8.3, 6])
JMA = np.array(
    [0.999705941, 0.997216654, 0.995162562, 0.992733959, 0.989710199, 0.985943645, 0.981029252, 0.974634364,
     0.966705137, 0.956132227, 0.942864263, 0.9260478, 0.903069813, 0.87528384, 0.84516337])

Temp = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
Pw_temp = [6.1, 8.7, 12.3, 17.1, 23.4, 31.7, 42.4, 56.2, 73.7, 95.8, 125.3]

yref_pair = [1000, 850, 700, 550, 400, 350, 300, 200, 150, 100, 75, 50, 35, 25, 20, 15,
        12, 10, 8, 6]


y_pair=  [925.0, 775.0, 625.0, 475.0, 375.0, 325.0, 250.0, 175.0, 125.0, 87.5, 62.5, 42.5, 30.0, 22.5, 17.5, 13.5, 11.0, 9.0, 7.0]

#**********************************************
# Main loop to merge all data sets
#**********************************************
for filename in allFiles:
    file = open(filename, 'r')
    # Get the participant information from the name of the file
    print(filename)
    # Get the participant information from the name of the file
    tmp_team = filename.split("/")[6]  # 7 for home, 6 for kmi
    header_team =( tmp_team.split("_")[2]).split(".")[0]
    file.readline()
    file.readline()
    header_part = int(header_team)
    header_sim = int(file.readline().split()[2])
    file.readline()
    file.readline()
    header_PFunc = float(file.readline().split()[1])
    header_PFcor = float(file.readline().split()[1])
    file.readline()
    header_IB1 = float(file.readline().split()[1])
    print(filename, 'header_IB1', header_IB1)
    
    df = pd.read_csv(filename, sep = "\t", engine="python", skiprows=12, names=columnStr)

     # Add the header information to the main df
    
    df = df.join(pd.DataFrame(
        [[header_part,  header_sim, header_PFunc, header_PFcor, header_IB1 ]], 
        index=df.index, 
        columns=['Header_Team', 'Header_Sim', 'Header_PFunc', 'Header_PFcor', 'Header_IB1']
    ))
 # Get the index of the metadata that corresponds to this Simulation Number and Participant (Team)
    
    select_indicesTeam = list(np.where(dfmeta["Team"] == df['Header_Team'][0]))[0]
    select_indicesSim = list(np.where(dfmeta["Sim"] == df['Header_Sim'][0]))[0]

    common = [i for i in select_indicesTeam if i in select_indicesSim]
    index_common = common[0]

    ## now the same for ib0 values

    select_indicesTeam_ib = list(np.where(dfmeta_ib["Team"] == df['Header_Team'][0]))[0]
    select_indicesSim_ib = list(np.where(dfmeta_ib["Sim"] == df['Header_Sim'][0]))[0]

    common_ib = [i for i in select_indicesTeam_ib if i in select_indicesSim_ib]
    index_common_ib = common_ib[0]

    ## now the same for mass diff values

    select_indicesTeam_m = list(np.where(dfmeta_m["Team"] == df['Header_Team'][0]))[0]
    select_indicesSim_m = list(np.where(dfmeta_m["Sim"] == df['Header_Sim'][0]))[0]

    common_m = [i for i in select_indicesTeam_m if i in select_indicesSim_m]
    index_common_m = common_m[0]

    print('common_m', common_m)

     ## The index of the metadata that has the information of this simulation = index_common
    #  assign this row into a list
    list_md = dfmeta.iloc[index_common,:].tolist()
    list_md_ib = dfmeta_ib.iloc[index_common_ib,:].tolist()
    list_md_m = dfmeta_m.iloc[index_common_m,:].tolist()

    ## Add  metadata to the main df
    df = df.join(pd.DataFrame(
        [list_md],
        index = df.index,
        columns=columnMeta
    ))

    df = df.join(pd.DataFrame(
        [list_md_ib],
        index=df.index,
        columns=columnMeta_ib
    ))

    df = df.join(pd.DataFrame(
        [list_md_m],
        index=df.index,
        columns=columnMeta_m
    ))

    # df['PO3_stp'] = df['PO3'] * (df['Tair'] / 273.15)
    # df['PO3_OPM_stp'] = df['PO3_OPM'] * (df['Tair'] / 273.15)

    ## convert OPM pressure to current
    df['I_OPM'] = (df['PO3_OPM'] * df['PFcor']) / (df['TPext'] * 0.043085)

    df['TPextC'] = df['TPext'] - 273

    for k in range(len(df)):
        ## jma corrections for OPM current, OPM_I_jma will be used only for Ua in the convolution of
        ## the slow component of the signal

        for pi in range(len(yref_pair) -1):

            if (df.at[k, 'Pair'] >= yref_pair[pi + 1]) & (df.at[k, 'Pair'] < yref_pair[pi]) :
                if (df.at[k, 'ENSCI'] == 1): df.at[k, 'Tcell'] = df.at[k, 'TPext'] - p_en(y_pair[pi])
                if (df.at[k, 'ENSCI'] == 0): df.at[k, 'Tcell'] = df.at[k, 'TPext'] - p_sp(y_pair[pi])

        if (df.at[k, 'Pair'] <= yref_pair[19]) :
            if(df.at[k, 'ENSCI'] == 1): df.at[k, 'Tcell'] = df.at[k, 'TPext'] - p_en(y_pair[18])
            if(df.at[k, 'ENSCI'] == 0): df.at[k, 'Tcell'] = df.at[k, 'TPext'] - p_sp(y_pair[18])

        df.at[k, 'TcellC'] = df.at[k, 'Tcell'] -  273

        for t in range(len(Temp) - 1):

            if (df.at[k, 'TcellC'] >= Temp[t]) & (df.at[k, 'TcellC'] < Temp[t + 1]):
                df.at[k, 'Pw'] = Pw_temp[t]

        # print(df.at[k, 'TcellC'])

        if (df.at[k, 'TcellC'] >= Temp[10]): df.at[k, 'Pw'] = Pw_temp[10]
        if (df.at[k, 'TcellC'] < Temp[0]): df.at[k, 'Pw'] = Pw_temp[0]


        for p in range(len(JMA) - 1):

            if (df.at[k, 'Pair'] >= Pval[p + 1]) & (df.at[k, 'Pair'] < Pval[p]):
                # print(p, Pval[p + 1], Pval[p ])
                df.at[k, 'I_OPM_jma'] = df.at[k, 'PO3_OPM'] * df.at[k, 'PFcor'] * JMA[p] / \
                                          (df.at[k, 'TPext'] * 0.043085)
                df.at[k,'PO3_jma'] = 0.043085 * df.at[k, 'TPext']  * (df.at[k, 'IM'] - df.at[k, 'IB1']) / (df.at[k, 'PFcor'] * JMA[p])

                df.at[k, 'JMA'] = JMA[p]


        if (df.at[k, 'Pair'] <= Pval[14]):
            df.at[k, 'I_OPM_jma'] = df.at[k, 'PO3_OPM'] * df.at[k, 'PFcor'] * JMA[14] / \
                                          (df.at[k, 'TPext'] * 0.043085)
            df.at[k, 'PO3_jma'] = 0.043085 * df.at[k, 'TPext'] * (df.at[k, 'IM'] - df.at[k, 'IB1']) / (
                        df.at[k, 'PFcor'] * JMA[14])
            df.at[k, 'JMA'] = JMA[14]



        # if (df.at[k, 'Pw'] < df.at[k, 'Pair']):
        df.at[k, 'massloss'] = 0.0001 * 1000 * (df.at[k, 'Pw'] / (461.52 * df.at[k, 'Tcell'])) * df.at[k, 'JMA'] * \
                                   df.at[k, 'PFcor']
        df.at[k, 'Tboil'] = (( 237.3 * np.log10(df.at[k, 'Pair']) )  - 186.47034)  / (8.2858 - np.log10(df.at[k, 'Pair']))


    df['total_massloss'] = np.trapz(df.massloss, x=df.Tsim)

    size = len(df)
    Ums_i = [0] * size
    Ua_i = [0] * size
    Ums_i[0] = df.at[0, 'IM']


    ## only convolute slow part of the signal, which is needed for beta calculation
    for i in range(size-1):

        Ua_i = df.at[i + 1, 'I_OPM_jma']
        t1 = df.at[i + 1,'Tsim']
        t2 = df.at[i,'Tsim']
        Xs = np.exp(-(t1 - t2) / slow)
        Xf = np.exp(-(t1 - t2) / fast)
        Ums_i[i + 1] = Ua_i - (Ua_i - Ums_i[i]) * Xs

    df['I_conv_slow'] = Ums_i


    O3_tot = 0; O3_tot_opm = 0; Adif = 0; Rdif = 0; frac = 0

    df = df.join(pd.DataFrame(
        [[O3_tot, O3_tot_opm, Adif, Rdif, frac]],
        index=df.index,
        columns=['O3S', 'OPM', 'ADif', 'RDif', 'frac']
    ))

    list_data.append(df)
#

    #  end of the allfiles loop    #
     
# Merging all the data files to df

df = pd.concat(list_data,ignore_index=True)

dfsim = df.drop_duplicates(['Sim'])
simlist = dfsim.Sim.tolist()

for s in simlist:
    filt1 = (df.Sim == s) & (df.Team == 1)
    filt2 = (df.Sim == s) & (df.Team == 2)
    filt3 = (df.Sim == s) & (df.Team == 3)
    filt4 = (df.Sim == s) & (df.Team == 4)

    df.loc[filt2, 'Pair'] = np.array(df.loc[filt1, 'Pair'])
    df.loc[filt3, 'Pair'] = np.array(df.loc[filt1, 'Pair'])
    df.loc[filt4, 'Pair'] = np.array(df.loc[filt1, 'Pair'])


#

# correct Pair values, and assign them to the first participants Pair values
calculate_O3frac(df, simlist)


df.to_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2010_Data_nocut_tempfixed_paper.csv")




