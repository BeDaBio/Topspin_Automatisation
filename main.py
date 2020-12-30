# -*- coding: utf-8 -*-
# newest version can be found at https://github.com/BeDaBio/Topspin_Automatisation
 # stored in C:\Bruker\TopSpin4.0.8\classes\lib\topspin_py\py\pycmd # for Processing of the Spectrums
from TopCmds import *
import data_management as dat # stored in C:\Bruker\TopSpin4.0.8\classes\lib\topspin_py\py\pycmd # for data handling
import processing as proz # stored in C:\Bruker\TopSpin4.0.8\classes\lib\topspin_py\py\pycmd # for processing algorythms
import quality_check # stored in C:\Bruker\TopSpin4.0.8\classes\lib\topspin_py\py\pycmd # for optional Quality check
from javax.swing import *
from java.awt import *





#Grab Variables from globalProp
Dimension = int(dat.get_globalParameter("Dimension"))
Type = str(dat.get_globalParameter("Type"))
Datalist = dat.get_globalParameter("Datalist",isList=True)
Process = int(dat.get_globalParameter("Process"))
Check = int(dat.get_globalParameter("Check"))
left_boundary=float(dat.get_globalParameter("left_boundary"))
right_boundary=float(dat.get_globalParameter("right_boundary"))

#Main processing Script
if Process == 3:
    dat.mult_open(Datalist,Dimension)
    MSG(message = "Processing succesfull", title=None)
    EXIT()
elif Process == 2:
    dat.mult_open_manual_processing(Datalist,Dimension,Type)  
    ERRMSG(message = "Please move this message aside without closing it.\n You can now process your data manually.\nThe baseline of your spectra will be adjusted automatically after you close this message.", modal=1)
    XCMD("closeall", WAIT_TILL_DONE)
    for i in Datalist:
        RE_PATH("{}/10/pdata/10/1r".format(i))
        Difference=proz.proz_manually() # to change Processing algorythm go to C:\Bruker\TopSpin4.0.8\classes\lib\topspin_py\py\pycmd\proz
else:
    un_processed=dat.check_already_processed(Datalist,Dimension)
    if Dimension==2:
        for i in Datalist:
            dat.copy_dat(i,Dimension,un_processed)
            proz.proz2D()
        dat.check(Datalist,Dimension)
    else:        
        for i in Datalist:
            dat.copy_dat(i,Dimension,un_processed)
            if Type == "CPMG":
                Difference=proz.proz() # to change Processing algorythm go to C:\Bruker\TopSpin4.0.8\classes\lib\topspin_py\py\pycmd\proz
            else: 
                Difference=proz.proz_noe()   # to change Processing algorythm go to C:\Bruker\TopSpin4.0.8\classes\lib\topspin_py\py\pycmd\proz
if quality_check.Qualitytest == True:
    print("Evaluation of Spectrum processing according to De Brouwer, H. (2009). Evaluation of algorithms for automated phase correction of NMR spectra. Journal of magnetic resonance, 201(2), 230-238.:\n\
        The first value represents the difference over the integral before and after the Spectrum was processed \n\
        For the second value the Spectrum was lifted above 0 before calculating the difference")
    print('\n'.join(map(str,Difference)))     
dat.check(Datalist,Dimension,Check)


