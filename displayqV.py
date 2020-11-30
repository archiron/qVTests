#! /usr/bin/env python
#-*-coding: utf-8 -*-

import os,sys
import re
from time import sleep

sys.path.append('/afs/cern.ch/user/a/archiron/lbin/ChiLib')

from networkFunctions import list_search_1
from datasetsqV import *
from optionsqV import *

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

def displaySummaryText(self):
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

def displayStatus(self, functionName): # to be seen later
    print('displayStatus')
    # keep the old help text
    old_text = functionName.__doc__
    print('fonction_10 : %s' % old_text)
    # give a new help text
    staticmethod(functionName).__func__.__doc__ = displaySummaryText(self)
    help(functionName)
    # give the old help text back
    staticmethod(functionName).__func__.__doc__ = old_text
    return

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

def print_tab_0(self, tab, color, a): # only for fonction_3 & fonction_5
    print('')
    if ((len(tab) % 2) == 0):
        for i in range(0, len(tab), 2):
            nb1 = nbDatasets(self, tab[i], a)
            nb2 = nbDatasets(self, tab[i+1], a)
            print('%40s [%s] - (%d) %40s [%s] - (%d)' % ( tab[i], colorText(str(i), color), nb1, tab[i+1], colorText(str(i+1), color), nb2 ) )
    elif ((len(tab) % 3) == 0):
        for i in range(0, len(tab), 3):
            nb1 = nbDatasets(self, tab[i], a)
            nb2 = nbDatasets(self, tab[i+1], a)
            nb3 = nbDatasets(self, tab[i+2], a)
            print('%40s [%s] - (%d) %40s [%s] - (%d) %40s [%s] - (%d)' % ( tab[i], colorText(str(i), color), nb1, tab[i+1], colorText(str(i+1), color), nb2,  tab[i+2], colorText(str(i+2), color), nb3 ) )
    else: # general case
        for i in range(0, len(tab), 2):
            if (i+1 == len(tab)):
                nb1 = nbDatasets(self, tab[i], a)
                print( '%40s [%s] - (%d)' % ( tab[i], colorText(str(i), color), nb1 ) )
            else: #
                nb1 = nbDatasets(self, tab[i], a)
                nb2 = nbDatasets(self, tab[i + 1], a)
                print('%40s [%s] - (%d) %40s [%s] - (%d)' % ( tab[i], colorText(str(i), color), nb1, tab[i+1], colorText(str(i+1), color), nb2 ) )

def colorText(sometext, color):
    return '\033' + changeColor(color) + sometext + '\033[0m'

