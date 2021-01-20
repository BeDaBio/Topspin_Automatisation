# -*- coding: utf-8 -*-
# newest version can be found at https://github.com/BeDaBio/Topspin_Automatisation
from TopCmds import *
import data_management as dat # stored in C:\Bruker\TopSpin4.0.8\classes\lib\topspin_py\py\pycmd # for data handling
import re
from javax.swing import *
from java.awt import *

# Skript is called in Topspin directly
# Contains GUI, sets global variables and calls main loop



#Initializing Variables
Dimension = 1
Type = "NOESY"
Path = None
Process = 3
Check = True
left_boundary=None
right_boundary=None

class MainGUI:
    def setvisibility(self):
        """sets visibility of conditional parameter"""
        global Type
        global Process
        global Dimension
        if Process == 3 or Dimension == 2:
            self.Label6.setVisible(False)
            self.Label9.setVisible(False)
            self.Label10.setVisible(False)
            self.Label7.setVisible(False)
            self.Label8.setVisible(False)
            self.left_boundary_CPMG.setVisible(False)
            self.right_boundary_CPMG.setVisible(False)
            self.left_boundary_NOESY.setVisible(False)
            self.right_boundary_NOESY.setVisible(False)
            self.Label4.setVisible(False)
            self.TypeButton1.setVisible(False)
            self.TypeButton2.setVisible(False)

        else:
            self.Label4.setVisible(True)
            self.TypeButton1.setVisible(True)
            self.TypeButton2.setVisible(True)
            if Type == "CPMG":
                self.Label6.setVisible(True)
                self.Label9.setVisible(True)
                self.Label10.setVisible(True)
                self.Label7.setVisible(False)
                self.Label8.setVisible(True)
                self.left_boundary_CPMG.setVisible(True)
                self.right_boundary_CPMG.setVisible(True)
                self.left_boundary_NOESY.setVisible(False)
                self.right_boundary_NOESY.setVisible(False)
            else: #Type == "NOESY"
                self.Label6.setVisible(True)
                self.Label7.setVisible(True)
                self.Label8.setVisible(False)
                self.Label9.setVisible(True)
                self.Label10.setVisible(True)
                self.left_boundary_CPMG.setVisible(False)
                self.right_boundary_CPMG.setVisible(False)
                self.left_boundary_NOESY.setVisible(True)
                self.right_boundary_NOESY.setVisible(True)
        


    #Initializing Action Listeners
    def Dimensioncheck(self,event):
        global Dimension
        if self.DimensionButton1.isSelected():
            #print("1D Spectrum")
            Dimension = 1
            self.ProcessButton3.setVisible(True)
            self.setvisibility()
        else:
            #print("2D Spectrum")
            self.ProcessButton3.setVisible(False) #conditional Paramter not used in 2D processing
            Dimension = 2
            self.setvisibility()
        return Dimension

    def Typecheck(self,event):
        global Type
        if self.TypeButton1.isSelected():
            #print("NOESY")
            Type = "NOESY"
            self.setvisibility()
        else:
            #print("CPMG")
            Type = "CPMG"
            self.setvisibility()
        return Type


    def Processcheck(self,event):
        global Process
        if self.ProcessButton1.isSelected():
            #print("Full automatic processing")
            Process = 1
            self.setvisibility()
        elif self.ProcessButton2.isSelected():
            #print("Semiautomatic processing")
            Process = 2
            self.setvisibility()
        else:
            #print("Just openening without processing...")
            Process = 3
            self.setvisibility()
        return Process

    def Checkcheck(self,event):
        if self.Checkbox1.isSelected():
            print("check data after processing")
            Check = 1
        else:
            Check = 0 

    def getReferenceRegion(self):
        """grabs left and right boundary of reference region from GUI input"""
        if Type == "CPMG":
            left_boundary=self.left_boundary_CPMG.getText()	
            right_boundary=self.right_boundary_CPMG.getText()
        else: #Type == "NOESY"
            left_boundary=self.left_boundary_NOESY.getText() 	
            right_boundary=self.right_boundary_NOESY.getText()
        return left_boundary,right_boundary



    def StartProcess(self,event):
        """Informs the user about selected parameter,saves them as global parameter and starts main processing script"""
        global Type
        global Process
        global Dimension
        
        if self.DimensionButton1.isSelected():
            print("Starting 1D Spectrum Processing ")
            Dimension = 1
            self.ProcessButton3.setVisible(True)
            self.setvisibility()
        else:
            print("Starting 2D Spectrum")
            Dimension = 2
            self.ProcessButton3.setVisible(False)
            self.setvisibility()
        if self.TypeButton1.isSelected():
            print("Type of Spectrum: NOESY")
            Type = "NOESY"
            self.setvisibility()
        else:
            print("Type of Spectrum: CPMG")
            Type = "CPMG" 
            self.setvisibility()
        if self.ProcessButton1.isSelected():
            print("Full automatic processing")
            self.setvisibility()
            Process = 1
        elif self.ProcessButton2.isSelected():
            self.setvisibility()
            print("Semiautomatic processing")
            Process = 2
        else:
            print("Only open without processing")
            self.setvisibility()
            Process = 3
        
        if self.Checkbox1.isSelected():
            print("Checking Data after processing")
            Check = 1
        else:
            Check = 0

        Datalist = dat.Import_and_Show(self.Input.getText()) # to change input Parameter go to C:\Bruker\TopSpin4.0.8\classes\lib\topspin_py\py\pycmd\data_management
        Datalist=[re.sub("\\\\", "/", x) for x in Datalist]
        left_boundary,right_boundary=self.getReferenceRegion()

        #variables are safed in globalProp:
        dat.toglobalParameter(left_boundary, Name="left_boundary")
        dat.toglobalParameter(right_boundary, Name="right_boundary")
        dat.toglobalParameter(Process, Name="Process")
        dat.toglobalParameter(Type, Name="Type") 
        dat.toglobalParameter(Check, Name="Check")  
        dat.toglobalParameter(Dimension, Name="Dimension") 
        dat.toglobalParameter(Datalist, Name="Datalist") 
        self.frame.dispose()
        #Safes Version number as global parameter to access the right directory for other parts of the script
        threat = EXEC_PYSCRIPT("root.GlobalSettings.globalProp.setProperty( 'globalTopspinVersion', TOPSPIN_VERSION()[0])")
        threat.join()
        TopspinVersion = root.GlobalSettings.globalProp.getProperty("globalTopspinVersion")
        VersionNumber = TopspinVersion.split(" ")[1]
        
        #The main processing steps are carried out in a separate script to avoid threading problems:
        EXEC_PYFILE("C:/Bruker/Topspin{}/classes/lib/topspin_py/py/pycmd/main".format(VersionNumber)) 




    def __init__(self):
        #define buttons:
        self.Label0=JLabel("Please specify you processing Parameters and continue by pressing 'Start'") 	
        self.Label1=JLabel("Input Path:")
        self.Input=JTextField(r"C:\...\NMR2020_27_09_*",50) 	
        self.Label2=JLabel("Use * to differ between samples")

        self.Label3=JLabel("Are your spectra 1D or 2D ?")
        self.DimensionButton1=JRadioButton("1D",True,actionPerformed=self.Dimensioncheck) 
        self.DimensionButton2=JRadioButton("2D",actionPerformed=self.Dimensioncheck)

        self.Label4=JLabel("What type of spectra would you like to process :")
        self.TypeButton1=JRadioButton("NOESY",True,actionPerformed=self.Typecheck) 
        self.TypeButton2=JRadioButton("CPMG",actionPerformed=self.Typecheck)

        self.Label5=JLabel("How do you want to process your Data ? ")
        self.ProcessButton1=JRadioButton("Full automatic processing",actionPerformed=self.Processcheck) 
        self.ProcessButton2=JRadioButton("Manual phase correction and automatic processing",actionPerformed=self.Processcheck)
        self.ProcessButton3=JRadioButton("Just open without processing afterwards",True,actionPerformed=self.Processcheck)

        self.Label6=JLabel("The spectra are zoomed to the signal of a reference metabolite to facilitate manual phase correction:")
        self.Label7=JLabel("The predefined internal standard used for NOESY spectra is TSP:")
        self.Label8=JLabel("The predefined internal standard used for CPMG spectra is formic acid:")
        self.Label9=JLabel("Left boundary of reference region")
        self.Label10=JLabel("Right boundary of reference region")
        self.left_boundary_CPMG=JTextField(r" 9.0 ",10) 	
        self.right_boundary_CPMG=JTextField(r" 8.0 ",10) 
        self.left_boundary_NOESY=JTextField(r" 0.5 ",10) 	
        self.right_boundary_NOESY=JTextField(r" -0.5 ",10)

        self.Checkbox1 = JCheckBox("Would you like to check your data after processing ?",True,actionPerformed=self.Checkcheck)
        self.StartButton = JButton("Start", actionPerformed = self.StartProcess)

        #Define Location
        self.Label0.setBounds(5,10,800,20)
        self.Label1.setBounds(5,40,80,20)
        self.Input.setBounds(95,40,500,25)
        self.Label2.setBounds(600,40,400,20)
        self.Label3.setBounds(5,80,400,20)
        self.DimensionButton1.setBounds(20,100,100,20)
        self.DimensionButton2.setBounds(20,120,100,20)

        self.Label5.setBounds(5,160,400,20)
        self.ProcessButton1.setBounds(20,180,600,20)
        self.ProcessButton2.setBounds(20,200,600,20)
        self.ProcessButton3.setBounds(20,220,600,20)

        self.Label4.setBounds(5,260,400,20)
        self.TypeButton1.setBounds(20,280,300,20)
        self.TypeButton2.setBounds(20,300,600,20)
        

        self.Label6.setBounds(5,340,800,20)
        self.Label7.setBounds(20,360,500,20)
        self.Label8.setBounds(20,360,500,20)
        self.left_boundary_CPMG.setBounds(20,400,35,25)
        self.right_boundary_CPMG.setBounds(20,420,35,25)
        self.left_boundary_NOESY.setBounds(20,400,35,25)
        self.right_boundary_NOESY.setBounds(20,420,35,25)
        self.Label9.setBounds(60,400,300,20)
        self.Label10.setBounds(60,420,300,20)

        self.Checkbox1.setBounds(5,460,500,25)	
        self.StartButton.setBounds(400,500,150,30)
        self.setvisibility()



        #Group buttons: 

        grp = ButtonGroup()
        grp.add(self.DimensionButton1)
        grp.add(self.DimensionButton2) 

        Typegrp = ButtonGroup()
        Typegrp.add(self.TypeButton1)
        Typegrp.add(self.TypeButton2) 

        Processgrp = ButtonGroup()
        Processgrp.add(self.ProcessButton1)
        Processgrp.add(self.ProcessButton2)
        Processgrp.add(self.ProcessButton3)  

        self.frame = JFrame('Welcome to the automatic NMR Data processor') # create window with title
        self.frame.setSize(1000, 600) # set window size x, y
        self.frame.setLocation(400,400)
        self.frame.setLayout(None) # layout manager for horizontal alignment

        self.frame.add(self.Label0)
        self.frame.add(self.Label1)
        self.frame.add(self.Input)
        self.frame.add(self.Label2)
        self.frame.add(self.Label3)
        self.frame.add(self.Label4)
        self.frame.add(self.Label5)
        self.frame.add(self.DimensionButton1)
        self.frame.add(self.DimensionButton2)
        self.frame.add(self.TypeButton1)
        self.frame.add(self.TypeButton2)
        self.frame.add(self.StartButton)
        self.frame.add(self.Checkbox1)
        self.frame.add(self.ProcessButton1)
        self.frame.add(self.ProcessButton2)
        self.frame.add(self.ProcessButton3)
        self.frame.add(self.Label6)
        self.frame.add(self.Label7)
        self.frame.add(self.Label8)
        self.frame.add(self.Label9)
        self.frame.add(self.Label10)
        self.frame.add(self.left_boundary_CPMG)
        self.frame.add(self.right_boundary_CPMG)
        self.frame.add(self.left_boundary_NOESY)
        self.frame.add(self.right_boundary_NOESY)
        self.frame.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE)
        self.frame.setVisible(True)
if __name__=="__main__":
    MainGUI()