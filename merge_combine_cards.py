#!/usr/bin/env python
#=========================================================================================
# merge_combine_cards.py -----------------------------------------------------------------
#-----------------------------------------------------------------------------------------
# Author(s): Abhishek Das, Brendan Regnery -----------------------------------------------
#-----------------------------------------------------------------------------------------
# Merge signal regions together into a single combine card and makes a corresponding -----
#   RooWorkspace -------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------

import os, sys
import ROOT as root

# list of the regions to be combined
regions = ["VLQ_1t0W0Z0H0b", "VLQ_0t1W0Z0H0b", "VLQ_0t0W1Z0H0b", "VLQ_0t0W0Z1H0b", "VLQ_0t0W0Z0H1b", "VLQ_0t0W0Z0H0b"] # For now just the validation regions

# Years, Signals, and masses for the combination
years = ["2017"]
signals = ["TPrimeTPrime"]
masses = ["1000", "1100", "1200", "1300", "1400", "1500", "1600", "1700", "1800"]

# Combine the cards
# Loop over all the directories containing the cards
for year in years :
    for signal in signals :
        for mass in masses :
            dirPath = "LIMITS/" + signal + "_" + year + "/" + mass

            # Make a string used for issuing the combine cards command
            mergeCardsStr = "combineCards.py "
            mergedCardName = "Merged_MR_" + signal + "_" + mass + ".txt"

            # Loop over the cards that you want to add together
            for region in regions :
                mergeCardsStr += " " + dirPath + "/" + region + ".txt"

            # Issue the combination command
            mergeCardsStr += " &> " + dirPath + "/" + mergedCardName

            print("Merging data cards for " + mass)
            os.system(mergeCardsStr)

            # Make a corresponding RooWorkspace
            workspaceStr = "text2workspace.py " + dirPath + "/" + mergedCardName + " -m " + mass + " -o " + dirPath + "/workspace_Merged_MR_" + signal + ".root"
            print("Making the corresponding RooWorkspace")
            os.system(workspaceStr)
