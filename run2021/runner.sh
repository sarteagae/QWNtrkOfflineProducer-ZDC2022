#!/bin/bash

for run_number in {374387..374411}; do
    
    cmsRun recHitUSC_cfg.py $run_number
done
