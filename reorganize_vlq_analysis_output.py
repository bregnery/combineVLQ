#!/usr/bin/env python
#=========================================================================================
# make_VLQ_combine_cards.py --------------------------------------------------------------
#-----------------------------------------------------------------------------------------
# Author(s): Brendan Regnery -------------------------------------------------------------
#-----------------------------------------------------------------------------------------
# This reorganizes the systematic shapes from various root files for proper use with the -
#   the combine harvester ----------------------------------------------------------------
#-----------------------------------------------------------------------------------------

# modules
import ROOT as root
import os

# User input variables
dirPath = "/afs/cern.ch/work/b/bregnery/public/VLQ/combineVLQ/CMSSW_10_2_13/src/combineVLQ/auxiliaries/shapes/TPrimeTPrime_2017/"

# The files  
print("Get all the root files for the signal samples")
files = os.listdir(dirPath)

# Create a dictionary with space for all of the files
fileDict = {}
i = 0
for file in files:
    # Store root file, with process as the key
    if not ".root" in file: continue
    beginIndex = len("HT_histograms_")
    endIndex = file.find(".root")
    fileDict[file[beginIndex:endIndex]] = dirPath + file 
    i += 1
    print(file)
    #if i > 4: break

# Make a new set of files divided by the signal regions
regions = open('Region_Names.txt').read().splitlines() 
newDirPath = dirPath + "reorganized/"
newFilesDict = {}
for region in regions:
    newFilesDict[region+".root"] = root.TFile(newDirPath + region + ".root", "RECREATE") 

# Access the histograms in each file
for process, tfileName in fileDict.items():
    j = 0
    print(process)
    tfile = root.TFile.Open(tfileName)
    tkeys = root.TIter(tfile.GetListOfKeys() )
    for ikey in tkeys:
        # get the bin name
        histRegion = str(ikey.GetName())[0:10]

        # Make sure that we are using the signal regions
        if histRegion in regions:
            # the histogram from the VLQ analysis
            # histogram has bin name and then HT or systematic
            hist = tfile.Get(ikey.GetName())

            # Get the observed in HT in each signal region
            if len(ikey.GetName()) == 13:
                hist.SetName(histRegion + "/" + process )

            # Get the systematics in each signal region
            else: 
                if "Up" in str(ikey.GetName() )[-2:] :
                    endIndex = str(ikey.GetName() ).find("Up")
                    suffix = "Up"
                elif "Down" in str(ikey.GetName() )[-4:] :
                    endIndex = str(ikey.GetName() ).find("Down")
                    suffix = "Down"
                else:
                    print("There's a fucking problem Brendan " + str(ikey.GetName() ) + " God, you forgot this, jez" )
                systematic =  str(ikey.GetName() )[14:endIndex-1]
                hist.SetName(histRegion + "/" + process + "_" + systematic + suffix)
            newFilesDict[histRegion+".root"].WriteObject(hist, hist.GetName() )
                
        j+=1
        #if j > 4: break
    del tkeys
    tfile.Close()
# print(fileDict)


