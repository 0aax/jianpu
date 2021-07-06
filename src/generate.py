from PIL import Image, ImageDraw
import src.config as cfg

def get_target_group_line(measured_notes, target_group={}, target_func=(lambda n0: None)):
    """
    Given measured notes, returns an array of notes and the corresponding target group operators.
    """
    def get_elems(n):
        if isinstance(n, int): return [n]
        elif n[0] in cfg.no_param_elems: return n
        elif n[0] in target_group: return target_func(n)
        elif n[0] in cfg.dur_group_set:
            dur_group_tmp = []
            for e in n[1:]: dur_group_tmp += get_elems(e)
            return dur_group_tmp
        else: return get_elems(n[1])
    
    tg_line = []
    for measure in measured_notes:
        tg_measure = []
        for n in measure:
            if not (isinstance(n, list) and n[0] == 'time'): tg_measure += get_elems(n)
        tg_line += tg_measure
    return tg_line

def get_primary_line(measured_notes):
    """
    Given measured notes, returns an array of notes and the corresponding operators that appear on the primary line.
    """

    def get_elems(n):
        if isinstance(n, int): return n
        elif n[0] in cfg.no_param_elems_primary_line: return n
        elif n[0] in cfg.one_param_elems_primary_line: return [n[0], get_elems(n[1])]
        elif n[0] in cfg.two_param_elems_primary_line: return [n[0], get_elems(n[1]), n[2]]
        elif n[0] in cfg.dur_group_set:
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
            if in_g or in_d: return str(n), cfg.note_base_width
            else: return str(n) + '   ', cfg.note_base_width + cfg.space_base_width * cfg.sym_factor['ccht']
        elif n[0] == 'time': return '   ', cfg.note_base_width + cfg.space_base_width # leave empty space for the time signature pass
        elif n[0] in cfg.types_bars: return cfg.sym[n[0]], cfg.sym_factor[n[0]]*cfg.space_base_width
        elif n[0] in cfg.one_param_elems_primary_line_back:
            n_tmp, n_alloc = get_walloc(n[1], in_g=in_g, in_d=in_d)
            return n_tmp + cfg.sym[n[0]], n_alloc + cfg.sym_factor[n[0]]*cfg.space_base_width
        elif n[0] in cfg.one_param_elems_primary_line_front:
            n_tmp, n_alloc = get_walloc(n[1], in_g=in_g, in_d=in_d)
            return cfg.sym[n[0]] + n_tmp, n_alloc + cfg.sym_factor[n[0]]*cfg.space_base_width
        elif n[0] in cfg.duration:
            notes_tmp = n[1:]
            k = cfg.sym_factor[n[0]]
            n_tmp, n_alloc = '', 0
            for v in notes_tmp:
                v_tmp, v_alloc = get_walloc(v, in_g=in_g, in_d=True)
                n_tmp += v_tmp + ' '*k
                n_alloc += v_alloc + cfg.space_base_width*k
            if not in_g:
                return n_tmp + '  ', n_alloc + 30
            else:
                return n_tmp, n_alloc
        elif n[0] == 'group':
            n_walloc = [get_walloc(e, in_g=True, in_d=in_d) for e in n[1:]]
            n_tmp, n_alloc = zip(*n_walloc)
            n_tmp = [l for v in n_tmp for l in v]
            n_tmp = ''.join(n_tmp) + '  '
            n_alloc = sum(n_alloc) + cfg.space_base_width*2
            return n_tmp, n_alloc
        else:
            print('else', n)
            return str(n), cfg.note_base_width
    
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
            walloc_tmp += cfg.space_base_width*(2-num_space)
        elif num_space > 2:
            notes_tmp = no_bar_notes[:(2-num_space)] + bar_notes
            walloc_tmp -= cfg.space_base_width*(num_space-2)

        if first_measure:
            notes += notes_tmp
            walloc += walloc_tmp
            first_measure = False
        else:
            notes += '  ' + notes_tmp
            walloc += 30 + walloc_tmp

    return notes, walloc

def match_primary_target_group(primary, target_group, target_sym=(lambda x: None)):
    """
    Given the string form of the primary line and an array notes and their corresponding directions, returns a string of the target group.
    """
    def arr_from_string(string):
        """
        Returns an array from a string.
        """
        return [e for e in string]

    primary_tmp = arr_from_string(primary)

    len_prim, len_dir = len(primary), len(target_group)
    i_prim, i_dir = 0, 0
    while i_dir < len_dir:
        curr_prim, curr_dir = primary[i_prim], target_group[i_dir]
        if curr_prim.isdigit():
            if isinstance(curr_dir, list) and int(curr_prim) == curr_dir[1]:
                primary_tmp[i_prim] = target_sym(curr_dir)
                i_prim += 1
                i_dir += 1
            elif int(curr_prim) == curr_dir:
                primary_tmp[i_prim] = '  '
                i_prim += 1
                i_dir += 1
            else:
                primary_tmp[i_prim] = '  '
                i_prim += 1
        else:
            primary_tmp[i_prim] = ' ' * cfg.sym_factor[cfg.sym_opp[curr_prim]]
            i_prim += 1
    primary_tmp[-1] = ' ' # end bar
    return ''.join(primary_tmp)
