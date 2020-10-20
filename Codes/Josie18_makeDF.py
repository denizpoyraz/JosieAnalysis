import pandas as pd
import numpy as np
import re
import glob
import math
from math import log

from Josie_Functions import calculate_O3frac


# Read the metadata file
dfmeta = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Josie18/Josie18_MetaData.csv")


# Path to all Josie18 simulation files

allFiles = glob.glob("/home/poyraden/Analysis/JOSIEfiles/Josie18/Si*/*.O3R")

list_data = []

#Some declarations

columnString = "Tact Tsim Pair Tair Tinlet IM TPint TPext PFcor I_Pump PO3 VMRO3 PO3_OPM VMRO3_OPM ADif_PO3S RDif_PO3S Z"
columnStr = columnString.split(" ")


column_metaString = "Year Sim ENSCI Team Code Flow IB1 Cor Sol Buf ADX"
columnMeta = column_metaString.split(" ")

#**********************************************
# Main loop to merge all data sets
#**********************************************
for filename in allFiles:
    print(filename)
    file = open(filename,'r')
    # Get the participant information from the name of the file
    tmp_team = filename.split("/")[7]
    print(tmp_team)
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

     ## The index of the metadata that has the information of this simulation = index_common
    #  assign this row into a list
    
    list_md = dfmeta.iloc[index_common,:].tolist()
    print('list', len(list_md), list_md)

    df['OPM_I'] = (df['PO3_OPM'] * df['PFcor']) / (df['TPint'] * 0.043085)

    
    ## Add  metadata to the main df
    df = df.join(pd.DataFrame(
        [list_md],
        index = df.index,
        columns=columnMeta
    ))

    df['OPM_I'] = (df['PO3_OPM'] * df['PFcor']) / (df['TPint'] * 0.043085)


    slow = 25 * 60  # 25 minutes in seconds
    fast = 20  # 25seconds

    size = len(df)

    Ums_i = [0] * size
    Ums_i[0] = df.at[0, 'IM']
    Umf_i = [0] * size
    Umf_i[0] = df.at[0, 'IM']
    Uapf_i = [0] * size
    Uaps_i = [0] * size

    for i in range(size-1):
        Ua_i = df.at[i + 1, 'OPM_I']

        t1 = df.at[i + 1,'Tsim']
        t2 = df.at[i,'Tsim']
        Xs = np.exp(-(t1 - t2) / slow)
        Xf = np.exp(-(t1 - t2) / fast)

        Ums_i[i + 1] = Ua_i - (Ua_i - Ums_i[i]) * Xs
        Umf_i[i + 1] = Ua_i - (Ua_i - Umf_i[i]) * Xf
        ## now de-convolution of PO3
        Uapf_i[i + 1] = (df.at[i + 1, 'IM'] - df.at[i, 'IM'] * Xf) / (1 - Xf)
        Uaps_i[i + 1] = (df.at[i + 1, 'IM'] - df.at[i, 'IM'] * Xs) / (1 - Xs)

    df['I_conv_slow'] = Ums_i
    df['I_conv_fast'] = Umf_i
    df['I_deconv_fast'] = Uapf_i
    df['I_deconv_slow'] = Uaps_i







    list_data.append(df)
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

calculate_O3frac(df, simlist)



df.to_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie18_Data_current_conv.csv")

    





