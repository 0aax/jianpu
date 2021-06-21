from PIL import Image, ImageDraw

DPI = 300 # typical print dpi
paper_sizes = {'A4': (2480, 3508),
               'Letter': (2550, 3300)}

class Composition:
    def __init__(self, paper_type, notes):
        
        self.paper_type = paper_type
        self.notes = notes
        
        self.paper = Image.new('RGB', paper_sizes[paper_type], (255, 255, 255))

        self.header = {}
        self.header_height = 0

        self.line_height = 0
        self.num_lines = 0
    
    def set_header_height(self, height):
        self.header_height = height
    
    def set_line_height(self, height):
        self.line_height = height
    
    def set_header(self, header_info):
        for k, v in header_info.items():
            self.header[k] = v
