class Tone:
    def __init__(self, time, note, duration, volume, instrument_name, instrument_params=None):
        # ''' future features? '''
        # self.start_volume = None
        # self.end_volume = None
        # self.start_note = None
        # self.end_note = None
        self.time = time
        self.note = note
        self.duration = duration
        self.volume = volume
        self.instrument_name = instrument_name
        self.instrument_params = instrument_params or {}

    def __repr__(self):
        rep = (
            f"time: {self.time}, "
            f"note: {self.note}, "
            f"duration: {self.duration}, "
            f"volume: {self.volume}, "
            f"instrument: {self.instrument_name}"
        )
        
        return rep

    def render(self):
        raise NotImplementedError
