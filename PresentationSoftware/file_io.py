# file_io.py - Contains the FileIO class which manages filenames and data saving
# saving data.

__author__ = 'Nicholas Greene'
__copyright__ = 'Copyright 2021 Nicholas Greene'
__license__ = 'MIT'
__version__ = '1.0'

import os
import re

# Get the absolute path to the project root (where file_io.py lives)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(BASE_DIR, "audio")

class FileIO:
    def __init__(self, participant_id_int: int):
        save_dir = os.path.join(BASE_DIR, "saved")
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        participant_id = str(participant_id_int).zfill(2)
        pattern = '^' + participant_id + r'[.]csv$'

        for f in os.listdir(save_dir):
            match = re.match(pattern, f)
            assert not match, ('Participant ' + participant_id
                               + ' already recorded!')

        self._cnd_fname = {
            'Practice': 'PracTrial2.wav',
            'Slow': 'BeetKarjan.wav',
            'Fast': 'VivAcc.wav'
        }

        if participant_id_int % 2 == 0:
            # even IDs: slow first
            self.filenames = [
                os.path.join(AUDIO_DIR, self._cnd_fname['Practice']),
                os.path.join(AUDIO_DIR, self._cnd_fname['Slow']),
                os.path.join(AUDIO_DIR, self._cnd_fname['Fast'])
            ]
        else:
            # odd IDs: fast first
            self.filenames = [
                os.path.join(AUDIO_DIR, self._cnd_fname['Practice']),
                os.path.join(AUDIO_DIR, self._cnd_fname['Fast']),
                os.path.join(AUDIO_DIR, self._cnd_fname['Slow'])
            ]

        self._temp_fname = os.path.join(save_dir, participant_id + ".temp")
        self._final_fname = os.path.join(save_dir, participant_id + ".csv")


    def write(self, arousal_rating : float):
        print("this is arousal rating ", arousal_rating, self.filenames)
        with open(self._temp_fname, 'a') as f:
            f.write('{0},{1:f}\n'.format(os.path.basename(self.filenames.pop(0)),
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
            
