from PIL import Image, ImageDraw
from src.config import *

def get_direction_line(measured_notes):
    """
    Given measured notes, returns an array of notes and the corresponding directions.
    """
    def get_note(n):
        if isinstance(n, int): return n
        else: return get_note(n[1])

    def get_elems(n):
        if isinstance(n, int): return [n]
        elif n[0] in no_param_elems: return [n]
        elif n[0] in directions: return [[n[0], get_note(n)]]
        elif n[0] in dur_group_set:
            dur_group_tmp = []
            for e in n[1:]: dur_group_tmp += get_elems(e)
            return dur_group_tmp
        else: return get_elems(n[1])
    
    directions_line = []
    for measure in measured_notes:
        directions_measure = []
        for n in measure:
            if isinstance(n, list) and n[0] != 'time': directions_measure += get_elems(n)
        directions_line += directions_measure
    return directions_line

def get_primary_line(measured_notes):
    """
    Given measured notes, returns an array of notes and the corresponding operators that appear on the primary line.
    """

    def get_elems(n):
        if isinstance(n, int): return n
        elif n[0] in no_param_elems_primary_line: return n
        elif n[0] in one_param_elems_primary_line: return [n[0], get_elems(n[1])]
        elif n[0] in two_param_elems_primary_line: return [n[0], get_elems(n[1]), n[2]]
        elif n[0] in dur_group_set:
            dur_group_tmp = [n[0]] + [get_elems(e) for e in n[1:]]
            return dur_group_tmp
        # elif n[0] == 'chord': # only the uppermost note matters for this particular case
        #     return get_elems(n[1])
        else: return get_elems(n[1])
    
    primary_line = [[get_elems(n) for n in measure] for measure in measured_notes]
    return primary_line

def gen_primary_line_str(primary_line):
    """
    Returns a character-by-character array of the primary line, as well as a corresponding array containing the exact width allocation.
    """
    def get_walloc(n, in_g=False, in_d=False):
        if isinstance(n, int):
            if in_g or in_d: return str(n), note_base_width
            else: return str(n) + '   ', note_base_width + space_base_width * sym_factor['ccht']
        elif n[0] == 'time': return '   ', note_base_width + space_base_width # leave empty space for the time signature pass
        elif n[0] in types_bars: return sym[n[0]], sym_factor[n[0]]*space_base_width
        elif n[0] in one_param_elems_primary_line_back:
            n_tmp, n_alloc = get_walloc(n[1], in_g=in_g, in_d=in_d)
            return n_tmp + sym[n[0]], n_alloc + sym_factor[n[0]]*space_base_width
        elif n[0] in one_param_elems_primary_line_front:
            n_tmp, n_alloc = get_walloc(n[1], in_g=in_g, in_d=in_d)
            return sym[n[0]] + n_tmp, n_alloc + sym_factor[n[0]]*space_base_width
        elif n[0] in duration:
            notes_tmp = n[1:]
            k = sym_factor[n[0]]
            n_tmp, n_alloc = '', 0
            for v in notes_tmp:
                v_tmp, v_alloc = get_walloc(v, in_g=in_g, in_d=True)
                n_tmp += v_tmp + ' '*k
                n_alloc += v_alloc + space_base_width*k
            if not in_g:
                return n_tmp + '  ', n_alloc + 30
            else:
                return n_tmp, n_alloc
        elif n[0] == 'group':
            n_walloc = [get_walloc(e, in_g=True, in_d=in_d) for e in n[1:]]
            n_tmp, n_alloc = zip(*n_walloc)
            n_tmp = [l for v in n_tmp for l in v]
            n_tmp = ''.join(n_tmp) + '  '
            n_alloc = sum(n_alloc) + space_base_width*2
            return n_tmp, n_alloc
        else:
            print('else', n)
            return str(n), note_base_width
    
    def count_comp(lst, comp=' '):
        """
        Counts to number of continuous 'comp' instances from the front of the list
        """
        num_comp = 0
        for n in lst:
            if n == comp: num_comp += 1
            else: break
        return num_comp

    walloc = 0
    notes = ''
    first_measure = True
    for measure in primary_line:
        measure_alloc = [get_walloc(n) for n in measure]
        notes_tmp, walloc_tmp = zip(*measure_alloc)
        notes_tmp = ''.join(notes_tmp)
        walloc_tmp = sum(walloc_tmp)

        num_space = count_comp(notes_tmp[-2::-1])
        no_bar_notes = notes_tmp[:-1]
        bar_notes = notes_tmp[-1]
        if num_space < 2:
            notes_tmp = no_bar_notes + ' '*(2-num_space) + bar_notes
            walloc_tmp += space_base_width*(2-num_space)
        elif num_space > 2:
            notes_tmp = no_bar_notes[:(2-num_space)] + bar_notes
            walloc_tmp -= space_base_width*(num_space-2)

        if first_measure:
            notes += notes_tmp
            walloc += walloc_tmp
            first_measure = False
        else:
            notes += '  ' + notes_tmp
            walloc += 30 + walloc_tmp

    return notes, walloc

def list_from_string(string):
    """
    Returns an array from a string.
    """
    return [e for e in string]

def match_primary_direction(primary, direction):
    primary_tmp = primary.copy()
    