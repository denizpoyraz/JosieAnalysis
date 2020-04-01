
To be done:

1) In Beta_ConvolutedDF.py you have not applied any smoothing, for now do this by using running averages, but check further the  gaussian filtering method


Some bugs fixed w.r.t. the previous version of the code:

Related with makeDF: while calculating total O3 and total O3 from OPM, total O3 OPM was not
the same for each participants in the same simulations. This was due to a missing line in
https://github.com/denizpoyraz/JosieAnalysis/blob/fe904240e45c7a8b8e55df8b38a71bc629f8dcac/Codes/makeDF_Functions.py#L34

Some notes:

a) If you need to use fraction of total O3 from the sonde and total O3 from OPM: you need to apply proper cuts while making the DF using JosieYEAR_makeDF.py
If you do not these values, it is better to use DF without applied cuts _nocut and apply the cuts afterwards in your main code, like RDif_Calibration
