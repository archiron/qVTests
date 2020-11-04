#! /usr/bin/env python
#-*-coding: utf-8 -*-

import os,sys
import re
from time import sleep

sys.path.append('/afs/cern.ch/user/a/archiron/lbin/ChiLib')

from networkFunctions import list_search_0, list_search_1
from functionsqV import *
from defaultqV import *

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
        self.releaseExtent = ''
        self.referenceExtent = ''
        self.default_dataset = []
        self.datasets = []
        self.DB_flags = []
        self.web_location = [DataLocation(self)[0][2],
                           DataLocation(self)[1][2]]
        self.web_extension = [DataLocation(self)[0][3],
                           DataLocation(self)[1][3]]
        self.Gev = [] # table for validations
        self.gev_tmp = []
        self.releasesList_4 = [] # root files list for release
        self.referencesList_4 = [] # root files list for reference
        self.releasesList_5 = [] # root files list for release after validation choice
        self.referencesList_5 = [] # root files list for reference after validation choice
        self.releasesGT = []
        self.referencesGT = []
        self.relRootFilesList = []
        self.refRootFilesList = []

        print('config.py file creation')
        try:
            self.configFile = open('configFile.py', 'w+') #
        except IOError:
            print("Could not open file!")

        i_back = 1
        while (i_back != 0):
            table=getattr(sys.modules[__name__], "fonction_%s" % str(i_back))(self)
            i_back = (table + 1) % 15
            print('i_back : %d' % i_back)
            # include the differents choices into Gev

        #screen_clear()
        '''print('RESUME : ')
        text_to_prompt = 'RELEASE : ' + colorText(self.release, 'blue') + ' - REFERENCE : ' + colorText(self.reference, 'blue')
        print(text_to_prompt)
        text_to_prompt = 'release extension : ' + colorText(self.releaseExtent, 'blue') + ' - reference extension : ' + colorText(self.referenceExtent, 'blue')
        print(text_to_prompt)
        print(self.GT_rel)
        print(self.GT_ref)
        print(self.relRootFilesList)
        print(self.refRootFilesList)
        print('')
        self.gev_tmp.append([str(self.release), str(self.reference)])
        self.gev_tmp.append([str(self.releaseExtent), str(self.referenceExtent)])
        self.gev_tmp.append(str(self.datasets))
        self.gev_tmp.append(str(self.comparisonChoice))
        self.gev_tmp.append(str(self.validationChoice))
        self.gev_tmp.append([str(self.GT_rel), str(self.GT_ref)])
        self.gev_tmp.append(str(self.DB_flags))
        print(self.gev_tmp)
        self.Gev.append(self.gev_tmp)
        print(self.Gev)

        print('suite ...')
        #stop

        if self.configFile:
            self.configFile.write('#! /usr/bin/env python\n')
            self.configFile.write('#-*-coding: utf-8 -*-\n')
            self.configFile.write('\n')
            self.configFile.write('import os,sys\n')
            self.configFile.write('\n')
            self.configFile.write('#############################################################################\n')
            self.configFile.write('# global data\n')
            self.configFile.write('web_repo = ' + str([self.location, self.extension]) + '\n')
            self.configFile.write('\n')
            ind = 0
            for elem in self.Gev:
                self.configFile.write('# personalization ' + str(ind+1) + '\n')
                self.configFile.write('GeV_'+ str(ind+1) +' = [\n')
                self.configFile.write(str(unicode(elem[0])) + ' , # release/reference\n')
                self.configFile.write(str(elem[1]) + ' , # relref_extent\n')
                self.configFile.write(str(elem[2]) + ' , # datasets\n')
                self.configFile.write('\'' + str(elem[3]) + '\' , # choice\n')
                self.configFile.write(str(elem[4]) + ' , # relrefValtype RECO vs RECO\n')
                self.configFile.write(str(elem[5]) + ' , # GT one couple rel/ref for all dataset\n')
                # ROOT files
                self.configFile.write(str(self.DB_flags) + ', # DB flag\n')
                self.configFile.write('\n')
            self.configFile.write('#############################################################################\n')
            self.configFile.write('\n')'''

        self.configFile.close()
        print('... et fin')
