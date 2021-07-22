import re

import src.config as cfg
import src.utils as utls

def rearrange(measured_notes, ignore_time=True):

    def rr_note(n, ops=tuple()):
        if isinstance(n, int) or n is None:
            if len(ops) == 0: return [n]
            else: return [[list(ops), n]]
        elif n[0] in cfg.one_param: return rr_note(n[1], ops + (n[0],))
        elif n[0] in cfg.two_param: return rr_note(n[1], ops + ((n[0], n[2]),))
        elif n[0] == 'chord': return rr_note(n[1], ops)
        elif n[0] == 'time': return rr_note(n[1], ops + ((n[0], n[2]),))
        elif n[0] in cfg.n_param:
            rr_tmp = []
            for e in n[1:]: rr_tmp += rr_note(e, ops)
            return rr_tmp
        else: print(n, 'oops')
    
    rr_tmp = []
    for measure in measured_notes:
        rr_measure = []
        for n in measure:
            if ignore_time and isinstance(n, list) and n[0] == 'time': continue
            rr_measure += rr_note(n)
        rr_tmp += rr_measure
    return rr_tmp

def add_sym(primary, notes_syms, helper=None, return_as_str=True):
    """
    Given the string form of the primary line and an array of notes and the symbols that should be applied to them, returns a string of the notes and the symbols in the correct placement.
    """
    if isinstance(primary, str):
        primary_tmp = utls.arr_from_string(primary).copy()
    else: primary_tmp = primary.copy()

    len_prim, len_ns = len(primary), len(notes_syms)
    i_prim, i_tg = 0, 0
    aln_height = 0
    while i_prim < len_prim:
        updated = False
        if i_tg < len_ns:
            curr_prim, curr_tg = primary[i_prim], notes_syms[i_tg]
            if helper is not None:
                if cfg.dur_sym['sqvr'][2] in helper[i_prim]: curr_helper = 2
                elif cfg.dur_sym['qvr'][2] in helper[i_prim]: curr_helper = 1
                else: curr_helper = 0
            else: curr_helper = 0
            if curr_prim.isdigit():
                if isinstance(curr_tg, list) and int(curr_prim) == curr_tg[1]:
                    primary_tmp[i_prim], h_tmp = utls.sym_to_add(curr_helper, curr_tg)
                    aln_height = max(aln_height, h_tmp)
                    i_prim += 1
                    i_tg += 1
                    updated = True
                elif int(curr_prim) == curr_tg:
                    i_prim += 1
                    i_tg += 1
                    updated = True

        if not updated:
            i_prim += 1

    if return_as_str: return ''.join(primary_tmp), aln_height
    else: return primary_tmp, aln_height

def add_sym_sub(primary, subln_prim, subln_sec, return_as_str=True, ending_subln=False):
    """
    Given the string form of the primary line and an array of notes and the symbols that should be applied to them, returns a string of the notes and the symbols in the correct placement.
    """

    def get_digit(s):
        """
        Given a string, returns the first digit occurance.
        """
        digit = re.search(r'\d', s)
        if digit is None: return None
        return digit.group()
    
    def count_spaces(s):
        """
        Given string, returns the number of space characters.
        """
        return sum(1 for i in s if i == ' ')
    
    def extract_sym(s):
        """
        Given string, extracts symbols that have width.
        """
        return [i for i in s if i not in cfg.no_additional_width]

    if isinstance(primary, str):
        primary_tmp = utls.arr_from_string(primary).copy()
    else: primary_tmp = primary.copy()

    len_prim, len_ns = len(primary), len(subln_prim)
    i_prim, i_tg = 0, 0
    while i_prim < len_prim:
        updated = False
        if i_tg < len_ns:
            curr_prim, curr_tg = primary[i_prim], subln_prim[i_tg]
            dur_sym = ''
            if ending_subln:
                if cfg.dur_sym['sqvr'][2] in curr_prim:
                    dur_sym = cfg.dur_sym['sqvr'][2]
                    curr_helper = 2
                elif cfg.dur_sym['qvr'][2] in curr_prim:
                    dur_sym = cfg.dur_sym['qvr'][2]
                    curr_helper = 1
                else: curr_helper = 0
            else: curr_helper = 0

            curr_prim_digit = get_digit(curr_prim)
            if curr_prim_digit is not None and int(curr_prim_digit) == curr_tg:
                curr_subln = subln_sec[i_tg]
                if curr_tg == 0 and ending_subln:
                    primary_tmp[i_prim] = '0' + dur_sym
                elif curr_subln is None:
                    primary_tmp[i_prim] = '  '
                else:
                    primary_tmp[i_prim] = utls.sym_to_add(curr_helper, subln_sec[i_tg])[0] + dur_sym
                i_prim += 1
                i_tg += 1
                updated = True
        
        if not updated:
            p = extract_sym(primary[i_prim])
            tmp = 0
            for s in p:
                if s in cfg.sym_opp:
                    tmp += cfg.sym_factor[cfg.sym_opp[s]]
                if s in cfg.time_dn_opp: tmp += 2
            primary_tmp[i_prim] = ' '*tmp
            i_prim += 1

    if return_as_str: return ''.join(primary_tmp)
    else: return primary_tmp

def chords_arranged(measured_notes):
    """
    Given measured notes, returns a 2D array where each subarray is one particular line of the chord. Notes that are not chords have None as a placeholder.
    """

    def get_chord(n):
        if isinstance(n, int): return [n]
        elif n[0] == 'chord': return [n[1:]]
        elif n[0] in cfg.n_param:
            ch_tmp = []
            for e in n[1:]: ch_tmp += get_chord(e)
            return ch_tmp
        else: return get_chord(n[1])
    
    def sublines(ch):
        len_line = len(ch)
        num_lines = max([len(c) if isinstance(c, list) else 1 for c in ch])
        ds = [[0]*len_line for _ in range(num_lines)]

        for i, c in enumerate(ch):
            if isinstance(c, int): pop_tmp = [c] + [None]*(num_lines-1)
            else: pop_tmp = c + [None]*(num_lines - len(c))
            for j, pt in enumerate(pop_tmp): ds[j][i] = pt
        
        return ds
    
    chords = []
    for measure in measured_notes:
        ch_measure = []
        for n in measure:
            if not (isinstance(n, list) and n[0] == 'time'): ch_measure += get_chord(n)
        chords += ch_measure
    
    sl = sublines(chords)
    sl[0] = [n if isinstance(n, int) else n[1] for n in sl[0]]

    return sl

def get_primary(measured_notes):
    """
    Given measured notes, returns an array of notes and the corresponding operators that appear on the primary line.
    """

    def get_elems(n):
        if isinstance(n, int): return n
        elif n[0] in cfg.no_param_elems_prim: return n
        elif n[0] in cfg.one_param_elems_prim: return [n[0], get_elems(n[1])]
        elif n[0] in cfg.two_param_elems_prim: return [n[0], get_elems(n[1]), n[2]]
        elif n[0] in cfg.dur_group_set:
            dur_group_tmp = [n[0]] + [get_elems(e) for e in n[1:]]
            return dur_group_tmp
        # elif n[0] == 'chord': # only the uppermost note matters for this particular case
        #     return get_elems(n[1])
        else: return get_elems(n[1])
    
    prim = [[get_elems(n) for n in measure] for measure in measured_notes]
    return prim

def gen_primary_str(primary, original):
    """
    Returns a character-by-character array of the primary line, as well as a corresponding array containing the exact width allocation.
    """
    
    def get_alloc(n, in_g=False, in_d=False):
        if isinstance(n, int):
            if in_g or in_d: return str(n), cfg.note_base_width
            else: return str(n) + ' '*cfg.sym_factor['ccht'], cfg.note_base_width + cfg.space_base_width*cfg.sym_factor['ccht']
        elif n[0] == 'time': return cfg.time_dn[n[2]] + cfg.time_up[n[1]] + '  ', cfg.note_base_width + cfg.space_base_width*2
        elif n[0] in cfg.types_bars: return cfg.sym[n[0]], cfg.sym_factor[n[0]]*cfg.space_base_width
        elif n[0] in cfg.one_param_elems_prim_back:
            n_tmp, n_walloc = get_alloc(n[1], in_g=in_g, in_d=in_d)
            return n_tmp + cfg.sym[n[0]], n_walloc + cfg.sym_factor[n[0]]*cfg.space_base_width
        elif n[0] in cfg.one_param_elems_prim_front:
            n_tmp, n_walloc = get_alloc(n[1], in_g=in_g, in_d=in_d)
            return cfg.sym[n[0]] + n_tmp, n_walloc + cfg.sym_factor[n[0]]*cfg.space_base_width
        elif n[0] in cfg.duration:
            notes_tmp = n[1:]
            k = cfg.sym_factor[n[0]]
            n_tmp, n_walloc = '', 0
            for v in notes_tmp:
                v_tmp, v_walloc = get_alloc(v, in_g=in_g, in_d=True)
                n_tmp += v_tmp + ' '*k
                n_walloc += v_walloc + cfg.space_base_width*k
            if not in_g:
                return n_tmp + '  ', n_walloc + 30
            else:
                return n_tmp, n_walloc
        elif n[0] == 'group':
            n_walloc = [get_alloc(e, in_g=True, in_d=in_d) for e in n[1:]]
            n_tmp, n_walloc = zip(*n_walloc)
            n_tmp = [l for v in n_tmp for l in v]
            n_tmp = ''.join(n_tmp) + '  '
            n_walloc = sum(n_walloc) + cfg.space_base_width*2
            return n_tmp, n_walloc
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

    walloc = []
    notes = []
    bars = []
    notes_orig = []

    for i, measure in enumerate(primary):
        measure_walloc = [get_alloc(n) for n in measure]
        notes_tmp, walloc_tmp = zip(*measure_walloc)

        notes_tmp = ''.join(notes_tmp)
        walloc_tmp = sum(walloc_tmp)

        # make sure that the spacing is correct
        num_space = count_comp(notes_tmp[-2::-1], ' ')
        no_bar_notes = notes_tmp[:-1]
        bars.append(notes_tmp[-1])

        if num_space > 0:
            notes_tmp = no_bar_notes[:(-num_space)]
            walloc_tmp -= cfg.space_base_width*num_space + cfg.note_base_width
        
        notes.append(notes_tmp)
        walloc.append(walloc_tmp)
        notes_orig.append(original[i])

    return notes, bars, walloc, notes_orig

def get_dur_group(measured_notes):
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

def match_prim_dur(primary, dur_group, return_as_str=False):
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