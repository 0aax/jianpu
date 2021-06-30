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
note_base_width = 55
base_spacer = 30

notes_space = {'sqvr': base_spacer*1,
               'qvr': base_spacer*2,
               'ccht': base_spacer*3,
               'mm': base_spacer*4,
               'sbrve': base_spacer*5}

duration = {'sqvr', 'qvr', 'ccht', 'mm', 'sbrve'}