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

# User input variables
boomfile = "0t0W0Z0H0b.root"

# Create a dictionary with space for all of the files
tfile = root.TFile.Open(boomfile)
hist = tfile.Get("0t0W0Z0H0b/data_obs")
#tfile.cd("0t0W0Z0H0b")
print (hist.GetName() )


'''
# Make a new set of files divided by the signal regions
regions = open('Region_Names.txt').read().splitlines() 
newFilesDict = {}
for region in regions:
    newFilesDict[region+".root"] = root.TFile(newDirPath + region + ".root", "RECREATE") 
    newFilesDict[region+".root"].mkdir(region)

# Access the histograms in each file
nObjs = 0
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
                hist.SetName(process )

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
                hist.SetName(process + "_" + systematic + suffix)
            newFilesDict[histRegion+".root"].GetDirectory(histRegion).WriteObject(hist, hist.GetName() )
                
        j+=1
        nObjs+=1
        # Have to open and close the files to deal with memory issues
        if nObjs % 6000 == 0:
            for region in regions:
                newFilesDict[region+".root"].Close()
                newFilesDict[region+".root"] = root.TFile.Open(newDirPath + region + ".root", "UPDATE") 
        #if j > 4: break
    del tkeys
    tfile.Close()

# Close everything
for region in regions:
    newFilesDict[region+".root"].Close()
# print(fileDict)

'''
