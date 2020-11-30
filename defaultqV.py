#! /usr/bin/env python
#-*-coding: utf-8 -*-

#import os,sys

version = '0.61.1'
# Explode the functionsqV.py into 4 files.
# minor bug from nb of datasets into release/reference choice.

comparisons = [['Full', 'Full'], ['Fast', 'Fast'], ['Fast', 'Full']]
#validations = [['RECO', 'RECO'], ['RECO', 'miniAOD'], ['PU25', 'PU25'], ['PUpmx25', 'PUpmx25'], ['PUpmx25', 'PU25'], ['miniAOD', 'miniAOD']] # PU25 instead of PU25ns to take news HGal cases into account.
validations = [['RECO', 'RECO'], ['RECO', 'miniAOD'], ['PU', 'PU'], ['pmx', 'pmx'], ['pmx', 'PU'], ['miniAOD', 'miniAOD']] # PU instead of PU25ns to take news HGal cases into account.

color = 'green' # color for the shell highlights #
color_nb = 'lightyellow'
time2sleep = 1



