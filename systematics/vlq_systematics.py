import CombineHarvester.CombineTools.ch as ch

def AddSystematics_vlq_had(cb):

  # Access the combine harvester object for the card creation
  src = cb.cp()
  
  # This regular expression will match any Higgs signal process.
  # It's useful for catching all these processes when we don't know
  # which of them will be signal or background
  # higgs_rgx = '^(qq|gg|[WZV])H.*$'

  signal = src.cp().signals().process_set()

  # Normalization Uncertainties
  src.cp().process(signal + ['WJets','ZJets']).AddSyst(
      cb, "lumi", "lnN", ch.SystMap()(1.025))

  src.cp().process(['ttZJets', 'ttWZ', 'ttWW']).AddSyst(
      cb, "topQuarkCrossSection", "lnN", ch.SystMap()(1.5))

  src.cp().process(['']).AddSyst(
      cb, "DiBosonCrossSection", "lnN", ch.SystMap()(1.15))

  src.cp().process(['WJets']).AddSyst(
      cb, "WJetsCrossSection", "lnN", ch.SystMap()(1.15))

  src.cp().process(['ZJets']).AddSyst(
      cb, "ZJetsCrossSection", "lnN", ch.SystMap()(1.15))

  # Shape Uncertainties
  src.cp().process(signal+['WJets','ZJets']).AddSyst(
      cb, "pileupReweight", "shape", ch.SystMap()(1.00))

  src.cp().process(signal+['WJets','ZJets']).AddSyst(
      cb, "jer", "shape", ch.SystMap()(1.00))

  # BEST Uncertainties
  src.cp().process(signal+['WJets','ZJets']).AddSyst(
      cb, "HiggsTagSF", "shape", ch.SystMap()(1.00))

  src.cp().process(signal+['WJets','ZJets']).AddSyst(
      cb, "HiggsMistagSF", "shape", ch.SystMap()(1.00))

  src.cp().process(signal+['WJets','ZJets']).AddSyst(
      cb, "topTagSF", "shape", ch.SystMap()(1.00))

  src.cp().process(signal+['WJets','ZJets']).AddSyst(
      cb, "TopMistagSF", "shape", ch.SystMap()(1.00))
 
  src.cp().process(signal+['WJets','ZJets']).AddSyst(
      cb, "WTagSF", "shape", ch.SystMap()(1.00))

  src.cp().process(signal+['WJets','ZJets']).AddSyst(
      cb, "WMistagSF", "shape", ch.SystMap()(1.00))

  src.cp().process(signal+['WJets','ZJets']).AddSyst(
      cb, "ZTagSF", "shape", ch.SystMap()(1.00))

  src.cp().process(signal+['WJets','ZJets']).AddSyst(
      cb, "ZMistagSF", "shape", ch.SystMap()(1.00))

  src.cp().process(signal+['WJets','ZJets']).AddSyst(
      cb, "BTagSF", "shape", ch.SystMap()(1.00))

  src.cp().process(signal+['WJets','ZJets']).AddSyst(
      cb, "BMistagSF", "shape", ch.SystMap()(1.00))

  src.cp().process(signal+['WJets','ZJets']).AddSyst(
      cb, "QCDTagSF", "shape", ch.SystMap()(1.00))

  src.cp().process(signal+['WJets','ZJets']).AddSyst(
      cb, "QCDMistagSF", "shape", ch.SystMap()(1.00))

  # Background Estimate Uncertainties
  src.cp().process(['DataDriven-Multijet']).AddSyst(
      cb, "DataDrivenQCD", "shape", ch.SystMap()(1.00))

  src.cp().process(['DataDriven-Multijet']).AddSyst(
      cb, "DataDrivenHiggs", "shape", ch.SystMap()(1.00))

  src.cp().process(['DataDriven-Multijet']).AddSyst(
      cb, "DataDriventop", "shape", ch.SystMap()(1.00))

  src.cp().process(['DataDriven-Multijet']).AddSyst(
      cb, "DataDrivenW", "shape", ch.SystMap()(1.00))

  src.cp().process(['DataDriven-Multijet']).AddSyst(
      cb, "DataDrivenZ", "shape", ch.SystMap()(1.00))

  src.cp().process(['DataDriven-Multijet']).AddSyst(
      cb, "DataDrivenB", "shape", ch.SystMap()(1.00))




