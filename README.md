1.- In 2023, cmssw release CMSSW_10_6_4 was used

   $   cmsrel CMSSW_10_6_4 
   $   cd CMSSW_10_6_4/src
2.- create a folder OfflineProducer/QWNtrkOfflineProducer-ZDC2022  and clone this repository
   $   mkdir OfflineProducer
   $   cd OfflineProducer
   $   git clone https://github.com/sarteagae/ZDC_local_runs.git

3.-Main config file "recHitUSC_cfg.py" is located in run2021/ folder. To run it espcify the run number and path to the local run as well as the emap desired .

   $  cmsRun recHitUSC_cfg.py

4.- It will create a zdc_'runNumber'.root


