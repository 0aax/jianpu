class Composition:
    def __init__(self, title=None, composer=None, instrument=None, \
                 time=None, key=None, tempo=None):
        
        self.title = title
        self.composer = composer
        self.instrument = instrument

        # composition may vary in time/key/tempo, but the 'first' one to appear will be put in the header
        self.time = time
        self.key = key
        self.tempo = tempo

        # self.notes is an array where each element has the format [{'time': abc, 'key': xyz, 'temp': qwe}, [notes....]]
        self.notes = []