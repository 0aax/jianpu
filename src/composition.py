from PIL import Image, ImageDraw

DPI = 300 # typical print dpi
paper_sizes = {'A4': (2480, 3508),
               'Letter': (2550, 3300)}

class Composition:
    def __init__(self, paper_type, notes):
        
        self.paper_type = paper_type
        self.notes = notes
        
        self.paper = Image.new('RGB', paper_sizes[paper_type], (255, 255, 255))

