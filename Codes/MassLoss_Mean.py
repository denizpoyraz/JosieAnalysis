import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.integrate import quad

df = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_deconv_ml.csv", low_memory=False)

df = df.drop(df[(df.iB0 < -1) ].index)
df = df.drop(df[(df.iB1 < -1) ].index)
df = df.drop(df[(df.iB2 < -1) ].index)

df = df.drop(df[(df.iB0 > 1) ].index)
df = df.drop(df[(df.iB1 > 1) ].index)
df = df.drop(df[(df.iB2 > 1) ].index)

# #
df = df.drop(df[(df.PO3 < 0)].index)
df = df.drop(df[(df.PO3_OPM < 0)].index)

# print('0910', list(df))
#
# #0910
df = df[df.ADX == 0]
df = df.drop(df[(df.Sim == 147) & (df.Team == 3)].index)
df = df.drop(df[(df.Sim == 158) & (df.Team == 1)].index)
df = df.drop(df[(df.Sim == 158) & (df.Team == 2)].index)
df = df.drop(df[(df.Sim == 160) & (df.Team == 4)].index)
df = df.drop(df[(df.Sim == 165) & (df.Team == 4)].index)


## 2017
df = df.drop(df[(df.PostTestSolution_Lost_gr < -1)].index)
df = df.drop(df[(df.Sim == 175) & (df.Team == 1)].index)
df = df.drop(df[(df.Sim == 172) & (df.Team == 2)].index)
df = df.drop(df[(df.Sim == 175) & (df.Team == 3)].index)
df = df.drop(df[(df.Sim == 175) & (df.Team == 4)].index)
df = df.drop(df[(df.Sim == 175) & (df.Team == 2)].index)
df = df.drop(df[(df.Sim == 179) & (df.Team == 2)].index)

## sonde solution buffer selection

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
profEN0505_nodup = profEN0505.drop_duplicates(['Sim', 'Team'])
profEN1010_nodup = profEN1010.drop_duplicates(['Sim', 'Team'])
###
filterSP1010 = (filtSP & filtS10 & filtB10)
filterSP0505 = (filtSP & filtS05 & filtB05)
#2017
# filterSP0505 = (filtSP & filtS10 & filtB01)

profSP1010 = df.loc[filterSP1010]
profSP0505 = df.loc[filterSP0505]
profSP1010_nodup = profSP1010.drop_duplicates(['Sim', 'Team'])
profSP0505_nodup = profSP0505.drop_duplicates(['Sim', 'Team'])
df_nodup = df.drop_duplicates(['Sim', 'Team'])



