#! /usr/bin/env python
#-*-coding: utf-8 -*-

import os,sys
import re
from time import sleep

sys.path.append('/afs/cern.ch/user/a/archiron/lbin/ChiLib')

from networkFunctions import list_search_1
from datasetsqV import *

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

def screen_clear():
     # The screen clear function
    # for mac and linux(here, os.name is 'posix')
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        # for windows platfrom
        _ = os.system('cls')

def check_terminal_size(self):
    if (terminal_size()[0] < 150): # too less cols
        print("not enough columns [%d]. Must be at least 150." % terminal_size()[0])
        exit()
    elif (terminal_size()[1] < 35): # too less rows
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

#def affiche_1(i, tab, color): # not used
#    print('%40s [%s]' % (tab[i], colorText(str(i), color)))

def affiche_2(i, tab, color): # not used
    print('%40s [%s] %40s [%s]' % ( tab[i], colorText(str(i), color), tab[i+1], colorText(str(i+1), color) ) )

def affiche_3(i, tab, color): # not used
    print('%40s [%s] %40s [%s] %40s [%s]' % ( tab[i], colorText(str(i), color), tab[i+1], colorText(str(i+1), color), tab[i+2], colorText(str(i+2), color) ) )

def changeColor(color):
    # 30:noir ; 31:rouge; 32:vert; 33:orange; 34:bleu; 35:violet; 36:turquoise; 37:blanc
    # other references at https://misc.flogisoft.com/bash/tip_colors_and_formatting
    if (color == 'black'):
        return '[30m'
    elif (color == 'red'):
        return '[31m'
    elif (color == 'green'):
        return '[32m'
    elif (color == 'orange'):
        return '[33m'
    elif (color == 'blue'):
        return '[34m'
    elif (color == ''):
        return '[35m'
    elif (color == 'purple'):
        return '[36m'
    elif (color == 'turquoise'):
        return '[37m'
    elif (color == 'lightyellow'):
        return '[93m'
    else:
        return '[30m'

def print_tab_6(tab, color, rel, ref):
    print('')
    for i in range(0, len(tab)):
        if ( ( tab[i][0] == 'RECO' and tab[i][1] == 'miniAOD' ) or ( tab[i][0] == 'pmx' and tab[i][1] == 'PU' ) ):
            print( '[%s] %s vs %s [%s]' % ( colorText(str(i), color), tab[i][0], tab[i][1], colorText(rel, 'blue') ) )
        else:
            print( '[%s] %s [%s] vs %s [%s]' % ( colorText(str(i), color), tab[i][0], colorText(rel, 'blue'), tab[i][1], colorText(ref, 'blue') ) )

def print_tab_5(tab, color): # only for GT
    print('')

    for i, elem in enumerate(tab):
        aa = elem[1:]
        print('[%s] - %s %s' % ( colorText(str(i), color), colorText(str(elem[0]), 'blue'), aa )) # 1 GT per line

def print_tab_4(tab, color):
    print('')
    for i in range(0, len(tab)):
        print('[%s] %s vs %s' % (colorText(str(i), color), tab[i][0], tab[i][1]))

def print_tab_3(tab, color): # only for default datasets
    print('')

    for i in range(0, len(tab), 1):
        color0 = color
        if ( tab[i][1] == 0):
            color0 = 'blue'
        print('%40s [%s] - [%2d]' % ( tab[i][0], colorText(str(tab[i][1]), color0), i )) # 1 dataset per line

def print_tab_2(tab, color): # only for tab with 2 elements
    print('')
    for i in range(0, len(tab)):
        print('[%s] %40s' % (colorText(str(i), color), tab[i]))

def print_tab_1(tab, color):
    print('')
    if ((len(tab) % 2) == 0):
        for i in range(0, len(tab), 2):
            affiche_2(i, tab, color)
    elif ((len(tab) % 3) == 0):
        for i in range(0, len(tab), 3):
            affiche_3(i, tab, color)
    else: # general case
        for i in range(0, len(tab), 2):
            if (i+1 == len(tab)):
                print( '%40s [%s]' % ( tab[i], colorText(str(i), color) ) )
            else: #
                affiche_2(i, tab, color)

def colorText(sometext, color):
    return '\033' + changeColor(color) + sometext + '\033[0m'

def get_answerText(self, text2prompt, nb):
    quitLoop = True
    print('')
    while ( quitLoop ):
        rel = raw_input(text2prompt + '\n >> : ') # blanck to see correctly what we answered
        if rel == 'q':
            exit()
        elif rel == 'b':
            quitLoop = False
            text = 'back'
        elif rel == 'h':
            if (nb == 6):
                help(fonction_6)
            elif (nb == 7):
                help(fonction_7)
            return "h"
        elif rel == 's':
            displaySummary(self)
            sleep(self.t2s)
            return "h"
        else:
            print('vous avez tapé : %s' % rel)
            quitLoop = False
            text = rel

    return text

def get_answer1(text2prompt, tab1, tab2):
    quitLoop = True
    print('')
    while ( quitLoop ):
        rel = raw_input(text2prompt + '\n >> : ') # blanck to see correctly what we answered
        #rel = input(text2prompt)  # Python 3
        if rel == 'q':
            exit()
        elif rel == 'h':
            help(fonction_1)
            return "h", 0
        else:
            print('you typed : %s' % rel)
        irel = ''
        try:
            irel = int(rel)
            if ( irel >= 0 and irel < len(tab1) ):
                quitLoop = False
                temp1 = tab1[int(rel)]
                temp2 = tab2[int(rel)]
            else:
                print('%d is not into the range [0:%d]' % (irel, len(tab)-1))
                quitLoop = True
        except:
            print('%s is not a number' % rel)

    return temp1, temp2

def get_answer10X(text2prompt, tab):
    nb = []
    quitLoop = True
    print('')
    while ( quitLoop ):
        vals = raw_input(text2prompt + '\n >> : ') # blanck to see correctly what we answered
        #rel = input(text2prompt)  # Python 3
        vals2 = vals.split(',')
        print(vals, vals2)
        for i in range(0, len(vals2)):
            irel = ''
            try:
                irel = int(vals2[i])
                if ( irel >= 0 and irel < len(tab) ):
                    nb.append(irel)
                    quitLoop = False
                else:
                    print('%d not in range [0, %d]' %(irel, len(tab)-1))
                    quitLoop = True
            except:
                print('%s is not a number' % vals2[i])
    #print(nb)
    return nb

def get_answer2(text2prompt):
    quitLoop = True
    print('')
    while ( quitLoop ):
        rel = raw_input(text2prompt + '\n >> : ') # blanck to see correctly what we answered
        #rel = input(text2prompt)  # Python 3
        if rel == 'q':
            exit()
        elif rel == 'b': # back
            quitLoop = False
            temp = 'b'
        elif rel == 'c': # continue
            quitLoop = False
            temp = 'c'
        else:
            print('you typed : %s' % rel)

    return temp

def get_answer3(self, text2prompt, tab, nb):
    quitLoop = True
    print('')
    while ( quitLoop ):
        rel = raw_input(text2prompt + '\n >> : ') # blanck to see correctly what we answered
        #rel = input(text2prompt)  # Python 3
        if rel == 'q':
            exit()
        elif rel == 'b':
            quitLoop = False
            temp = ''
        elif rel == 'h':
            if (nb == 2):
                help(fonction_2)
            elif (nb == 3):
                help(fonction_3)
            elif (nb == 4):
                help(fonction_4)
            elif (nb == 5):
                help(fonction_5)
            elif (nb == 8):
                help(fonction_8)
            elif (nb == 9):
                help(fonction_9)
            return "h"
        elif rel == 's':
            displaySummary(self)
            sleep(self.t2s)
            return "h"
        else:
            print('you typed : %s' % rel)
        irel = ''
        try:
            irel = int(rel)
            if ( irel >= 0 and irel < len(tab) ):
                quitLoop = False
                temp = tab[int(rel)]
            else:
                print('%d is not into the range [0:%d]' % (irel, len(tab)-1))
                quitLoop = True
        except:
            print('%s is not a number' % rel)

    return temp

def get_answer4(self, text2prompt):
    quitLoop = True
    print('')
    while ( quitLoop ):
        rel = raw_input(text2prompt + '\n >> : ') # blanck to see correctly what we answered
        #rel = input(text2prompt)  # Python 3

        #print('rel : %s' % rel)
        if rel == 'q':
            exit()
        elif rel == 'b':
            quitLoop = False
            temp = ''
        elif rel == 'd':
            quitLoop = False
            temp = 'd'
        elif rel == 't':
            quitLoop = False
            temp = 't'
        elif rel == 'c':
            quitLoop = False
            temp = 'c'
        elif rel == 'h':
            help(fonction_10)
            quitLoop = False
            temp = "h"
        elif rel == 's':
            quitLoop = False
            # keep the old help text
            old_text = fonction_10.__doc__
            print('fonction_10 : %s' % old_text)
            # give a new help text
            staticmethod(fonction_10).__func__.__doc__ = displaySummary2(self)
            help(fonction_10)
            # give the old help text back
            staticmethod(fonction_10).__func__.__doc__ = old_text
            temp = "h"
        else:
            print('you typed : %s' % rel)

    return temp

def get_answer5(self, text2prompt, nb):
    quitLoop = True
    print('')
    while ( quitLoop ):
        rel = raw_input(text2prompt + '\n >> : ') # blanck to see correctly what we answered
        #rel = input(text2prompt)  # Python 3
        temp = ''

        if rel == 'q':
            exit()
        elif rel == 'b':
            print('back')
            quitLoop = False
            temp = ''
        elif rel == 'y':
            quitLoop = False
            temp = 'y'
        elif rel == 'n':
            quitLoop = False
            temp = 'n'
        elif rel == 'h':
            if (nb == 13):
                help(fonction_13)
            elif (nb == 15):
                help(fonction_15)
            quitLoop = False
            return "h"
        elif rel == 's':
            quitLoop = False
            displaySummary(self)
            sleep(self.t2s)
            return "h"
        else:
            print('you typed : %s' % rel)

    return temp

def get_answer6(self, text2prompt, tab, nb): # for GT
    quitLoop = True
    print('')
    while ( quitLoop ):
        rel = raw_input(text2prompt + '\n >> : ') # blanck to see correctly what we answered
        #rel = input(text2prompt)  # Python 3
        if rel == 'q':
            exit()
        elif rel == 'b':
            quitLoop = False
            temp = ''
        elif rel == 'h':
            quitLoop = False
            if (nb == 11):
                help(fonction_11)
            elif (nb == 12):
                help(fonction_12)
            return "h"
        elif rel == 's':
            quitLoop = False
            displaySummary(self)
            sleep(self.t2s)
            return "h"
        else:
            print('you typed : %s' % rel)
        irel = ''
        try:
            irel = int(rel)
            if ( irel >= 0 and irel < len(tab) ):
                quitLoop = False
                temp = tab[int(rel)][0]
            else:
                print('%d is not into the range [0:%d]' % (irel, len(tab)-1))
                quitLoop = True
        except:
            print('%s is not a number' % rel)

    return temp

def fonction_1(self):
    """Folder location :
    it is the path you want to use on eos to store the validations you will make.
    """
    screen_clear()
    #print('vous appelez la fonction 1')
    print('Pictures & web pages can be located on 2 eos folders : Dev or Releases.')
    print_tab_2(self.web_location, self.color_nb)
    text_to_prompt = "number of the folder choice or [" + colorText('q', self.color) +"]uit. ? "
    text_to_prompt += "                    [" + colorText('h', self.color) + "]elp"
    #text_to_prompt += colorText('s', self.color) + "]tatus "
    self.location, self.extension = get_answer1(text_to_prompt, self.web_location, self.web_extension)
    #self.logFile.seek(0)
    self.logFile.write('1 - self.location : %s\n' % self.location)
    #self.logFile.seek(0)
    self.logFile.write('1 - self.extension : %s\n' % self.extension)
    if (self.location=='h'):
        return 0
    else:
        print('WEB LOCATION : %s' % colorText(self.location, 'blue'))  # now we have the web folder location
        sleep(self.t2s)
        return 1

def fonction_2(self):
    """RELEASE family :
    Before to choose the release you want to validate you need to choose its family.
    For the all next steps, this release to validate is named as : RELEASE
    in opposition of the release which is used as reference which is named REFERENCE.
    """
    screen_clear()
    #print('vous appelez la fonction 2')
    # initialization
    self.default_dataset = []
    self.datasets = []
    self.DB_flags = []
    self.gev_tmp = []
    self.releasesList_5 = []  # root files list for release after validation choice
    self.referencesList_5 = []  # root files list for reference after validation choice
    self.releasesGT = []
    self.referencesGT = []
    self.release = ''
    self.reference = ''
    self.comparisonChoice = ['', '']
    self.validationChoice = ['', '']
    self.GT_rel = []
    self.GT_ref = []
    self.relRootFilesList = []
    self.refRootFilesList = []

    print('RELEASE family for the validation ')
    # get the list for RELEASE
    print_tab_1(self.list_0, self.color_nb)

    text_to_prompt = "number of the RELEASE family, [" + colorText('b', self.color) + "]ack or [" + colorText('q', self.color) +"]uit. ? "
    text_to_prompt += "                    [" + colorText('h', self.color) + "]elp - ["
    text_to_prompt += colorText('s', self.color) + "]tatus "  
    self.releaseFamily = get_answer3(self, text_to_prompt, self.list_0, 2)
    if self.releaseFamily == "":
        return 0
    if self.releaseFamily == "h" :
        return 1
    else:
        print('RELEASE FAMILY : %s' % colorText(self.releaseFamily, 'blue')) # now we have the release family
        self.logFile.write('2 - RELEASE FAMILY : %s' % colorText(self.releaseFamily, 'blue') + '\n')
        sleep(self.t2s)
        # here we get the release list
        self.releasesList_1 = list_search_1(self.releaseFamily) # all the releases
        self.logFile.write('2 - get all the releases for the release family' + '\n')
        #print('there is %d files for %s' % (len(self.releasesList_1), self.releaseFamily))
        self.releasesList_2 = sub_releases(self.releasesList_1) # extract the releases CMSSW_X_Y_Z...
        self.logFile.write('2 - get all the releases' + '\n')
        return 2

def fonction_3(self):
    """RELEASE :
    Inside the chosen family, choose the release you want to validate.
    Be careful of all possibilities
    """
    screen_clear()
    #print('vous appelez la fonction 3')
    print('RELEASE to validate choice')
    print_tab_1(self.releasesList_2, self.color_nb)
    text_to_prompt = "number of the RELEASE, [" + colorText('b', self.color) + "]ack or [" + colorText('q', self.color) +"]uit. ? "
    text_to_prompt += "                    [" + colorText('h', self.color) + "]elp - ["
    text_to_prompt += colorText('s', self.color) + "]tatus "  
    self.release = get_answer3(self, text_to_prompt, self.releasesList_2, 3)

    if self.release == "h":
        return 2
    elif self.release != '':
        print('RELEASE : %s' % self.release) # now we have the release
        self.logFile.write('3 - RELEASE : %s' % self.release + '\n')
        print('')
        self.releasesList_3 = sub_releases3(self.release, self.releasesList_1) # extract the list of the root files for the chosen release
        self.logFile.write('3 - get the list of the root files of the release' + '\n')
        self.datasetsList_1 = sub_releases2(self.release, self.releasesList_3) # extract the datasets of the root files for the chosen release
        self.logFile.write('3 - get the datasets of the release' + '\n')
        return 3
    else:
        return 1

def fonction_4(self):
    """REFERENCE family :
    As for the release, before to choose the release you want to use as a reference you need to choose its family
    """
    screen_clear()
    #print('vous appelez la fonction 4')
    print('REFERENCE family for the validation ')  #

    # get the list for REFERENCE
    print_tab_1(self.list_0, self.color_nb)

    text_to_prompt = "number of the REFERENCE family, [" + colorText('b', self.color) + "]ack or [" + colorText('q', self.color) +"]uit. ? "
    text_to_prompt += "                    [" + colorText('h', self.color) + "]elp - ["
    text_to_prompt += colorText('s', self.color) + "]tatus "  
    self.referenceFamily = get_answer3(self, text_to_prompt, self.list_0, 4)
    if self.referenceFamily == "h":
        return 3
    elif self.referenceFamily != '':
        print('REFERENCE FAMILY : %s' % colorText(self.referenceFamily, 'blue')) # now we have the reference family
        self.logFile.write('4 - REFERENCE FAMILY : %s' % colorText(self.referenceFamily, 'blue')  + '\n')
        sleep(self.t2s)

        # here we get the reference list

        self.referencesList_1 = list_search_1(self.referenceFamily) # all the references
        self.logFile.write('4 - get all the releases for the reference family' + '\n')
        #print('there is %d files for %s' % (len(self.referencesList_1), self.referenceFamily))
        #self.referenceFamily2 = self.referenceFamily[:-1] # not used ?

        self.referencesList_2 = sub_releases(self.referencesList_1) # extract the references CMSSW_X_Y_Z...
        self.logFile.write('4 - get all the releases' + '\n')
        return 4
    else:
        return 2

def fonction_5(self):
    """REFERENCE :
    Inside the chosen family, choose the releference.
    Be careful of all possibilities"""
    screen_clear()
    #print('vous appelez la fonction 5')
    print('REFERENCE choice')
    print_tab_1(self.referencesList_2, self.color_nb)
    text_to_prompt = "number of the REFERENCE, [" + colorText('b', self.color) + "]ack or [" + colorText('q', self.color) +"]uit. ? "
    text_to_prompt += "                    [" + colorText('h', self.color) + "]elp - ["
    text_to_prompt += colorText('s', self.color) + "]tatus "  
    self.reference = get_answer3(self, text_to_prompt, self.referencesList_2, 5)

    if self.reference == "h":
        return 4
    elif self.reference != '':
        print('REFERENCE : %s' % self.reference) # now we have the reference
        self.logFile.write('5 - REFERENCE : %s' % self.release + '\n')
        print('')
        self.referencesList_3 = sub_releases3(self.reference, self.referencesList_1) # extract the list of the root files for the chosen reference
        self.logFile.write('5 - get the list of the root files of the reference' + '\n')
        self.datasetsList_2 = sub_releases2(self.reference, self.referencesList_3) # extract the datasets of the root files for the chosen reference
        self.logFile.write('5 - get the datasets of the reference' + '\n')
        return 5
    else:
        return 3

def fonction_6(self):
    """RELEASE folder extension :
    The web page & the pictures are saved into a folder which is generally of the form
    1X_Y_Z_[preK]_DQM_std/dev (see help from the first choice) for last releases.
    For some validations such as 2021 or PHASE2 there can be some pbms with the path :
    without personalization, all validations could be written into the same release folder.
    In order to avoid that, we add an extension to personalize those paths.
    """
    screen_clear()
    #print('vous appelez la fonction 6')
    # web folder name customization
    # text to add into folder name for release

    print('')
    text_to_prompt = "input a RELEASE folder extension (hit return for none), [" + colorText('b', self.color) + "]ack or [" + colorText('q', self.color) +"]uit. ? "
    text_to_prompt += "                    [" + colorText('h', self.color) + "]elp - ["
    text_to_prompt += colorText('s', self.color) + "]tatus "  

    self.releaseExtent = get_answerText(self, text_to_prompt, 6) # get a text
    if (self.releaseExtent == 'h'):
        return 5
    elif (len(self.releaseExtent) == 0):
        print("no extension for release.")
        self.logFile.write('6 - no extension for release.' + '\n')
        self.path = self.location + self.release[6:] + '_DQM_' + self.extension
        print('path for location : %s' % self.path)
        sleep(self.t2s)
        return 6
    else:
        if (self.releaseExtent == 'back'):
            return 4
        else:
            print('extension for release : %s' % self.releaseExtent)
            self.logFile.write('6 - extension for release : %s' % self.releaseExtent + '\n')
            self.path = self.location + self.release[6:] + '_' + self.releaseExtent + '_DQM_' + self.extension
            print('path for location : %s' % self.path)
            sleep(self.t2s)
            return 6

def fonction_7(self):
    """REFERENCE folder extension :
    In a same form as for RELEASE extent, for some validations there can be some pbms with the path :
    without personalization, some validations such as tests for a new gcc version, or a ROOT one
    could be written into the same reference folder.
    In order to avoid that, we add an extension to personalize those paths.
"""
    screen_clear()
    #print('vous appelez la fonction 7')
    # web folder name customization
    # text to add into folder name for reference

    print('')
    text_to_prompt = "input a REFERENCE folder extension(hit return for none), [" + colorText('b', self.color) + "]ack or [" + colorText('q', self.color) +"]uit. ? "
    text_to_prompt += "                    [" + colorText('h', self.color) + "]elp - ["
    text_to_prompt += colorText('s', self.color) + "]tatus "  

    self.referenceExtent = get_answerText(self, text_to_prompt, 7) # get a text
    if (self.referenceExtent == 'h'):
        return 6
    elif (len(self.referenceExtent) == 0):
        print("no extension for reference.")
        self.logFile.write("7 - no extension for reference." + '\n')
        path = self.path + '/FullvsFull_' + self.reference[6:]
        print('path for location : %s' % path)
        sleep(self.t2s)
        return 7
    else:
        if (self.referenceExtent == 'back'):
            return 5
        else:
            print('extension for reference : %s' % self.referenceExtent)
            self.logFile.write('7 - extension for reference : %s' % self.referenceExtent + '\n')
            path = self.path + '/FullvsFull_' + self.reference[6:] + '_' + self.referenceExtent
            print('path for location : %s' % path)
            sleep(self.t2s)
            return 7

def fonction_8(self):
    """Comparison :
    here we define the type of comparison we want to make : Full vs Full, Fast vs Fast or Fast vs Full.
    This choice will be integrated into the full path where the web pages are saved.
    """
    screen_clear()
    #print('vous appelez la fonction 8')
    # comparison choice
    self.comparisonChoice = ['', '']
    print('which type of comparison do you want ? ')
    print_tab_4(self.comparisons, self.color_nb)
    text_to_prompt = "number of the comparison type, [" + colorText('b', self.color) + "]ack or [" + colorText('q', self.color) +"]uit. ? "
    text_to_prompt += "                    [" + colorText('h', self.color) + "]elp - ["
    text_to_prompt += colorText('s', self.color) + "]tatus "  

    self.comparisonChoice = get_answer3(self, text_to_prompt, self.comparisons, 8) #
    print('comparaisonChoice : ')
    print(self.comparisonChoice)
    self.logFile.write('8 - comparaisonChoice : %s vs %s' % (self.comparisonChoice[0], self.comparisonChoice[1] + '\n'))

    if self.comparisonChoice == '':
        self.comparisonChoice = ['', '']
        return 6
    elif self.comparisonChoice == 'h':
        self.comparisonChoice = ['', '']
        return 7
    else:
        if (len(self.referenceExtent) == 0):
            self.path += '/' + self.comparisonChoice[0] + 'vs' + self.comparisonChoice[1] + '_' + self.reference[6:]
        else:
            self.path += '/' + self.comparisonChoice[0] + 'vs' + self.comparisonChoice[1] + '_' + self.reference[6:] + '_' + self.referenceExtent
        print('complete path for location : %s' % self.path)
        self.logFile.write('8 - complete path for location : %s' % self.path + '\n')
        sleep(self.t2s)
        return 8

def fonction_9(self):
    """Validation :
    What sort of comparison do you want : standard RECO vs RECO or miniAOD, PU vs PU or pmx vs pmx, ... ?
    Note that for pmx & miniAOD, this choice is integrated into the complete path.
    Also note that if you chose RECO vs miniAOD or pmx vs PU, the REFERENCE becomes the RELEASE !
    """
    screen_clear()
    #print('vous appelez la fonction 9')
    # validation choice
    self.validationChoice = ['', '']
    print('which validation do you want ? ')
    print_tab_6(self.validations, self.color_nb, self.release, self.reference)
    text_to_prompt = "number of the validation type, [" + colorText('b', self.color) + "]ack or [" + colorText('q', self.color) +"]uit. ? "
    text_to_prompt += "                    [" + colorText('h', self.color) + "]elp - ["
    text_to_prompt += colorText('s', self.color) + "]tatus "  

    self.validationChoice = get_answer3(self, text_to_prompt, self.validations, 9) #
    self.logFile.write('9 - validationChoice : %s vs %s' % (self.validationChoice[0], self.validationChoice[1]) + '\n')

    if self.validationChoice == '':
        self.validationChoice = ['', '']
        return 7
    elif self.validationChoice == 'h':
            self.validationChoice = ['', '']
            return 8
    else:
        #print(self.validationChoice)
        if ( self.validationChoice[0] == 'RECO' and self.validationChoice[1] == 'miniAOD' ):
            self.reference = self.release
            self.referencesList_3 = self.releasesList_3
            self.logFile.write('9 - get the references list' + '\n')
            self.datasetsList_2 = self.datasetsList_1
            self.logFile.write('9 - get the datasets list' + '\n')
        if ( self.validationChoice[0] == 'pmx' and self.validationChoice[1] == 'PU' ):
            self.reference = self.release
            self.referencesList_3 = self.releasesList_3
            self.logFile.write('9 - get the references list' + '\n')
            self.datasetsList_2 = self.datasetsList_1
            self.logFile.write('9 - get the datasets list' + '\n')
        return 9

def fonction_10(self):
    """DATASETS :
    the base of the comparisons are the datasets. In the operations to be made we distinguish 2 sets of datasets.
    - default datasets : defined into the datasetqV.py file and used classically for the validations.
    Those default are presented with a number [0/1], 1 defining that the dataset is selected \"by default\" and 0 unselected.
    - common datasets : these are the datasets inherited from all the datasets common to the RELEASE and the REFERENCE.
    You can chose to use the default datasets (hit d), a lot of them (hit t) or chose some into the commons (hit c).
    For the 2 last choices, from the list you have to hit the numbers of the chosen datasets, separated by commas.
    """
    screen_clear()
    #print('vous appelez la fonction 10')
    # datasets choice
    print('Datasets to be compared : ')
    fieldname = 'DataSetsFilter_' + self.comparisonChoice[0] + 'vs' + self.comparisonChoice[1] + self.validationChoice[0]
    if self.validationChoice[1] == 'miniAOD':
        fieldname = 'DataSetsFilter_' + self.comparisonChoice[0] + 'vs' + self.comparisonChoice[1] + self.validationChoice[1]
    print('datasets default : %s' % fieldname)
    self.default_dataset = DataSetsFilter(self, fieldname)
    print_tab_3(self.default_dataset, self.color_nb)
    print('those with %s are not selected' % (colorText('0', 'blue')))
    print('those with %s are selected' % (colorText('1', self.color_nb)))
    text_to_prompt = "you can use the [" + colorText('d', self.color) + "]efault selected datasets, [" + colorText('b', self.color) + "]ack or [" + colorText('q', self.color) +"]uit.\n "
    text_to_prompt += "you can [" + colorText('t', self.color) + "]ake datasets from the list, or [" + colorText('c', self.color) + "]hose between the common datasets : "
    text_to_prompt += "                    [" + colorText('h', self.color) + "]elp - ["
    text_to_prompt += colorText('s', self.color) + "]tatus "  

    self.datasets = []
    self.dts = get_answer4(self, text_to_prompt) #
    #print(self.datasets)
    self.logFile.write('10 - get datasets' + '\n')
    if ( self.dts == ''): # back
        return 8
    elif (self.dts == 'h'):
        return 9
    elif ( self.dts == 't'): # default
        self.logFile.write('10 - peek datasets into default list' + '\n')
        function_101(self)
        self.logFile.write('10 - done' + '\n')
        return 10
    elif ( self.dts == 'c'): # default
        self.logFile.write('10 - choose datasets into common ones' + '\n')
        function_102(self)
        self.logFile.write('10 - done' + '\n')
        return 10
    elif ( self.dts == 'd'): # default
        print('d')
        for item in self.default_dataset:
            #print(item)
            self.logFile.write('10 - get datasets from default' + '\n')
            if item[1] == 1:
                self.datasets.append(item[0])
                self.logFile.write('10 - %s\n' % item[0])
        #print('datasets : ')
        #print(self.datasets)
        return 10

    #return 10

def function_101(self):
    """DEFAULT DATASETS :
    into this list, chose the datasets by their number, separated by commas.
    then hit return.
    """
    #screen_clear()
    #print('vous appelez la fonction 101')
    print('Select from default datasets : ')
    print_tab_3(self.default_dataset, self.color_nb) # all datasets with same color
    text_to_prompt = "enter the numbers of the datasets you want, separated by commas : "
    #text_to_prompt += "                    [" + colorText('h', self.color) + "]elp - ["
    #text_to_prompt += colorText('s', self.color) + "]tatus "
    numbers = get_answer10X(text_to_prompt, self.default_dataset)
    #print(numbers)
    self.datasets = []
    for i in numbers:
        self.datasets.append(str(self.default_dataset[i][0]))
        self.logFile.write('101 - %s\n' % str(self.default_dataset[i][0]))
    #print('datasets 101 : ')
    #print(self.datasets)
    return

def function_102(self):
    """COMMON DATASETS :
    into this list, chose the datasets by their number, separated by commas.
    then, hit return.
    """
    screen_clear()
    #print('vous appelez la fonction 102')

    # perhaps make a test if len(commonDatasets) = 0 !
    print('Select from common datasets : ')
    self.commonDatasets = set(self.datasetsList_1).intersection(set(self.datasetsList_2))
    self.commonDatasets = list(self.commonDatasets) # get the common datasets for the comparisons
    print_tab_1(self.commonDatasets, self.color) # all datasets with same color
    text_to_prompt = "enter the numbers of the datasets you want, separated by commas : "
    #text_to_prompt += "                    [" + colorText('h', self.color) + "]elp - ["
    #text_to_prompt += colorText('s', self.color) + "]tatus "
    numbers = get_answer10X(text_to_prompt, self.commonDatasets)
    for i in numbers:
        self.datasets.append(str(self.commonDatasets[i]))
        self.logFile.write('102 - %s\n' % str(self.commonDatasets[i]))
    #print('datasets 102 : ')
    #print(self.datasets)
    return

def fonction_11(self):
    """Global Tag selection for RELEASE :
    We can extract some ROOT files which are coherent with the precedent choices.
    From those files, we can extract the Global Tags.
    Be careful in this list, there is no precision for GT for 2021 or PHASE2 validations.
    This function is clearly made for a Full vs Full validation since no datasets are useful for Fast vs Fast/Full validations.
    This will be updated next year.
    """
    screen_clear()
    #print('vous appelez la fonction 11')
    self.releasesGT = []
    self.referencesGT = []
    self.relRootFilesList = []
    self.refRootFilesList = []
    self.releasesList_4 = []  # root files list for release
    self.referencesList_4 = []  # root files list for reference

    # get the self.releasesList_4/self.referencesList_4 lists of root files
    print('ROOT files extraction')
    rootFilesExtraction(self)
    self.logFile.write('11 - ROOT files extraction OK' + '\n')

    # extract to keep only for comparison choice
    #print('comparison choice for release')
    #for elem in self.releasesList_4:
    #    print(elem)
    #    if re.search('Fast', elem[i]):
    #        print(elem)
    #print('comparison choice for reference')
    #for elem in self.referencesList_4:
    #    print(elem)
    #    if re.search('Fast', elem[i]): # must be searched with _13 extension & not _14 !
    #        print(elem)

    # extract to keep only for validation choice
    #print('validation choice for release')
    self.releasesList_5 = getFilesList(self, self.releasesList_4) # tmp_list_rel
    #print('validation choice for reference')
    self.referencesList_5 = getFilesList(self, self.referencesList_4) # tmp_list_ref

    # get the self.releasesGT/self.referencesGT lists for GT
    print('GT extraction')
    GlobalTagsExtraction(self)
    self.logFile.write('11 - GT extraction OK' + '\n')

    # rewrite GT list in a more convenient way
    self.logFile.write('11 - rewrite GT list in a more convenient way' + '\n')
    tmp_GT = []
    for elem in self.releasesGT:
        for i in range(1, len(elem)):
            tmp_GT.append(elem[i])
    #print('GT releases')
    tmp_GT_rel = sorted(set(tmp_GT))
    self.GT_rel = []
    for elem in tmp_GT_rel:
        tmp = []
        tmp.append(elem)
        for item1 in self.releasesGT:
            for i in range(1, len(item1)):
                if item1[i] == elem:
                    tmp.append(item1[0])
        self.GT_rel.append(tmp)
    #print(self.GT_rel)
    # reduce the list to kept only those corresponding to ALL datasets
    self.logFile.write('11 - reduce the list to kept only those corresponding to ALL datasets' + '\n')    
    tt_rel = []
    for elem in self.GT_rel:
        if len(elem[1:]) == len(self.datasets):
            tt_rel.append(elem)
    self.GT_rel = tt_rel
    #print(self.GT_rel)

    tmp_GT = []
    for elem in self.referencesGT:
        for i in range(1, len(elem)):
            tmp_GT.append(elem[i])
    #print('GT references')
    tmp_GT_ref = sorted(set(tmp_GT))
    self.GT_ref = []
    for elem in tmp_GT_ref:
        tmp = []
        tmp.append(elem)
        for item1 in self.referencesGT:
            for i in range(1, len(item1)):
                if item1[i] == elem:
                    tmp.append(item1[0])
        self.GT_ref.append(tmp)
    #print(self.GT_ref)
    # reduce the list to kept only those corresponding to ALL datasets
    self.logFile.write('11 - reduce the list to kept only those corresponding to ALL datasets' + '\n')
    tt_ref = []
    for elem in self.GT_ref:
        if len(elem[1:]) == len(self.datasets):
            tt_ref.append(elem)
    self.GT_ref = tt_ref
    #print(self.GT_ref)

    if len(self.GT_rel) == 0 or len(self.GT_ref) == 0 :
        print(colorText('len(self.GT_rel) == 0 or len(self.GT_ref) == 0', 'red'))
        return 9 # back to datasets choice

    print('Choose a GT for %s from the list below ' % self.release)
    print_tab_5(self.GT_rel, self.color_nb)
    text_to_prompt = "get a RELEASE GT number, [" + colorText('b', self.color) + "]ack or [" + colorText('q', self.color) +"]uit. ? "
    text_to_prompt += "                    [" + colorText('h', self.color) + "]elp - ["
    text_to_prompt += colorText('s', self.color) + "]tatus "  
    GT = get_answer6(self, text_to_prompt, self.GT_rel, 11)  #
    if ( GT == ''): # back
        return 9
    elif ( GT == 'h'):
        return 10
    else:
        self.GT_rel = GT
        for elem in self.releasesList_5:
            for i in range(1, len(elem)):
                if re.search(self.GT_rel, elem[i]):
                    #print(elem[i])
                    self.relRootFilesList.append(elem[i])
                    self.logFile.write('11 - get the GT list for release' + '\n')
        return 11

def fonction_12(self):
    """Global Tag selection for REFERENCE :
    Same as for RELEASE Global Tags.
    Be careful in this list, there is no precision for GT for 2021 or PHASE2 validations.
    """
    screen_clear()
    #print('vous appelez la fonction 12')

    print('Choose a GT for %s from the list below ' % self.reference)
    print_tab_5(self.GT_ref, self.color_nb)
    text_to_prompt = "get a REFERENCE GT number, [" + colorText('b', self.color) + "]ack or [" + colorText('q', self.color) +"]uit. ? "
    text_to_prompt += "                    [" + colorText('h', self.color) + "]elp - ["
    text_to_prompt += colorText('s', self.color) + "]tatus "  
    GT = get_answer6(self, text_to_prompt, self.GT_ref, 12)  #
    if ( GT == ''): # back
        return 10
    elif (GT == 'h'):
        return 11
    else:
        self.GT_ref = GT
        #print('GT = %s' % GT)
        #print(GT)
        for elem in self.referencesList_5:
            for i in range(1, len(elem)):
                if re.search(GT, elem[i]):
                    #print(elem[i])
                    self.refRootFilesList.append(elem[i])
                    self.logFile.write('12 - get the GT list for reference' + '\n')
        return 12

def fonction_13(self):
    """Decision Box :
    a dev module which use a decision box tools for ZEE.
    This tool use some Kolmogorov tests and produce some pictures (3x those of the ZEE web page !) which can be used for validation control.
    """
    screen_clear()
    #print('vous appelez la fonction 13')
    # DB Flag choice
    if testZEE(self.datasets):
        text_to_prompt= "use Decision Box for ZEE, [" + colorText('y', self.color) + "]es/[" + colorText('n', self.color) + "o] [" + colorText('b', self.color) + "]ack or [" + colorText('q', self.color) +"]uit. ? "
        text_to_prompt += "                    [" + colorText('h', self.color) + "]elp - [" 
        text_to_prompt += colorText('s', self.color) + "]tatus "  
        DB_flag = get_answer5(self, text_to_prompt, 13) #
    else:
        DB_flag = 'n'

    if DB_flag == '':
        return 10 # back to RELEASE GT number because there is some modifications in the GT arrays
    elif DB_flag == 'h':
        return 12
    elif DB_flag == 'y':
        self.DB_flags = []
        for item in self.datasets:
            if item != 'ZEE_14':
                self.DB_flags.append(False)
            else:
                self.DB_flags.append(True)
                self.logFile.write('13 - set a DB flag for ZEE' + '\n')
        return 13
    elif DB_flag == 'n':
        self.DB_flags = []
        for i in range(0, len(self.datasets)):
            self.DB_flags.append(False)
            self.logFile.write('13 - no GT at all' + '\n')
        return 13

def fonction_14(self):
    """SUMMARY :
    display (as the \'status\' function the summary of all the choices.
    """
    screen_clear()
    #print('vous appelez la fonction 14')
    # Summary

    displaySummary(self)
    sleep(self.t2s)
    text_to_prompt = "[" + colorText('c', self.color) + "]ontinue, [" + colorText( 'b', self.color) + "]ack or [" + colorText('q', self.color) +"]uit. ? "
    answer_14 = get_answer2(text_to_prompt)
    if answer_14 == 'b': # back
        self.gev_tmp = [] # to be sure that gev_temp is empty
        return 12
    else: # must have only 2 answers
        # include the differents choices into Gev
        self.gev_tmp.append([str(self.release), str(self.reference)])
        self.gev_tmp.append([str(self.releaseExtent), str(self.referenceExtent)])
        self.gev_tmp.append(str(self.datasets))
        self.gev_tmp.append(str(self.comparisonChoice[0] + 'vs' + self.comparisonChoice[1]))
        self.gev_tmp.append(str(self.validationChoice))
        self.gev_tmp.append([str(self.release) + '-' + str(self.GT_rel), str(self.reference) + '-' + str(self.GT_ref)])
        self.gev_tmp.append(str(self.DB_flags))
        print(self.gev_tmp)
        self.Gev.append(self.gev_tmp)
        self.logFile.write('14 - save in RAM the set of validation' + '\n')

        return 14

def fonction_15(self):
    """NEW SET :
    asking for a new set of choices for validation. We can made a lot of validations
    such as RECO vs RECO, RECO vs miniAOD and PU vs PU for a couple of (RELEASE/REFERENCE) for one case,
    and others tests for another case.
    """
    screen_clear()
    #print('vous appelez la fonction 15')
    # New set ?
    text_to_prompt = "Adding another set of validation ?, [" + colorText('y', self.color) + "]es/["
    text_to_prompt += colorText('n', self.color) + "o], [" + colorText( 'b', self.color)
    text_to_prompt += "]ack or [" + colorText('q', self.color) + "]uit. ? "
    text_to_prompt += "                    [" + colorText('h', self.color) + "]elp"
    answer4new = get_answer5(self, text_to_prompt, 15)  #
    print('answer for new set : %s' % answer4new)
    if answer4new == '': # back
        self.Gev = self.Gev[:-1]
        return 12
    elif answer4new == 'h':
        return 14
    elif answer4new == 'y': # back to release choice
        self.logFile.write('15 - ask for a new set of validation' + '\n')
        return 1
    elif answer4new == 'n': # so we close after writing into config file
        if self.configFile:
            print('config file OK for writing')
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
                self.configFile.write('# personalization ' + str(ind + 1) + '\n')
                self.configFile.write('GeV_' + str(ind + 1) + ' = [\n')
                self.configFile.write(str(unicode(elem[0])) + ' , # release/reference\n')
                self.configFile.write(str(elem[1]) + ' , # relref_extent\n')
                self.configFile.write(str(elem[2]) + ' , # datasets\n')
                self.configFile.write('\'' + str(elem[3]) + '\' , # choice\n')
                self.configFile.write(str(elem[4]) + ' , # relrefValtype RECO vs RECO\n')
                self.configFile.write(str(elem[5]) + ' , # GT one couple rel/ref for all dataset\n')
                self.configFile.write('[\'\', \'\'] , # relref files one couple rel/ref for each dataset\n')
                self.configFile.write(str(self.DB_flags) + ', # DB flag\n')
                self.configFile.write(']\n')
                ind += 1
            self.logFile.write('15 - write into config.py file' + '\n')
	    self.configFile.write('#############################################################################\n')
            self.configFile.write('\n')
        else:
            print('no config file open')
            exit()
        return 15

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

def displaySummary(self):
    # Summary
    print('SUMMARY : ')
    text_to_prompt = 'RELEASE : ' + colorText(self.release, 'blue') + ' - REFERENCE : ' + colorText(self.reference, 'blue')
    print(text_to_prompt)
    text_to_prompt = 'release extension : \'' + colorText(self.releaseExtent, 'blue') + '\' - reference extension : \'' + colorText(self.referenceExtent, 'blue') + '\''
    print(text_to_prompt)
    print('Datasets : ' + ' '.join("{:s}".format(colorText(x, 'blue')) for x in self.datasets))
    print('Comparison choice : %s vs %s' % (colorText(str(self.comparisonChoice[0]), 'blue'), colorText(str(self.comparisonChoice[1]), 'blue')))
    print('Validation type : %s vs %s' % (colorText(str(self.validationChoice[0]), 'blue'), colorText(str(self.validationChoice[1]), 'blue')))
    print('Global Tag[s] : %s - %s' %(self.GT_rel, self.GT_ref))
    print('%s list of the ROOT files : ' % colorText(self.release, 'blue'))
    for elem in self.relRootFilesList:
        print(elem)
    print('%s list of the ROOT files : ' % colorText(self.reference, 'blue'))
    for elem in self.refRootFilesList:
        print(elem)
    print('')
    return

def displaySummary2(self):
    # Summary
    statusText = 'SUMMARY : \n'
    statusText += 'RELEASE : ' + self.release + ' - REFERENCE : ' + self.reference + '\n'
    statusText += 'release extension : \'' + self.releaseExtent + '\' - reference extension : \'' + self.referenceExtent + '\'' + '\n'
    statusText += 'Datasets : ' + ' '.join("{:s}".format(x) for x in self.datasets)
    statusText += 'Comparison choice : %s vs %s' % (str(self.comparisonChoice[0]), str(self.comparisonChoice[1])) + '\n'
    statusText += 'Validation type : %s vs %s' % (str(self.validationChoice[0]), str(self.validationChoice[1])) + '\n'
    statusText += 'Global Tag[s] : %s - %s' %(self.GT_rel, self.GT_ref) +'\n'
    statusText += '%s list of the ROOT files : ' % self.release + '\n'
    for elem in self.relRootFilesList:
        statusText += elem + '\n'
    statusText += '%s list of the ROOT files : ' % self.reference +'\n'
    for elem in self.refRootFilesList:
        statusText += elem + '\n'
    statusText += '' + '\n'

    return statusText
