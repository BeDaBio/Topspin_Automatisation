# Topspin Spectrum Processing Automatisation

Automatisation of NMR Spectrum processing using the Bruker Topspin software. 

## Installation: 

1. Download all files from repository pressing the green code button and selecting  "Download ZIP".

2. Unzip file.

3. Save autoproc.py in C:\Bruker\*TOPSPIN_VERSION*\exp\stan\nmr\py.

4. Save data_management.py, main.py, quality_Check.py and processing.py in C:\Bruker\*TOPSPIN_VERSION*\classes\lib\topspin_py\py\pycmd.


To Start the pipeline open Topspin and enter "autoproc" in the command line.


## Caution:

 quality_check.py is still under construction. activating setting "Qualitytest" to "True" can cause errors !
 
 If you want to evaluate the processing algorythms open quality_check.py and change the value of "Qualitytest"  to "True"
