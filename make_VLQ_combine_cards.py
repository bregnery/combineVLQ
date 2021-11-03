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
import CombineHarvester.CombineTools.systematics.Hhh as HhhSysts
import ROOT as r
import glob
import os

# Create a combine harvester instance and set aux dir
cb = ch.CombineHarvester()
auxiliaries  = os.environ['CMSSW_BASE'] + '/src/combineVLQ/auxiliaries/'
aux_shapes   = auxiliaries +'shapes/'

# List the Analysis channels
chns = ['TPrimeTprime']

'''
chns = ['et', 'mt', 'tt']
input_folders = {
  'et' : 'Imperial',
  'mt' : 'Imperial',
  'tt' : 'Italians',
}

'''
# dictionary for the backgrounds
bkg_procs = ['DataDriven-Multijet', 'WJets', 'ZJets']

sig_procs = ['TPrimeTPrime']

'''
cats = {
  'et_8TeV' : [
    (0, 'eleTau_2jet0tag'), 
    (1, 'eleTau_2jet1tag'),
    (2, 'eleTau_2jet2tag')
  ],
  'mt_8TeV' : [
    (0, 'muTau_2jet0tag'), 
    (1, 'muTau_2jet1tag'),
    (2, 'muTau_2jet2tag')
  ],
  'tt_8TeV' : [
    (0, 'tauTau_2jet0tag'), 
    (1, 'tauTau_2jet1tag'),
    (2, 'tauTau_2jet2tag')
  ]
}

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

'''
print '>> Adding systematic uncertainties...'
HhhSysts.AddSystematics_hhh_et_mt(cb)
HhhSysts.AddSystematics_hhh_tt(cb)

print '>> Extracting histograms from input root files...'
for chn in chns:
    file = aux_shapes + input_folders[chn] + "/htt_" + chn + ".inputs-Hhh-8TeV.root" 
    cb.cp().channel([chn]).era(['8TeV']).backgrounds().ExtractShapes(
        file, '$BIN/$PROCESS', '$BIN/$PROCESS_$SYSTEMATIC')
    cb.cp().channel([chn]).era(['8TeV']).signals().ExtractShapes(
        file, '$BIN/$PROCESS$MASS', '$BIN/$PROCESS$MASS_$SYSTEMATIC')

print '>> Merging bin errors and generating bbb uncertainties...'
bbb = ch.BinByBinFactory()
bbb.SetAddThreshold(0.1).SetMergeThreshold(0.5).SetFixNorm(True)

cb_et = cb.cp().channel(['et'])
bbb.MergeAndAdd(cb_et.cp().era(['8TeV']).bin_id([0, 1, 2]).process(['QCD','W','ZL','ZJ','VV','ZTT','TT']), cb)
cb_mt = cb.cp().channel(['mt'])
bbb.MergeAndAdd(cb_mt.cp().era(['8TeV']).bin_id([0, 1, 2]).process(['QCD','W','ZL','ZJ','VV','ZTT','TT']), cb)
cb_tt = cb.cp().channel(['tt'])
bbb.MergeAndAdd(cb_tt.cp().era(['8TeV']).bin_id([0, 1, 2]).process(['QCD','W','ZLL','VV','ZTT','TT']), cb)
'''

print '>> Setting standardised bin names...'
ch.SetStandardBinNames(cb)

writer = ch.CardWriter('LIMITS/$TAG/$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt',
                       'LIMITS/$TAG/common/$ANALYSIS_$CHANNEL.input.root')
#writer.SetVerbosity(1)
writer.WriteCards('cmb', cb)
for chn in chns: writer.WriteCards(chn,cb.cp().channel([chn]))

print '>> Done!'
