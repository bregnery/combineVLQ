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




