# Topspin Spectrum Processing Automatisation

Automatisation of NMR Spectrum processing using the Bruker Topspin software. 

## Installation: 

1. Download all files from repository pressing the green "⤓ Code" button and selecting  "Download ZIP".

2. Unzip file.

3. Save autoproc.py in C:\Bruker\\*TOPSPIN_VERSION*\exp\stan\nmr\py.

4. Save data_management.py, main.py, quality_Check.py and processing.py in C:\Bruker\\*TOPSPIN_VERSION*\classes\lib\topspin_py\py\pycmd.


To Start the pipeline open Topspin and enter "autoproc" in the command line.


## Caution:

 quality_check.py is still under construction. Setting "Qualitytest" to "True" can cause errors !
 
 If you want to evaluate the processing algorythms open quality_check.py and change the value of "Qualitytest"  to "True"
 
 ## Known Issues:
 
 *Error: java.lang.NullPointerException*
 
 Even though the Topspin Window switcher shows the thumbnail of a spectrum it does not apear in the count. If one trys to open it the error "java.lang.NullPointerException" appears. This can cause problems if many spectra are processed at once. The internal count of Topspin is then not equal to the counting system of the python programm. The sum of the windows causing the "java.lang.NullPointerException" error together with the sum of spectra selected for processing should be smaller than 35.
*Solution: restart Topspin.*




 Even though all windows are closed they still appear in the Topspin Window switcher count and in the .
  Windows are no longer visible in the Topspin Window switcher but are still opened in the java backround.
 *Solution: restart Topspin*
 
 
 
 
 *Tabbed pane error:* 
 
 The automated procession seems to be faster than the Topspin Spectrum overview sometimes.
 This error can be ignored as processing continues anyway. 
 So far no misclaculations in the atuomatic processing caused by this error have been reported.
 *Solution: Spectra should be checked manually afterwards.* 
 
