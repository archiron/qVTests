#! /usr/bin/env python
#-*-coding: utf-8 -*-

import os,sys

comparisons = ['FullvsFull', 'FastvsFast', 'FastvsFull']
validations = [['RECO', 'RECO'], ['RECO', 'miniAOD'], ['PU25', 'PU25'], ['PUpmx25', 'PUpmx25'], ['PUpmx25', 'PU25'], ['miniAOD', 'miniAOD']] # PU25 instead of PU25ns to take news HGal cases into account.

color = 'green' # color for the shell highlights #
color_nb = 'lightyellow'
