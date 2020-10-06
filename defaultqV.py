#! /usr/bin/env python
#-*-coding: utf-8 -*-

import os,sys

#############################################################################
# fixed data
tmp_path = '/eos/project/c/cmsweb/www/egamma/validation/Electrons/GUI/Projet_Validations-PortableDev/HistosConfigFiles/'
image_up = "http://cms-egamma.web.cern.ch/cms-egamma/validation/Electrons/img/up.gif"
image_point = "http://cms-egamma.web.cern.ch/cms-egamma/validation/Electrons/img/point.gif"
image_OK = "http://cms-egamma.web.cern.ch/cms-egamma/validation/Electrons/img/OK.gif"
image_KO = "http://cms-egamma.web.cern.ch/cms-egamma/validation/Electrons/img/KO.gif"

KS_path_local = '/eos/project/c/cmsweb/www/egamma/validation/Electrons/Store/KS_Curves/'
KS_path_web = 'http://cms-egamma.web.cern.ch/cms-egamma/validation/Electrons/Store/KS_Curves/'
#############################################################################

################## datasets ##################
#datasets_default = ['TTbar_13', 'ZEE_13']
datasets_default = ['TTbar_14TeV', 'ZEE_14']
##############################################

comparisons = ['FullvsFull', 'FastvsFast', 'FastvsFull']
validations = ['RECO', 'PU25', 'PUpmx25', 'miniAOD'] # PU25 instead of PU25ns to take news HGal cases into account. 

color = 'green' # color for the shell highlights ## perhaps unused
