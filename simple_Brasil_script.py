#!/usr/bin/env python
#=========================================================================================
# simple_Brasil_script.py ----------------------------------------------------------------
#-----------------------------------------------------------------------------------------
# Author(s): Abhishek Das, Brendan Regnery -----------------------------------------------
#-----------------------------------------------------------------------------------------
# This makes a simple Brasil plot after the asymptotic limits have been calculated -------
#-----------------------------------------------------------------------------------------

import ROOT
from CombineHarvester.CombineTools.plotting import *
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

# Style and pads
ModTDRStyle()
canv = ROOT.TCanvas('limit', 'limit')
pads = OnePad()

# Get limit TGraphs as a dictionary
graphs = StandardLimitsFromJSONFile('limits_default.json')

# Create an empty TH1 from the first TGraph to serve as the pad axis and frame
axis = CreateAxisHist(graphs.values()[0])
axis.GetXaxis().SetTitle('m_{T} (GeV)')
axis.GetYaxis().SetTitle('95% CL limit on #mu')
pads[0].cd()
axis.Draw('axis')

# Create a legend in the top left
legend = PositionedLegend(0.3, 0.2, 3, 0.015)

# Set the standard green and yellow colors and draw
StyleLimitBand(graphs)
DrawLimitBand(pads[0], graphs, legend=legend)
legend.Draw()

# Re-draw the frame and tick marks
pads[0].RedrawAxis()
pads[0].GetFrame().Draw()

# Adjust the y-axis range such that the maximum graph value sits 25% below
# the top of the frame. Fix the minimum to zero.
FixBothRanges(pads[0], 0, 0, GetPadYMax(pads[0]), 0.25)

# Standard CMS logo
DrawCMSLogo(pads[0], 'CMS', 'Internal', 11, 0.045, 0.035, 1.2, '', 0.8)

canv.Print('.pdf')
canv.Print('.png')
