from PIL import Image, ImageDraw

# default values
measures_per_row = 6

dpi = 300 # typical print dpi
paper_sizes = {'a4': (2480, 3508),
               'letter': (2550, 3300)}

header_elems = {'title', 'composer', 'instrument', 'affiliation', 'time', 'key', 'tempo'}
types_measures = {'bar', 'dbar', 'ebar', 'lrep', 'rrep'}

two_no_add_halloc = {'roct', 'loct'}
n_no_add_halloc = {'qvr', 'sqvr', 'ccht', 'mm', 'sbrve'}
no_add_halloc = two_no_add_halloc | n_no_add_halloc | types_measures

one_add_halloc_notes = {'down', 'up', 'trem', 'grace', 'scresc', 'ecresc', 'sdim', 'edim'}
two_add_halloc_notes = {'fing'}
n_add_halloc_notes = {'chord'}
add_halloc_notes = one_add_halloc_notes | two_add_halloc_notes | n_add_halloc_notes

two_commands = two_no_add_halloc | two_add_halloc_notes
n_commands = n_add_halloc_notes | n_no_add_halloc | {'group'}

pitch = {'roct', 'loct', 'sharp', 'flat', 'natural'}

# note width scaling factors
note_base_width = 50
base_note_spacer = 30

notes_space = {'sqvr': 10,
               'qvr': 20,
               'ccht': 30,
               'mm': 50,
               'sbrve': 70}

duration = {'sqvr', 'qvr', 'ccht', 'mm', 'sbrve'}

class Composition:
    def __init__(self, parsed=list(), paper_type='letter', margins=[75, 75, 75, 75]):
        
        self.paper_type = paper_type
        self.parsed = parsed
        self.uniform_parsed = self.gen_uniform_parse(parsed)
        self.header, self.notes = self.split_header_notes(self.uniform_parsed)
        
        self.paper = Image.new('RGB', paper_sizes[paper_type], (255, 255, 255))
        self.margins = {'top': margins[0], 'right': margins[1], 'bottom': margins[2], 'left': margins[3]} # initally set to quarter-inch margins on all sides

        self.header_height = 0
        self.line_height = 0
        self.num_lines = 0

        self.measured_notes = self.gen_measured_notes(self.notes)
        self.only_notes = self.gen_only_notes(self.measured_notes, grouped=False)
        self.only_dur_group = self.gen_only_dur_group(self.measured_notes)
        self.notes_height_alloc = self.gen_notes_height_alloc(self.measured_notes)
        self.notes_width_alloc = self.gen_notes_width_alloc(self.only_dur_group)
        # self.only_notes_grouped = self.gen_only_notes(self.measured_notes, grouped=True)

        self.measure_heights = self.gen_measure_heights(self.notes_height_alloc)
        self.measure_widths = self.gen_measure_widths(self.notes_width_alloc)
    
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
            if isinstance(n, int): parse_uni.append(['ccht', n])
            # elif n[0] in n_no_add_halloc:
            #     for v in n[1:]: parse_uni.append([n[0], v])
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

    def gen_measured_notes(self, notes):
        """
        Re-organizes notes such that all notes in a bar are grouped in an array.
        """
        measured_notes = []
        curr_bar = []
        for n in notes:
            if n[0] in types_measures:
                measured_notes.append(curr_bar)
                curr_bar = []
            else: curr_bar.append(n)
        if len(curr_bar) != 0: measured_notes.append(curr_bar)
        return measured_notes
    
    def gen_only_notes(self, measured_notes, grouped=False):
        """
        Given an input that has already been grouped into measures, returns only the notes.
        - grouped=False, notes that are part of the same group will not be nested in a separate array
        - grouped=True, notes that are grouped will be put into a separate array
        """
        if grouped: nest_array = n_add_halloc_notes | {'group'}
        else: nest_array = n_add_halloc_notes

        def get_note(n):
            if isinstance(n, int): return [n]
            elif n[0] in pitch: return [[n[0]] + get_note(n[1])]
            elif n[0] in n_commands:
                n_notes = []
                for e in n[1:]: n_notes += get_note(e)
                n_notes = [n_notes] if n[0] in nest_array else n_notes
                return n_notes
            else:
                return get_note(n[1])
        
        notes = []
        for measure in measured_notes:
            measure_notes = []
            for n in measure: measure_notes += get_note(n)
            notes.append(measure_notes)
        return notes

    def gen_only_dur_group(self, measured_notes):
        """
        Given an input that has already been grouped into measures, returns all notes. Notes that are part of a group or have a duration will have an additional indicator. Only the first note of a chord will appear as a placeholder.
        """
        dur_group_set = {'group', 'grace'} | duration
        
        def get_dur_group(n):
            if isinstance(n, int): return n
            elif n[0] in dur_group_set:
                dur_group_tmp = [n[0]] + [get_dur_group(e) for e in n[1:]]
                return dur_group_tmp
            elif n[0] == 'chord': return get_dur_group(n[1])
            else: return get_dur_group(n[1])

        dur_group = []
        for measure in measured_notes:
            dur_group_measure = [get_dur_group(n) for n in measure]
            dur_group.append(dur_group_measure)
        return dur_group

    def gen_notes_height_alloc(self, measured_notes):
        """
        Given an input that has already been grouped into measures, returns height allocation for notes.
        """
        def get_halloc(n):
            if isinstance(n, int): return 1
            elif n[0] == 'group':
                n_alloc = []
                for e in n[1:]:
                    n_alloc_tmp = get_halloc(e)
                    if isinstance(n_alloc_tmp, int): n_alloc.append(n_alloc_tmp)
                    else: n_alloc += n_alloc_tmp
                return n_alloc
            elif n[0] in n_add_halloc_notes:
                n_alloc = 0
                for e in n[1:]: n_alloc += get_halloc(e)
                return n_alloc
            elif n[0] in n_no_add_halloc:
                n_alloc = []
                for e in n[1:]: n_alloc += [get_halloc(e)]
                return n_alloc
            else:
                alloc_tmp = 1 if n[0] in add_halloc_notes else 0
                return get_halloc(n[-1]) + alloc_tmp
        
        halloc = []
        for measure in measured_notes:
            measure_alloc = []
            for n in measure:
                alloc_tmp = get_halloc(n)
                if isinstance(alloc_tmp, int): measure_alloc.append(alloc_tmp)
                else: measure_alloc += alloc_tmp
            halloc.append(measure_alloc)
        return halloc
    
    def gen_notes_width_alloc(self, dur_group_notes):
        """
        Given an input that has already been grouped into measures and has indicators for durations and groups, returns width allocation for notes.
        """
        def get_walloc(n):
            if isinstance(n, int): return note_base_width
            elif n[0] in duration:
                n_count = len(n[1:])
                return note_base_width * n_count + notes_space[n[0]] * (n_count - 1)
            elif n[0] == 'group':
                n_alloc = [get_walloc(e) for e in n[1:]]
                return n_alloc
            else: return note_base_width

        walloc = []
        for measure in dur_group_notes:
            measure_alloc = [get_walloc(n) for n in measure]
            measure_alloc.append(base_note_spacer * (len(measure_alloc) - 1))
            walloc.append(measure_alloc)
        return walloc

    def gen_measure_heights(self, heights):
        """
        Given array of note heights that have already been divided into measures, returns an array of the heights for each measure.
        """
        max_h = [max(m) for m in heights]
        return max_h
    
    def gen_measure_widths(self, widths):
        """
        Given array of note widths that have already been divided into measures, returns an array of the widths for each measure.
        """
        def deep_sum(n):
            """
            Returns the sum of an array that may have nested arrays.
            """
            if isinstance(n, int): return n
            else: return sum([deep_sum(e) for e in n])

        width_m = [deep_sum(m) for m in widths]
        return width_m
