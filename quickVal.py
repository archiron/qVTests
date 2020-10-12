#! /usr/bin/env python
#-*-coding: utf-8 -*-

import os,sys #,subprocess,shutil
#import urllib2
import re
from time import sleep

sys.path.append('/afs/cern.ch/user/a/archiron/lbin/ChiLib')

from networkFunctions import list_search_0, list_search_1#, cmd_load_files
#from functions import getDataSet, analyzeDTS
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
        self.Gev = [] # table for validations
        self.gev_tmp = []
        self.releasesList_4 = []
        self.referencesList_4 = []
        self.releasesGT = []
        self.referencesGT = []

        i_back = 1
        while (i_back != 0):
            table=getattr(sys.modules[__name__], "fonction_%s" % str(i_back))(self)
            i_back = (table + 1) % 13
            print('i_back : %d' % i_back)
            # include the differents choices into Gev

        #screen_clear()
        print('RESUME : ')
        text_to_prompt = 'RELEASE : ' + colorText(self.release, 'blue') + ' - REFERENCE : ' + colorText(self.reference, 'blue')
        print(text_to_prompt)
        text_to_prompt = 'release extension : ' + colorText(self.releaseExtent, 'blue') + ' - reference extension : ' + colorText(self.referenceExtent, 'blue')
        print(text_to_prompt)
        print('')
        #self.Gev.append([self.location, self.extension])
        self.gev_tmp.append([str(self.release), str(self.reference)])
        self.gev_tmp.append([str(self.releaseExtent), str(self.referenceExtent)])
        self.gev_tmp.append(str(self.datasets))
        self.gev_tmp.append(str(self.comparisonChoice))
        self.gev_tmp.append(str(self.validationChoice))
        self.gev_tmp.append(str(self.DB_flags))
        print(self.gev_tmp)
        self.Gev.append(self.gev_tmp)
        print(self.Gev)

        print('suite ...')
        #stop

        print('config.py file creation')
        try:
            configFile = open('configFile.py', 'w+') #
        except IOError:
            print("Could not open file!")
        if configFile:
            configFile.write('#! /usr/bin/env python\n')
            configFile.write('#-*-coding: utf-8 -*-\n')
            configFile.write('\n')
            configFile.write('import os,sys\n')
            configFile.write('\n')
            configFile.write('#############################################################################\n')
            configFile.write('# global data\n')
            configFile.write('web_repo = ' + str([self.location, self.extension]) + '\n')
            configFile.write('\n')
            ind = 0
            for elem in self.Gev:
                configFile.write('# personalization ' + str(ind+1) + '\n')
                configFile.write('GeV_'+ str(ind+1) +' = [\n')
                configFile.write(str(unicode(elem[0])) + ' , # release/reference\n')
                configFile.write(str(elem[1]) + ' , # relref_extent\n')
                configFile.write(str(elem[2]) + ' , # datasets\n')
                configFile.write('\'' + str(elem[3]) + '\' , # choice\n')
                configFile.write(str(elem[4]) + ' , # relrefValtype RECO vs RECO\n')
                # GT
                # ROOT files
                configFile.write(str(self.DB_flags) + ', # DB flag\n')
                configFile.write('\n')
            configFile.write('#############################################################################\n')
            configFile.write('\n')

        # ROOT files extraction for selected datasets
        rootFilesExtraction(self)
        print('')
        # GT extraction from lists
        for elem in self.releasesList_4:
            gt_tmp = []
            #gt_tmp.append(elem[0])
            for i in range(1, len(elem)):
                aa = explode_item(elem[i])
                print(aa)
                for dts in self.datasets:
                    if re.search(dts, aa[0]):
                        gt_tmp.append(aa[2])
            gt_tmp = sorted(set(gt_tmp))
            gt_tmp.insert(0, elem[0])
            self.releasesGT.append(gt_tmp)
        for elem in self.referencesList_4:
            gt_tmp = []
            #gt_tmp.append(elem[0])
            for i in range(1, len(elem)):
                aa = explode_item(elem[i])
                print(aa)
                for dts in self.datasets:
                    if re.search(dts, aa[0]):
                        gt_tmp.append(aa[2])
            #print(sorted(set(gt_tmp)))
            gt_tmp = sorted(set(gt_tmp))
            gt_tmp.insert(0, elem[0])
            #print(gt_tmp)
            self.referencesGT.append(gt_tmp)
        print('')
        print('GT')
        for elem in self.releasesGT:
            print(elem)
        print('')
        for elem in self.referencesGT:
            print(elem)
        self.releasesGT1 = []
        self.referencesGT1 = []
        GlobalTagsExtraction(self)

        print('***')
        for elem in self.releasesGT1:
            print(elem)
        print('')
        for elem in self.referencesGT1:
            print(elem)

        print('end of run')
