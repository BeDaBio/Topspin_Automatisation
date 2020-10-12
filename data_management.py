import math
import os
import sys
import glob
import Processing_Algorithms as proz
from TopCmds import *

# open processed data when using only open 

def check_already_processed(List_of_Data_Paths,dimension):
    """Checks if there are Spectra that are already processed"""
    for paths in List_of_Data_Paths:
        if dimension == 0:
            old_version_exists = os.path.isfile(paths+r"\10\pdata\10\1r")
        else:
            old_version_exists = os.path.isfile(paths+r"\12\pdata\10\1r")
        if old_version_exists==True :
            un_processed = SELECT("","Your dataset contains already processed data.\n How do you want to continue ?",buttons=["Open unprocessed", "Open processed", "Stop processing"]) #Display Datalist with linebreaker
            if int(un_processed) == 2: # value gets saved as string; has to be changed to int before comparing
                ERRMSG(message = "Process canceled")
                EXIT()
                return    
            elif un_processed==1:  
                un_processed=str(10)
                return un_processed
            else:
                un_processed=str(1)
                return un_processed

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
def copy_dat (path,dimension,un_processed):
    """Processed data gets saved in folder "10" in "pdata" Directory """
    if dimension == 0:
        if un_processed == str(10):
                RE_PATH(str(path)+"\\10\\pdata\\"+un_processed+"\\1r")
        else:
            RE_PATH(str(path)+"\\10\\pdata\\1\\1r",show="n")
            WR([CURDATA()[0],"10","10",CURDATA()[3]])
            RE_PATH(str(path)+"\\10\\pdata\\10\\1r")
    else:
        if un_processed == str(10):
                RE_PATH(str(path)+"\\12\\pdata\\"+un_processed+"\\1r")
                return
        else:
            RE_PATH(str(path)+"\\12\\pdata\\1\\1r",show="n")# copying the data using shutil does not work inside topspin, so data is opened silently and copied using Topspin language    
            WR([CURDATA()[0],"12","10",CURDATA()[3]])
            RE_PATH(str(path)+"\\12\\pdata\\10\\1r")

        

def mult_open(Data,dimension):
    """Opens Data for automatic processing from a list. 35 at a time."""
    un_processed=check_already_processed(Data,dimension)
    count = 0
    for i in Data:
        copy_dat(i,dimension,un_processed) 
        count +=1
        if count > 34:
            ERRMSG(message = "Topspin can only open 35 Spectra at once.\n Please move this message aside without closing it.\n You can now process your data manually.\n Missing Spectra of your Dataset are opened when you close this message", modal=1)
            XCMD("closeall",WAIT_TILL_DONE) # closes all windows in Topspin
            count=0
        NEWWIN()

def mult_open_manual_processing(Data,dimension):
    """Opens Data for manual processing from a list. 35 at a time.  """
    un_processed=check_already_processed(Data,dimension)
    if dimension == 1:
        for i in Data:
            copy_dat(i,dimension,un_processed)
            count +=1
            if count > 34:
                ERRMSG(message = "Topspin can only open 35 Spectra at once.\n Please move this message aside without closing it.\n You can analyse or process your data while this message is open.\n Missing Spectra of your Dataset are opened when you close this message", modal=1)
                XCMD("closeall",WAIT_TILL_DONE)  # closes all windows in Topspin
                count=0
            NEWWIN()
        return 
    Type = SELECT("","What type of data would you like to process",buttons=["NOESY", "CPMG","Cancel"])
    count = 0
    if Type == 2:
        ERRMSG(message = "Process canceled")
        EXIT()
    for i in Data:
        copy_dat(i,dimension,un_processed) 
        XCMD("*8",WAIT_TILL_DONE)   # upscale Spectrum
        XCMD("*8",WAIT_TILL_DONE)
        XCMD(".ph",WAIT_TILL_DONE)  # activates phase correction mode in Topspin
        if Type == 1:
            left_boundary=0.5
            right_boundary=-0.5  
            PUTPAR('F2P',str(right_boundary)) # Set region right bound
            PUTPAR('F1P',str(left_boundary))  # Set PP region left bound
            XCMD("plotreg",WAIT_TILL_DONE)
        else: 
            left_boundary=9.0
            right_boundary=8.0  
            PUTPAR('F2P',str(right_boundary)) # Set region right bound
            PUTPAR('F1P',str(left_boundary))  # Set PP region left bound
            XCMD("plotreg",WAIT_TILL_DONE)    #Zoom into region set by F1P/F2P        
        count +=1
        if count > 34:
            ERRMSG(message = "Topspin can only open 35 Spectra at once.\n Please move this message aside without closing it.\n You can analyse or process your data while this message is open.\n Missing Spectra of your Dataset are opened when you close this message", modal=1)
            XCMD("closeall",WAIT_TILL_DONE)  # closes all windows in Topspin
            count=0
        NEWWIN()    
    
def mult_open_check(Data,dimension):
    """Opens Data from a list for checking after processing"""
    count = 0
    for path in Data:
        if dimension == 0:
            RE_PATH(str(path)+"\\10\\pdata\\10\\1r")
            XCMD("*8",WAIT_TILL_DONE)   # upscale Spectrum
            XCMD("*8",WAIT_TILL_DONE)
        else:
            RE_PATH(str(path)+"\\12\\pdata\\10\\1r")
        count +=1
        if count > 34:
            ERRMSG(message = "Topspin can only open 35 Spectra at once.\n Please move this message aside without closing it.\n You can now check your processed Spectra.\n Missing Spectra of your Dataset are opened when you close this message", modal=1)
            XCMD("closeall",WAIT_TILL_DONE)  # closes all windows in Topspin
            count=0
        NEWWIN()

def check(Data,dimension):
    Check = SELECT("Process finished","Would you like to check the results ?",buttons=["Yes", "No"])
    if Check==0:
        mult_open_check(Data,dimension)
        MSG(message = "Processing succesfull", title=None)
    else:
        XCMD("closeall",WAIT_TILL_DONE)  # closes all windows in Topspin
        MSG(message = "Processing succesfull", title=None)


