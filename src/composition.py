from os import set_inheritable
from PIL import Image, ImageDraw

# default values
bars_per_row = 6

DPI = 300 # typical print dpi
paper_sizes = {'A4': (2480, 3508),
               'Letter': (2550, 3300)}

header_elems = {'title', 'comp', 'inst'}
types_bars = {'bar', 'lrep', 'rrep'}

no_add_alloc = {'roct', 'loct'} | types_bars
add_alloc_notes = {'fing', 'down', 'up', 'trem', 'grace'}
add_alloc_misc = {'scresc', 'ecresc', 'sdim', 'edim'}

class Composition:
    def __init__(self, paper_type='letter', parsed=list()):
        
        self.paper_type = paper_type
        self.parsed = parsed
        self.uniform_parsed = self.gen_uniform_parse(parsed)
        self.notes = self.split_header_notes(self.uniform_parsed)
        
        self.paper = Image.new('RGB', paper_sizes[paper_type], (255, 255, 255))

        self.header = {}
        self.header_height = 0

        self.line_height = 0
        self.num_lines = 0

        self.barred_notes = self.gen_barred_notes(self.notes)
        self.naive_notes_alloc = self.gen_naive_notes_alloc(self.barred_notes)
    
    def set_header_height(self, height):
        self.header_height = height
    
    def set_line_height(self, height):
        self.line_height = height
    
    def gen_header_info(self, header_info):
        header = {}
        for n in header_info:
            header[n[0]] = n[-1]
        return header
    
    def gen_uniform_parse(self, parsed):
        parse_uni = []
        for n in parsed:
            if isinstance(n, int): parse_uni.append(['qtr', n])
            else: parse_uni.append(n)
        return parse_uni

    def split_header_notes(self, uni_parsed):
        notes_tmp = []
        header = []
        for n in uni_parsed:
            if n[0] == 'header':
                header = self.gen_header_info(n[1:])
            else: notes_tmp.append(n)
        return header, notes_tmp

    def gen_barred_notes(self, notes):
        barred_notes = []
        curr_bar = []
        for n in notes:
            if n[0] in types_bars: barred_notes.append(curr_bar)
            else: curr_bar += [n]
        return barred_notes

    def gen_naive_notes_alloc(self, barred_notes):

        def get_alloc(n):
            if isinstance(n, int) or n[0] in no_add_alloc: return 1
            else:
                alloc_tmp = 1 if n[0] in add_alloc_notes else 0
                return get_alloc(n[-1]) + alloc_tmp

        alloc = []
        for n in barred_notes:
            if n[0] == 'chord':
                chord_alloc = 0
                for e in n[1:]: chord_alloc += get_alloc(e)
                alloc.append(chord_alloc)
            else:
                alloc.append(get_alloc(n))
        return alloc