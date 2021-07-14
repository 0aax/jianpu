from PIL import Image, ImageDraw
import src.config as cfg
import src.utils as utls

def rearrange(measured_notes):

    def rr_note(n, ops=tuple()):
        if isinstance(n, int):
            if len(ops) == 0: return [n]
            else: return [[list(ops), n]]
        elif n[0] in cfg.one_param: return rr_note(n[1], ops + (n[0],))
        elif n[0] in cfg.two_param: return rr_note(n[1], ops + ((n[0], n[2]),))
        elif n[0] == 'chord': return rr_note(n[1], ops)
        elif n[0] in cfg.n_param:
            rr_tmp = []
            for e in n[1:]: rr_tmp += rr_note(e, ops)
            return rr_tmp
        else: print(n, 'oops')
    
    rr_tmp = []
    for measure in measured_notes:
        rr_measure = []
        for n in measure:
            if not (isinstance(n, list) and n[0] == 'time'): rr_measure += rr_note(n)
        rr_tmp += rr_measure
    return rr_tmp


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

def get_dur_group_line(measured_notes):
    """
    Given an input that has already been grouped into measures, returns notes such that notes of a group or have a duration will have an additional indicator.
    """
    
    def get_dur_group(n):
        if isinstance(n, int): return n
        elif n[0] == 'group':
            group_tmp = []
            for e in n[1:]: group_tmp += get_dur_group(e)
            return group_tmp
        elif n[0] in cfg.duration:
            dur_tmp = [n[0]] + [get_dur_group(e) for e in n[1:]]
            return dur_tmp
        else: return get_dur_group(n[1])

    dur_group = []
    for measure in measured_notes:
        measure_dur_group = []
        for n in measure:
            if not (isinstance(n, list) and n[0] == 'time'): measure_dur_group.append(get_dur_group(n))
        dur_group += measure_dur_group
    return dur_group

def get_chord_line(measured_notes):
    """
    Given an input that has already been grouped into measures, returns notes such that notes of a chord are grouped.
    """
    
    def get_chord(n):
        if isinstance(n, int): return n
        elif n[0] == 'chord':
            chord_tmp = [get_chord(e) for e in n[1:]]
            return chord_tmp
        else: return get_chord(n[1])

    chords = []
    for measure in measured_notes:
        measure_chords = []
        for n in measure:
            if not (isinstance(n, list) and n[0] == 'time'): measure_chords.append(get_chord(n))
        chords += measure_chords
    return chords

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

def match_primary_target_group(primary, target_group, helper=None, target_sym=(lambda x: None), return_as_str=False):
    """
    Given the string form of the primary line and an array notes and their corresponding target group, returns a string of the target group symbols in the correct placement.
    """
    primary_tmp = primary.copy()

    len_prim, len_tg = len(primary), len(target_group)
    i_prim, i_tg = 0, 0
    while i_prim < len_prim:
        updated = False
        if i_tg < len_tg:
            curr_prim, curr_tg = primary[i_prim], target_group[i_tg]
            if helper is not None:
                if cfg.dur_sym['sqvr'][2] in helper[i_prim]: curr_helper = 2
                elif cfg.dur_sym['qvr'][2] in helper[i_prim]:
                    curr_helper = 1
                else: curr_helper = 0
            else: curr_helper = 0
            if curr_prim.isdigit():
                if isinstance(curr_tg, list) and int(curr_prim) == curr_tg[1]:
                    primary_tmp[i_prim] = target_sym(curr_tg, curr_helper)
                    i_prim += 1
                    i_tg += 1
                    updated = True
                elif int(curr_prim) == curr_tg:
                    primary_tmp[i_prim] = ''
                    i_prim += 1
                    i_tg += 1
                    updated = True
        
        if not updated:
            primary_tmp[i_prim] = ''
            i_prim += 1

    if return_as_str: return ''.join(primary_tmp)
    else: return primary_tmp

def match_primary_duration(primary, dur_group, return_as_str=False):
    """
    Given the string form of the primary line and an array notes and their corresponding durations, returns a string of the duration symbols in their proper places.
    """
    primary_tmp = primary.copy()

    len_prim, len_dir = len(primary), len(dur_group)
    i_prim, i_dur = 0, 0

    while i_prim < len_prim:
        updated = False
        if i_dur < len_dir:
            curr_dur = dur_group[i_dur]
            curr_prim = primary[i_prim]
            if isinstance(curr_dur, list) and curr_prim != ' ':
                i_match = 0
                len_match = len(curr_dur)

                prev_sym = ''
                while i_match < len_match:
                    curr_prim = primary[i_prim]

                    if not curr_prim.isdigit():
                        primary_tmp[i_prim] = prev_sym
                        i_prim += 1
                        continue

                    if curr_dur[i_match] in cfg.duration:
                        dur_sym_dict = cfg.dur_sym[curr_dur[i_match]]
                        i_match += 1

                    if curr_prim.isdigit() and int(curr_prim) == curr_dur[i_match]:
                        primary_tmp[i_prim] = dur_sym_dict[2]
                        i_prim += 1
                        i_match += 1
                        prev_sym = dur_sym_dict[2]
                    else:
                        primary_tmp[i_prim] = dur_sym_dict[1]
                        i_prim += 1
                        prev_sym = dur_sym_dict[1]
                updated = True
                i_dur += 1
            else:
                if curr_prim.isdigit() and int(curr_prim) == curr_dur:
                    primary_tmp[i_prim] = ''
                    i_prim += 1
                    i_dur += 1
                    updated = True
                
        if not updated:
            primary_tmp[i_prim] = ''
            i_prim += 1

    if return_as_str: return ''.join(primary_tmp)
    else: return primary_tmp