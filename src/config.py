# default values
measures_per_row = 6

dpi = 300 # typical print dpi
paper_sizes = {'a4': (2480, 3508),
               'letter': (2550, 3300)}

header_elems = {'title', 'composer', 'instrument', 'affiliation', 'time', 'key', 'tempo'}
types_bars = {'bar', 'dbar', 'ebar', 'lrep', 'rrep'}

n_commands = {'chord', 'group', 'qvr', 'sqvr', 'ccht', 'mm', 'sbrve'}

pitch = {'oct', 'sharp', 'flat', 'natural'}

# note width scaling factors
note_base_width = 30
space_base_width = int(30/2)

notes_space = {'sqvr': space_base_width*1,
               'qvr': space_base_width*2,
               'ccht': space_base_width*3,
               'mm': space_base_width*4,
               'sbrve': space_base_width*5}

duration = {'sqvr', 'qvr', 'ccht', 'mm', 'sbrve'}
dur_group_set = {'group', 'grace'} | duration

l_marg, r_marg = 150, 150

no_param_elems_primary_line = {'time'} | types_bars
one_param_elems_primary_line_front = {'grace', 'sharp', 'flat', 'natural'}
one_param_elems_primary_line_back = {'ddot', 'dot'}
two_param_elems_primary_line = {'fing'}

one_param_elems_primary_line = one_param_elems_primary_line_front | one_param_elems_primary_line_back

directions = {'down', 'up'}
octaves = {'oct'}
no_param_elems = types_bars

sym_factor = {'bar': 2,
              'dbar': 2,
              'lebar': 2,
              'rebar': 2,
              'lrep': 2,
              'rrep': 2,

              'sqvr': 1,
              'qvr': 2,
              'ccht': 3,
              'mm': 4,

              'sbrve': 5,
              'sharp': 1,
              'flat': 1,

              'natural': 1,
              'dot': 1, 
              'ddot': 2,
                
              'space': 1}

sym = {'bar': '|',
       'lebar': '[',
       'rebar': ']',
       'lrep': '{',
       'rrep': '}',

       'sharp': 's',
       'flat': 'b',
       'natural': 'n',

       'dot': '.',
       'ddot': '..',
       
       'down': u'\u0302',
       'up': u'\u0303',
       
       'space': ' '}

sym_opp = {v: k for k, v in sym.items()}

oct_sym = {-1: u'\u0300', # TODO: Change this to the actual symbol later
           1: u'\u0300',
           2: u'\u0301'}