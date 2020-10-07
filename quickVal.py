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
#from datasetsqV import *

class quickVal():
    def __init__(self):
        screen_clear()
        print('begin to run')
        actual_dir = os.getcwd()
        print('actual_dir : %s' % actual_dir)
        print('\nEach number/string must be validated with return !\n')

        check_terminal_size(self)

        text_to_prompt= "Release family for the validation "
        print(text_to_prompt)  #
        sleep(1)

        print('loading releases list')
        self.list_0 = list_search_0()
        self.list_0.sort()

        self.color = color
        self.color_nb = color_nb
        self.comparisons = comparisons
        self.validations = validations
        self.default_dataset = []
        self.datasets = []
        self.DB_flags = []

        self.web_location = [DataLocation(self)[0][2],
                           DataLocation(self)[1][2]]
        self.web_extension = [DataLocation(self)[0][3],
                           DataLocation(self)[1][3]]
        #print(self.web_location)
        #print(self.web_extension)
        #print('data location : ')
        #print(DataLocation(self))
        sleep(1)

        self.Gev = [] # table for validations
        self.gev_tmp = []

        i_back = 1
        while (i_back != 0):
            table=getattr(sys.modules[__name__], "fonction_%s" % str(i_back))(self)
            i_back = (table + 1) % 12
            print('i_back : %d' % i_back)
            # include the differents choices into Gev

        #screen_clear()
        print('RESUME : ')
        text_to_prompt = 'RELEASE : ' + colorText(self.release, 'blue') + ' - REFERENCE : ' + colorText(self.reference, 'blue')
        print(text_to_prompt)
        text_to_prompt = 'release extension : ' + colorText(self.releaseExtent, 'blue') + ' - reference extension : ' + colorText(self.referenceExtent, 'blue')
        print(text_to_prompt)
        print('')
        self.Gev.append(self.location)
        self.gev_tmp.append([self.release, self.reference])
        self.gev_tmp.append([self.releaseExtent, self.referenceExtent])
        # insert dataset choice
        self.gev_tmp.append(self.comparisonChoice)
        self.gev_tmp.append(self.validationChoice)
        self.gev_tmp.append(self.datasets)
        self.gev_tmp.append(self.DB_flags)
        print(self.gev_tmp)
        self.Gev.append(self.gev_tmp)
        print(self.Gev)

        print(' ')
        #print(self.tabGlobal)

        print('suite ...')
        #stop

        # Comparison of the datasets lists
        print(' ')
        print('Common datasets')

        self.commonDatasets = set(self.datasetsList_1).intersection(set(self.datasetsList_2))
        self.commonDatasets = list(self.commonDatasets) # get the common datasets for the comparisons
        #print_tab_1(self.commonDatasets, self.color_nb)

        print('end of run')
