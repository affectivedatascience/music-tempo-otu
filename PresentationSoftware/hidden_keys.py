#!/usr/bin/env python3

# hidden_keys.py - 

__author__ = 'Nicholas Greene'
__copyright__ = 'Copyright 2021 Nicholas Greene'
__license__ = 'MIT'
__version__ = '1.0'

from psychopy import event, core

class HiddenKeys:

    def __init__(self):
        _quit_key = 'q'
        _quit_modifiers = ['ctrl', 'alt']
        event.globalKeys.add(key=_quit_key, modifiers=_quit_modifiers, 
                             func=self._quit_experiment)

        _skip_key = 'n'
        self._press_count = 0
        self.skip_enabled = False
        event.globalKeys.add(key=_skip_key, func=self._enable_skip)

    def _quit_experiment(self):
        '''Quits the experiment with key combination 'ctrl', 'alt/option', 
        and 'q'.
        '''
        core.quit()

    def _enable_skip(self):
        '''Sets the boolean to skip the current playing clip to True when 
        the 'n' key is pressed 3 times.
        '''
        self._press_count += 1

        if self._press_count >= 3:
            self.skip_enabled = True
            self._press_count = 0

