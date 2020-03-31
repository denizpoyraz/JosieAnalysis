#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import glob

from makeDF_Functions import calculate_O3frac17

slow = 25 * 60  # 25 minutes in seconds
fast = 25  # 25seconds

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

    df['PO3_stp'] = df['PO3'] * (df['Tair'] / 273.15)
    df['PO3_OPM_stp'] = df['PO3_OPM'] * (df['Tair'] / 273.15)

    ## convert OPM pressure to current
    df['I_OPM'] = (df['PO3_OPM'] * df['PFcor']) / (df['TPint'] * 0.043085)

    Pval = np.array([1000, 730, 535, 382, 267, 185, 126, 85, 58, 39, 26.5, 18.1, 12.1, 8.3, 6])
    JMA = np.array(
        [0.999705941, 0.997216654, 0.995162562, 0.992733959, 0.989710199, 0.985943645, 0.981029252, 0.974634364,
         0.966705137, 0.956132227, 0.942864263, 0.9260478, 0.903069813, 0.87528384, 0.84516337])

    for k in range(len(df)):
        ## jma corrections for OPM current, OPM_I_jma will be used only for Ua in the convolution of
        ## the slow component of the signal
        for p in range(len(JMA) - 1):
            if (df.at[k, 'Pair'] >= Pval[p + 1]) & (df.at[k, 'Pair'] < Pval[p]):
                # print(p, Pval[p + 1], Pval[p ])
                df.at[k, 'I_OPM_jma'] = df.at[k, 'PO3_OPM'] * df.at[k, 'PFcor'] * JMA[p] / \
                                        (df.at[k, 'TPint'] * 0.043085)
                df.at[k, 'PO3_jma'] = 0.043085 * df.at[k, 'TPint'] * (df.at[k, 'IM'] - df.at[k, 'iB1']) / (
                            df.at[k, 'PFcor'] * JMA[p])
        if (df.at[k, 'Pair'] <= Pval[14]):
            df.at[k, 'OPM_I_jma'] = df.at[k, 'PO3_OPM'] * df.at[k, 'PFcor'] * JMA[14] / \
                                    (df.at[k, 'TPint'] * 0.043085)
            df.at[k, 'PO3_jma'] = 0.043085 * df.at[k, 'TPint'] * (df.at[k, 'IM'] - df.at[k, 'iB1']) / (
                    df.at[k, 'PFcor'] * JMA[14])

    size = len(df)
    Ums_i = [0] * size
    Ua_i = [0] * size
    Ums_i[0] = df.at[0, 'IM']

    ## only convolute slow part of the signal, which is needed for beta calculation
    for i in range(size - 1):
        Ua_i = df.at[i + 1, 'I_OPM_jma']
        t1 = df.at[i + 1, 'Tsim']
        t2 = df.at[i, 'Tsim']
        Xs = np.exp(-(t1 - t2) / slow)
        Xf = np.exp(-(t1 - t2) / fast)
        Ums_i[i + 1] = Ua_i - (Ua_i - Ums_i[i]) * Xs

    df['I_conv_slow'] = Ums_i

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
df = df.drop(df[((df.Sim == 171) | (df.Sim == 172) | (df.Sim == 180) | (df.Sim == 185))].index)
df = df.drop(df[(df.Sim == 179) & (df.Team == 4) & (df.Tsim > 4000)].index)
df = df.drop(df[(df.Sim == 172) & (df.Tsim < 500)].index)
df = df.drop(df[(df.Sim == 172) & (df.Team == 1) & (df.Tsim > 5000) & (df.Tsim < 5800)].index)
df = df.drop(df[(df.Sim == 178) & (df.Team == 3) & (df.Tsim > 1700) & (df.Tsim < 2100)].index)
df = df.drop(df[(df.Sim == 178) & (df.Team == 3) & (df.Tsim > 2500) & (df.Tsim < 3000)].index)

df = df.drop(df[((df.Sim == 175))].index)
df = df.drop(df[((df.Tsim > 7000))].index)

calculate_O3frac17(df, simlist)


df.to_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2017_Data_withcut.csv")

# In[ ]:



