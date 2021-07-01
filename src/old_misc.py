from src.config import *

def arrange_lines(approx_widths, only_notes, available_horiz_space=2550):
    """
    Given approximate measure widths, arranges measures (and the notes contained in each measure) into lines using a greedy approach.
    """
    lines_prelim = {}
    curr_line_num = 0
    curr_avail_space = available_horiz_space

    for i, measure_width in enumerate(approx_widths):
        if measure_width > curr_avail_space:
            curr_avail_space = available_horiz_space
            curr_line_num += 1

        if curr_line_num in lines_prelim:
            lines_prelim[curr_line_num]['measures'].append(i)
        else:
            lines_prelim[curr_line_num] = {}
            lines_prelim[curr_line_num]['measures'] = [i]
        
        curr_avail_space -= measure_width
        lines_prelim[curr_line_num]['avail_space'] = curr_avail_space
    
    lines = []
    for l, v in lines_prelim.items():
        curr_line = v['measures']
        expanded_line = [only_notes[i] for i in curr_line]
        lines.append(expanded_line)

    return lines

def gen_notes_width_alloc(primary_line):
    """
    Returns a character-by-character array of the primary line, as well as a corresponding array containing the exact width allocation.
    """
    def get_walloc(n):
        if isinstance(n, int): return [n], [note_base_width]
        elif n[0] == 'time': return ['time', 'space'], [note_base_width, space_base_width]
        elif n[0] in types_bars: return [n[0]], [sym_factor[n[0]]*space_base_width]
        elif n[0] in one_param_elems_primary_line_back:
            n_tmp, n_alloc = get_walloc(n[1])
            return n_tmp + [n[0]], n_alloc + [15]
        elif n[0] in one_param_elems_primary_line_front:
            n_tmp, n_alloc = get_walloc(n[1])
            return [n[0]] + n_tmp, [note_base_width] + n_alloc
        elif n[0] in duration:
            notes_tmp = n[1:]
            k = sym_factor[n[0]]
            n_tmp, n_alloc = [], []
            for v in notes_tmp:
                v_tmp, v_alloc = get_walloc(v)
                n_tmp += v_tmp + ['space']*k
                n_alloc += v_alloc + [space_base_width]*k
            return n_tmp, n_alloc
        elif n[0] == 'group':
            n_walloc = [get_walloc(e) for e in n[1:]]
            n_tmp, n_alloc = zip(*n_walloc)
            n_tmp = [l for v in n_tmp for l in v]
            n_alloc = [l for v in n_alloc for l in v]
            return n_tmp, n_alloc
        else: return [n], [note_base_width]
    
    def count_comp(lst, comp='space'):
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
    for measure in primary_line:
        measure_alloc = [get_walloc(n) for n in measure]
        notes_tmp, walloc_tmp = zip(*measure_alloc)
        notes_tmp = [l for v in notes_tmp for l in v]
        walloc_tmp = [l for v in walloc_tmp for l in v]
        num_space = count_comp(notes_tmp[-2:-5:-1]) # last 4 elements excluding the bar
        no_bar_notes, no_bar_walloc = notes_tmp[:-1], walloc_tmp[:-1]
        bar_notes, bar_walloc = notes_tmp[-1], walloc_tmp[-1]
        if num_space < 2:
            notes_tmp = no_bar_notes + ['space']*(2-num_space) + [bar_notes]
            walloc_tmp = no_bar_walloc + [15]*(2-num_space) + [bar_walloc]
        elif num_space > 2:
            notes_tmp = no_bar_notes[:(2-num_space)] + [bar_notes]
            walloc_tmp = no_bar_walloc[:(2-num_space)] + [bar_walloc]

        notes.append(['space'] * 2 + notes_tmp)
        walloc.append([15] * 2 + walloc_tmp)
    return notes, walloc