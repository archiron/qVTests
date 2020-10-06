#! /usr/bin/env python
#-*-coding: utf-8 -*-

import os,sys,subprocess, shutil
import re
from time import sleep
import numpy as np

sys.path.append('/afs/cern.ch/user/a/archiron/lbin/ChiLib')

from networkFunctions import list_search_1, cmd_load_files

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

def affiche_1(i, tab): # not used
    print('%50s [%2d]' % (tab[i], i))

def affiche_2(i, tab): # not used
    print('%50s [%2d] %50s [%2d]' % (tab[i], i, tab[i+1], i+1))

def affiche_3(i, tab): # not used
    print('%50s [%2d] %50s [%2d] %50s [%2d]' % (tab[i], i, tab[i+1], i+1, tab[i+2], i+2))

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
    else:
        return '[30m'

def print_tab(tab):
    print('')
    if ((len(tab) % 2) == 0):
        for i in range(0, len(tab), 2):
            affiche_2(i, tab)
    elif ((len(tab) % 3) == 0):
        for i in range(0, len(tab), 3):
            affiche_3(i, tab)
    else: # general case
        for i in range(0, len(tab), 2):
            if (i+1 == len(tab)):
                print('%50s [%2d]' % (tab[i], i))
            else: # 
                affiche_2(i, tab)

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

def get_answer1(text2prompt, tab):
    quitLoop = True
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

def get_answer2(text2prompt, tab):
    quitLoop = True
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

def get_comparisonAnswer(self, text2prompt, tab, it_comp, t_choice):
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
    # get the list for RELEASE
    print_tab(self.list_0)

    text_to_prompt= "number of the release family or [" + colorText('q', self.color) +"]uit. ? " 
    self.releaseFamily = get_answer1(text_to_prompt, self.list_0)
    print('RELEASE FAMILY : %s' % colorText(self.releaseFamily, 'blue')) # now we have the release family
    sleep(1)

    # here we get the release list

    self.releasesList_1 = list_search_1(self.releaseFamily) # all the releases
    print('there is %d files for %s' % (len(self.releasesList_1), self.releaseFamily))
    self.releaseFamily2 = self.releaseFamily[:-1] # not used ?
        
    self.releasesList_2 = sub_releases(self.releasesList_1) # extract the releases CMSSW_X_Y_Z...
    #for item in self.releasesList_2:
    #    print(item)

    return 1

def fonction_2(self):
    screen_clear()
    print('vous appelez la fonction 2')
    print_tab(self.releasesList_2)
    text_to_prompt= "number of the release, [" + colorText('b', self.color) + "]ack or [" + colorText('q', self.color) +"]uit. ? " 
    self.release = get_answer2(text_to_prompt, self.releasesList_2)

    if self.release != '':
        print('RELEASE : %s' % self.release) # now we have the release

        print('')
        self.releasesList_3 = sub_releases3(self.release, self.releasesList_1) # extract the list of the root files for the chosen release
        self.datasetsList_1 = sub_releases2(self.release, self.releasesList_3) # extract the datasets of the root files for the chosen release
        return 2
    else:
        return 0

def fonction_3(self):
    screen_clear()
    print('vous appelez la fonction 3')
    text_to_prompt= "Reference family for the validation " 
    print(text_to_prompt)  # 

    # get the list for REFERENCE
    print_tab(self.list_0)

    text_to_prompt= "number of the reference family, [" + colorText('b', self.color) + "]ack or [" + colorText('q', self.color) +"]uit. ? " 
    self.referenceFamily = get_answer2(text_to_prompt, self.list_0)
    if self.referenceFamily != '':
        print('REFERENCE FAMILY : %s' % colorText(self.referenceFamily, 'blue')) # now we have the reference family
        sleep(1)

        # here we get the reference list

        self.referencesList_1 = list_search_1(self.referenceFamily) # all the references
        print('there is %d files for %s' % (len(self.referencesList_1), self.referenceFamily))
        self.referenceFamily2 = self.referenceFamily[:-1] # not used ?
        
        self.referencesList_2 = sub_releases(self.referencesList_1) # extract the references CMSSW_X_Y_Z...
        return 3
    else:
        return 1
        
def fonction_4(self):
    screen_clear()
    print('vous appelez la fonction 4')
    print_tab(self.referencesList_2)
    text_to_prompt= "number of the reference, [" + colorText('b', self.color) + "]ack or [" + colorText('q', self.color) +"]uit. ? " 
    self.reference = get_answer2(text_to_prompt, self.referencesList_2)

    if self.reference != '':
        print('REFERENCE : %s' % self.reference) # now we have the reference
        print('')
        self.referencesList_3 = sub_releases3(self.reference, self.referencesList_1) # extract the list of the root files for the chosen reference
        self.datasetsList_2 = sub_releases2(self.reference, self.referencesList_3) # extract the datasets of the root files for the chosen reference
        return 4
    else:
        return 2

def fonction_5(self):
    screen_clear()
    # choose the comparison to to (Full/Fast/...)
    print(self.comparisons)
    print('')
    text_to_prompt= "numbers of the comparisons, [" + colorText('b', self.color) + "]ack or [" + colorText('q', self.color) +"]uit. ? " 
    print_tab(self.comparisons)
    self.comparisonChoice = get_comparisonAnswer(self, text_to_prompt, self.comparisons, '', 'comp') # get a tuple with the comparison choice
    if (len(self.comparisonChoice) == 0):
        print("Sorry, no valid choice.")
        return 3
        #exit()
    else:                                                                                  
        self.comparisonChoice = list(self.comparisonChoice)
        return 5

def fonction_6(self):
    self.tabGlobal = []

    # extract rel/ref lists corresponding to it_comp/it_val values from self.releasesList_3/self.referencesList_3
    getFilesList(self)
    for it_comp in self.comparisonChoice: # for each choice in [FastvsFast, FullvsFull, FastvsFull]
        t_comp = it_comp.split('vs') # t_comp[0] for self.releasesList_3 & t_comp[1] for self.referencesList_3
        print('it_comp')
        print(t_comp)
        # choose the validations to be done (RECO/PU25ns/...)
        #screen_clear()
        print(self.validations)
        print('')
        text_to_prompt= "numbers of the validations to be done for " + colorText(it_comp, 'blue') + " or [q]uit. ? " 
        print_tab(self.validations)
        self.validationsChoice = get_comparisonAnswer(self, text_to_prompt, self.validations, it_comp, 'val') # get a tuple with the validations choice
        if len(self.validationsChoice) == 0:
            return 4
        print(it_comp)
        for it_val in self.validationsChoice: # for each choice in (RECO/PU25ns/...)
            # load datasets from default datasets
            dts = createDTSname(self, it_comp, it_val) # look for datasets for each case
            for item in dts:
                if item[1] == 1:
                    print(colorText(item[0], 'blue'))
                else:
                    print([item[0]])
            sleep(1)
            #print(dts)
            self.tabGlobal.append([it_comp, it_val, dts]) 
                
    return 6

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