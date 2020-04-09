import pandas as pd
import numpy as np
import glob
from pathlib import Path
import re

slow = 25 * 60  # 25 minutes in seconds
fast = 25  # 25seconds

# Read the metadata file
dfmeta = pd.read_excel("/home/poyraden/Analysis/JOSIEfiles/JOSIE-96-02/Josie_1996_metadata.xls")

for i in range(len(dfmeta)):
    if(dfmeta.at[i,'SondeTypeNr'] < 2): dfmeta.at[i,'ENSCI'] = 0
    if(dfmeta.at[i,'SondeTypeNr'] == 0): dfmeta.at[i,'ENSCI'] = 1
    if(dfmeta.at[i,'SST_Nr'] == 1):
        dfmeta.at[i,'Sol'] = 1.0
        dfmeta.at[i,'Buf'] = 1.0
    if(dfmeta.at[i,'SST_Nr'] == 2):
        dfmeta.at[i,'Sol'] = 0.5
        dfmeta.at[i,'Buf'] = 0.5
    if(dfmeta.at[i,'SST_Nr'] == 3):
        dfmeta.at[i,'Sol'] = 2.0
        dfmeta.at[i,'Buf'] = 0.0
    if(dfmeta.at[i,'SST_Nr'] == 4):
        dfmeta.at[i,'Sol'] = 1.0
        dfmeta.at[i,'Buf'] = 0.1
    if(dfmeta.at[i,'SST_Nr'] == 5):
        dfmeta.at[i,'Sol'] = 2.0
        dfmeta.at[i,'Buf'] = 0.1

# all files
## use pathlib jspr
filenames = dfmeta.Data_FIleName.tolist()
path = '/home/poyraden/Analysis/JOSIEfiles/JOSIE-96-02/1996/JOSIE-1996-DS1/DS1-Data/'
filenames = [path + i for i in filenames]
filenamespath = [Path(j) for j in filenames]

list_data = []

#Some declarations

columnMeta  = ['JOSIE_Nr', 'Sim_Nr', 'R1_Tstart', 'R1_Tstop', 'R2_Tstart', 'R2_Tstop', 'GAW_Report_Nr_Details',
               'Part_Nr' , 'SondeTypeNr', 'SST_Nr', 'Data_FIleName', 'ENSCI', 'Sol', 'Buf']

columnString = "RecNr Time Tsim PRES_R_Ist Temp_R_Is Temp_TMC_Ist_1 Alt_Ist PO3_OPM" \
               " TEO_1_Ch2 TEO_1_Ch3 PO3_Sonde_raw PO3_Sonde_Corr PO3_Sonde_TCO3 O3_Col_corr O3_Col_OPM Valid"
columnStr = columnString.split(" ")

#**********************************************
# Main loop to merge all data sets
#**********************************************
for filename in filenamespath:
    file = open(filename, 'r', encoding="ISO-8859-1")
    line1 = file.readline()
    matchObj = re.search(r"SIM0(.*)\.DS1 ", line1)
    sim = int(matchObj.group(1)[0:2])
    team = int(matchObj.group(1)[3:4])
    print(sim, team)
    infolist = file.readlines()[0:6]
    IB0 = float(infolist[1].split("=")[0])
    PFcor = float(infolist[2].split("=")[0])
    O3S = float(infolist[3].split("=")[0])
    OPM = float(infolist[4].split("=")[0])
    frac = float(infolist[5].split("=")[0])

    df = pd.read_csv(filename, engine="python", sep="\s+", skiprows=8, names=columnStr)
    #     ,  encoding = "ISO-8859-1"

    #     # Add the header information to the main df
    df = df.join(pd.DataFrame(
        [[sim, team, IB0, PFcor, O3S, OPM, frac]],
        index=df.index,
        columns=['Sim', 'Team', 'IB0', 'PFcor', 'O3S', 'OPM', 'frac']
    ))

    # Get the index of the metadata that corresponds to this Simulation Number and Participant (Team)

    select_indicesTeam = list(np.where(dfmeta["Part_Nr"] == df['Team'][0]))[0]
    select_indicesSim = list(np.where(dfmeta["Sim_Nr"] == df['Sim'][0]))[0]

    common = [i for i in select_indicesTeam if i in select_indicesSim]
    index_common = common[0]

    list_md = dfmeta.iloc[index_common, :].tolist()

    ## Add  metadata to the main df
    df = df.join(pd.DataFrame(
        [list_md],
        index=df.index,
        columns=columnMeta
    ))

    ## now convert variables to usual Josie naming conventions

    df['PO3'] = df['PO3_Sonde_Corr']
    df['IM'] = df['TEO_1_Ch2']
    df['TPint'] = df['TEO_1_Ch3']
    df['Pair'] = df['PRES_R_Ist']

    print(df['PO3_OPM'].dtypes, df['PFcor'].dtypes, df['TPint'].dtypes )

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
                # df.at[k,'PO3_jma'] = 0.043085 * df.at[k, 'TPint']  * (df.at[k, 'IM'] - df.at[k, 'IB1']) / (df.at[k, 'PFcor'] * JMA[p])
        if (df.at[k, 'Pair'] <= Pval[14]):
            df.at[k, 'OPM_I_jma'] = df.at[k, 'PO3_OPM'] * df.at[k, 'PFcor'] * JMA[14] / \
                                          (df.at[k, 'TPint'] * 0.043085)
            # df.at[k, 'PO3_jma'] = 0.043085 * df.at[k, 'TPint'] * (df.at[k, 'IM'] - df.at[k, 'IB1']) / (
            #             df.at[k, 'PFcor'] * JMA[14])



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

    list_data.append(df)
#

    #  end of the allfiles loop    #
     
# Merging all the data files to df

df = pd.concat(list_data,ignore_index=True)




df.to_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie1996_Data.csv")


    





