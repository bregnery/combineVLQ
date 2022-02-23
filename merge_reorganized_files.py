#!/usr/bin/env python
#=========================================================================================
# make_VLQ_combine_cards.py --------------------------------------------------------------
#-----------------------------------------------------------------------------------------
# Author(s): Brendan Regnery, Sam Abbott -------------------------------------------------
#-----------------------------------------------------------------------------------------
# This reorganizes the systematic shapes from various root files for proper use with the -
#   the combine harvester ----------------------------------------------------------------
#-----------------------------------------------------------------------------------------

# modules
import ROOT as root
import os

# Now we need to look at each signal region and the processes that it contains
# Path to the histograms 
dirPath = "/afs/cern.ch/work/b/bregnery/public/VLQ/combineVLQ/CMSSW_10_2_13/src/combineVLQ/auxiliaries/shapes_intermediate/TPrimeTPrime_2017/"
newDirPath = "/afs/cern.ch/work/b/bregnery/public/VLQ/combineVLQ/CMSSW_10_2_13/src/combineVLQ/auxiliaries/shapes/TPrimeTPrime_2017/"
newFileName = "2017_proc_obs_systematics.root"
files = os.listdir(dirPath)

# Create a dictionary with space for all of the files
newFile = root.TFile(newDirPath + newFileName, "RECREATE") 
fileDict = {}
i = 0
for file in files:
    # Store root file, with region as the key
    if not ".root" in file: continue
    endIndex = file.find(".root")
    fileDict[file[:endIndex]] = dirPath + file 
    i += 1

# Find the backgrounds for each signal region
for region, tfileName in fileDict.items():
    tfile = root.TFile.Open(tfileName)
    #newFile.AddDirectory(tfile.GetDirectory(region) )
    newFile.WriteObject(tfile.GetDirectory(region), region)
    print("file name: " + region)
    # put background process in the dictionary
    tfile.Close()
    #quit()

newFile.Close()
