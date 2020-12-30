# -*- coding: utf-8 -*-
import re
import os
import glob
from TopCmds import *

# Used to save and grab variables as global Topspin variables: 
def get_globalParameter(Parameter,isList=False):
    """grabs values from global Topspin parameter saved in globalProp"""
    Output=root.GlobalSettings.globalProp.getProperty("{}".format(Parameter)) # get global Parameter back from globalProp
    if isList == True: 
        # converts paths to spectrum file back from string in globalProp to list of paths needed for further analysis.
        Output = Output.split(",") 
    return Output

def toglobalParameter(Parameter, Name=None):
        """Saves Parameter as global Topspin variable"""
        if type(Parameter)== list: # Topspin can´t save Lists, but the paths to the files are saved as list of paths.
            Parameter=",".join(Parameter) # converts list to string.
        if Name==None:
            Name="Temp"
        ab=EXEC_PYSCRIPT("root.GlobalSettings.globalProp.setProperty( '{}', '{}')".format(Name,Parameter)) # Saves Parameter in "globalProp" see : Topcmds.py , EXEC_PYSCRIPT is needed, because its called inside the GUI. see Python Manual
        ab.join() # wait until EXEC_PYSCRIPT is done


def check_already_processed(List_of_Data_Paths,dimension):
    """Checks if there are Spectra that are already processed"""
    old_version_exists=False
    print("old_version_exists",old_version_exists)
    for paths in List_of_Data_Paths:
        if dimension == 1:
            old_version_exists = os.path.isfile(paths+r"\10\pdata\10\1r")
            print("path to file: ",paths+r"\10\pdata\10\1r")
        else:
            old_version_exists = os.path.isfile(paths+r"\12\pdata\10\1r")
        print("old_version_exists outside loop",old_version_exists)
        if old_version_exists==True :
            print("old_version_exists inside loop",old_version_exists)
            un_processed = SELECT("","Your dataset contains already processed data.\n How do you want to continue ?",buttons=["Overwrite processed", "Open processed", "Stop processing"])
            print("un_processed",un_processed)
            if int(un_processed) == 2: # value gets saved as string; has to be changed to int before comparing
                ERRMSG(message = "Process canceled")
                EXIT()
            elif un_processed==1:  
                un_processed=str(10)
                return un_processed
            else:
                un_processed=str(1)
                return un_processed
        else:
            print("unprocessed")
            un_processed=str(1)
            return un_processed  

def Import_and_Show(path):
    """Displays data from path. Multiple datasets can be selected using Regex"""
    Datalist=[] 
    Datalist = sorted(glob.glob(path))
    Datalist=[re.sub('\\\\', '/', i) for i in Datalist]
    value = SELECT("Is this your complete datalist ?","\n".join(Datalist),buttons=["Yes", "No"]) #Display Datalist with linebreaker
    if int(value) == 0: # value gets saved as string; has to be changed to int before comparing
        return Datalist
    else:
        new_Input=INPUT_DIALOG("Would you like to correct your input ?",
        "",
        ["Your Input="],
        [path],buttons=["Let us try again","Cancel"])
        if new_Input == None:
            EXEC_PYSCRIPT('ERRMSG(message = "Processing canceled")')
            EXEC_PYSCRIPT('EXIT()')
            return
        else:
            return Import_and_Show(new_Input[0]) # recursion for input correction

# if WR copy = RE_Path
def copy_dat (path,dimension,un_processed):
    """Processed data gets saved in folder "10" in "pdata" Directory """ 
    if dimension == 1:
        if un_processed == str(10):
            RE_PATH("{}/10/pdata/10/1r".format(path))
        else:
            RE_PATH("{}/10/pdata/1/1r".format(path),show="n")
            WR([CURDATA()[0],"10","10",CURDATA()[3]])
            RE_PATH("{}/10/pdata/10/1r".format(path))
    else:
        if un_processed == str(10):
                RE_PATH("{}/12/pdata/10/1r".format(path))
                return
        else:
            RE_PATH("{}/12/pdata/1/1r".format(path),show="n")# data is opened silently and copied using predefined commands   
            WR([CURDATA()[0],"12","10",CURDATA()[3]])
            RE_PATH("{}/12/pdata/10/1r".format(path))

        

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

def mult_open_manual_processing(Data,dimension,Type):
    """Opens Data for manual processing from a list. 35 at a time.  """
    un_processed=check_already_processed(Data,dimension)
    count =0
    if dimension == 2:
        for i in Data:
            copy_dat(i,dimension,un_processed)
            count +=1
            if count > 34:
                ERRMSG(message = "Topspin can only open 35 Spectra at once.\n Please move this message aside without closing it.\n You can analyse or process your data while this message is open.\n Missing Spectra of your Dataset are opened when you close this message", modal=1)
                XCMD("closeall",WAIT_TILL_DONE)  # closes all windows in Topspin
                count=0
            XCMD("newwin", 1)
        return 
    else:
        for i in Data:
            copy_dat(i,dimension,un_processed) 
            XCMD("*8",WAIT_TILL_DONE)   # upscale Spectrum
            XCMD("*8",WAIT_TILL_DONE)
            XCMD(".ph",WAIT_TILL_DONE)  # activates phase correction mode in Topspin
            if Type == "NOESY":
                left_boundary=0.5
                right_boundary=-0.5  
                PUTPAR("F2P",str("{}".format(right_boundary))) # Set region right bound
                PUTPAR("F1P",str("{}".format(left_boundary)))  # Set PP region left bound
                XCMD("plotreg",WAIT_TILL_DONE)
            else:  #Type== "CPMG"
                left_boundary=9.0
                right_boundary=8.0  
                PUTPAR("F2P",str("{}".format(right_boundary))) # Set region right bound
                PUTPAR("F1P",str("{}".format(left_boundary)))  # Set PP region left bound
                XCMD("plotreg",WAIT_TILL_DONE)
            count +=1
            if count > 34:
                ERRMSG(message = "Topspin can only open 35 Spectra at once.\n Please move this message aside without closing it.\n You can analyse or process your data while this message is open.\n Missing Spectra of your Dataset are opened when you close this message", modal=1)
                XCMD("closeall",WAIT_TILL_DONE)  # closes all windows in Topspin
                count=0
            XCMD("newwin", 1)  
    
def mult_open_check(Data,dimension):
    """Opens Data from a list for checking after processing"""
    count = 0
    for path in Data:
        if dimension == 1:  
            RE_PATH("{}/10/pdata/10/1r".format(path))
            XCMD("*8",WAIT_TILL_DONE)  # upscale Spectrum
            XCMD("*8",WAIT_TILL_DONE)
        else:
            RE_PATH("{}/12/pdata/10/1r".format(path))
        count +=1
        if count > 34:
            ERRMSG(message = "Topspin can only open 35 Spectra at once.\n Please move this message aside without closing it.\n You can now check your processed Spectra.\n Missing Spectra of your Dataset are opened when you close this message", modal=1)
            XCMD("closeall",WAIT_TILL_DONE)  # closes all windows in Topspin
            count=0
        XCMD("newwin", 1)

def check(Data,dimension,Check):
    #Check = SELECT("Process finished","Would you like to check the results ?",buttons=["Yes", "No"])
    if Check==1:
        mult_open_check(Data,dimension)
        MSG(message = "Processing succesfull", title=None)
    else:
        XCMD("closeall",WAIT_TILL_DONE)  # closes all windows in Topspin
        MSG(message = "Processing succesfull", title=None)


