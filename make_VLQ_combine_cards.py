#!/usr/bin/env python
#=========================================================================================
# make_VLQ_combine_cards.py --------------------------------------------------------------
#-----------------------------------------------------------------------------------------
# Author(s): Abhishek Das, Brendan Regnery -----------------------------------------------
#-----------------------------------------------------------------------------------------
# This uses the combine harvester to make the Pair Produced VLQ All Hadronic Combine Cards
# It is based off of the Hhh example included in the combine harvester. ------------------
#-----------------------------------------------------------------------------------------

# Import necessary tools
import CombineHarvester.CombineTools.ch as ch
import systematics.vlq_systematics as vlqSysts
import ROOT as r
import glob
import os
import ROOT as root

# Create a combine harvester instance and set aux dir
cb = ch.CombineHarvester()
#cb.SetVerbosity(2)
auxiliaries  = os.environ['CMSSW_BASE'] + '/src/combineVLQ/auxiliaries/'
#aux_shapes   = auxiliaries +'shapes_intermediate/'
aux_shapes   = auxiliaries +'shapes/'

# List the Analysis channels
testing = True
if testing == True : 
    chns = ['TPrimeTPrime_2017']
    sig_procs = ['TPrimeTPrime_M-']
else :
    chns = ['TPrimeTPrime_2016', 'TPrimeTPrime_2017', 'TPrimeTPrime_2018'
            'BPrimeBPrime_2016', 'BPrimeBPrime_2017', 'BPrimeBPrime_2018']
    sig_procs = ['TPrimeTPrime']

# dictionary for the backgrounds
#bkg_procs = ['DataDriven-Multijet', 'WJets', 'ZJets', 'ttWJets', 'ttWW', 'ttWZ', 'ttZJets', 'ttZZ', 'ttbar']
bkg_procs = ['DD-Multijet', 'WJets', 'ZJets', 'ttWJets', 'ttWW', 'ttWZ', 'ttZJets', 'ttZZ', 'ttbar']
#possible_bkg_procs = ['DD-Multijet', 'WJets', 'ZJets', 'ttWJets', 'ttWW', 'ttWZ', 'ttZJets', 'ttZZ', 'ttbar']

'''
# Now we need to look at each signal region and the processes that it contains
# Path to the histograms 
#dirPath = "/afs/cern.ch/work/b/bregnery/public/VLQ/combineVLQ/CMSSW_10_2_13/src/combineVLQ/auxiliaries/shapes_intermediate/TPrimeTPrime_2017/"
dirPath = "/afs/cern.ch/work/b/bregnery/public/VLQ/combineVLQ/CMSSW_10_2_13/src/combineVLQ/auxiliaries/shapes/TPrimeTPrime_2017/"
files = os.listdir(dirPath)

# Create a dictionary with space for all of the files
fileDict = {}
i = 0
for file in files:
    # Store root file, with region as the key
    if not ".root" in file: continue
    endIndex = file.find(".root")
    fileDict[file[:endIndex]] = dirPath + file 
    i += 1

# Find the backgrounds for each signal region
regions_bkgs_dict = {}
for region, tfileName in fileDict.items():
    regions_bkgs_dict[region] = []
    tfile = root.TFile.Open(tfileName)
    tkeys = root.TIter(tfile.GetDirectory(region).GetListOfKeys() )
    #print("file name: " + region)
    for ikey in tkeys:
        if str(ikey.GetName() ) == "WJets_TopMistagSFUp":
            print("region: "+ region + " name: " + str(ikey.GetName() ) )

        for bkg in possible_bkg_procs :
            # see if the bkg is present
            if bkg == str(ikey.GetName()) : 
                regions_bkgs_dict[region].append(bkg)
                #print("bkg: " + bkg + str(ikey.GetName() ) )
    # put background process in the dictionary
    tfile.Close()
    #quit()

#print(regions_bkgs_dict)
'''

regions = open('Region_Names.txt').read().splitlines() 

iCat = 0
cats = []
for region in regions:
    cats.append( (iCat, region) )
    iCat += 1

masses = ch.ValsFromRange('1000:1800|100')

print '>> Creating processes and observations...'

for chn in chns:
    # Analysis and Era strings are left blank to save space in the cards
    cb.AddObservations(  ['*'],  [''], [''], [chn],                 cats ) #cats[chn+"_8TeV"]      )
    cb.AddProcesses(     ['*'],  [''], [''], [chn], bkg_procs,      cats, False ) #cats[chn+"_8TeV"], False  )
    cb.AddProcesses(     masses, [''], [''], [chn], sig_procs,      cats, True ) #cats[chn+"_8TeV"], True   )

print '>> Adding systematic uncertainties...'
vlqSysts.AddSystematics_vlq_had(cb)

print '>> Extracting histograms from input root files...'
for chn in chns:
    file = aux_shapes + chn + "/2017_proc_obs_systematics.root" 
    cb.cp().channel([chn]).era(['']).backgrounds().ExtractShapes(
        file, '$BIN/$PROCESS', '$BIN/$PROCESS_$SYSTEMATIC')
    cb.cp().channel([chn]).era(['']).signals().ExtractShapes(
        file, '$BIN/$PROCESS$MASS', '$BIN/$PROCESS$MASS_$SYSTEMATIC')
'''

for chn in chns:
    for region in regions:
        #file = aux_shapes + chn + "/" + region + ".root" 
        file = aux_shapes + chn + "/2017_proc_obs_systematics.root" 
        cb.cp().channel([chn]).era(['']).backgrounds().ExtractShapes(
            file, region + '/$PROCESS', region + '/$PROCESS_$SYSTEMATIC')
        cb.cp().channel([chn]).era(['']).signals().ExtractShapes(
            file, region + '/$PROCESS$MASS', region + '/$PROCESS$MASS_$SYSTEMATIC')
for chn in chns:
    for region in regions:
        file = aux_shapes + chn + "/" + region + ".root" 

        cb.cp().channel([chn]).era().backgrounds().ExtractShapes(
            file, region + '/' + '$PROCESS', region + '/' + '$PROCESS_$SYSTEMATIC')
        cb.cp().channel([chn]).era().signals().ExtractShapes(
            file, region + '/' + '$PROCESS$MASS', region + '/' + '$PROCESS$MASS_$SYSTEMATIC')

        cb.cp().channel([chn]).era().backgrounds().ExtractShapes(
            file, '$BIN/$PROCESS', '$BIN/$PROCESS_$SYSTEMATIC')
        cb.cp().channel([chn]).era().signals().ExtractShapes(
            file, '$BIN/$PROCESS$MASS', '$BIN/$PROCESS$MASS_$SYSTEMATIC')
'''
         #for bkg in bkg_procs :
         #   if bkg == "DataDriven-Multijet": bkg_str = "DD-Multijet"
         #   else: bkg_str = bkg
#        cb.cp().channel([chn]).era(['']).backgrounds().ExtractShapes(
#            aux_shapes + chn + "/HT_histograms_$PROCESS.root",
#            region + "_HT", region + '_HT' + '_$SYSTEMATIC')
#        for sig in sig_procs :
#            cb.cp().channel([chn]).era(['']).signals().ExtractShapes(
#                aux_shapes + chn + "/HT_histograms_" + sig + "_M-" + '$MASS' + ".root", 
#                region + '_HT', region + '_HT' + '_$SYSTEMATIC')

print '>> Merging bin errors and generating bbb uncertainties...'
bbb = ch.BinByBinFactory()
bbb.SetAddThreshold(0.1).SetMergeThreshold(0.5).SetFixNorm(True)

'''
cb_et = cb.cp().channel(['et'])
bbb.MergeAndAdd(cb_et.cp().era(['8TeV']).bin_id([0, 1, 2]).process(['QCD','W','ZL','ZJ','VV','ZTT','TT']), cb)
cb_mt = cb.cp().channel(['mt'])
bbb.MergeAndAdd(cb_mt.cp().era(['8TeV']).bin_id([0, 1, 2]).process(['QCD','W','ZL','ZJ','VV','ZTT','TT']), cb)
cb_tt = cb.cp().channel(['tt'])
bbb.MergeAndAdd(cb_tt.cp().era(['8TeV']).bin_id([0, 1, 2]).process(['QCD','W','ZLL','VV','ZTT','TT']), cb)
'''

print '>> Setting standardised bin names...'
ch.SetStandardBinNames(cb)

writer = ch.CardWriter('LIMITS/$TAG/$MASS/$CHANNEL_$BINID.txt',
                       'LIMITS/$TAG/common/$CHANNEL.input.root')
#writer.SetVerbosity(1)
writer.WriteCards('cmb', cb)
for chn in chns: writer.WriteCards(chn,cb.cp().channel([chn]))

print '>> Done!'
