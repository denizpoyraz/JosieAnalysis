#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import glob

from makeDF_Functions import calculate_O3frac17
from Analyse_Functions import polyfit


##########  part for TP Cell:


df17 = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_deconv.csv", low_memory=False)

p_en, p_sp = polyfit(df17)



#######################################################################

slow = 25 * 60  # 25 minutes in seconds
fast = 20  # 20seconds

# Read the metadata file
dfmeta = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/JOSIE_Table_2017_summary.csv")

# Path to all Josie17 simulation files

allFiles = glob.glob("/home/poyraden/Analysis/JOSIEfiles/Josie17/*.O3R")
list_data = []

# Some declarations

columnString = "Tact Tsim Pair Tair Tinlet IM TPint TPext PFcor I_Pump PO3 VMRO3 PO3_OPM VMRO3_OPM ADif_PO3S RDif_PO3S Z"
columnStr = columnString.split(" ")
# related with metadata

column_metaString = 'Sim Simulator_RunNr Date Team Ini_Prep_Date Prep_SOP SerialNr ENSCI SerNr Date_1 SondeAge ' \
                    'Solutions Sol Buf Volume_Cathode ByPass_Cell Current_10min_after_noO3 Resp_Time_4_1p5_sec' \
                    ' RespTime_1minOver2min Final_BG iB0 iB1 iB2 T100 mlOvermin T100_post mlOverminp1 ' \
                    'RespTime_4_1p5_sec_p1 RespTime_1minOver2min_microamps PostTestSolution_Lost_gr PumpMotorCurrent ' \
                    'PumpMotorCurrent_Post PF_Unc PF_Cor BG'
columnMeta = column_metaString.split(" ")

Pval = np.array([1000, 730, 535, 382, 267, 185, 126, 85, 58, 39, 26.5, 18.1, 12.1, 8.3, 6])
JMA = np.array(
    [0.999705941, 0.997216654, 0.995162562, 0.992733959, 0.989710199, 0.985943645, 0.981029252, 0.974634364,
     0.966705137, 0.956132227, 0.942864263, 0.9260478, 0.903069813, 0.87528384, 0.84516337])

Temp = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
Pw_temp = [6.1, 8.7, 12.3, 17.1, 23.4, 31.7, 42.4, 56.2, 73.7, 95.8, 125.3]

yref_pair = [1000, 850, 700, 550, 400, 350, 300, 200, 150, 100, 75, 50, 35, 25, 20, 15,
        12, 10, 8, 6]

y_pair=  [925.0, 775.0, 625.0, 475.0, 375.0, 325.0, 250.0, 175.0, 125.0, 87.5, 62.5, 42.5, 30.0, 22.5, 17.5, 13.5, 11.0, 9.0, 7.0]

Pval_komhyr = np.array([1000, 199, 59, 30, 20, 10, 7, 5])
komhyr_sp_tmp = np.array([1, 1.007, 1.018, 1.022, 1.032, 1.055, 1.070, 1.092])
komhyr_en_tmp = np.array([1, 1.007, 1.018, 1.029, 1.041, 1.066, 1.087, 1.124])

komhyr_sp = [1/i for i in komhyr_sp_tmp]
komhyr_en = [1/i for i in komhyr_en_tmp]

# **********************************************
# Main loop to merge all data sets
# **********************************************
for filename in allFiles:
    file = open(filename, 'r')
    # Get the participant information from the name of the file
    print(filename)
    tmp_team = filename.split("/")[6]
    header_team = (tmp_team.split("_")[2]).split(".")[0]

    # Not a very nice way of getting the headers, but it works :)
    # Be careful for different file formats, then needs to be changed

    file.readline()
    file.readline()
    header_part = float(header_team)
    header_sim = int(file.readline().split()[2])
    file.readline()
    file.readline()
    header_PFunc = float(file.readline().split()[1])
    header_PFcor = float(file.readline().split()[1])
    file.readline()
    header_IB1 = float(file.readline().split()[1])

    # Assign the main df

    df = pd.read_csv(filename, sep="\t", engine="python", skiprows=12, names=columnStr)

    # Add the header information to the main df

    df = df.join(pd.DataFrame(
        [[header_part, header_sim, header_PFunc, header_PFcor, header_IB1]],
        index=df.index,
        columns=['Header_Team', 'Header_Sim', 'Header_PFunc', 'Header_PFcor', 'Header_IB1']
    ))

    # Get the index of the metadata that corresponds to this Simulation Number and Participant (Team)

    select_indicesTeam = list(np.where(dfmeta["Team"] == df['Header_Team'][0]))[0]
    select_indicesSim = list(np.where(dfmeta["Sim"] == df['Header_Sim'][0]))[0]
    common = [i for i in select_indicesTeam if i in select_indicesSim]
    index_common = common[0]

    ## The index of the metadata that has the information of this simulation = index_common
    #  assign this row into a list

    list_md = dfmeta.iloc[index_common, :].tolist()
    # print(list_md)

    ## Add  metadata to the main df
    df = df.join(pd.DataFrame(
        [list_md],
        index=df.index,
        columns=columnMeta
    ))

    # df['PO3_stp'] = df['PO3'] * (df['Tair'] / 273.15)
    # df['PO3_OPM_stp'] = df['PO3_OPM'] * (df['Tair'] / 273.15)
    # df['RDif_PO3'] = 100 * (df['PO3'] - df['PO3_OPM'])/(df['PO3_OPM'])

    df['TPextC'] = df['TPext'] - 273


    ## convert OPM pressure to current
    df['I_OPM'] = (df['PO3_OPM'] * df['PFcor']) / (df['TPext'] * 0.043085)


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

        df.at[k, 'TcellC'] = df.at[k, 'Tcell'] - 273

        for t in range(len(Temp) - 1):

            if (df.at[k, 'TcellC'] >= Temp[t]) & (df.at[k, 'TcellC'] < Temp[t + 1]):
                df.at[k, 'Pw'] = Pw_temp[t]

        if (df.at[k, 'TcellC'] >= Temp[10]): df.at[k, 'Pw'] = Pw_temp[10]
        if (df.at[k, 'TcellC'] < Temp[0]): df.at[k, 'Pw'] = Pw_temp[0]


        for p in range(len(JMA) - 1):

            if (df.at[k, 'Pair'] >= Pval[p + 1]) & (df.at[k, 'Pair'] < Pval[p]):
                # print(p, Pval[p + 1], Pval[p ])
                df.at[k, 'I_OPM_jma'] = df.at[k, 'PO3_OPM'] * df.at[k, 'PFcor'] * JMA[p] / \
                                        (df.at[k, 'TPext'] * 0.043085)
                df.at[k, 'PO3_jma'] = 0.043085 * df.at[k, 'TPext'] * (df.at[k, 'IM'] - df.at[k, 'iB1']) / (
                            df.at[k, 'PFcor'] * JMA[p])

                df.at[k, 'JMA'] = JMA[p]

        if (df.at[k, 'Pair'] <= Pval[14]):
            df.at[k, 'I_OPM_jma'] = df.at[k, 'PO3_OPM'] * df.at[k, 'PFcor'] * JMA[14] / \
                                    (df.at[k, 'TPext'] * 0.043085)
            df.at[k, 'PO3_jma'] = 0.043085 * df.at[k, 'TPext'] * (df.at[k, 'IM'] - df.at[k, 'iB1    ']) / (
                    df.at[k, 'PFcor'] * JMA[14])
            df.at[k, 'JMA'] = JMA[14]

        ## komhyr corrections
        for p in range(len(komhyr_en) - 1):

            if df.at[k, 'ENSCI'] == 1:
                if (df.at[k, 'Pair'] >= Pval_komhyr[p + 1]) & (df.at[k, 'Pair'] < Pval_komhyr[p]):
                    # print(p, Pval[p + 1], Pval[p ])
                    df.at[k, 'I_OPM_komhyr'] = df.at[k, 'PO3_OPM'] * df.at[k, 'PFcor'] * komhyr_en[p] / \
                                               (df.at[k, 'TPext'] * 0.043085)
            if df.at[k, 'ENSCI'] == 0:
                if (df.at[k, 'Pair'] >= Pval_komhyr[p + 1]) & (df.at[k, 'Pair'] < Pval_komhyr[p]):
                    # print(p, Pval[p + 1], Pval[p ])
                    df.at[k, 'I_OPM_komhyr'] = df.at[k, 'PO3_OPM'] * df.at[k, 'PFcor'] * komhyr_sp[p] / \
                                               (df.at[k, 'TPext'] * 0.043085)

        if (df.at[k, 'Pair'] <= Pval_komhyr[7]):

            if df.at[k, 'ENSCI'] == 1:
                df.at[k, 'I_OPM_komhyr'] = df.at[k, 'PO3_OPM'] * df.at[k, 'PFcor'] * komhyr_en[7] / \
                                           (df.at[k, 'TPext'] * 0.043085)
            if df.at[k, 'ENSCI'] == 0:
                df.at[k, 'I_OPM_komhyr'] = df.at[k, 'PO3_OPM'] * df.at[k, 'PFcor'] * komhyr_sp[7] / \
                                           (df.at[k, 'TPext'] * 0.043085)

        # if (df.at[k, 'Pw'] < df.at[k, 'Pair']):
        df.at[k, 'massloss'] = 0.0001 * 1000 * df.at[k, 'Pw'] / (461.52 * df.at[k, 'Tcell']) * df.at[k, 'JMA'] * \
                                   df.at[k, 'PFcor']
        df.at[k, 'Tboil'] = (( 237.3 * np.log10(df.at[k, 'Pair']) )  - 186.47034)  / (8.2858 - np.log10(df.at[k, 'Pair']))

        # if (df.at[k, 'Pw'] >= df.at[k, 'Pair']):
        #     df.at[k, 'massloss'] = 0

    df['total_massloss'] = np.trapz(df.massloss, x=df.Tsim)

    size = len(df)
    Ums_i = [0] * size
    Ums_i_kom = [0] * size

    Ua_i = [0] * size
    Ums_i[0] = df.at[0, 'IM']
    Ums_i_kom[0] = df.at[0, 'IM']

    ## only convolute slow part of the signal, which is needed for beta calculation
    for i in range(size - 1):
        Ua_i = df.at[i + 1, 'I_OPM_jma']
        t1 = df.at[i + 1, 'Tsim']
        t2 = df.at[i, 'Tsim']
        Xs = np.exp(-(t1 - t2) / slow)
        Xf = np.exp(-(t1 - t2) / fast)
        Ums_i[i + 1] = Ua_i - (Ua_i - Ums_i[i]) * Xs

        Ua_i = df.at[i + 1, 'I_OPM_komhyr']
        t1 = df.at[i + 1, 'Tsim']
        t2 = df.at[i, 'Tsim']
        Xs = np.exp(-(t1 - t2) / slow)
        Xf = np.exp(-(t1 - t2) / fast)
        Ums_i_kom[i + 1] = Ua_i - (Ua_i - Ums_i[i]) * Xs

    df['I_conv_slow'] = Ums_i
    df['I_conv_slow_komhyr'] = Ums_i_kom

    O3_tot = 0;
    O3_tot_opm = 0;
    Adif = 0;
    Rdif = 0;
    frac = 0

    df = df.join(pd.DataFrame(
        [[O3_tot, O3_tot_opm, Adif, Rdif, frac]],
        index=df.index,
        columns=['O3S', 'OPM', 'ADif', 'RDif', 'frac']
    ))


    list_data.append(df)
    #  end of the allfiles loop    #

# Merging all the data files to df

df = pd.concat(list_data, ignore_index=True)


dfsim = df.drop_duplicates(['Sim'])
simlist = dfsim.Sim.tolist()

for s in simlist:
    filt1 = (df.Sim == s) & (df.Team == 1)
    filt2 = (df.Sim == s) & (df.Team == 2)
    filt3 = (df.Sim == s) & (df.Team == 3)
    filt4 = (df.Sim == s) & (df.Team == 4)
    filt5 = (df.Sim == s) & (df.Team == 5)
    filt6 = (df.Sim == s) & (df.Team == 6)
    filt7 = (df.Sim == s) & (df.Team == 7)
    filt8 = (df.Sim == s) & (df.Team == 8)

    df.loc[filt2, 'Pair'] = np.array(df.loc[filt1, 'Pair'])
    df.loc[filt3, 'Pair'] = np.array(df.loc[filt1, 'Pair'])
    df.loc[filt4, 'Pair'] = np.array(df.loc[filt1, 'Pair'])
    df.loc[filt6, 'Pair'] = np.array(df.loc[filt5, 'Pair'])
    df.loc[filt7, 'Pair'] = np.array(df.loc[filt5, 'Pair'])
    df.loc[filt8, 'Pair'] = np.array(df.loc[filt5, 'Pair'])


#  ## aply the cuts here for O3 calculation
#
# df = df.drop(df[((df.Sim == 171) | (df.Sim == 172) | (df.Sim == 180) | (df.Sim == 185))].index)
# df = df.drop(df[(df.Sim == 179) & (df.Team == 4) & (df.Tsim > 4000)].index)
# df = df.drop(df[(df.Sim == 172) & (df.Tsim < 500)].index)
# df = df.drop(df[(df.Sim == 172) & (df.Team == 1) & (df.Tsim > 5000) & (df.Tsim < 5800)].index)
# df = df.drop(df[(df.Sim == 178) & (df.Team == 3) & (df.Tsim > 1700) & (df.Tsim < 2100)].index)
# df = df.drop(df[(df.Sim == 178) & (df.Team == 3) & (df.Tsim > 2500) & (df.Tsim < 3000)].index)
#
# df = df.drop(df[((df.Sim == 175))].index)
# df = df.drop(df[((df.Tsim > 7000))].index)

calculate_O3frac17(df, simlist)


df.to_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_Data_nocut_1607.csv")
# df.to_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_Data_nocut.csv")
#

# In[ ]:




