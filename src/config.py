# default values
measures_per_row = 6

dpi = 300 # typical print dpi
paper_sizes = {'a4': (2480, 3508),
               'letter': (2550, 3300)}
side_margin = {'a4': 70,
               'letter': 90}

header_elems = {'title', 'composer', 'instrument', 'affiliation', 'time', 'key', 'tempo'}
types_bars = {'bar', 'dbar', 'ebar', 'lrep', 'rrep'}

n_commands = {'chord', 'group', 'qvr', 'sqvr', 'ccht', 'mm', 'sbrve'}

pitch = {'oct', 'sharp', 'flat', 'natural'}

prim_vert_space = 150
# note width scaling factors
note_base_width = 30
space_base_width = int(30/2)

note_base_height = 50
above_note_height = 20

notes_space = {'sqvr': space_base_width*1,
               'qvr': space_base_width*2,
               'ccht': space_base_width*3,
               'mm': space_base_width*4,
               'sbrve': space_base_width*5}

duration = {'sqvr', 'qvr', 'ccht', 'mm', 'sbrve'}
dur_group_set = {'group', 'grace'} | duration

l_marg, r_marg = 150, 150

no_param_elems_prim = types_bars
one_param_elems_prim_front = {'grace', 'sharp', 'flat', 'natural'}
one_param_elems_prim_back = {'ddot', 'dot'}
two_param_elems_prim = {'fing', 'time'}

one_param_elems_prim = one_param_elems_prim_front | one_param_elems_prim_back

directions = {'down', 'up'}
octaves = {'oct'}
tie_slur = {'stie', 'etie', 'sslur', 'eslur'}
dynamics = {'p', 'mp', 'f', 'mf'}
dots = {'dot', 'ddot'}
no_param_elems = types_bars

ignore_syms = dots

one_param = directions | tie_slur | dynamics | {'ddot', 'dot', 'trem', 'grace'}
two_param = {'time', 'fing'} | octaves
n_param = duration | {'group'}

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
                
              'space': 1,
              'big_space': 2,
              
              'none': 0,
              'one': 1,
              'two': 2}

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
       
       'space': ' ',
       'big_space': '!'}

sym_opp = {v: k for k, v in sym.items()}

loct_info = {u'\u0305', u'\u0304'}
oct_sym = {-2: {0: u'\u030D', 1: u'\u0309', 2: u'\u030B'},
           -1: {0: u'\u030C', 1: u'\u0308', 2: u'\u030A'},
            1: {0: u'\u0300', 1: u'\u0300', 2: u'\u0300'},
            2: {0: u'\u0301', 1: u'\u0301', 2: u'\u0301'}}

dur_sym = {'sqvr': {1: u'\u0307', 2: u'\u0305'},
           'qvr':  {1: u'\u0306', 2: u'\u0304'},
           'ccht': {1: '', 2: ''},
           'mm':   {1: '', 2: ''}}

time_dn = {0: 'A',
           1: 'B',
           2: 'C',
           3: 'D',
           4: 'E',
           5: 'F',
           6: 'G',
           7: 'H',
           8: 'I',
           9: 'J'}

time_dn_opp = {v: k for k, v in time_dn.items()}

time_up = {0: u'\u0318',
           1: u'\u0319',
           2: u'\u031A',
           3: u'\u031B',
           4: u'\u031C',
           5: u'\u031D',
           6: u'\u031E',
           7: u'\u031F',
           8: u'\u0320',
           9: u'\u0321'}