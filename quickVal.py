#! /usr/bin/env python
#-*-coding: utf-8 -*-

import os,sys
import re
from time import sleep

#sys.path.append('/afs/cern.ch/user/a/archiron/lbin/ChiLib')
sys.path.append('/eos/project-c/cmsweb/www/egamma/validation/Electrons/ChiLib/')

from networkFunctions import list_search_0
from functionsqV import *
from defaultqV import *
from datasetsqV import DataLocation

class quickVal():
    def __init__(self):
        screen_clear()
        print('begin to run with version %s' % colorText(str(version), 'blue'))
        actual_dir = os.getcwd()
        print('actual dir for work : %s' % actual_dir)
        print('\nEach number/string must be validated with RETURN !\n')

        check_terminal_size(self)

        self.t2s = time2sleep
        print("\nRelease family for the validation ")  #
        sleep(self.t2s)

        print('loading releases list')
        self.list_0 = list_search_0()
        self.list_0.sort()

        self.color = color
        self.color_nb = color_nb
        self.comparisons = comparisons
        self.validations = validations
        self.releaseExtent = ''
        self.referenceExtent = ''
        self.web_location = [DataLocation(self)[0][2],
                           DataLocation(self)[1][2]]
        self.web_extension = [DataLocation(self)[0][3],
                           DataLocation(self)[1][3]]
        self.Gev = [] # table for validations

        print('config.py file creation')
        try:
            self.configFile = open('config.py', 'w') #
        except IOError:
            print("Could not open file!")

        i_back = 1
        while (i_back != 0):
            table=getattr(sys.modules[__name__], "fonction_%s" % str(i_back))(self)
            i_back = (table + 1) % 16
            print('i_back : %d' % i_back)

        self.configFile.close()
        print('... End')
