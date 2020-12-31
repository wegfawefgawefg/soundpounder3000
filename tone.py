class Tone:
    def __init__(self, time, note, duration, volume):
        # ''' future features? '''
        # self.start_volume = None
        # self.end_volume = None
        # self.start_note = None
        # self.end_note = None
        self.time = time
        self.note = note
        self.duration = duration
        self.volume = volume

    def __repr__(self):
        rep = (
            f"time: {self.time}, "
            f"note: {self.note}, "
            f"duration: {self.duration}, "
            f"volume: {self.volume}"
        )
        
        return rep

    def render(self):
        raise NotImplementedError