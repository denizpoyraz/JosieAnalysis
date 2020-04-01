
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

**I_slow_conv :** convoluted slow component of the signal, made at Beta_ConvolutedDF level

**I_fast :** fast part of the signal, I_ECC - I_slow_conv

**I_fast_deconv :** deconvoluted fast component of the signal
 
 ######The de/convolution is always made using the current, therefore current is converted to pressure
 
**PO3_slow_conv:** I_slow_conv is converted to pressure
 
**PO3_slow_conv_jma:** I_slow_conv is converted to pressure with JMA corrections

**PO3_deconv:** *I_fast_deconv* is converted to pressure

**PO3_deconv_jma:** *I_fast_deconv* is converted to pressure with JMA corrections

**I_fast_deconv_smSECOND**, **PO3_deconv_smSECOND**, **PO3_deconv_jma_smSECOND** are smoothed deconvoluted signals, for the moment
only running average method is used

 




