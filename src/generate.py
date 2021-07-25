from src.composition import Composition
from src.parser import parse
from src.lines import get_primary, gen_primary_str, rearrange, add_sym, get_dur_group, match_prim_dur, chords_arranged, add_sym_sub
from src.utils import element_wise_sum, arr_from_string

from PIL import Image, ImageDraw, ImageFont

import os
import src.config as cfg

def generate_str(file, paper_type='letter'):
    parsed = parse(file)
    comp = Composition(parsed, paper_type=paper_type)

    measured_w_bar = comp.gen_measured_notes(comp.notes, with_bar=True)
    measured_no_bar = comp.gen_measured_notes(comp.notes, with_bar=False)

    pl = get_primary(measured_w_bar)
    notes, bars, walloc, notes_orig = gen_primary_str(pl, measured_no_bar)

    final_prelim = []
    aln_heights = []
    bln_heights = []

    for i, mnb in enumerate(notes_orig):
        mnb = [mnb]
        rr = rearrange(mnb)

        notes_lst = arr_from_string(notes[i])
        dg = get_dur_group(mnb)
        pd = match_prim_dur(notes_lst, dg)

        tmp, aln_h, bln_h = add_sym(notes[i], rr, helper=pd, return_as_str=False)
        final = element_wise_sum(tmp, pd)
        final_prelim.append(final)
        aln_heights.append(aln_h)
        bln_heights.append(bln_h)
    
    all_final, mnb_lines, aln_heights, bln_heights = combine_measures(final_prelim, measured_no_bar, bars, aln_heights, bln_heights, walloc, paper_type=paper_type)

    all_sublns = []
    sub_aln = []
    sub_bln = []

    for i, mnb in enumerate(mnb_lines):
        ca = chords_arranged(mnb)
        len_ca = len(ca)
        sublns = []
        aln_tmp = []
        bln_tmp = []
        sb_prim = ca[0]
        for j in range(1, len_ca):
            sb_j = rearrange([ca[j]], ignore_time=True)
            is_ending = j == len_ca - 1
            sb, aln, bln = add_sym_sub(all_final[i], sb_prim, sb_j, return_as_str=False, ending_subln=is_ending)
            sublns.append(''.join(sb))
            aln_tmp.append(aln)
            bln_tmp.append(bln)
        all_sublns.append(sublns)
        sub_aln.append(aln_tmp)
        sub_bln.append(bln_tmp)

    all_final = [''.join(i) for i in all_final]

    return all_final, all_sublns, aln_heights, bln_heights, sub_aln, sub_bln

def combine_measures(primary, measures, bars, aln, bln, walloc, paper_type='letter', return_str=False):
    """
    Combines measures into lines of the target length.
    """

    def compress_spaces(msrs):
        """
        Compresses editable spaces into one element in the array.
        """
        comp = []
        for _, msr in enumerate(msrs):
            cp_tmp = []
            curr_comp, num_comp = '', 0
            for _, n in enumerate(msr):
                n_set = set(v for v in n)
                if n_set.issubset(cfg.editable_spaces): curr_comp += n; num_comp += 1
                elif curr_comp != '':
                    cp_tmp += [curr_comp, n]
                    curr_comp, num_comp = '', 0
                else:
                    cp_tmp.append(n)
            comp.append(cp_tmp)
        return comp

    def editable_spaces(cpmsrs):
        """
        Returns dictionary of editable spaces. Spaces are grouped in arrays depending on whether they are connected or not.
        """
        idx = {0: [], 1: [], 2: []}
        for i, msr in enumerate(cpmsrs):
            curr_group = ''
            group_spaces = []
            for j, n in enumerate(msr):
                n_set = set(v for v in n)
                n_set_nospace = set(v for v in n if v != ' ')
                if n_set.issubset(cfg.editable_spaces):
                    curr_space = list(n_set_nospace)[0] if len(n_set_nospace) != 0 else ' '
                    if curr_space == curr_group: group_spaces.append((i, j))
                    elif len(group_spaces) != 0:
                        idx[cfg.editable_sym[curr_group]].append((curr_group, group_spaces))
                        curr_group = curr_space
                        group_spaces = [(i, j)]
                    else:
                        curr_group = curr_space
                        group_spaces = [(i, j)]
                else: continue
            if len(group_spaces) != 0: idx[cfg.editable_sym[curr_group]].append((curr_group, group_spaces))
        return idx

    def edit_spacing(prim, edtb, to_edit):
        """
        Add spaces to reach target line length.
        """
        edit_op = (lambda orig, mod: orig + mod) if to_edit > 0 else (lambda orig, mod: orig.replace(mod, '', 1))
        num_spaces_to_edit = int(abs(to_edit) / cfg.space_base_width)
        
        useable = [j[1] for _, i in edtb.items() for j in i if len(i) != 0]
        useable_sym = [j[0] for _, i in edtb.items() for j in i if len(i) != 0]

        i_use, len_use = 0, len(useable)
        iter_over_lst = False

        while num_spaces_to_edit > 0:
            curr_spaces = useable[i_use]
            if num_spaces_to_edit >= len(curr_spaces):
                for i, j in curr_spaces:
                    sym_tmp = useable_sym[i_use] if useable_sym[i_use] != ' ' else ''
                    mod = ' ' + sym_tmp
                    prim[i][j] = edit_op(prim[i][j], mod) 
                    num_spaces_to_edit -= 1
            elif iter_over_lst: 
                sym_tmp = useable_sym[i_use] if useable_sym[i_use] != ' ' else ''
                mod = ' ' + sym_tmp
                prim[i][j] = edit_op(prim[i][j], mod) 
                num_spaces_to_edit -= 1
            if i_use < len_use - 1: i_use += 1
            else: i_use = 0; iter_over_lst = True

        return prim

    margin = cfg.side_margin[paper_type]
    target_width = cfg.paper_sizes[paper_type][0] - margin*2

    curr_line_width = 0

    plines = []
    measured_lns = []
    measured_aln = []
    measured_bln = []

    for i, p_ln in enumerate(primary):
        add_w = walloc[i] + cfg.space_base_width*6

        if curr_line_width == 0: opt = 0
        elif curr_line_width + add_w == target_width: opt = 1
        elif curr_line_width + add_w < target_width: opt = 2
        elif abs(curr_line_width + add_w - target_width) < abs(curr_line_width - target_width):
            opt = 3; to_expand = target_width - (curr_line_width + add_w)
        else:
            opt = 4; to_expand = target_width - curr_line_width

        if opt in {1, 2}:
            plines[-1] += [p_ln]
            measured_lns[-1] += [measures[i]]
            measured_aln[-1] = max(measured_aln[-1], aln[i])
            measured_bln[-1] = max(measured_bln[-1], bln[i])
            curr_line_width += add_w
        elif opt == 3:
            plines[-1] += [p_ln]
            measured_lns[-1] += [measures[i]]
            measured_aln[-1] = max(measured_aln[-1], aln[i])
            measured_bln[-1] = max(measured_bln[-1], bln[i])
            curr_line_width = 0
        else:
            plines.append([p_ln])
            measured_lns.append([measures[i]])
            measured_aln.append(aln[i])
            measured_bln.append(bln[i])
            curr_line_width = add_w - cfg.space_base_width*2

        if opt == 3:
            cp_plines = compress_spaces(plines[-1])
            ed_plines = editable_spaces(cp_plines)
            plines[-1] = edit_spacing(cp_plines, ed_plines, to_expand)
        if opt == 4:
            cp_plines = compress_spaces(plines[-2])
            ed_plines = editable_spaces(cp_plines)
            plines[-2] = edit_spacing(cp_plines, ed_plines, to_expand)
    
    if return_str:
        i_bar = 0
        lines_fin = []
        for line in plines:
            line_str = ''
            for j, measure in enumerate(line):
                if j == 0: line_str += ''.join(measure) + '  ' + bars[i_bar]
                else: line_str += '  ' + ''.join(measure) + '  ' + bars[i_bar]
                i_bar += 1
            lines_fin.append(line_str)
    else:
        i_bar = 0
        lines_fin = []
        for line in plines:
            line_str = []
            for j, measure in enumerate(line):
                if j == 0: line_str += measure + [' ', ' ', bars[i_bar]]
                else: line_str += [' ', ' '] + measure + [' ', ' ', bars[i_bar]]
                i_bar += 1
            lines_fin.append(line_str)

    return lines_fin, measured_lns, measured_aln, measured_bln

def write_to_paper(y, in_file, out_file, paper_type='letter', gen_txt_files=False):
    x = cfg.left_start[paper_type]
    paper = Image.new('RGB', cfg.paper_sizes[paper_type], (255, 255, 255))
    paper_editable = ImageDraw.Draw(paper)

    NotoSerif_reg = ImageFont.truetype('assets/NotoSerifCJKsc-Regular.otf', 50)
    NotoSerif_li = ImageFont.truetype('assets/NotoSerifCJKsc-Light.otf', 50)

    notes = ImageFont.truetype('assets/jianpu2.otf', 55)
    notes_small = ImageFont.truetype('assets/jianpu2_small.otf', 55)

    all_final, all_sublns, aln_heights, bln_heights, sub_aln, sub_bln = generate_str(in_file, paper_type=paper_type)

    start_y = y

    if gen_txt_files:
        f_lns = open('output/composition.txt', 'w', encoding='utf-8')

    for i, fln in enumerate(all_final):
        aln_h = aln_heights[i]*cfg.above_note_height
        print('aln', aln_h)
        start_y += aln_h

        paper_editable.text((x, start_y), fln, fill=(0, 0, 0), font=notes)

        if gen_txt_files:
            f_lns.write('## primary ({}, {})'.format(x, start_y) + '\n')
            f_lns.write(fln + '\n')

        sub_aln_tmp = sub_aln[i]
        sub_bln_tmp = sub_bln[i]

        if len(all_sublns[i]) == 0: start_y += cfg.note_base_height
        else: start_y += cfg.sub_spacer

        start_y += bln_heights[i]*cfg.below_note_height

        for j, sb in enumerate(all_sublns[i]):
            add_space = sub_aln_tmp[j]*cfg.sub_above_note_height
            start_y += add_space
            paper_editable.text((x, start_y), sb, fill=(0, 0, 0), font=notes_small)
            if gen_txt_files:
                f_lns.write('## sub ({}, {})'.format(x, start_y) + '\n')
                f_lns.write(sb + '\n')
            start_y += sub_bln_tmp[j]*cfg.sub_below_note_height + cfg.sub_note_base_height

        start_y += cfg.line_break
    
    if gen_txt_files: f_lns.close()

    cwd = os.getcwd()
    paper.save(os.path.join(cwd, out_file), 'PNG')