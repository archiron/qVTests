#! /usr/bin/env python
#-*-coding: utf-8 -*-

import os,sys,subprocess, shutil
import re
from time import sleep
import numpy as np

sys.path.append('/afs/cern.ch/user/a/archiron/lbin/ChiLib')

from networkFunctions import list_search_1, cmd_load_files
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
    #print('release : ', release)
    for t in tab_files:
        #print('t : ', t)
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
        if ( re.search(release, t) ):
            #tt = explode_item(t)
            #temp.append(tt[0])
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

    #print('item : ', item)
    temp_item = item[22:] # DQM_V0001_R000000001__ removed
    #print('item 22 : ', temp_item)
    temp_item = temp_item[:-12] # __DQMIO.root removed
    #print('item -12 : ', temp_item)
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
    #print("Number of columns and Rows: ", self.terminal_size())
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
    return tw, th

def affiche_1(i, tab, color): # not used
    #print('%50s [%2d]' % (tab[i], i))
    print('%50s [%s]' % (tab[i], colorText(str(i), color)))

def affiche_2(i, tab, color): # not used
    #print('%50s [%2d] %50s [%2d]' % (tab[i], i, tab[i+1], i+1))
    print('%50s [%s] %50s [%s]' % ( tab[i], colorText(str(i), color), tab[i+1], colorText(str(i+1), color) ) )

def affiche_3(i, tab, color): # not used
    #print('%50s [%2d] %50s [%2d] %50s [%2d]' % (tab[i], i, tab[i+1], i+1, tab[i+2], i+2))
    print('%50s [%s] %50s [%s] %50s [%s]' % ( tab[i], colorText(str(i), color), tab[i+1], colorText(str(i+1), color), tab[i+2], colorText(str(i+2), color) ) )

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

def print_tab_3(tab, color): # only for datasets
    print('')

    for i in range(0, len(tab), 2):
        #print( tab[i][0], str(tab[i][1]) )
        #print( tab[i+1][0], str(tab[i+1][1]) )
        color0 = color
        color1 = color
        if ( tab[i][1] == 0):
            color0 = 'blue'
        if ( tab[i+1][1] == 0):
            color1 = 'blue'
        print('%40s [%s] %40s [%s]' % (tab[i][0], colorText(str(tab[i][1]), color0), tab[i+1][0], colorText(str(tab[i+1][1]), color1)))

def print_tab_2(tab, color): # only for tab with 2 elements
    print('')
    for i in range(0, len(tab)):
        #print(' [%d] %50s' % (i, tab[i]))
        print('[%s] %50s' % (colorText(str(i), color), tab[i]))

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
                print('%50s [%2d]' % (tab[i], i))
            else: #
                affiche_2(i, tab, color)

def colorText(sometext, color):
    return '\033' + changeColor(color) + sometext + '\033[0m'

def createDTSname(self, it_comp, it_val):
    name = ''
    print('it_comp : %s - it_val : %s' % (it_comp, it_val))
    name = 'DataSetsFilter_' + it_comp + it_val

    from datasetsqV import DataSetsFilter
    try:
        table = DataSetsFilter(self, name)
        return table
    except:
        print('pas de module %s' % name)
    return

def get_answerText(text2prompt):
    quitLoop = True
    print('')
    while ( quitLoop ):
        rel = raw_input(text2prompt)
        #rel = input(text2prompt)  # Python 3
        if rel == 'q':
            exit()
        elif rel == 'b':
            quitLoop = False
            text = 'back'
        else:
            print('vous avez tapé : %s' % rel)
            quitLoop = False
            text = rel

    return text

def get_answer1(text2prompt, tab1, tab2):
    quitLoop = True
    print('')
    while ( quitLoop ):
        rel = raw_input(text2prompt)
        #rel = input(text2prompt)  # Python 3
        if rel == 'q':
            exit()
        else:
            print('vous avez tapé : %s' % rel)
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

def get_answer2(text2prompt, tab):
    quitLoop = True
    print('')
    while ( quitLoop ):
        rel = raw_input(text2prompt)
        #rel = input(text2prompt)  # Python 3
        if rel == 'q':
            exit()
        else:
            print('vous avez tapé : %s' % rel)
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

def get_answer3(text2prompt, tab):
    quitLoop = True
    print('')
    while ( quitLoop ):
        rel = raw_input(text2prompt)
        #rel = input(text2prompt)  # Python 3
        if rel == 'q':
            exit()
        elif rel == 'b':
            quitLoop = False
            temp = ''
        else:
            print('vous avez tapé : %s' % rel)
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

def get_answer4(text2prompt):
    quitLoop = True
    print('')
    while ( quitLoop ):
        rel = raw_input(text2prompt)
        #rel = input(text2prompt)  # Python 3
        if rel == 'q':
            exit()
        elif rel == 'b':
            quitLoop = False
            temp = ''
        elif rel == 'd':
            quitLoop = False
            temp = 'd'
        elif rel == 'a':
            quitLoop = False
            temp = 'a'
        elif rel == 'c':
            quitLoop = False
            temp = 'c'
        else:
            print('vous avez tapé : %s' % rel)

    return temp

def get_answer5(text2prompt):
    quitLoop = True
    print('')
    while ( quitLoop ):
        rel = raw_input(text2prompt)
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
        else:
            print('vous avez tapé : %s' % rel)

    return temp

def check_comparisonChoice(self, t1, t2, it_comp, t_choice):
    #print('tablo : %s' % t1)
    if ((len(t1 )>0) and (len(t1)<=len(t2))):
        #print('longueurs OK')
        temp = []
        for it in t1:
            #print(it)
            irel = ''
            try:
                irel = int(it)
                print(type(it))
                print(type(irel))
                if ( irel >= 0 and irel < len(t2) ):
                    # test with lengths of lists (self.rel_Full, self.ref_Fast, self.rel_PU, ...)
                    if t_choice == 'val':
                        a = check_listLengths(self, t2[irel], it_comp)
                        print(a)
                        if a[0]:
                            temp.append(t2[irel])
                        else:
                            print('no enough file for %s comparison, re[%d] - ref[%d]' % (t2[irel], a[1], a[2]))
                    else:
                        temp.append(t2[int(it)])
                else:
                    print('%d is not into the range [0:%d]' % (irel, len(t2)-1))
                # need to  test if all nbs are differents
            except:
                print('%s is not a number in check_comparisonChoice for %s' % (it, t_choice))
        temp = np.unique(temp)
    else:
        print('lengths does not match')
        print('t1 : %d - t2 : %d' % (len(t1), len(t2)))
    return temp

def get_comparisonAnswer(self, text2prompt, tab, it_comp, t_choice): # not used ?
    quitLoop = True
    while ( quitLoop ):
        rel = raw_input(text2prompt)
        #rel = input(text2prompt)  # Python 3
        if rel == 'q':
            exit()
        elif rel == 'b':
            quitLoop = False
            tabl = []
        else:
            quitLoop = False
            tablo = extractFrom(rel)
            tabl = check_comparisonChoice(self, tablo, tab, it_comp, t_choice)
            print(tabl)

    return tabl

def extractFrom(nb):
    print(nb)
    t = []
    for i in range(0, len(nb)):
        t.append(nb[i])
    return t

def fonction_1(self):
    screen_clear()
    print('vous appelez la fonction 1')
    print_tab_2(self.web_location, self.color_nb)
    #print('==')

    text_to_prompt= "number of the folder choice or [" + colorText('q', self.color) +"]uit. ? "
    self.location, self.extension = get_answer1(text_to_prompt, self.web_location, self.web_extension)
    print('WEB LOCATION : %s' % colorText(self.location, 'blue')) # now we have the web folder location
    #self.gev_tmp.append(self.location) # seems to be inefficient
    sleep(1)
    return 1

def fonction_2(self):
    screen_clear()
    print('vous appelez la fonction 2')
    # get the list for RELEASE
    print_tab_1(self.list_0, self.color_nb)

    text_to_prompt= "number of the RELEASE family or [" + colorText('q', self.color) +"]uit. ? "
    self.releaseFamily = get_answer3(text_to_prompt, self.list_0)
    print('RELEASE FAMILY : %s' % colorText(self.releaseFamily, 'blue')) # now we have the release family
    sleep(1)

    # here we get the release list

    self.releasesList_1 = list_search_1(self.releaseFamily) # all the releases
    print('there is %d files for %s' % (len(self.releasesList_1), self.releaseFamily))
    self.releaseFamily2 = self.releaseFamily[:-1] # not used ?

    self.releasesList_2 = sub_releases(self.releasesList_1) # extract the releases CMSSW_X_Y_Z...
    #for item in self.releasesList_2:
    #    print(item)

    return 2

def fonction_3(self):
    screen_clear()
    print('vous appelez la fonction 3')
    print_tab_1(self.releasesList_2, self.color_nb)
    text_to_prompt= "number of the RELEASE, [" + colorText('b', self.color) + "]ack or [" + colorText('q', self.color) +"]uit. ? "
    self.release = get_answer3(text_to_prompt, self.releasesList_2)

    if self.release != '':
        print('RELEASE : %s' % self.release) # now we have the release

        print('')
        self.releasesList_3 = sub_releases3(self.release, self.releasesList_1) # extract the list of the root files for the chosen release
        self.datasetsList_1 = sub_releases2(self.release, self.releasesList_3) # extract the datasets of the root files for the chosen release
        return 3
    else:
        return 1

def fonction_4(self):
    screen_clear()
    print('vous appelez la fonction 4')
    text_to_prompt= "Reference family for the validation "
    print(text_to_prompt)  #

    # get the list for REFERENCE
    print_tab_1(self.list_0, self.color_nb)

    text_to_prompt= "number of the REFERENCE family, [" + colorText('b', self.color) + "]ack or [" + colorText('q', self.color) +"]uit. ? "
    self.referenceFamily = get_answer3(text_to_prompt, self.list_0)
    if self.referenceFamily != '':
        print('REFERENCE FAMILY : %s' % colorText(self.referenceFamily, 'blue')) # now we have the reference family
        sleep(1)

        # here we get the reference list

        self.referencesList_1 = list_search_1(self.referenceFamily) # all the references
        print('there is %d files for %s' % (len(self.referencesList_1), self.referenceFamily))
        self.referenceFamily2 = self.referenceFamily[:-1] # not used ?

        self.referencesList_2 = sub_releases(self.referencesList_1) # extract the references CMSSW_X_Y_Z...
        return 4
    else:
        return 2

def fonction_5(self):
    screen_clear()
    print('vous appelez la fonction 5')
    print_tab_1(self.referencesList_2, self.color_nb)
    text_to_prompt= "number of the REFERENCE, [" + colorText('b', self.color) + "]ack or [" + colorText('q', self.color) +"]uit. ? "
    self.reference = get_answer3(text_to_prompt, self.referencesList_2)

    if self.reference != '':
        print('REFERENCE : %s' % self.reference) # now we have the reference
        print('')
        self.referencesList_3 = sub_releases3(self.reference, self.referencesList_1) # extract the list of the root files for the chosen reference
        self.datasetsList_2 = sub_releases2(self.reference, self.referencesList_3) # extract the datasets of the root files for the chosen reference
        return 5
    else:
        return 3

def fonction_6(self):
    screen_clear()
    print('vous appelez la fonction 6')
    # web folder name customization
    # text to add into folder name for release

    print('')
    text_to_prompt= "input a RELEASE folder extension (hit return for none), [" + colorText('b', self.color) + "]ack or [" + colorText('q', self.color) +"]uit. ? "

    self.releaseExtent = get_answerText(text_to_prompt) # get a text
    if (len(self.releaseExtent) == 0):
        print("no extension for release.")
        return 6
    else:
        if (self.releaseExtent == 'back'):
            return 4
        else:
            print('extension for release : %s' % self.releaseExtent)
            return 6

def fonction_7(self):
    screen_clear()
    print('vous appelez la fonction 7')
    # web folder name customization
    # text to add into folder name for reference

    print('')
    text_to_prompt= "input a REFERENCE folder extension(hit return for none), [" + colorText('b', self.color) + "]ack or [" + colorText('q', self.color) +"]uit. ? "

    self.referenceExtent = get_answerText(text_to_prompt) # get a text
    if (len(self.referenceExtent) == 0):
        print("no extension for reference.")
        return 7
    else:
        if (self.referenceExtent == 'back'):
            return 5
        else:
            print('extension for reference : %s' % self.referenceExtent)
            return 7

def fonction_8(self):
    screen_clear()
    print('vous appelez la fonction 8')
    # comparison choice
    print_tab_1(self.comparisons, self.color_nb)
    text_to_prompt= "number of the comparison type, [" + colorText('b', self.color) + "]ack or [" + colorText('q', self.color) +"]uit. ? "

    self.comparisonChoice = get_answer3(text_to_prompt, self.comparisons) #

    return 8

def fonction_9(self):
    screen_clear()
    print('vous appelez la fonction 9')
    # validation choice
    print_tab_1(self.validations, self.color_nb)
    text_to_prompt= "number of the validation type, [" + colorText('b', self.color) + "]ack or [" + colorText('q', self.color) +"]uit. ? "

    self.validationChoice = get_answer3(text_to_prompt, self.validations) #

    return 9

def fonction_10(self):
    screen_clear()
    print('vous appelez la fonction 10')
    # datasets choice
    fieldname = 'DataSetsFilter_' + self.comparisonChoice + self.validationChoice
    print('datasets default')
    self.default_dataset = DataSetsFilter(self, fieldname)
    print_tab_3(self.default_dataset, self.color_nb)
    print('those with %s are not selected' % (colorText('0', 'blue')))
    print('those with %s are selected' % (colorText('1', self.color_nb)))
    text_to_prompt = "you can use the [" + colorText('d', self.color) + "]efault selected datasets, [" + colorText('b', self.color) + "]ack or [" + colorText('q', self.color) +"]uit.\n "
    text_to_prompt += "you can [" + colorText('a', self.color) + "]dd datasets from those non selected, or [" + colorText('c', self.color) + "]hose between the common datasets : "

    self.dts = get_answer4(text_to_prompt) #
    if ( self.dts == ''): # back
        return 9
    elif ( self.dts == 'a'): # default
        return 10
    elif ( self.dts == 'c'): # default
        return 10
    elif ( self.dts == 'd'): # default
        self.datasets = []
        for item in self.default_dataset:
            if item[1] == 1:
                self.datasets.append(item[0])
        print('datasets : ')
        print(self.datasets)
        return 10

    return 10

def fonction_11(self):
    screen_clear()
    print('vous appelez la fonction 11')
    # add dataset from defaults
    #print_tab_1(self.validations, self.color_nb)
    #text_to_prompt= "number of the validation type, [" + colorText('b', self.color) + "]ack or [" + colorText('q', self.color) +"]uit. ? "

    #self.validationChoice = get_answer3(text_to_prompt, self.validations) #

    return 11

def fonction_12(self):
    screen_clear()
    print('vous appelez la fonction 12')
    # DB Flag choice
    if testZEE(self.datasets):
        text_to_prompt= "use Decision Box for ZEE, [" + colorText('y', self.color) + "]es/[" + colorText('n', self.color) + "o] [" + colorText('b', self.color) + "]ack or [" + colorText('q', self.color) +"]uit. ? "
        DB_flag = get_answer5(text_to_prompt) #
        print('DB flag : %s' % DB_flag)
    else:
        DB_flag = 'n'

    if DB_flag == '':
        return 9
    elif DB_flag == 'y':
        for item in self.datasets:
            if item != 'ZEE_14':
                self.DB_flags.append('False')
            else:
                self.DB_flags.append('True')
        return 12
    elif DB_flag == 'n':
        for i in range(0, len(self.datasets)):
            self.DB_flags.append('False')
        return 12

def getFilesList(self):
    # case release
    self.rel_FullRECO, self.rel_FullPU, self.rel_Fullpmx, self.rel_FastRECO, self.rel_FastPU, self.rel_Fastpmx = extractFilesList(self.releasesList_3)
    # case reference
    self.ref_FullRECO, self.ref_FullPU, self.ref_Fullpmx, self.ref_FastRECO, self.ref_FastPU, self.ref_Fastpmx = extractFilesList(self.referencesList_3)
    print('len rel_FullRECO : %d - len ref_Full : %d' % (len(self.rel_FullRECO), len(self.ref_FullRECO)))
    print('len rel_FullPU : %d - len ref_FullPU : %d' % (len(self.rel_FullPU), len(self.ref_FullPU)))
    print('len rel_Fullpmx : %d - len ref_Fullpmx : %d' % (len(self.rel_Fullpmx), len(self.ref_Fullpmx)))
    print('len rel_FastRECO : %d - len ref_FastRECO : %d' % (len(self.rel_FastRECO), len(self.ref_FastRECO)))
    print('len rel_FastPU : %d - len ref_FastPU : %d' % (len(self.rel_FastPU), len(self.ref_FastPU)))
    print('len rel_Fastpmx : %d - len ref_Fastpmx : %d' % (len(self.rel_Fastpmx), len(self.ref_Fastpmx)))

    return

def extractFilesList(tab):
    temp_Fast = []
    temp_FastallPU = []
    temp_FastPU = []
    temp_FastRECO = []
    temp_Fastpmx = []
    temp_noFast = []
    temp_allPU = []
    temp_FullRECO = []
    temp_FullPU = []
    temp_Fullpmx = []

    for it in tab:
        if ( re.search('fast', it) or re.search('Fast', it)):
            temp_Fast.append(it)
        else: # no Fast
            temp_noFast.append(it)
    for it in temp_noFast:
        if ( re.search('PU', it) and not re.search('NoPU', it) ):
            temp_allPU.append(it)
        else: # no Fast
            temp_FullRECO.append(it)
    for it in temp_allPU:
        if ( re.search('pmx', it) or re.search('Pmx', it)):
            temp_Fullpmx.append(it)
        else: # no Fast
            temp_FullPU.append(it)
    for it in temp_Fast:
        if ( re.search('PU', it) and not re.search('NoPU', it) ):
            temp_FastallPU.append(it)
        else: # no Fast
            temp_FastRECO.append(it)
    for it in temp_FastallPU:
        if ( re.search('pmx', it) or re.search('Pmx', it)):
            temp_Fastpmx.append(it)
        else: # no Fast
            temp_FastPU.append(it)
    return temp_FullRECO, temp_FullPU, temp_Fullpmx, temp_FastRECO, temp_FastPU, temp_Fastpmx

def check_listLengths(self, value, it_comp):
    print('value to test : %s' % value)
    print('len rel_FullRECO : %d - len ref_Full : %d' % (len(self.rel_FullRECO), len(self.ref_FullRECO)))
    print('len rel_FullPU : %d - len ref_FullPU : %d' % (len(self.rel_FullPU), len(self.ref_FullPU)))
    print('len rel_Fullpmx : %d - len ref_Fullpmx : %d' % (len(self.rel_Fullpmx), len(self.ref_Fullpmx)))
    print('len rel_FastRECO : %d - len ref_FastRECO : %d' % (len(self.rel_FastRECO), len(self.ref_FastRECO)))
    print('len rel_FastPU : %d - len ref_FastPU : %d' % (len(self.rel_FastPU), len(self.ref_FastPU)))
    print('len rel_Fastpmx : %d - len ref_Fastpmx : %d' % (len(self.rel_Fastpmx), len(self.ref_Fastpmx)))
    # WARNING : must be identical to validations list in the default.py file
    if value == 'RECO':
        if it_comp == 'FullvsFull':
            l1 = len(self.rel_FullRECO)
            l2 = len(self.ref_FullRECO)
        elif it_comp == 'FastvsFast':
            l1 = len(self.rel_FastRECO)
            l2 = len(self.ref_FastRECO)
        else: # FastvsFull
            l1 = len(self.rel_FastRECO)
            l2 = len(self.ref_FullRECO)
    elif value == 'PU25':
        if it_comp == 'FullvsFull':
            l1 = len(self.rel_FullPU)
            l2 = len(self.ref_FullPU)
        elif it_comp == 'FastvsFast':
            l1 = len(self.rel_FastPU)
            l2 = len(self.ref_FastPU)
        else: # FastvsFull
            l1 = len(self.rel_FastPU)
            l2 = len(self.ref_FullPU)
    elif value == 'PUpmx25':
        if it_comp == 'FullvsFull':
            print('OK')
            l1 = len(self.rel_Fullpmx)
            l2 = len(self.ref_Fullpmx)
            print(l1, l2)
        elif it_comp == 'FastvsFast':
            l1 = len(self.rel_Fastpmx)
            l2 = len(self.ref_Fastpmx)
        else: # FastvsFull
            l1 = len(self.rel_Fastpmx)
            l2 = len(self.ref_Fullpmx)
    print('[l1, l2] : [%d, %d]' % (l1, l2))
    if l1*l2 > 0:
        return [True, l1, l2]
    else:
        return [False, l1, l2]

def testZEE(tab):
    test = False
    for item in tab:
        if item == 'ZEE_14':
            test = 'True'
    return test
