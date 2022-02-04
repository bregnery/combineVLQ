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

# Create a combine harvester instance and set aux dir
cb = ch.CombineHarvester()
auxiliaries  = os.environ['CMSSW_BASE'] + '/src/combineVLQ/auxiliaries/'
aux_shapes   = auxiliaries +'shapes/'

# List the Analysis channels
testing = True
if testing == True : 
    chns = ['TPrimeTPrime_2017']
    sig_procs = ['TPrimeTPrime']
else :
    chns = ['TPrimeTPrime_2016', 'TPrimeTPrime_2017', 'TPrimeTPrime_2018'
            'BPrimeBPrime_2016', 'BPrimeBPrime_2017', 'BPrimeBPrime_2018']
    sig_procs = ['TPrimeTPrime']

# dictionary for the backgrounds
bkg_procs = ['DataDriven-Multijet', 'WJets', 'ZJets', 'ttWJets', 'ttWW', 'ttWZ', 'ttZJets', 'ttZJets', 'ttZZ', 'ttbar']


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
    for region in regions:
#    file = aux_shapes + chn + "/HT_histograms_" + chn + ".root" 
#    cb.cp().channel([chn]).era().backgrounds().ExtractShapes(
#        file, '$BIN/$PROCESS', '$BIN/$PROCESS_$SYSTEMATIC')
        for bkg in bkg_procs :
            if bkg == "DataDriven-Multijet": bkg_str = "DD-Multijet"
            else: bkg_str = bkg
            cb.cp().channel([chn]).era(['']).backgrounds().ExtractShapes(
                aux_shapes + chn + "/HT_histograms_" + bkg_str + ".root",
                region + "_HT", region + '_HT' + '_$SYSTEMATIC')
        for sig in sig_procs :
            cb.cp().channel([chn]).era(['']).signals().ExtractShapes(
                aux_shapes + chn + "/HT_histograms_" + sig + "_M-" + '$MASS' + ".root", 
                region + '_HT', region + '_HT' + '_$SYSTEMATIC')

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