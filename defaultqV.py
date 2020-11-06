#! /usr/bin/env python
#-*-coding: utf-8 -*-

import os,sys

version = '0.52.3'
# improve the presentation of the summary.

comparisons = [['Full', 'Full'], ['Fast', 'Fast'], ['Fast', 'Full']]
#validations = [['RECO', 'RECO'], ['RECO', 'miniAOD'], ['PU25', 'PU25'], ['PUpmx25', 'PUpmx25'], ['PUpmx25', 'PU25'], ['miniAOD', 'miniAOD']] # PU25 instead of PU25ns to take news HGal cases into account.
validations = [['RECO', 'RECO'], ['RECO', 'miniAOD'], ['PU', 'PU'], ['pmx', 'pmx'], ['pmx', 'PU'], ['miniAOD', 'miniAOD']] # PU instead of PU25ns to take news HGal cases into account.

color = 'green' # color for the shell highlights #
color_nb = 'lightyellow'

