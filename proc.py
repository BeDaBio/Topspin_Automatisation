# -*- coding: utf-8 -*-
# newest version can be found at https://github.com/BeDaBio/NMR_processing
 # stored in C:\Bruker\TopSpin4.0.8\classes\lib\topspin_py\py\pycmd # for Processing of the Spectrums
from TopCmds import *
import data_management as dat # stored in C:\Bruker\TopSpin4.0.8\classes\lib\topspin_py\py\pycmd # for data handling
import Processing_Algorithms as proz # stored in C:\Bruker\TopSpin4.0.8\classes\lib\topspin_py\py\pycmd # for processing algorythms
import Quality_Check # stored in C:\Bruker\TopSpin4.0.8\classes\lib\topspin_py\py\pycmd # for optional Quality check

# Data Input
INPUT = INPUT_DIALOG("Welcome to the automatic NMR Data processor",
    "Where is your data stored",
    ["Input Path = "],
    [r"C:\...\NMR2020_27_09_*"], ["Use `*` to differ between your samples"],buttons=["Ok","Cancel"])
if INPUT == None:
    ERRMSG(message = "Processing canceled")
    EXIT()
Datalist = dat.Import_and_Show(INPUT[0]) # to change input Parameter go to C:\Bruker\TopSpin4.0.8\classes\lib\topspin_py\py\pycmd\dat

# Selection of Type of Processing
Processing_Type = SELECT("","How do you want to continue ?",buttons=["Manual Phase correction and automatic processing", "Full automatic processing","Just open without processing afterwards"])
if Processing_Type == 0:
    dat.mult_open_manual_processing(Datalist)  
    ERRMSG(message = "Please move this message aside without closing it.\n You can now process your data manually.\nThe baseline of your spectra will be adjusted automatically after you close this message.", modal=1)
    XCMD("closeall",WAIT_TILL_DONE)
    for i in Datalist:
        RE_PATH(str(i)+"\\10\\pdata\\10\\1r")
        SLEEP(1)
        Difference=proz.proz_manually() # to change Processing algorythm go to C:\Bruker\TopSpin4.0.8\classes\lib\topspin_py\py\pycmd\proz
    #dat.check(Datalist)
elif Processing_Type == 2:
    dat.mult_open(Datalist)
    EXIT()
else:
    dat.check_already_processed(Datalist)
    Data_Type = SELECT("","What type of data would you like to process",buttons=["NOESY", "CPMG","Cancel"])
    if Data_Type == 2:
            ERRMSG(message = "Process canceled")
            EXIT()
    for i in Datalist:
        dat.copy_dat(i)
        if Data_Type == 1:
            left_boundary=0.5
            right_boundary=-0.5  
            Difference=proz.proz(left_boundary,right_boundary) # to change Processing algorythm go to C:\Bruker\TopSpin4.0.8\classes\lib\topspin_py\py\pycmd\proz
        else:
            left_boundary=9.0
            right_boundary=8.0   
            Difference=proz.proz_noe()   # to change Processing algorythm go to C:\Bruker\TopSpin4.0.8\classes\lib\topspin_py\py\pycmd\proz
if Quality_Check.Qualitytest == True:
    print("Evaluation of Spectrum processing according to De Brouwer, H. (2009). Evaluation of algorithms for automated phase correction of NMR spectra. Journal of magnetic resonance, 201(2), 230-238.:\n\
        The first value represents the difference over the integral before and after the Spectrum was processed \n\
        For the second value the Spectrum was lifted above 0 before calculating the difference")
    print('\n'.join(map(str,Difference)))     
dat.check(Datalist)


