import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Beta_Functions import ratiofunction_beta, ratiofunction_beta_9602, filter, ratiofunction_beta_pre
from Convolution_Functions import convolution, convolution_hs, smooth_and_convolute, convolution_pre

tslow = 25 * 60
tfast = 30

# df1 = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_preparationadded.csv", low_memory=False)
# df1 = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_Data_nocut_tempfixed_ml.csv", low_memory=False)

df1 = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_Data_nocut_1607.csv", low_memory=False)


df1 = df1[df1.ADX == 0]

df1 = df1.drop(df1[(df1.Sim == 147) & (df1.Team == 3)].index)
df1 = df1.drop(df1[(df1.Sim == 158) & (df1.Team == 1)].index)
df1 = df1.drop(df1[(df1.Sim == 158) & (df1.Team == 2)].index)
df1 = df1.drop(df1[(df1.Sim == 160) & (df1.Team == 4)].index)
df1 = df1.drop(df1[(df1.Sim == 165) & (df1.Team == 4)].index)

sim_0910, team_0910 = filter(df1)


# ## for 0910
# rmean_en0505_0910, rstd_en0505, rmedian_en0505_0910, rqerr_en0505 = ratiofunction_beta_pre(df1, sim_0910[0], team_0910[0], 'EN0505', 1, tslow, tfast)
# rmean_en1010_0910, rstd_en1010, rmedian_en1010_0910, rqerr_en1010 = ratiofunction_beta_pre(df1, sim_0910[1], team_0910[1], 'EN1010', 1, tslow, tfast)
# rmean_sp0505_0910, rstd_sp0505, rmedian_sp0505_0910, rqerr_sp0505 = ratiofunction_beta_pre(df1, sim_0910[2], team_0910[2], 'SP0505', 1, tslow, tfast)
# rmean_sp1010_0910, rstd_sp1010, rmedian_sp1010_0910, rqerr_sp1010 = ratiofunction_beta_pre(df1, sim_0910[3], team_0910[3], 'SP1010', 1, tslow, tfast)

rmean_en0505_0910, rstd_en0505, rmedian_en0505_0910, rqerr_en0505 = ratiofunction_beta(df1, sim_0910[0], team_0910[0], 'EN0505', 1, tslow, tfast)
rmean_en1010_0910, rstd_en1010, rmedian_en1010_0910, rqerr_en1010 = ratiofunction_beta(df1, sim_0910[1], team_0910[1], 'EN1010', 1, tslow, tfast)
rmean_sp0505_0910, rstd_sp0505, rmedian_sp0505_0910, rqerr_sp0505 = ratiofunction_beta(df1, sim_0910[2], team_0910[2], 'SP0505', 1, tslow, tfast)
rmean_sp1010_0910, rstd_sp1010, rmedian_sp1010_0910, rqerr_sp1010 = ratiofunction_beta(df1, sim_0910[3], team_0910[3], 'SP1010', 1, tslow, tfast)