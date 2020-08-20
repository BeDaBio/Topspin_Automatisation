from TopCmds import *
import Quality_Check

Qualitytest = Quality_Check.Qualitytest

# Processing of CPMG data
@Quality_Check.conditional_decorator(Quality_Check.Quality,Quality_Check.Quality_lifted,Qualitytest)
def proz():
    """processing pipeline for CPMG data"""  
    EF()  #exponential window multiplication + fourier
    APK0() #1. Phase correction 0th Ordnung
    APK1() #1. Phase correction 1st Ordnung
    ABS() #Baseline correction  

# Processing of NOESY data
@Quality_Check.conditional_decorator(Quality_Check.Quality,Quality_Check.Quality_lifted,Qualitytest)
def proz_noe():
    """processing pipeline for NOESY data"""
    EFP() # Exponential window multiplication + Fourier Transformation + phase correction
    ABS() # Baseline correction  


# After manual processing
@Quality_Check.conditional_decorator(Quality_Check.Quality,Quality_Check.Quality_lifted,Qualitytest)
def proz_manually ():
    """processing pipeline used after manual phase 	correction"""
    ABS() # Baseline correction 
    XCMD("closeall",WAIT_TILL_DONE)


