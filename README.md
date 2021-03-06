# combineVLQ
This repository works with the Higgs Combine Tool (or simply "Combine") to perform
the statistical analysis for the Full run 2 `T'T'` all hadronic search

## Dependencies

The version of Combine in this analysis uses `CMSSW_10_2_X`, which can be installed as follows

```
export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_2_13
cd CMSSW_10_2_13/src
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
cd $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v8.2.0
scramv1 b clean; scramv1 b # always make a clean build
```

The combine cards for this analysis are created with the recommended CombineHarvester, which is installed as followed

```
git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
scram b
```

## Instructions

First, we need to reorganize the output histograms containing the systematic uncertainties from the VLQ Analyzer. 
This is done with `reorganize_vlq_analysis_output.py`. The `dirPath` argument gives the path to the old files, 
`newDirPath` gives the path to the output file location, and `newFileName` gives the output file name.

```
python reorganize_vlq_analysis_output.py
```

The next step is to make the data cards for combine. At the moment, only TPrimeTPrime with branching ration 1:1:1 has 
been implemented. The documentation will change as more options are added.

```
python make_VLQ_combine_cards.py
```

Then, the data cards can be merged and made into RooWorkSpaces.

```
python merge_combine_cards.py
```

The merged cards can then be used for a number of studies:

### Asymptotic limits

To run asymptotic limits on the merged cards

```
python run_asymptotic_limits.py
```

And then make the Brazil plot

```
simple_Brasil_script.py
```


