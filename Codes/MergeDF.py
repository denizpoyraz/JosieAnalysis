import pandas as pd
import numpy as np

df1 = pd.read_csv('/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2009_Data_withcut.csv')
df2 = pd.read_csv('/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie2010_Data_withcut.csv')

frames = [df1,df2]

dfall = pd.concat(frames)

dfall.to_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_Data_withcut.csv")


# df = pd.read_csv('/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie17_data_notimecut.csv')
#
# dfsim = df.drop_duplicates(['Sim'])
# simlist = dfsim.Sim.tolist()
#
# for s in simlist:
#     filt1 = (df.Sim == s) & (df.Team == 1)
#     filt2 = (df.Sim == s) & (df.Team == 2)
#     filt3 = (df.Sim == s) & (df.Team == 3)
#     filt4 = (df.Sim == s) & (df.Team == 4)
#     filt5 = (df.Sim == s) & (df.Team == 5)
#     filt6 = (df.Sim == s) & (df.Team == 6)
#     filt7 = (df.Sim == s) & (df.Team == 7)
#     filt8 = (df.Sim == s) & (df.Team == 8)
#
#
#     df.loc[filt2, 'Pair'] = np.array(df.loc[filt1, 'Pair'])
#     df.loc[filt3, 'Pair'] = np.array(df.loc[filt1, 'Pair'])
#     df.loc[filt4, 'Pair'] = np.array(df.loc[filt1, 'Pair'])
#     df.loc[filt6, 'Pair'] = np.array(df.loc[filt5, 'Pair'])
#     df.loc[filt7, 'Pair'] = np.array(df.loc[filt5, 'Pair'])
#     df.loc[filt8, 'Pair'] = np.array(df.loc[filt5, 'Pair'])
#
# df.to_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie17_data_notimecut_pair.csv")
