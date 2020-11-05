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

def get_answerText(text2prompt):
    quitLoop = True
    print('')
    while ( quitLoop ):
        rel = raw_input(text2prompt)
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
        vals = raw_input(text2prompt)
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

'''def get_answer2(text2prompt, tab):
    quitLoop = True
    print('')
    while ( quitLoop ):
        rel = raw_input(text2prompt)
        #rel = input(text2prompt)  # Python 3
        if rel == 'q':
            exit()
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

    return temp'''

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

def get_answer4(text2prompt):
    quitLoop = True
    print('')
    while ( quitLoop ):
        rel = raw_input(text2prompt)
        #rel = input(text2prompt)  # Python 3

        print('rel : %s' % rel)
        if rel == 'q':
            exit()
        elif rel == 'b':
            quitLoop = False
            temp = ''
        elif rel == 'd':
            quitLoop = False
            temp = 'd'
        elif rel == 's':
            quitLoop = False
            temp = 's'
        elif rel == 'c':
            quitLoop = False
            temp = 'c'
        else:
            print('you typed : %s' % rel)

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
            print('you typed : %s' % rel)

    return temp

def get_answer6(text2prompt, tab): # for GT
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
    screen_clear()
    #print('vous appelez la fonction 1')

    print_tab_2(self.web_location, self.color_nb)
    text_to_prompt= "number of the folder choice or [" + colorText('q', self.color) +"]uit. ? "
    self.location, self.extension = get_answer1(text_to_prompt, self.web_location, self.web_extension)
    print('WEB LOCATION : %s' % colorText(self.location, 'blue')) # now we have the web folder location
    sleep(1)

    return 1

def fonction_2(self):
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

    # get the list for RELEASE
    print_tab_1(self.list_0, self.color_nb)

    text_to_prompt= "number of the RELEASE family or [" + colorText('q', self.color) +"]uit. ? "
    self.releaseFamily = get_answer3(text_to_prompt, self.list_0)
    print('RELEASE FAMILY : %s' % colorText(self.releaseFamily, 'blue')) # now we have the release family
    sleep(1)

    # here we get the release list

    self.releasesList_1 = list_search_1(self.releaseFamily) # all the releases
    #print('there is %d files for %s' % (len(self.releasesList_1), self.releaseFamily))

    self.releasesList_2 = sub_releases(self.releasesList_1) # extract the releases CMSSW_X_Y_Z...

    return 2

def fonction_3(self):
    screen_clear()
    #print('vous appelez la fonction 3')
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
    #print('vous appelez la fonction 4')
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
        #self.referenceFamily2 = self.referenceFamily[:-1] # not used ?

        self.referencesList_2 = sub_releases(self.referencesList_1) # extract the references CMSSW_X_Y_Z...
        return 4
    else:
        return 2

def fonction_5(self):
    screen_clear()
    #print('vous appelez la fonction 5')
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
    #print('vous appelez la fonction 6')
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
    #print('vous appelez la fonction 7')
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
    #print('vous appelez la fonction 8')
    # comparison choice
    print_tab_4(self.comparisons, self.color_nb)
    text_to_prompt= "number of the comparison type, [" + colorText('b', self.color) + "]ack or [" + colorText('q', self.color) +"]uit. ? "

    self.comparisonChoice = get_answer3(text_to_prompt, self.comparisons) #

    return 8

def fonction_9(self):
    screen_clear()
    #print('vous appelez la fonction 9')
    # validation choice
    #print_tab_4(self.validations, self.color_nb)
    print_tab_6(self.validations, self.color_nb, self.release, self.reference)
    text_to_prompt= "number of the validation type, [" + colorText('b', self.color) + "]ack or [" + colorText('q', self.color) +"]uit. ? "

    self.validationChoice = get_answer3(text_to_prompt, self.validations) #
    if ( self.validationChoice[0] == 'RECO' and self.validationChoice[1] == 'miniAOD' ):
        self.reference = self.release
        self.referencesList_3 = self.releasesList_3
        self.datasetsList_2 = self.datasetsList_1
    if ( self.validationChoice[0] == 'pmx' and self.validationChoice[1] == 'PU' ):
        self.reference = self.release
        self.referencesList_3 = self.releasesList_3
        self.datasetsList_2 = self.datasetsList_1

    return 9

def fonction_10(self):
    screen_clear()
    #print('vous appelez la fonction 10')
    # datasets choice
    fieldname = 'DataSetsFilter_' + self.comparisonChoice[0] + 'vs' + self.comparisonChoice[1] + self.validationChoice[0]
    if self.validationChoice[1] == 'miniAOD':
        fieldname = 'DataSetsFilter_' + self.comparisonChoice[0] + 'vs' + self.comparisonChoice[1] + self.validationChoice[1]
    print('datasets default : %s' % fieldname)
    self.default_dataset = DataSetsFilter(self, fieldname)
    print_tab_3(self.default_dataset, self.color_nb)
    print('those with %s are not selected' % (colorText('0', 'blue')))
    print('those with %s are selected' % (colorText('1', self.color_nb)))
    text_to_prompt = "you can use the [" + colorText('d', self.color) + "]efault selected datasets, [" + colorText('b', self.color) + "]ack or [" + colorText('q', self.color) +"]uit.\n "
    text_to_prompt += "you can [" + colorText('s', self.color) + "]elect datasets from the list, or [" + colorText('c', self.color) + "]hose between the common datasets : "

    self.dts = get_answer4(text_to_prompt) #
    self.datasets = []
    if ( self.dts == ''): # back
        return 8
    elif ( self.dts == 's'): # default
        function_101(self)
        return 10
    elif ( self.dts == 'c'): # default
        function_102(self)
        return 10
    elif ( self.dts == 'd'): # default
        for item in self.default_dataset:
            if item[1] == 1:
                self.datasets.append(item[0])
        print('datasets : ')
        print(self.datasets)
        return 10

    return 10

def function_101(self):
    screen_clear()
    #print('vous appelez la fonction 101')
    print_tab_3(self.default_dataset, self.color_nb) # all datasets with same color
    text_to_prompt= "enter the numbers of the datasets you want, separated by commas : "
    numbers = get_answer10X(text_to_prompt, self.default_dataset)
    #print(numbers)
    self.datasets = []
    for i in numbers:
        self.datasets.append(str(self.default_dataset[i][0]))
    #print('datasets 101 : ')
    #print(self.datasets)
    return

def function_102(self):
    screen_clear()
    #print('vous appelez la fonction 102')

    # perhaps make a test if len(commonDatasets) = 0 !

    self.commonDatasets = set(self.datasetsList_1).intersection(set(self.datasetsList_2))
    self.commonDatasets = list(self.commonDatasets) # get the common datasets for the comparisons
    print_tab_1(self.commonDatasets, self.color) # all datasets with same color
    text_to_prompt= "enter the numbers of the datasets you want, separated by commas : "
    numbers = get_answer10X(text_to_prompt, self.commonDatasets)
    for i in numbers:
        self.datasets.append(str(self.commonDatasets[i]))
    #print('datasets 102 : ')
    #print(self.datasets)
    return

def fonction_11(self):
    screen_clear()
    #print('vous appelez la fonction 11')
    self.releasesGT = []
    self.referencesGT = []
    self.relRootFilesList = []
    self.refRootFilesList = []
    self.releasesList_4 = []  # root files list for release
    self.referencesList_4 = []  # root files list for reference

    # get the self.releasesList_4/self.referencesList_4 lists of root files
    print('root files extraction')
    rootFilesExtraction(self)

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

    # rewrite GT list in a more convenient way
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
    tt_ref = []
    for elem in self.GT_ref:
        if len(elem[1:]) == len(self.datasets):
            tt_ref.append(elem)
    self.GT_ref = tt_ref
    #print(self.GT_ref)

    if len(self.GT_rel) == 0 or len(self.GT_ref) == 0 :
        print(colorText('len(self.GT_rel) == 0 or len(self.GT_ref) == 0', 'red'))
        return 9 # back to datasets choice

    print_tab_5(self.GT_rel, self.color_nb)
    text_to_prompt = "get a RELEASE GT number, [" + colorText('b', self.color) + "]ack or [" + colorText('q', self.color) +"]uit. ? "
    GT = get_answer6(text_to_prompt, self.GT_rel)  #
    if ( GT == ''): # back
        return 9
    else:
        self.GT_rel = GT
        for elem in self.releasesList_5:
            for i in range(1, len(elem)):
                if re.search(self.GT_rel, elem[i]):
                    #print(elem[i])
                    self.relRootFilesList.append(elem[i])
        return 11

def fonction_12(self):
    screen_clear()
    #print('vous appelez la fonction 12')

    print_tab_5(self.GT_ref, self.color_nb)
    text_to_prompt = "get a REFERENCE GT number, [" + colorText('b', self.color) + "]ack or [" + colorText('q', self.color) +"]uit. ? "
    GT = get_answer6(text_to_prompt, self.GT_ref)  #
    if ( GT == ''): # back
        return 10
    else:
        self.GT_ref = GT
        #print('GT = %s' % GT)
        #print(GT)
        for elem in self.referencesList_5:
            for i in range(1, len(elem)):
                if re.search(GT, elem[i]):
                    #print(elem[i])
                    self.refRootFilesList.append(elem[i])
        return 12

def fonction_13(self):
    screen_clear()
    #print('vous appelez la fonction 13')
    # DB Flag choice
    if testZEE(self.datasets):
        text_to_prompt= "use Decision Box for ZEE, [" + colorText('y', self.color) + "]es/[" + colorText('n', self.color) + "o] [" + colorText('b', self.color) + "]ack or [" + colorText('q', self.color) +"]uit. ? "
        DB_flag = get_answer5(text_to_prompt) #
    else:
        DB_flag = 'n'

    if DB_flag == '':
        return 11
    elif DB_flag == 'y':
        self.DB_flags = []
        for item in self.datasets:
            if item != 'ZEE_14':
                self.DB_flags.append(False)
            else:
                self.DB_flags.append(True)
        return 13
    elif DB_flag == 'n':
        for i in range(0, len(self.datasets)):
            self.DB_flags.append(False)
        return 13

def fonction_14(self):
    screen_clear()
    #print('vous appelez la fonction 14')
    # Summary
    print('SUMMARY : ')
    text_to_prompt = 'RELEASE : ' + colorText(self.release, 'blue') + ' - REFERENCE : ' + colorText(self.reference, 'blue')
    print(text_to_prompt)
    text_to_prompt = 'release extension : ' + colorText(self.releaseExtent, 'blue') + ' - reference extension : ' + colorText(self.referenceExtent, 'blue')
    print(text_to_prompt)
    print(self.GT_rel)
    print(self.GT_ref)
    print(self.relRootFilesList)
    print(self.refRootFilesList)
    print('')
    # include the differents choices into Gev
    self.gev_tmp.append([str(self.release), str(self.reference)])
    self.gev_tmp.append([str(self.releaseExtent), str(self.referenceExtent)])
    self.gev_tmp.append(str(self.datasets))
    #self.gev_tmp.append(str(self.comparisonChoice))
    self.gev_tmp.append(str(self.comparisonChoice[0] + 'vs' + self.comparisonChoice[1]))
    self.gev_tmp.append(str(self.validationChoice))
    self.gev_tmp.append([str(self.release) + '-' + str(self.GT_rel), str(self.reference) + '-' + str(self.GT_ref)])
    self.gev_tmp.append(str(self.DB_flags))
    print(self.gev_tmp)
    self.Gev.append(self.gev_tmp)

    return 14

def fonction_15(self):
    screen_clear()
    #print('vous appelez la fonction 15')
    # New set ?
    text_to_prompt = "Adding another set of validation ?, [" + colorText('y', self.color) + "]es/["
    text_to_prompt += colorText('n', self.color) + "o], [" + colorText( 'b', self.color)
    text_to_prompt += "]ack or [" + colorText('q', self.color) + "]uit. ? "
    answer4new = get_answer5(text_to_prompt)  #
    print('answer for new set : %s' % answer4new)
    if answer4new == '': # back
        return 12
    elif answer4new == 'y': # back to release choice
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
        print('dts : %s' % dts)
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