# -*- coding: utf-8 -*-
from TopCmds import *
Qualitytest = False # If Qualitytest = True: Evaluation of Spectrum processing gets printed in console
# Do not activate yet Under construction!! : 
# Check integral of Spectrum 
# save results in separate file

def Quality_lifted(method):
    """Decorator calcualting the Difference in Integral area after lifting the Spectrum above 0 before and after processing"""
    Column_Area_Spectrum_lifted_Difference=[]
    def lift_area():
        """Lifting the Spectrum above 0"""
        minimal_value=str(min(GETPROCDATA(500, -500))) # get Integral from Spectrum from 500 ppm to -500 ppm (extrem values chosen to get whole Spectrum)
        PUTPAR("DC", str(abs(float(minimal_value)))) # Set addition constant "DC" to minimal value of Spectrum
        XCMD("addc",WAIT_TILL_DONE) # Add addition constant
        area_lifted=sum(GETPROCDATA(500, -500)) # get sum of integral over whole Spectrum
        PUTPAR("DC", str(minimal_value)) #"-"+ set Spectrum back
        XCMD("addc",WAIT_TILL_DONE) # set Spectrum back
        return area_lifted

    def inner(*args,**kwargs):
        area_before_processing = lift_area() # lifted area is calculated
        Difference_over_integral=method(*args,**kwargs) # method is function that is decorated, using a conditional decorator class we created a double decorator. Difference_over_integral is the return from the first decorator "Quality".  
        area_after_processing = lift_area() # lifted area is calculated
        Difference_lifted = area_after_processing - area_before_processing # Difference in lifted area is calculated
        Column_Area_Spectrum_lifted_Difference.append(str(CURDATA()[0])+": "+str(Difference_over_integral)+", "+str(Difference_lifted))
        return Column_Area_Spectrum_lifted_Difference
    return inner
      
def Quality(method):
    """Decorator calcualting the Difference in integral area before and after processing"""
    def inner(*args,**kwargs):
        area_before = sum(GETPROCDATA(500, -500)) # get Integral from Spectrum from 500 ppm to -500 ppm (extrem values chosen to get whole Spectrum)
        method(*args,**kwargs) # decorated function gets executed 
        area_after = sum(GETPROCDATA(500, -500)) # Integral after processing
        Difference_over_integral = area_before - area_after
        if area_before == area_after:
            Difference_over_integral = "Spectrum did not change after processing" 
        return Difference_over_integral
    return inner

class conditional_decorator(object):
    '''Class for a conditional Operator using two decorators as input'''
    def __init__(self, dec1, dec2, condition):
        self.decorator = dec1
        self.decorator2 = dec2
        self.condition = condition
        #self.counter = 0
    def __call__(self, func):
        if self.condition == True:
            # Return the function unchanged, not decorated.
            return self.decorator2(self.decorator(func))
        else:
            return func
     

def phase_error(manually,automatic):
    """compare values of phase error from manually corrected and automatic corrected files"""


