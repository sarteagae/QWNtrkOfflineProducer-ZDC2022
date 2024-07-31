import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras
from Configuration.AlCa.autoCond import autoCond
from Configuration.AlCa.GlobalTag import GlobalTag
import os
import sys

#runNumber = '345574'
runNumber = '373100'
if len(sys.argv) > 2:
	runNumber = sys.argv[2]

#---------------
# My definitions
#---------------

sourceTag = "HcalTBSource"         # for global runs
rawTag    = cms.InputTag('source')
#GT        = "80X_dataRun2_v2"
#GT        = "130X_dataRun3_Prompt_v3"

#infile = 'file: /afs/cern.ch/user/s/sarteaga/for_zdc_work_P5files/CMSSW_10_6_4/src/OfflineProducer/QWNtrkOfflineProducer-ZDC2022/run2021/69a0867a-b1c4-44e3-b1c7-b2a43f5fd442.root'
infile    = 'file:/eos/cms/store/group/dpg_hcal/comm_hcal/USC/run'+runNumber+'/USC_'+runNumber+'.root'
#Saray
#infile    = 'file:/eos/cms/store/group/dpg_hcal/comm_hcal/ZDC/USC/run'+runNumber+'/USC_'+runNumber+'.root'


#-----------------------------------
# Standard CMSSW Imports/Definitions
#-----------------------------------
process = cms.Process('MyTree')


process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = autoCond['run2_data']
#process.GlobalTag.globaltag = GT

#----------
process.es_prefer = cms.ESPrefer('HcalTextCalibrations', 'es_ascii')
process.es_ascii = cms.ESSource(
    'HcalTextCalibrations',
    input = cms.VPSet(
        cms.PSet(
#Saray
            object = cms.string('ElectronicsMap'),
	    #file = cms.FileInPath("OfflineProducer/QWNtrkOfflineProducer-ZDC2022/run2021/emap_tunel_both_numer.txt")
            #file = cms.FileInPath("OfflineProducer/QWNtrkOfflineProducer-ZDC2022/run2021/emap_all_tunel.txt")
	   #file = cms.FileInPath("OfflineProducer/QWNtrkOfflineProducer-ZDC2022/run2021/zdc_emap_and_TPchannels.txt") # basically final emap
	    file = cms.FileInPath("OfflineProducer/QWNtrkOfflineProducer-ZDC2022/run2021/emap_USC_1_Intev.txt") #emap sep9 after re-arranging fibers in USC 
	    # file = cms.FileInPath("OfflineProducer/QWNtrkOfflineProducer-ZDC2022/run2021/ZDC_emap_2023.txt")
	     #file = cms.FileInPath("OfflineProducer/QWNtrkOfflineProducer-ZDC2022/run2021/emap_sep_13.txt")
	    #file = cms.FileInPath("OfflineProducer/QWNtrkOfflineProducer-ZDC2022/run2021/ZDC_intervention_2_emap.txt")	   
            #  file = cms.FileInPath("OfflineProducer/QWNtrkOfflineProducer-ZDC2022/run2021/emap_temporal_42channels_tunel.txt")
            #file = cms.FileInPath("OfflineProducer/QWNtrkOfflineProducer-ZDC2022/run2021/emap_2023_newZDC_v4.txt")
           #file = cms.FileInPath("OfflineProducer/QWNtrkOfflineProducer-ZDC2022/run2021/ZDC_emap_proposal.txt") #emap before tunnel intervention
		)
        )
    )
#process.es_prefer = cms.ESPrefer('HcalTextCalibrations', 'es_ascii')

#-----------
# Log output
#-----------
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = ''
process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
    SkipEvent = cms.untracked.vstring('ProductNotFound')
    )

#Saray
#process.MessageLogger = cms.Service(
#    "MessageLogger",
#    destinations = cms.untracked.vstring(
#        'detailedInfo',
#         'critical'
#         ),
#    detailedInfo = cms.untracked.PSet(
#        threshold = cms.untracked.string('DEBUG')
#         ),
#    debugModules = cms.untracked.vstring(
#        'hcalDigis',
#        'zdcdigis' 
#        )
#    )



#-----------------
# Files to process
#-----------------
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
    )

process.source = cms.Source(
    sourceTag,
    fileNames = cms.untracked.vstring(infile),
    firstLuminosityBlockForEachRun = cms.untracked.VLuminosityBlockID(*[cms.LuminosityBlockID(0,345574)])
    )

# ZDC info
process.load('QWZDC2018Producer_cfi')
process.load('ZDC2018Pedestal_cfg')
process.zdcdigi.SOI = cms.untracked.int32(4)

#-----------------------------------------
# CMSSW/Hcal Related Module import
#-----------------------------------------
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load("EventFilter.HcalRawToDigi.HcalRawToDigi_cfi")


#set digi and analyzer
process.hcalDigis.InputLabel = rawTag
#process.hcalDigis.saveQIE10DataNSamples = cms.untracked.vint32(6, 10)
#process.hcalDigis.saveQIE10DataTags = cms.untracked.vstring( "UNUSED6", "UNUSED10" )

#process.hcalDigis.saveQIE10DataNSamples = cms.untracked.vint32(6)
#process.hcalDigis.saveQIE10DataTags = cms.untracked.vstring( "UNUSED6" )



process.zdcana = cms.EDAnalyzer('QWZDC2018Analyzer',
		srcADC = cms.untracked.InputTag('zdcdigi', 'ADC'),
		srcfC = cms.untracked.InputTag('zdcdigi', 'regularfC'),
		srcDetId = cms.untracked.InputTag('zdcdigi', 'DetId'),
		srcCapId = cms.untracked.InputTag('zdcdigi', 'CapId'),
		srcHigh = cms.untracked.InputTag('zdcdigi', 'chargeHigh'),
		srcLow = cms.untracked.InputTag('zdcdigi', 'chargeLow'),
		srcSum = cms.untracked.InputTag('zdcdigi', 'chargeSum'),
		Norm = cms.untracked.bool(False),
		bTree = cms.untracked.bool(True)
		)

process.zdcADCFilter = cms.EDFilter('QWZDC2018ADCFilter',
		srcDetId = cms.untracked.InputTag('zdcdigi', 'DetId'),
		srcCapId = cms.untracked.InputTag('zdcdigi', 'CapId'),
		srcADC = cms.untracked.InputTag('zdcdigi', 'ADC'),
		)

process.TFileService = cms.Service("TFileService",
		fileName = cms.string('zdc_'+runNumber+'.root')
		)


process.digiPath = cms.Path(
    process.hcalDigis *
    process.zdcdigi * 
    process.zdcana
)

process.output = cms.OutputModule(
		'PoolOutputModule',
		outputCommands = cms.untracked.vstring("drop *",
			"keep *_*_*_MyTree"
			),
		SelectEvents = cms.untracked.PSet(
			SelectEvents = cms.vstring('digiPath')
			),
		fileName = cms.untracked.string('digis_USC'+runNumber+'.root')
		)

process.outpath = cms.EndPath(process.output)

