import random

import numpy as np

SAMPLE_RATE = 44100 #Frequecy in Hz
DURATION = 0.1

def gen_tone(freq, duration=0.5, volume=1.0):
    amplitude = 4096 * volume
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    wave = amplitude * np.sin(2 * np.pi * freq * t)
    
    return wave

class Note:
    MIDDLE_OCTAVE = 4
    MIDDLE_C_FREQ = 261.63
    NOTE_TO_NUM = {
        'C':0, 'C#':1, 'Cb':11, 
        'D':2, 'D#':3, 'Db':1, 
        'E':4, 'E#':5, 'Eb':3, 
        'F':5, 'F#':6, 'Fb':4, 
        'G':7, 'G#':8, 'Gb':6, 
        'A':9, 'A#':10, 'Ab':8, 
        'B':11, 'B#':0, 'Bb':10, 
        }

    def __init__(self, note, octave=MIDDLE_OCTAVE):
        self.num = Note.NOTE_TO_NUM[note]
        self.octave = octave

    def get_freq(self):
        freq = Note.MIDDLE_C_FREQ * pow(2, self.num / 12)
        freq = freq * pow(2, Note.MIDDLE_OCTAVE - self.octave)  #   shift up/down by octave

        return freq

    @classmethod
    def is_note(self, note_letter):
        if note_letter in Note.all_notes():
            return True

    @classmethod
    def all_notes(self):
        return list(Note.NOTE_TO_NUM.keys())

def gen_song(sheet_music):
    note_letters = sheet_music.split(' ')

    tones = []
    for note_letter in note_letters:
        if Note.is_note(note_letter):
            note = Note(note_letter)
            freq = note.get_freq()
            tone = gen_tone(freq=freq, duration=DURATION, volume=1.0)
            tones.append(tone)
        elif note_letter == '-':   #   its a rest
            tone = gen_tone(freq=0, duration=DURATION)
            tones.append(tone)
    
    waveform = np.concatenate(tones)

    return waveform

def gen_random_sheet_music(num_notes=100):
    note_letters = [random.choice(Note.all_notes()) for _ in range(num_notes)]
    sheet_music = ' '.join(note_letters)

    return sheet_music

'''     SONGS   '''
twinkle_twinkle = 'C C G G A A G - F F E E D D C - G G F F E E D - G G F F E E D - C C G G A A G - F F E E D D C'
something = 'C E G C E G C E G C E G C E G B B B B B'
larrys_song = 'Eb C C# D E F# A G D B G# A B C E D# D C C# D B A G F# D'

sheet_music = something
# sheet_music = gen_random_sheet_music()

waveform = gen_song(sheet_music)

from scipy.io.wavfile import write
write('song.wav', SAMPLE_RATE, waveform.astype(np.int16))