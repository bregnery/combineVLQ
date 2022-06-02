#!/usr/bin/env python
#=========================================================================================
# run_asymptotic_limits.py -----------------------------------------------------------------
#-----------------------------------------------------------------------------------------
# Author(s): Abhishek Das, Brendan Regnery -----------------------------------------------
#-----------------------------------------------------------------------------------------
# Merge signal regions together into a single combine card and makes a corresponding -----
#   RooWorkspace -------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------

import os, sys
import ROOT as root

# Years, Signals, and masses for the combination
years = ["2017"]
signals = ["TPrimeTPrime"]
masses = ["1000", "1100", "1200", "1300", "1400", "1500", "1600", "1700", "1800"]

# Run asymptotic limits on the workspace created from 
# Loop over all the directories containing the cards
for year in years :
    for signal in signals :
        for mass in masses :
            dirPath = "LIMITS/" + signal + "_" + year + "/" + mass

            # Get the name of the data card to run limits on
            mergedCardName = "Merged_MR_" + signal + "_" + mass + ".txt"

            # Run the asymptotic limits
            asymptoticLimStr = "combine -M AsymptoticLimits " + dirPath + "/workspace_Merged_MR_" + signal + ".root -m " + mass
            print("Running asymptotic limits for signal: " + year + " " + signal + " " + mass)
            os.system(asymptoticLimStr)

# Collect the limits into a json file
collectStr = "combineTool.py -M CollectLimits *.AsymptoticLimits.* --use-dirs -o limits.json"
os.system(collectStr)
