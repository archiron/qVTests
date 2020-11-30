#! /usr/bin/env python
#-*-coding: utf-8 -*-

import os,sys
import re
from time import sleep

sys.path.append('/afs/cern.ch/user/a/archiron/lbin/ChiLib')

#from networkFunctions import list_search_1
from datasetsqV import *

def screen_clear():
    # The screen clear function
    # for mac and linux(here, os.name is 'posix')
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        # for windows platfrom
        _ = os.system('cls')

def check_terminal_size(self):
    if (terminal_size()[0] < 150):  # too less cols
        print("not enough columns [%d]. Must be at least 150." % terminal_size()[0])
        exit()
    elif (terminal_size()[1] < 35):  # too less rows
        print("not enough rows [%d]. Must be at least 35." % terminal_size()[1])
        exit()
    else:
        print('terminal size OK.')

def terminal_size():
    import fcntl, termios, struct
    th, tw, hp, wp = struct.unpack('HHHH',
                                   fcntl.ioctl(0, termios.TIOCGWINSZ,
                                               struct.pack('HHHH', 0, 0, 0, 0)))
    return tw, th, hp, wp

def nbDatasets(self, release, a):
    if ( a == 'rel' ):
        tempReleaseList = sub_releases3(release, self.releasesList_1)  # extract the list of the root files for each release
        tempDatasetsList = sub_releases2(release, tempReleaseList)  # extract the datasets of the root files for the chosen release
        nb = len(tempDatasetsList)
    else: # a == 'ref'
        tempReleaseList = sub_releases3(release, self.referencesList_1)  # extract the list of the root files for each release
        tempDatasetsList = sub_releases2(release, tempReleaseList)  # extract the datasets of the root files for the chosen release
        nb = len(tempDatasetsList)
    return nb

def sub_releases(tab_files):
    i = 0
    temp = []
    for t in tab_files:
        tt = explode_item(t)
        temp.append(tt[1])
        i += 1
    temp = sorted(set(temp), reverse=True)
    return temp

def sub_releases2(release, tab_files):
    import re
    i = 0
    temp = []
    for t in tab_files:
        if ( re.search(release, t) ):
            tt = explode_item(t)
            temp.append(tt[0])
        i += 1
    temp = sorted(set(temp)) # , reverse=True
    return temp

def sub_releases3(release, tab_files):
    import re
    i = 0
    temp = []
    for t in tab_files:
        if ( re.search('__' + release + '-', t) ):
            temp.append(t)
        i += 1
    temp = sorted(set(temp)) # , reverse=True
    return temp

def explode_item(item):
    # initial file name : DQM_V0001_R000000001__RelValTTbar_13__CMSSW_7_4_0_pre8-PUpmx50ns_MCRUN2_74_V6_gs_pre7-v1__DQMIO.root
    # prefix in DQM_V0001_R000000001__ removed : RelValTTbar_13__CMSSW_7_4_0_pre8-PUpmx50ns_MCRUN2_74_V6_gs_pre7-v1__DQMIO.root
    # suffix in __DQMIO.root removed : RelVal
    # new prefix in RelVal removed : TTbar_13__CMSSW_7_4_0_pre8-PUpmx50ns_MCRUN2_74_V6_gs_pre7-v1
    # splitting with __ : TTbar_13 CMSSW_7_4_0_pre8-PUpmx50ns_MCRUN2_74_V6_gs_pre7-v1
    # splitting second term with - : TTbar_13 CMSSW_7_4_0_pre8 PUpmx50ns_MCRUN2_74_V6_gs_pre7-v1

    temp_item = item[22:] # DQM_V0001_R000000001__ removed
    temp_item = temp_item[:-12] # __DQMIO.root removed
    temp_item = temp_item[6:] # RelVal removed
    temp_item = temp_item.split('__')
    temp_item2 = temp_item[1].split('-', 1)
    temp_item = [ temp_item[0] ]
    for it in temp_item2:
        temp_item.append(it)

    return temp_item

def testZEE(tab):
    test = False
    for item in tab:
        if item == 'ZEE_14':
            test = 'True'
    return test

def rootFilesExtraction(self):
    # ROOT files extraction for selected datasets
    for i, dts in enumerate(self.datasets):
        #print('dataset : %s' % dts)
        tmp_rel = []
        tmp_ref = []
        tmp_rel.append(dts)
        tmp_ref.append(dts)
        for file in self.releasesList_3:
            #print(file)
            if re.search(dts, file):
                if re.search(self.release, file):
                    #print('rel ', file)
                    tmp_rel.append(str(file))

        for file in self.referencesList_3:
            #print(file)
            if re.search(dts, file):
                if re.search(self.reference, file):
                    #print('ref ', file)
                    tmp_ref.append(str(file))
        self.releasesList_4.append(tmp_rel)
        self.referencesList_4.append(tmp_ref)

def GlobalTagsExtraction(self):
    for elem in self.releasesList_5:
        gt_tmp = []
        for i in range(1, len(elem)):
            aa = explode_item(elem[i])
            gt_tmp.append(aa[2])
        gt_tmp = sorted(set(gt_tmp))
        gt_tmp.insert(0, elem[0])
        self.releasesGT.append(gt_tmp)

    for elem in self.referencesList_5:
        gt_tmp = []
        for i in range(1, len(elem)):
            aa = explode_item(elem[i])
            gt_tmp.append(aa[2])
        gt_tmp = sorted(set(gt_tmp))
        gt_tmp.insert(0, elem[0])
        self.referencesGT.append(gt_tmp)

def getFilesList(self, tab):
    tmp_list = []
    if self.validationChoice[1] != 'RECO' and self.validationChoice[1] != 'miniAOD': # PU or pmx
        if self.validationChoice[1] == 'pmx': # pmx
            #print('pmx')
            for elem in tab:
                tmp_elem = []
                tmp_elem.append(elem[0])
                for i in range(1, len(elem)):
                    if re.search(self.validationChoice[1], elem[i]) and not re.search('noPU', elem[i]): # noPU exclusion ! to be tested
                        tmp_elem.append(elem[i])
                tmp_list.append(tmp_elem)
        else: # PU
            #print('PU')
            for elem in tab:
                tmp_elem = []
                tmp_elem.append(elem[0])
                for i in range(1, len(elem)):
                    if re.search(self.validationChoice[1], elem[i]) and not re.search('noPU', elem[i]):  # noPU exclusion ! to be tested
                        tmp_elem.append(elem[i])
                tmp_list.append(tmp_elem)
    else: # RECO or miniAOD
        #print('RECO/miniAOD')
        for elem in tab:
            tmp_elem = []
            tmp_elem.append(elem[0])
            for i in range(1, len(elem)):
                if not re.search('PU', elem[i]) and not re.search('pmx', elem[i]) or re.search('noPU', elem[i]):  # noPU inclusion ! to be tested
                    tmp_elem.append(elem[i])
            tmp_list.append(tmp_elem)
    return tmp_list

def getDatasetsDefault(self, fieldname):
    self.default_dataset = DataSetsFilter(self, fieldname)
    self.commonDatasets = set(self.datasetsList_1).intersection(set(self.datasetsList_2))
    defaults =[]
    for elem in self.default_dataset:
        if elem[1] == 1:
            defaults.append(elem[0])
    #print(defaults)
    intersection = set(self.commonDatasets).intersection(set(defaults))
    self.commonDatasets = list(self.commonDatasets) # get the common datasets for the comparisons.
    #print('default', self.default_dataset)
    len_default = 0
    for elem in self.default_dataset:
        len_default += elem[1]
    #print('len default : %s' % len_default)
    #print('inter avec common')
    intersection = list(intersection)
    #print(intersection)
    len_inter = len(intersection)
    if len_inter > 0:
        for el1 in self.default_dataset:
            el1[1] = 0
            for el2 in intersection:
                if el1[0] == el2:
                    el1[1] = 1
    #print(self.default_dataset)
    return len_inter, len_default