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

# the lower and upper bounds on the parameter of interest
rmin = -10
rmax = 10

# Run asymptotic limits on the workspace created from 
# Loop over all the directories containing the cards
for year in years :
    for signal in signals :
        for mass in masses :
            dirPath = "LIMITS/" + signal + "_" + year + "/" + mass

            # Get the name of the data card to run impacts on
            mergedCardName = "Merged_MR_" + signal + "_" + mass + ".txt"

            # Perform an intital fit for the signal strength and its uncertainty
            impactStr = "combineTool.py -M Impacts -d " + dirPath + "/workspace_Merged_MR_" + signal + ".root -m " + mass + " --rMin " + str(rmin) + " --rMax " + str(rmax) + " --robustFit 1 --doInitialFit"
            print("Running nuisance parameter impacts for signal: " + year + " " + signal + " " + mass)
            os.system(impactStr)

            # Run impacts for all of the nuisance parameters
            impactStr = "combineTool.py -M Impacts -d " + dirPath + "/workspace_Merged_MR_" + signal + ".root -m " + mass + " --rMin " + str(rmin) + " --rMax " + str(rmax) + " --robustFit 1 --doFits"
            os.system(impactStr)

            # Collect the impacts and put them in a json file
            impactJsonStr = "combine -M Impacts -d " + dirPath + "/workspace_Merged_MR_" + signal + ".root -m " + mass + " --rMin " + str(rmin) + " --rMax " + str(rmax) + " --robustFit 1 --output impacts_Merged_MR_" + signal + ".json"
            os.system(impactJsonStr)

        # Plot the impacts
        plotImpactsStr = "plotImpacts.py -i impacts_Merged_MR_" + signal + ".json" + " -o impacts_Merged_MR_" + signal + "_" + year

# Collect the limits into a json file
#collectStr = "combineTool.py -M CollectLimits *.AsymptoticLimits.* --use-dirs -o limits.json"
#os.system(collectStr)
