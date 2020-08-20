import math
import os
import sys
import glob
from TopCmds import *

def check_already_processed(List_of_Data_Paths):
    """Checks if there are Spectra that are already processed"""
    for paths in List_of_Data_Paths:
        old_version_exists=os.path.isfile(paths+r"\10\pdata\10\1r")
        if old_version_exists==True:
            value = SELECT("","Your dataset contains already processed data.\n Do you want to overwrite them ?",buttons=["Yes", "No"]) #Display Datalist with linebreaker
            if int(value) == 1: # value gets saved as string; has to be changed to int before comparing
                ERRMSG(message = "Process canceled")
                EXIT()
                break    
            else:
                break  

def Import_and_Show(path):
    """Displays data from path. Multiple datasets can be selected using Regex"""
    Datalist=[] 
    Datalist = sorted(glob.glob(path))
    value = SELECT("Is this your complete datalist ?","\n".join(Datalist),buttons=["Yes", "No"]) #Display Datalist with linebreaker
    if int(value) == 0: # value gets saved as string; has to be changed to int before comparing
        return Datalist
    else:
        new_Input=INPUT_DIALOG("Would you like to correct your input ?",
        "",
        ["Your Input="],
        [path],buttons=["Let us try again","Cancel"])
        if new_Input == None:
            ERRMSG(message = "Processing canceled")
            EXIT()
        else:
            return Import_and_Show(new_Input[0]) # recursion for input correction

# if WR copy = RE_Path
def copy_dat (path):
    """Processed data gets saved in folder "10" in "pdata" Directory """
    RE_PATH(str(path)+"\\10\\pdata\\1\\1r",show="n") # copying the data using shutil does not work inside topspin, so data is opened silently and copied using Topspin language
    if CURDATA()[2] == u"10":
        RE_PATH(str(path)+"\\10\\pdata\\10\\1r")   
    else:
        WR([CURDATA()[0],"10","10",CURDATA()[3]])
        #SLEEP(0.5)
        RE_PATH(str(path)+"\\10\\pdata\\10\\1r")

def mult_open(Data):
    """Opens Data for automatic processing from a list. 35 at a time."""
    check_already_processed(Data)
    count = 0
    for i in Data:
        copy_dat(i) 
        count +=1
        if count > 34:
            ERRMSG(message = "Topspin can only open 35 Spectra at once.\n Please move this message aside without closing it.\n You can now process your data manually.\n Missing Spectra of your Dataset are opened when you close this message", modal=1)
            XCMD("closeall",WAIT_TILL_DONE) # closes all windows in Topspin
            count=0
        NEWWIN()

def mult_open_manual_processing(Data):
    """Opens Data for manual processing from a list. 35 at a time.  """
    check_already_processed(Data)
    Type = SELECT("","What type of data would you like to process",buttons=["NOESY", "CPMG","Cancel"])
    count = 0
    if Type == 2:
        ERRMSG(message = "Process canceled")
        EXIT()
    for i in Data:
        copy_dat(i) 
        XCMD("*8",WAIT_TILL_DONE)   # upscale Spectrum
        XCMD("*8",WAIT_TILL_DONE)
        XCMD(".ph",WAIT_TILL_DONE)  # activates phase correction mode in Topspin
        if Type == 1:   
            PUTPAR('F2P',str(-0.5)) # Set region right bound
            PUTPAR('F1P',str(0.5))  # Set PP region left bound
            XCMD("plotreg",WAIT_TILL_DONE)
        else: 
            PUTPAR('F2P',str(8.0))  # Set region right bound
            PUTPAR('F1P',str(9.0))  # Set PP region left bound
            XCMD("plotreg",WAIT_TILL_DONE)    #Zoom into region set by F1P/F2P        
        count +=1
        if count > 34:
            ERRMSG(message = "Topspin can only open 35 Spectra at once.\n Please move this message aside without closing it.\n You can analyse or process your data while this message is open.\n Missing Spectra of your Dataset are opened when you close this message", modal=1)
            XCMD("closeall",WAIT_TILL_DONE)  # closes all windows in Topspin
            count=0
        NEWWIN()    
    
def mult_open_check(Data):
    """Opens Data from a list for checking after processing"""
    count = 0
    for path in Data:
        RE_PATH(str(path)+"\\10\\pdata\\10\\1r")
        count +=1
        if count > 34:
            ERRMSG(message = "Topspin can only open 35 Spectra at once.\n Please move this message aside without closing it.\n You can now check your processed Spectra.\n Missing Spectra of your Dataset are opened when you close this message", modal=1)
            XCMD("closeall",WAIT_TILL_DONE)  # closes all windows in Topspin
            count=0
        NEWWIN()

def check(Data):
    Check = SELECT("Process finished","Would you like to check the results ?",buttons=["Yes", "No"])
    if Check==0:
        mult_open_check(Data)
        MSG(message = "Processing succesfull", title=None)
    else:
        XCMD("closeall",WAIT_TILL_DONE)  # closes all windows in Topspin
        MSG(message = "Processing succesfull", title=None)


