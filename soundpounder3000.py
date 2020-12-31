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
        else: #     chord
            chord_notes
    
    waveform = np.concatenate(tones)

    return waveform

# def gen_random_sheet_music(num_notes=100):
#     note_letters = [random.choice(Note.all_notes()) for _ in range(num_notes)]
#     sheet_music = ' '.join(note_letters)

#     return sheet_music

# '''     SONGS   '''
# twinkle_twinkle = 'C C G G A A G - F F E E D D C - G G F F E E D - G G F F E E D - C C G G A A G - F F E E D D C'
# something = 'C E G C E G C E G C E G C E G C E G B B B B'
# something_with_octaves = 'bpm60 nC.o4.d1/16 o4'
# larrys_song = 'Eb C C# D E F# A G D B G# A B C E D# D C C# D B A G F# D D D D D D D D D D D D D D D'

# sheet_music = something
# # sheet_music = gen_random_sheet_music()

# # waveform = gen_song(sheet_music)
# something_wave = gen_song(something)
# larrys_song_wave = gen_song(larrys_song)


# waveforms = (something_wave, larrys_song_wave)

# def sum_waveforms(waveforms):
#     lengths = [wave.shape[0] for wave in waveforms]
#     longest_length = max(lengths)

#     base = np.zeros(longest_length)
#     for waveform in waveforms:
#         length = waveform.shape[0]
#         indices = np.arange(length)
#         base[indices] += waveform[indices]

#     return base

# waveform = sum_waveforms(waveforms)

# from scipy.io.wavfile import write
# write('song.wav', SAMPLE_RATE, waveform.astype(np.int16))



# ex_num_or_frac_frac = '1/16'
# ex_num_or_frac_num = '0.2'

# print(parse_num_or_frac(ex_num_or_frac_frac))
# print(parse_num_or_frac(ex_num_or_frac_num))
# quit()

def get_cursor_delta(bpm, step_size):
    bps = bpm / 60
    samples_per_second = bps * SAMPLE_RATE
    num_samples_to_step = samples_per_second * step_size

    return num_samples_to_step

def parse_num_or_frac(num_or_frac):
    if '/' in num_or_frac:  #   its a frac
        numerator, denom = num_or_frac.split('/')
        return float(numerator) / float(denom)
    else:   #   its a num
        return float(num_or_frac)
        
class TokenParams:
    def __init__(self, token):
        self.duration = None
        self.octave = None
        self.relative_octave = None
        self.volume = None

        sectors = token.split('_')
        for sector in sectors:
            head = sector[0]
            tail = sector[1:]
            if head == 'd':
                self.duration = parse_num_or_frac(tail)
            elif head == "v":
                self.volume = parse_num_or_frac(tail)
            elif head == "o":
                subhead = tail[0]
                subtail = tail[1:]
                if subhead == '+':
                    self.relative_octave = parse_num_or_frac(subtail)
                elif subhead == '-':
                    self.relative_octave = -parse_num_or_frac(subtail)
                else:   #   its a one time absolute octave
                    self.octave = parse_num_or_frac(tail)

    def __repr__(self):
        attributes = []
        if self.duration:
            attributes.append("duration: {}".format(self.duration))
        if self.octave:
            attributes.append("octave: {}".format(self.octave))
        if self.relative_octave:
            attributes.append("relative_octave: {}".format(self.relative_octave))
        if self.volume:
            attributes.append("volume: {}".format(self.volume))
        string = ', '.join(attributes)
        return string

test_notes = ['E_v0.5', 'G_o5_d1/16_v1/4', 'B_o-1.3']

params = [TokenParams(token) for token in test_notes]
[print(param) for param in params]
quit()

example_aybc = 'tTitle_Here s60 C_o4_d1/16 o4 r r_d1/16 o4 d1/16 C [ C_d4 f1 E_d3 f1 G_d2 f1 B_d1_o+1 ] [ C E_v0.5 G_v0.25 B_o+1 ]'

sectors = example_aybc.split()
print(sectors)

title = "Untitled"
bpm = 60
base_octave = 4
base_duration = 1
auto_step = True
cursor = 0
for sector in sectors:
    head = sector[0]
    tail = sector[1:]
    token_params = parse_token()
    if head == 't':     #   title
        title = tail
    elif head == 's':   #   speed
        bpm = int(tail)
    elif head == 'd':   #   set duration
        base_duration = int(tail)
    elif head == 'o':   #   set octave
        base_octave = int(tail)
    elif head == 'r':   #   rest
        cursor += get_cursor_delta(bpm, base_duration)
    elif head in Note.all_notes():  #   note
        #   do note things
        if auto_step:
            cursor += get_cursor_delta(bpm, base_duration)
    elif head == '[':   #   disable auto step
        auto_step = True
    elif head == ']':   #   enable auto step
        auto_step = False
    elif head == 'f':   #   move cursor
        if not tail == '':
            one_time_duration = parse_num_or_frac(tail)
            cursor += get_cursor_delta(bpm, one_time_duration)
        else:
            cursor += get_cursor_delta(bpm, base_duration)
    
    