#! /usr/bin/env python
#-*-coding: utf-8 -*-

import os,sys

version = '0.50.3'
# minor correction for output of comparison choice into the config.py file.
# correction of output of DB_flag.
# correction of the output of GT

comparisons = [['Full', 'Full'], ['Fast', 'Fast'], ['Fast', 'Full]']]
#validations = [['RECO', 'RECO'], ['RECO', 'miniAOD'], ['PU25', 'PU25'], ['PUpmx25', 'PUpmx25'], ['PUpmx25', 'PU25'], ['miniAOD', 'miniAOD']] # PU25 instead of PU25ns to take news HGal cases into account.
validations = [['RECO', 'RECO'], ['RECO', 'miniAOD'], ['PU', 'PU'], ['pmx', 'pmx'], ['pmx', 'PU'], ['miniAOD', 'miniAOD']] # PU instead of PU25ns to take news HGal cases into account.

color = 'green' # color for the shell highlights #
color_nb = 'lightyellow'
