from os import set_inheritable
from PIL import Image, ImageDraw

# default values
bars_per_row = 6

DPI = 300 # typical print dpi
paper_sizes = {'a4': (2480, 3508),
               'letter': (2550, 3300)}

header_elems = {'title', 'comp', 'inst'}
types_bars = {'bar', 'lrep', 'rrep'}

two_no_add_alloc = {'roct', 'loct'}
n_no_add_alloc = {'qvr', 'sqvr', 'qtr', 'mm', 'sbrve'}
no_add_alloc = two_no_add_alloc | n_no_add_alloc | types_bars

one_add_alloc_notes = {'down', 'up', 'trem', 'grace', 'scresc', 'ecresc', 'sdim', 'edim'}
two_add_alloc_notes = {'fing'}
n_add_alloc_notes = {'chord'}
add_alloc_notes = one_add_alloc_notes | two_add_alloc_notes | n_add_alloc_notes

class Composition:
    def __init__(self, paper_type='letter', parsed=list()):
        
        self.paper_type = paper_type
        self.parsed = parsed
        self.uniform_parsed = self.gen_uniform_parse(parsed)
        self.header, self.notes = self.split_header_notes(self.uniform_parsed)
        
        self.paper = Image.new('RGB', paper_sizes[paper_type], (255, 255, 255))

        self.header_height = 0
        self.line_height = 0
        self.num_lines = 0

        self.barred_notes = self.gen_barred_notes(self.notes)
        self.naive_notes_alloc = self.gen_naive_notes_alloc(self.barred_notes)
    
    def set_header_height(self, height):
        """
        Sets height of header.
        """
        self.header_height = height
    
    def set_line_height(self, height):
        """
        Sets line height.
        """
        self.line_height = height
    
    def gen_header_info(self, header_info):
        """
        Returns a dictionary from a list of header info.
        """
        header = {}
        for n in header_info:
            header[n[0]] = n[-1]
        return header
    
    def gen_uniform_parse(self, parsed):
        """
        Makes the parsed input more uniform in style.
        """
        parse_uni = []
        for n in parsed:
            if isinstance(n, int): parse_uni.append(['qtr', n])
            elif n[0] in n_no_add_alloc:
                for v in n[1:]: parse_uni.append([n[0], v])
            else: parse_uni.append(n)
        return parse_uni

    def split_header_notes(self, uni_parsed):
        """
        Given input, separates the header info from the notes.
        """
        notes_tmp = []
        header = []
        for n in uni_parsed:
            if n[0] == 'header':
                header = self.gen_header_info(n[1:])
            else: notes_tmp.append(n)
        return header, notes_tmp

    def gen_barred_notes(self, notes):
        """
        Re-organizes notes such that all notes in a bar are grouped in an array.
        """
        barred_notes = []
        curr_bar = []
        for n in notes:
            if n[0] in types_bars:
                barred_notes.append(curr_bar)
                curr_bar = []
            else: curr_bar.append(n)
        if len(curr_bar) != 0: barred_notes.append(curr_bar)
        return barred_notes

    def gen_naive_notes_alloc(self, barred_notes):
        """
        Given an input that has already been grouped into bars, returns naive line allocation for notes.
        """
        def get_alloc(n):
            if isinstance(n, int) or n[0] in no_add_alloc: return 1
            elif n[0] in n_add_alloc_notes:
                chord_alloc = 0
                for e in n[1:]: chord_alloc += get_alloc(e)
                return chord_alloc
            else:
                alloc_tmp = 1 if n[0] in add_alloc_notes else 0
                return get_alloc(n[-1]) + alloc_tmp
        
        alloc = []
        for bar in barred_notes:
            bar_alloc = []
            for n in bar: bar_alloc.append(get_alloc(n))
            alloc.append(bar_alloc)
        return alloc