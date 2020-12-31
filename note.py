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
        self.note = note
        self.num = Note.NOTE_TO_NUM[note]
        self.octave = int(octave)

    def get_freq(self):
        freq = Note.MIDDLE_C_FREQ * pow(2, self.num / 12)
        freq = freq * pow(2, Note.MIDDLE_OCTAVE - self.octave)  #   shift up/down by octave

        return freq

    def __repr__(self):
        return f"{self.note}{self.octave}"

    @classmethod
    def is_note(self, note_letter):
        if note_letter in Note.all_notes():
            return True

    @classmethod
    def all_notes(self):
        return list(Note.NOTE_TO_NUM.keys())