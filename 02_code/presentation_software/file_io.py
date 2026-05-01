# file_io.py - Contains the FileIO class which manages filenames and data saving
# saving data.

__author__ = 'Nicholas Greene'
__copyright__ = 'Copyright 2021 Nicholas Greene'
__license__ = 'MIT'
__version__ = '1.0'

import os
import re

audio_dir = 'audio/'

class FileIO:

    def __init__(self, participant_id_int : int):
        '''Initialise FileIO 
        '''
        save_dir = 'saved/'
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        participant_id = str(participant_id_int).zfill(2)
        pattern = '^' + participant_id + '[.]csv$'
 
        for f in os.listdir(save_dir):
            match = re.match(pattern, f)
            assert not match, ('Participant ' + participant_id 
                                + ' already recorded!')

        # Maps the experimental conditions (practice, slow, and fast) to their
        # respective filenames
        self._cnd_fname = {'Practice': 'PracTrial2.wav',
                           'Slow': 'BeetKarjan.wav',
                           'Fast': 'VivAcc.wav'}

        if participant_id_int % 2 == 0:
            # Participants with even IDs listen to the slow condition first
            self.filenames = ['audio/' + self._cnd_fname['Practice'],
                              'audio/' + self._cnd_fname['Slow'],
                              'audio/' + self._cnd_fname['Fast']]
        else:
            # Participants with odd IDs listen to the fast condition first
            self.filenames = ['audio/' + self._cnd_fname['Practice'],
                              'audio/' + self._cnd_fname['Fast'],
                              'audio/' + self._cnd_fname['Slow']]


        self._temp_fname = save_dir + participant_id + '.temp'
        self._final_fname = save_dir + participant_id + '.csv'

    def write(self, arousal_rating : float):
        with open(self._temp_fname, 'a') as f:
            f.write('{0},{1:f}\n'.format(self.filenames.pop(0).split('/')[1],
                                         arousal_rating))
    
    def save_final(self):
        with open(self._temp_fname, 'r') as re:
            for i, line in enumerate(re):
                fname, remainder = tuple(line.split(',', 1))
                if fname == self._cnd_fname['Practice']:
                    practice_line = 'Practice,' + str(i+1) + ',' + remainder
                elif fname == self._cnd_fname['Slow']:
                    slow_line = 'Slow,' + str(i+1) + ',' + remainder
                elif fname == self._cnd_fname['Fast']:
                    fast_line = 'Fast,' + str(i+1) + ',' + remainder

        with open(self._final_fname, 'a') as wr:
            wr.write('Condition,Order,Arousal\n')
            wr.write(practice_line)
            wr.write(slow_line)
            wr.write(fast_line)

        os.remove(self._temp_fname)
            
