
# JosieAnalysis

Codes inherited from Analysis_Josie repository: https://github.com/denizpoyraz/Analysis_Josie
Analysis_Josie had many unused, old-dated codes that need to be organized.

Explanation of the codes:

**Josie0910_makeDF.py:** reads 2009/2010 data and meta-data. Converts into a format which is analyzable for me.

**Josie17_makeDF.py:** The same as 0910, but the meta data is different for 2017 data.

**MergeDF.py:** general code to add DFs, like adding 2009 and 2010 and making one DF 

**makeDF_Functions.py**: Functions used by makeDF codes, Josie0910_makeDF and Josie17_makeDF

**Ratio_TimeConstant.py:** Takes the ratio of I_ECC/ (0.1*I_conv_slow) to calculate beta values, this code is for plotting

**Beta_ConvolutedDF.py:** Calculates the beta values as in Ratio_TimeConstant.py and uses it to make DFs with deconvoluted signal

###
## Variables in the convoluted DF's

**I_conv_slow:** this is obtained at JosieYEAR_makeDF level, it is used to calculate beta and 
for Ua OPM corrected with JMA is used. **This is ONLY used for beta calculation.**

From Josie0910_makeDF.py

    for i in range(size-1):

        Ua_i = df.at[i + 1, 'I_OPM_jma']
        t1 = df.at[i + 1,'Tsim']
        t2 = df.at[i,'Tsim']
        Xs = np.exp(-(t1 - t2) / slow)
        Ums_i[i + 1] = Ua_i - (Ua_i - Ums_i[i]) * Xs

    df['I_conv_slow'] = Ums_i
The rest of the variables are calculated in Beta_ConvolutedDF
**I_slow_conv :** convoluted slow component of the signal, made at Beta_ConvolutedDF level

        Islow[i] = beta * dft[j].at[i, 'I_OPM_jma']
        Islow_conv[i + 1] = Islow[i] - (Islow[i] - Islow_conv[i]) * Xs

**I_fast :** fast part of the signal, I_ECC - I_slow_conv

        Ifast[i + 1] = af * (dft[j].at[i + 1, 'IM'] - Islow_conv[i + 1])

**I_fast_deconv :** deconvoluted fast component of the signal

        Ifast_deconv[i + 1] = (Ifast[i + 1] - Ifast[i] * Xf) / (1 - Xf)

 
 ######The de/convolution is always made using the current, therefore current is converted to pressure
 
**PO3_slow_conv:** I_slow_conv is converted to pressure

    dft[j]['PO3_slow_conv'] = 0.043085 * dft[j]['TPint'] * dft[j]['I_slow_conv'] / dft[j]['PFcor']
 
**PO3_slow_conv_jma:** I_slow_conv is converted to pressure with JMA corrections

**PO3_deconv:** *I_fast_deconv* is converted to pressure

    dft[j]['PO3_deconv'] = 0.043085 * dft[j]['TPint'] * dft[j]['I_fast_deconv'] / dft[j]['PFcor']
    

**PO3_deconv_jma:** *I_fast_deconv* is converted to pressure with JMA corrections

     dft[j].at[k, 'PO3_deconv_jma'] = 0.043085 * dft[j].at[k, 'TPint'] * dft[j].at[k, 'I_fast_deconv'] / \
                                                (dft[j].at[k, 'PFcor'] * JMA[p])

**I_fast_deconv_smSECOND**, **PO3_deconv_smSECOND**, **PO3_deconv_jma_smSECOND** are smoothed deconvoluted signals, for the moment
only running average method is used

 




