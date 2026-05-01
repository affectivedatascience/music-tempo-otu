#!/usr/bin/env python3

# main.py - Run this script to run an experiment

__author__ = 'Nicholas Greene'
__copyright__ = 'Copyright 2021 Nicholas Greene'
__license__ = 'MIT'
__version__ = '1.0'

# psychopy 
from psychopy import logging

# my files
from experiment import Experiment

logging.console.setLevel(logging.CRITICAL) # stops psychopy console warnings

experiment = Experiment()
experiment.run_training()
experiment.display_questionnaire_screen(5*60)
experiment.run_current_trial()
experiment.display_questionnaire_screen(5*60)
experiment.run_current_trial()
experiment.close()  

