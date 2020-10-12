from TopCmds import *
import Quality_Check

Qualitytest = Quality_Check.Qualitytest


def Check_180turn(leftboundary,rightboundary):
    """ turns the Spectrum for 180 degrees if Reference Region has an overall negative Signal"""
    Intensities_of_reference=sum(GETPROCDATA(leftboundary,rightboundary))
    if Intensities_of_reference < 0:
        XCMD(".ph",WAIT_TILL_DONE) # opens phase correction mode
        XCMD(".ph180",WAIT_TILL_DONE) # adds 180 degrees to ph0
        XCMD(".sret",WAIT_TILL_DONE) # adjusts Spectrum according to ph and safes result

# Processing of CPMG data
@Quality_Check.conditional_decorator(Quality_Check.Quality,Quality_Check.Quality_lifted,Qualitytest)
def proz(leftboundary,rightboundary):
    """processing pipeline for CPMG data""" 
    print("processing: ",CURDATA()[0]) 
    Check_180turn(leftboundary,rightboundary)
    EF()  #exponential window multiplication + fourier
    APK0() #1. Phase correction 0th Ordnung
    APK1() #1. Phase correction 1st Ordnung
    ABS() #Baseline correction
    APK() 
    ABS() #Baseline correction
    Check_180turn(leftboundary,rightboundary) 

def proz2D():
    """processing pipeline for CPMG data""" 
    XCMD("apk2d",WAIT_TILL_DONE)
    ABS2() #Baseline correction 
    ABS1()

# Processing of NOESY data
@Quality_Check.conditional_decorator(Quality_Check.Quality,Quality_Check.Quality_lifted,Qualitytest)
def proz_noe(leftboundary,rightboundary):
    """processing pipeline for NOESY data"""
    print("processing: ",CURDATA()[0]) 
    Check_180turn(leftboundary,rightboundary)
    EFP() # Exponential window multiplication + Fourier Transformation + phase correction
    ABS() # Baseline correction  
    Check_180turn(leftboundary,rightboundary)


# After manual processing
@Quality_Check.conditional_decorator(Quality_Check.Quality,Quality_Check.Quality_lifted,Qualitytest)
def proz_manually (leftboundary,rightboundary):
    """processing pipeline used after manual phase 	correction"""
    ABS() # Baseline correction 
    XCMD("closeall",WAIT_TILL_DONE)


