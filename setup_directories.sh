#!/bin/bash
#=========================================================================================
# setup_directories.sh -------------------------------------------------------------------
#=========================================================================================
# Author(s): Brendan Regnery -------------------------------------------------------------
#-----------------------------------------------------------------------------------------

# Make directories to store the input shape root files
mkdir auxiliaries/
mkdir auxiliaries/shapes/

# Create string arrays for looping through the various files
declare -a channelArray=('TPrimeTPrime_2016' 'TPrimeTPrime_2017' 'TPrimeTPrime_2018'
                         'BPrimeBPrime_2016' 'BPrimeBPrime_2017' 'BPrimeBPrime_2018')

declare -a TmassArray=('700' '800' '900' '1000' '1100' '1200' '1300' '1400' '1500' '1600' '1700')

#declare -a BmassArray=('700' '800' '900' '1000' '1100' '1200' '1300' '1400' '1500' '1600' '1700')

# Make directories to store the input shape root files
for chan in ${channelArray[@]}; do
    echo "auxiliaries/shape/$chan"
    if [[ $chan == *"TPrimeTPrime"* ]]; then
        for mass in ${TmassArray[@]}; do
            echo "auxiliaries/shape/$chan/$mass"
        done
    fi
done



