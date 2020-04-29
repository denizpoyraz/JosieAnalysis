import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from Beta_Functions import ratiofunction_beta, ratiofunction_beta_9602


def filter(df):

    filtEN = df.ENSCI == 1
    filtSP = df.ENSCI == 0

    filtS10 = df.Sol == 1
    filtS05 = df.Sol == 0.5

    filtB10 = df.Buf == 1.0
    filtB05 = df.Buf == 0.5

    filterEN0505 = (filtEN & filtS05 & filtB05)
    filterEN1010 = (filtEN & filtS10 & filtB10)

    profEN0505 = df.loc[filterEN0505]
    profEN1010 = df.loc[filterEN1010]
    profEN0505_nodup = profEN0505.drop_duplicates(['Sim', 'Team'])
    profEN1010_nodup = profEN1010.drop_duplicates(['Sim', 'Team'])

    ###

    filterSP1010 = (filtSP & filtS10 & filtB10)
    filterSP0505 = (filtSP & filtS05 & filtB05)

    profSP1010 = df.loc[filterSP1010]
    profSP0505 = df.loc[filterSP0505]
    profSP1010_nodup = profSP1010.drop_duplicates(['Sim', 'Team'])
    profSP0505_nodup = profSP0505.drop_duplicates(['Sim', 'Team'])

    sim_en0505 = profEN0505_nodup.Sim.tolist()
    team_en0505 = profEN0505_nodup.Team.tolist()

    sim_en1010 = profEN1010_nodup.Sim.tolist()
    team_en1010 = profEN1010_nodup.Team.tolist()

    sim_sp0505 = profSP0505_nodup.Sim.tolist()
    team_sp0505 = profSP0505_nodup.Team.tolist()

    sim_sp1010 = profSP1010_nodup.Sim.tolist()
    team_sp1010 = profSP1010_nodup.Team.tolist()

    sim = [sim_en0505, sim_en1010, sim_sp0505, sim_sp1010]
    team = [team_en0505, team_en1010, team_sp0505, team_sp1010]

    return sim, team


#######################################################################################################################
clist =[ 'Tsim', 'Sim', 'Team', 'ENSCI', 'Sol', 'Buf', 'Pair','PO3', 'IM','TPint', 'PO3_OPM', 'I_OPM', 'I_OPM_jma',
         'I_conv_slow',  'PFcor', 'R1_Tstart', 'R1_Tstop', 'R2_Tstart', 'R2_Tstop']

df1 = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie0910_Data_nocut.csv", low_memory=False)
df1 = df1.drop(['Unnamed: 0', 'Unnamed: 0.1', 'ADX', 'ADif', 'ADif_PO3S','Flow','Header_IB1', 'Header_PFcor',
                'Header_PFunc', 'Header_Sim', 'Header_Team', 'IB1', 'I_Pump','O3S', 'OPM', 'PO3_OPM_stp', 'PO3_jma',
                'PO3_stp', 'RDif', 'RDif_PO3S', 'TPext','Tact', 'Tair', 'Tinlet', 'VMRO3', 'VMRO3_OPM', 'Year', 'Z', 'frac']
               , axis=1)

df1 = df1.reindex(columns=clist)
print(list(df1))
# df2 = df1.copy()

df2 = pd.read_csv("/home/poyraden/Analysis/JOSIEfiles/Proccessed/Josie9602_Data.csv", low_memory=False)

df2 = df2.drop([ 'SST_Nr', 'SondeTypeNr'], axis=1)


# df = df.drop(df[(df.Sim == 140)].index)
# df = df.drop(df[(df.Sim == 147)].index)

# df = df.drop(df[(df.PO3 < 0)].index)
# df = df.drop(df[(df.PO3_OPM < 0)].index)
# df = df[df.ADX == 0]


sim_0910, team_0910 = filter(df1)
sim_9602, team_9602 = filter(df2)

## for 0910
rmean_en0505_0910, rstd_en0505, rmedian_en0505_0910, rqerr_en0505 = ratiofunction_beta(df1, sim_0910[0], team_0910[0], 'EN0505')
rmean_en1010_0910, rstd_en1010, rmedian_en1010_0910, rqerr_en1010 = ratiofunction_beta(df1, sim_0910[1], team_0910[1], 'EN1010')
rmean_sp0505_0910, rstd_sp0505, rmedian_sp0505_0910, rqerr_sp0505 = ratiofunction_beta(df1, sim_0910[2], team_0910[2], 'SP0505')
rmean_sp1010_0910, rstd_sp1010, rmedian_sp1010_0910, rqerr_sp1010 = ratiofunction_beta(df1, sim_0910[3], team_0910[3], 'SP1010')


## for 9602
rmean_en0505_9602, rstd_en0505_9602, rmedian_en0505_9602, rqerr_en0505_9602 = ratiofunction_beta_9602(df2, sim_9602[0], team_9602[0], 'EN0505')
rmean_en1010_9602, rstd_en1010_9602, rmedian_en1010_9602, rqerr_en1010_9602 = ratiofunction_beta_9602(df2, sim_9602[1], team_9602[1], 'EN1010')
rmean_sp0505_9602, rstd_sp0505_9602, rmedian_sp0505_9602, rqerr_sp0505_9602 = ratiofunction_beta_9602(df2, sim_9602[2], team_9602[2], 'SP0505')
rmean_sp1010_9602, rstd_sp1010_9602, rmedian_sp1010_9602, rqerr_sp1010_9602 = ratiofunction_beta_9602(df2, sim_9602[3], team_9602[3], 'SP1010')


rmean_en0505 = np.concatenate((rmean_en0505_9602, rmean_en0505_0910),  axis=None)
rmean_en1010 = np.concatenate((rmean_en1010_9602, rmean_en1010_0910),  axis=None)
rmean_sp0505 = np.concatenate((rmean_sp0505_9602, rmean_sp0505_0910),  axis=None)
rmean_sp1010 = np.concatenate((rmean_sp1010_9602, rmean_sp1010_0910),  axis=None)

rmedian_en0505 = np.concatenate((rmedian_en0505_9602, rmedian_en0505_0910),  axis=None)
rmedian_en1010 = np.concatenate((rmedian_en1010_9602, rmedian_en1010_0910),  axis=None)
rmedian_sp0505 = np.concatenate((rmedian_sp0505_9602, rmedian_sp0505_0910),  axis=None)
rmedian_sp1010 = np.concatenate((rmedian_sp1010_9602, rmedian_sp1010_0910),  axis=None)

print('0910')
print(np.nanmedian(rmedian_en0505_0910), np.nanmedian(rmedian_en1010_0910), np.nanmedian(rmedian_sp0505_0910), np.nanmedian(rmedian_sp1010_0910))
print('9602')
print(np.nanmedian(rmedian_en0505_9602), np.nanmedian(rmedian_en1010_9602), np.nanmedian(rmedian_sp0505_9602), np.nanmedian(rmedian_sp1010_9602))


print('mean en0505  en1010 sp0505 sp1010')
print(np.nanmedian(rmean_en0505), np.nanmedian(rmean_en1010), np.nanmedian(rmean_sp0505), np.nanmedian(rmean_sp1010))

print('median en0505  en1010 sp0505 sp1010')
print(np.nanmedian(rmedian_en0505), np.nanmedian(rmedian_en1010), np.nanmedian(rmedian_sp0505), np.nanmedian(rmedian_sp1010))
