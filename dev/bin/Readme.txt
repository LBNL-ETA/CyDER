09/06/2016 by T. Nouidui 

To Run the FMUChecker

**Get the FMUChecker from the repository**

On Unix machine,

run getFmuChecker.sh + version of FMUChecker to use

  ./getFmuChecker.sh 2.0.1

This will download the FMUChecker from the fmi-standard.org repository and 
copy the files which are necessary to run the checker in the correct folder.

On a Windows machine, you will need to 
- manually download the files from the repository (https://svn.fmi-standard.org/fmi/branches/public/Test_FMUs/FMI_1.0/Compliance-Checker/)
- unzip the folder,
- copy the executables (fmuChecker.linux64, fmuChecker.win64.exe) 
  to the top level of the fmuChecker folder.
  
PS: We currently restricted the unit test to Linux 64 and Windows 64 which are 
the most anticipated used platforms. This can be extended if needs be.

The unit test only needs the executables to be at the top level of the 
fmuChecker folder. 


**Run the unit test with Python**

run runUnitTest.py which is in the bin folder with

  python runUnitTest.py

Please note that runUnitTest.py call fmuChecker with
default settings. Consequently, running EnergyPlus exported as 
an FMU won't run.


**Run the unit test with ant**

source setDevelopment.sh in bin folder to set environment variable with

  source bin/setDevelopment.sh

run ant unitTest with

  ant unitTest

This will run the unit test which consists of testing FMUs which are in
the fmus folder.
The user needs to add any additional unit test to build.xml in the fmus folder.
