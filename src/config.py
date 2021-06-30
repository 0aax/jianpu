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
base_spacer = int(30/2)

notes_space = {'sqvr': base_spacer*1,
               'qvr': base_spacer*2,
               'ccht': base_spacer*3,
               'mm': base_spacer*4,
               'sbrve': base_spacer*5}

space_factors = {'sqvr': 1,
                'qvr': 2,
                'ccht': 3,
                'mm': 4,
                'sbrve': 5}

duration = {'sqvr', 'qvr', 'ccht', 'mm', 'sbrve'}

l_marg, r_marg = 150, 150

elems_notes_line = {'ddot', 'dot', 'sharp', 'flat', 'natural', 'grace', 'fing'} | types_bars