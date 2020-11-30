#! /usr/bin/env python
#-*-coding: utf-8 -*-

#import os,sys

version = '0.62'
# correcting a bug with function_11/12 sattus redirection.
# add some control of the existing datasets.
# The default datasets are compared to the common ones.
# - if all defaults are in commons, continue
# - is some of the default datasets are missing, a WARNING sentence is displayed.
# - if none of the default datasets are present, the pgm sent you back to release family choice because no validation is possible.

comparisons = [['Full', 'Full'], ['Fast', 'Fast'], ['Fast', 'Full']]
#validations = [['RECO', 'RECO'], ['RECO', 'miniAOD'], ['PU25', 'PU25'], ['PUpmx25', 'PUpmx25'], ['PUpmx25', 'PU25'], ['miniAOD', 'miniAOD']] # PU25 instead of PU25ns to take news HGal cases into account.
validations = [['RECO', 'RECO'], ['RECO', 'miniAOD'], ['PU', 'PU'], ['pmx', 'pmx'], ['pmx', 'PU'], ['miniAOD', 'miniAOD']] # PU instead of PU25ns to take news HGal cases into account.

color = 'green' # color for the shell highlights #
color_nb = 'lightyellow'
time2sleep = 1


