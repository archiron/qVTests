#! /usr/bin/env python
#-*-coding: utf-8 -*-

import os,sys
import re
from time import sleep

sys.path.append('/afs/cern.ch/user/a/archiron/lbin/ChiLib')

from networkFunctions import list_search_1
from datasetsqV import *

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
            if (nb == 6):
                displayStatus(self, fonction_6)
            elif (nb == 7):
                displayStatus(self, fonction_7)
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
            if (nb == 2):
                displayStatus(self, fonction_2)
            elif (nb == 3):
                displayStatus(self, fonction_3)
            elif (nb == 4):
                displayStatus(self, fonction_4)
            elif (nb == 5):
                displayStatus(self, fonction_5)
            elif (nb == 8):
                displayStatus(self, fonction_8)
            elif (nb == 9):
                displayStatus(self, fonction_9)
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
            displayStatus(self, fonction_10)
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
            if (nb == 13):
                displayStatus(self, fonction_13)
            elif (nb == 15):
                displayStatus(self, fonction_15)
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
            if (nb == 13):
                displayStatus(self, fonction_11)
            elif (nb == 15):
                displayStatus(self, fonction_12)
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

