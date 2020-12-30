# -*- coding: utf-8 -*-
from TopCmds import *
import quality_check
import data_management as dat

Qualitytest = quality_check.Qualitytest
left_boundary=float(dat.get_globalParameter("left_boundary"))
right_boundary=float(dat.get_globalParameter("right_boundary"))

def Check_180turn(leftboundary,rightboundary):
    """ turns the Spectrum for 180 degrees if Reference Region has an overall negative Signal"""
    Intensities_of_reference=sum(GETPROCDATA(left_boundary,left_boundary))
    if Intensities_of_reference < 0:
        XCMD(".ph",WAIT_TILL_DONE) # opens phase correction mode
        XCMD(".ph180",WAIT_TILL_DONE) # adds 180 degrees to ph0
        XCMD(".sret",WAIT_TILL_DONE) # adjusts Spectrum according to ph and safes result

# Processing of CPMG data
@quality_check.conditional_decorator(quality_check.Quality,quality_check.Quality_lifted,Qualitytest)
def proz():
    """processing pipeline for CPMG data""" 
    print("processing: ",CURDATA()[0]) 
    Check_180turn(left_boundary,right_boundary)
    EF()  #exponential window multiplication + fourier
    APK0() #1. Phase correction 0th Ordnung
    APK1() #1. Phase correction 1st Ordnung
    ABS() #Baseline correction
    APK()
    ABS() #Baseline correction
    Check_180turn(left_boundary,right_boundary)

def proz2D():
    """processing pipeline for CPMG data"""
    print("processing: ",CURDATA()[0]) 
    XCMD("apk2d",WAIT_TILL_DONE)
    ABS2() #Baseline correction 
    ABS1()

# Processing of NOESY data
@quality_check.conditional_decorator(quality_check.Quality,quality_check.Quality_lifted,Qualitytest)
def proz_noe():
    """processing pipeline for NOESY data"""
    print("processing: ",CURDATA()[0]) 
    Check_180turn(left_boundary,right_boundary)
    EFP() # Exponential window multiplication + Fourier Transformation + phase correction
    ABS() # Baseline correction  
    Check_180turn(left_boundary,right_boundary)


# After manual processing
@quality_check.conditional_decorator(quality_check.Quality,quality_check.Quality_lifted,Qualitytest)
def proz_manually ():
    """processing pipeline used after manual phase 	correction"""
    Check_180turn(left_boundary,right_boundary)
    ABS() # Baseline correction 
    XCMD("closeall",WAIT_TILL_DONE)


