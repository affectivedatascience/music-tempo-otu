# trial_manager.py - Contains the TrialManager class which handles all the
# things that occur during a trial. This involves playing the audio clips, 
# drawing the arousal slider, and sending the participant ratings (with 
# timestamps) to the FileIO object to be saved.

__author__ = 'Nicholas Greene'
__copyright__ = 'Copyright 2021 Nicholas Greene'
__license__ = 'MIT'
__version__ = '1.0'

# Psychopy
from psychopy import event, visual, sound, core, constants

# My files
import event_marker 


class TrialManager():
    
    def __init__(self, win, clip_list, shortcut, mouse):
        self.win = win
        self._background = visual.ImageStim(win=self.win,
                                            image=None,
                                            units='pix',
                                            size=(2560, 1440))

        self._valence_slider = visual.Slider(win=self.win, 
                                             ticks=[1, 2500, 5000, 7500, 10000],
                                             borderColor='black',
                                             styleTweaks=['triangleMarker'])
        accept_pos = (0, -0.5)
        self._accept_box = visual.Rect(win=self.win,
                                       units='norm',
                                       size=0.25,
                                       pos=accept_pos)
        self._accept_text = visual.TextStim(win=self.win,
                                            text='Accept',
                                            color='black',
                                            pos=accept_pos)
        self._accept_text.size = 0.1
        self.mouse = mouse
        self.shortcut = shortcut
        self._load_clips(clip_list)

    def _load_clips(self, clip_list):
        '''Loads all the audio clips as psychopy sound objects.
        '''
        self._clip_objs = []
        print("this is the clip list: ", clip_list)
        loading_text = visual.TextStim(self.win, 
                                       text='',
                                       pos=(0,0), 
                                       units='norm', 
                                       color='black', 
                                       wrapWidth=2)

        for i, filename in enumerate(clip_list):
            loading_text.text = ('Loading audio files\n' + str(i+1) + '/' 
                                 + str(len(clip_list)))
            loading_text.draw()
            self.win.flip()
            obj = sound.Sound(filename)
            self._clip_objs.append(obj)

    def run_current_trial(self):
        '''Plays the next audio clip and draws the arousal slider.
        '''

        if not self._clip_objs: return 

        self._background.image = 'img/while-listening.png'
        audio = self._clip_objs.pop(0)
        stime = core.getTime()
        event_marker.begin_trial() # event to acqknowledge
        audio.play()
        while not audio.isFinished:
            if self.shortcut.skip_enabled: # skip if n is pressed three times
                audio.pause()
                self.shortcut.skip_enabled = False
                break
            self._background.draw()
            self.win.flip()


        event_marker.end_trial()    # event to acknowledge

        self._valence_slider.reset()
        self._background.image = 'img/arousal-slider.png'

        while True:
            self._background.draw()
            self._valence_slider.draw()

            if self._valence_slider.getRating():
                if self._accept_box.contains(self.mouse):
                    if self.mouse.getPressed()[0]: 
                        return self._valence_slider.getRating()
                    # light blue
                    self._accept_box.setColor([0.2, 0.6, 1], colorSpace='rgb')
                else:
                    # less light blue
                    self._accept_box.setColor([0.5, 0.75, 1], colorSpace='rgb')

                self._accept_box.draw()
                self._accept_text.draw()

            self.win.flip()
        

        
      
