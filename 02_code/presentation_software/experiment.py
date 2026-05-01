# experiment.py - Contains the Experiment class which provides a clean interface
# to setup and run an experiment.

__author__ = 'Nicholas Greene'
__copyright__ = 'Copyright 2021 Nicholas Greene'
__license__ = 'MIT'
__version__ = '1.0'

# Python standard libs
import os

# Psychopy
from psychopy.visual import TextStim, Window, ImageStim
from psychopy.gui import Dlg
from psychopy import core, event

# My files
from trial_manager import TrialManager
from file_io import FileIO
import event_marker
import hidden_keys


class Experiment():

    def __init__(self):
        ''' Sets up and begins an experiment
        '''

        # Collect participant ID
        dlg = Dlg(title='Movie presentation experiment')
        dlg.addField('Participant ID:')
        participant_id_int = int(dlg.show()[0].lstrip('0')) # type: ignore
        participant_id = str(participant_id_int).zfill(2)
        print('participant_id', participant_id)
        if not dlg.OK: core.quit()
       
        self.win = Window(fullscr=True, 
                           color='white')
        event.globalKeys.add(key='escape', func=core.quit)

        self.mouse = event.Mouse(win=self.win)

        self.f_io = FileIO(participant_id_int)
        self.shortcut = hidden_keys.HiddenKeys()
        self.trial_manager = TrialManager(self.win, self.f_io.filenames, 
                                          self.shortcut, self.mouse)

        self._background = ImageStim(win=self.win,
                                     image='img/wait.png',
                                     units='pix',
                                     size=(2560, 1440))
     
        self._participant_id_text = TextStim(self.win, 
                                             text='ID: ' + participant_id, 
                                             pos=(-0.8, 0.9), 
                                             units='norm', 
                                             color='black', 
                                             wrapWidth=2)
        self._participant_id_text.size = 0.8

        self._timer = TextStim(self.win,
                               text='',
                               pos=(0, -0.1),
                               units='norm',
                               color='grey')
        self._timer.size = 0.2

    def _check_quit(self):
        if "escape" in event.getKeys():
            self.win.close()
            core.quit()

    def run_training(self):
        info_files = [
            'img/intro-1.png',
            'img/intro-2.png',
            'img/intro-3.png',
        ]

        self._background = ImageStim(win=self.win,
                                     image='img/press-to-continue.png',
                                     units='pix',
                                     size=(2560, 1440))

        while not self.mouse.getPressed()[0]:
                    self._check_quit()
                    self._background.draw()
                    self._participant_id_text.draw()
                    self.win.flip()

        # minimum time before accepting participant input
        min_time = core.getTime() + 1.0 

        self._background.image = info_files.pop(0)
        self._background.size = self.win.size
        while True:
            self._background.draw()
            self.win.flip()
            if self.mouse.getPressed()[0] and core.getTime() > min_time: 
                if not info_files: break
                self._background.image = info_files.pop(0) 
                self._background.size = self.win.size
                min_time = core.getTime() + 1.0

        self.run_current_trial() # play training clip

        self._background.image = 'img/intro-4.png'
        min_time = core.getTime() + 1.0
        while True:
            self._background.draw()
            self.win.flip()
            if self.mouse.getPressed()[0] and core.getTime() > min_time: return
    # end run_training

    def _time_fmt(self, time : float):
        return '{0:02.0f}:{1:02.0f}'.format(*divmod(round(time), 60))

    def display_wait_screen(self, seconds_to_wait : float):
        self._background.image = 'img/wait.png'
        wait_t = core.getTime() + seconds_to_wait
        while core.getTime() < wait_t:
            if self.shortcut.skip_enabled: # skip if n is pressed 3 times
                self.shortcut.skip_enabled = False
                break
            self._background.draw()
            self._timer.text = self._time_fmt(wait_t - core.getTime())
            self._timer.draw()
            self.win.flip()

    def display_questionnaire_screen(self, seconds_to_wait : float):
        self._background.image = 'img/questionnaire-1.png'
        wait_t = core.getTime() + seconds_to_wait
        while core.getTime() < wait_t:
            if self.shortcut.skip_enabled: # skip if n is pressed 3 times
                self.shortcut.skip_enabled = False
                break
            self._background.draw()
            self._timer.text = self._time_fmt(wait_t - core.getTime())
            self._timer.draw()
            self.win.flip()

        self._background.image = 'img/questionnaire-2.png'
        while True:
            self._background.draw()
            self.win.flip()
            if self.mouse.getPressed()[0]: return

    def run_current_trial(self):
        arousal_rating = self.trial_manager.run_current_trial()
        self.f_io.write(arousal_rating)

    def close(self):
        self.f_io.save_final()
        # normal breathing
        self.display_wait_screen(30)

        # deep breathing
        breath_count = 3
        inhale_time = 6 # seconds
        exhale_time = 8 # seconds
        event_marker.begin_trial() # event to acqknowledge
        for _ in range(breath_count):
            # inhale
            self._background.image = 'img/breathing-in.png'
            t = core.getTime()
            while core.getTime() < t + inhale_time:
                self._background.draw()
                self._timer.text = self._time_fmt(t + inhale_time 
                                                  - core.getTime())
                self._timer.draw()
                self.win.flip()

            # exhale
            self._background.image = 'img/breathing-out.png'
            t = core.getTime()
            while core.getTime() < t + exhale_time:
                self._background.draw()
                self._timer.text = self._time_fmt(t + exhale_time 
                                                  - core.getTime())
                self._timer.draw()
                self.win.flip()

        event_marker.end_trial() # event to acqknowledge

        self._background.image = 'img/end.png'
        while not self.mouse.getPressed()[0]:
            self._check_quit()
            self._background.draw()
            self.win.flip()

        self.win.close()
        core.quit()

