# default values
measures_per_row = 6

dpi = 300 # typical print dpi
paper_sizes = {'a4': (2480, 3508),
               'letter': (2550, 3300)}

header_elems = {'title', 'composer', 'instrument', 'affiliation', 'time', 'key', 'tempo'}
types_bars = {'bar', 'dbar', 'ebar', 'lrep', 'rrep'}

# two_no_add_halloc = {'roct', 'loct'}
# n_no_add_halloc = {'qvr', 'sqvr', 'ccht', 'mm', 'sbrve'}
# no_add_halloc = two_no_add_halloc | n_no_add_halloc | types_bars

# one_add_halloc_notes = {'down', 'up', 'trem', 'grace', 'scresc', 'ecresc', 'sdim', 'edim'}
# two_add_halloc_notes = {'fing'}
# n_add_halloc_notes = {'chord'}
# add_halloc_notes = one_add_halloc_notes | two_add_halloc_notes | n_add_halloc_notes

# two_commands = two_no_add_halloc | two_add_halloc_notes
n_commands = {'chord', 'group', 'qvr', 'sqvr', 'ccht', 'mm', 'sbrve'}

pitch = {'roct', 'loct', 'sharp', 'flat', 'natural'}

# note width scaling factors
note_base_width = 30
space_base_width = int(30/2)

notes_space = {'sqvr': space_base_width*1,
               'qvr': space_base_width*2,
               'ccht': space_base_width*3,
               'mm': space_base_width*4,
               'sbrve': space_base_width*5}

space_factors = {'sqvr': 1,
                'qvr': 2,
                'ccht': 3,
                'mm': 4,
                'sbrve': 5}

bar_spacers = {'bar': space_base_width,
               'dbar': space_base_width,
               'ebar': space_base_width,
               'lrep': note_base_width,
               'rrep': note_base_width}

duration = {'sqvr', 'qvr', 'ccht', 'mm', 'sbrve'}
dur_group_set = {'group', 'grace'} | duration

l_marg, r_marg = 150, 150

no_param_elems_primary_line = {'time'} | types_bars
one_param_elems_primary_line_front = {'grace', 'sharp', 'flat', 'natural'}
one_param_elems_primary_line_back = {'ddot', 'dot'}
two_param_elems_primary_line = {'fing'}

one_param_elems_primary_line = one_param_elems_primary_line_front | one_param_elems_primary_line_back