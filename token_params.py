from utils import parse_num_or_frac

class TokenParams:
    def __init__(self, token):
        self.empty = True
        self.duration = None
        self.octave = None
        self.relative_octave = None
        self.volume = None

        sectors = token.split('_')
        for sector in sectors:
            head = sector[0]
            tail = sector[1:]
            if head == 'd':
                self.empty = False
                self.duration = parse_num_or_frac(tail)
            elif head == "v":
                self.empty = False
                self.volume = parse_num_or_frac(tail)
            elif head == "o":
                self.empty = False
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
