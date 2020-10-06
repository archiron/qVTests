#! /usr/bin/env python
#-*-coding: utf-8 -*-

import os,sys,subprocess,shutil
import urllib2
import re
from time import sleep

sys.path.append('/afs/cern.ch/user/a/archiron/lbin/ChiLib')

from networkFunctions import list_search_0, list_search_1, cmd_load_files
from functions import getDataSet, analyzeDTS
from functionsqV import *
from defaultqV import *
from datasetsqV import *

class quickVal(): 
    def __init__(self):
        screen_clear()
        print('begin to run')
        actual_dir = os.getcwd()
        print('actual_dir : %s' % actual_dir)
        self.CMSSWBASE = os.environ['CMSSW_BASE'] # donne le repertoire de travail
        self.CMSSWBASECMSSWRELEASEBASE = os.environ['CMSSW_RELEASE_BASE'] # donne la release et l'architecture
        self.CMSSWBASECMSSWVERSION = os.environ['CMSSW_VERSION'] # donne la release (CMSSW_7_1_0 par exemple)
        print('CMSSWBASE : %s' % self.CMSSWBASE)
        print('CMSSWBASECMSSWRELEASEBASE : %s' % self.CMSSWBASECMSSWRELEASEBASE)
        print('CMSSWBASECMSSWVERSION : %s' % self.CMSSWBASECMSSWVERSION)
        print('\nEach number/string must be validated with return !\n')
        
        check_terminal_size(self)

        text_to_prompt= "Release family for the validation " 
        print(text_to_prompt)  # 
        sleep(1)

        self.list_0 = list_search_0()
        self.list_0.sort()

        self.color = color
        self.comparisons = comparisons
        self.validations = validations
        
        i_back = 1
        while (i_back != 0):
            table=getattr(sys.modules[__name__], "fonction_%s" % str(i_back))(self)
            i_back = (table + 1) % 7
            print('i_back : %d' % i_back)

        #screen_clear()
        print('RESUME : ')
        text_to_prompt = 'RELEASE : ' + colorText(self.release, 'blue') + ' - REFERENCE : ' + colorText(self.reference, 'blue')
        print(text_to_prompt)
        print('')
                                                                                       
        print(' ')
        print(self.tabGlobal)
        
        print('suite ...')
        #stop
        
        
        # Comparison of the datasets lists
        print(' ')
        print('Common datasets')

        self.commonDatasets = set(self.datasetsList_1).intersection(set(self.datasetsList_2))
        self.commonDatasets = list(self.commonDatasets) # get the common datasets for the comparisons
        print_tab(self.commonDatasets)
        '''
        
        for i in range(0, len(datasets), 3):
            if (i+1 == len(datasets)):
                print('%50s [%2d]' % (datasets[i], i))
            elif (i+2 == len(datasets)):
                print('%50s [%2d] %50s [%2d]' % (datasets[i], i, datasets[i+1], i+1))
            else:
                print('%50s [%2d] %50s [%2d] %50s [%2d]' % (datasets[i], i, datasets[i+1], i+1, datasets[i+2], i+2))
        
        #item_0 == releaseFamily

        # test if datasets_default is included into datasets
        v = 0
        for item in datasets:
            for item2 in datasets_default:
                if item == item2:
                    v += 1
        if (v == 2): # we can use default datasets
            print('default datasets : ' + '[' + ' '.join("{:s}".format(x) for x in datasets_default) + ']')
            text_to_prompt = 'insert the # of the datasets you want separated by a comma or d to use default : '
            dts_list_txt = raw_input(text_to_prompt)
            if (dts_list_txt == 'd'):
                dts_list_2 = datasets_default
            else:
                dts_list = analyzeDTS(dts_list_txt)
        else: # we cannot use default datasets
            text_to_prompt = 'insert the # of the datasets you want separated by a comma : '
            dts_list_txt = raw_input(text_to_prompt)
            dts_list = analyzeDTS(dts_list_txt)

        # test if all # are < len(datasets)
        if (dts_list_txt != 'd'):
            dts_list_2 = []
            for item in dts_list:
                if (item >= len(datasets) or item < 0):
                    dts_list.remove(item)
                else:
                    dts_list_2.append(datasets[item])
            
        print('datasets final list : ' + '[' + ' '.join("{:s}".format(x) for x in dts_list_2) + ']')
        print('default datasets : ' + '[' + ' '.join("{:s}".format(x) for x in datasets_default) + ']')
        #stop
        
        list_2 = [] # get the list of the files for all the datasets
        nb_2 = [] # get the number of files per dataset
        for item1 in dts_list_2:
            i = 0
            for item2 in list_1:
                if re.search(item1, item2):
                    print(item2, item1)
                    list_2.append(item2)
                    i += 1
            nb_2.append(i)
                    
        for item1 in enumerate(list_2):
            print('[%2d] : %s' %(item1[0], list_2[item1[0]]))
            
        text_to_prompt = 'insert the # of the files you want to download separated by a comma or a for all : '
        files_list_txt = raw_input(text_to_prompt)
        if (files_list_txt == 'a'):
            files_list = range(0, len(list_2))
        else:
            files_list = analyzeDTS(files_list_txt)
        print(files_list)

        # test if all # are < len(datasets)
        files_list_2 = []
        for item in files_list:
            if (item >= len(list_2) or item < 0):
                files_list.remove(item)
            else:
                files_list_2.append(list_2[item])
        print('files final list : ' + '[' + ' '.join("{:s}".format(x) for x in files_list_2) + ']')
        
        # download
        cmd_load_files(files_list_2, item_0+'x')
        '''
        print('end of run')
               
