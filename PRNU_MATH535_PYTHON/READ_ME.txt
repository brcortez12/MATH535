Note that the functions NoiseExtractFromImage and getFingerprint call other functions
in this folder, so be sure to write your code and save it in this folder,
otherwise your code will not run. Please only turn in the .py files
that you write.

The Current Folder you are working in should
include the following files:
Math535_Example.py
requirements.txt

src folder with the following files:
extraUtils.py
Filter.py
Functions.py
getFingerprint.py
maindir.py

Use requirements.txt to install the necessary packages for using this software.


To use NoiseExtractFromImage:
Pass an individual image name to the function to generate an estimate
of the PRNU
If passing a filename within a folder (not the current working directory),
separate the folders using the os.sep, which accounts for 
different file separators used in various operating systems
An example of how to use this is given on line 19 of Math535_Example.py

To use getFingerprint:
Pass a folder name to the function to generate an estimate of the PRNU
for this device 
If passing a folder name within a folder (not the current working 
directory), separate the folders using the os.path.join, which 
accounts for different file separators used in various operating systems
An example of how to use this is given on line 25 of example.m and an
example of how to write .mat is on line 27

An example of how to calculate correlation is on lines 34-35