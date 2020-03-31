Some bugs fixed w.r.t. the previous version of the code:

Related with makeDF: while calculating total O3 and total O3 from OPM, total O3 OPM was not
the same for each participants in the same simulations. This was due to a missing line in
https://github.com/denizpoyraz/JosieAnalysis/blob/fe904240e45c7a8b8e55df8b38a71bc629f8dcac/Codes/makeDF_Functions.py#L34
