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
    notes_str, walloc = gen_primary_str(pl)
    rr = rearrange(measured_no_bar)

    notes_lst = arr_from_string(notes_str)
    dg = get_dur_group(measured_no_bar)
    pd = match_prim_dur(notes_lst, dg)

    tmp = add_sym(notes_str, rr, helper=pd, return_as_str=False)
    final = ''.join(element_wise_sum(tmp, pd))

    ca = chords_arranged(measured_no_bar)
    len_ca = len(ca)
    sublns = []
    sb_prim = ca[0]
    for i in range(1, len_ca):
        sb_i = rearrange([ca[i]], ignore_time=True)
        is_ending = i == len_ca - 1
        sublns.append(''.join(add_sym_sub(notes_str, sb_prim, sb_i, helper=pd, return_as_str=False, ending_subln=is_ending)))

    return final, sublns

def write_to_paper(x, y, in_file, out_file, paper_type='letter'):
    paper = Image.new('RGB', cfg.paper_sizes[paper_type], (255, 255, 255))
    paper_editable = ImageDraw.Draw(paper)

    NotoSerif_reg = ImageFont.truetype("assets/NotoSerifCJKsc-Regular.otf", 50)
    NotoSerif_li = ImageFont.truetype("assets/NotoSerifCJKsc-Light.otf", 50)

    notes = ImageFont.truetype("assets/jianpu2.otf", 55)
    notes_small = ImageFont.truetype("assets/jianpu2_small.otf", 55)

    final, sublns = generate_str(in_file, paper_type=paper_type)

    paper_editable.text((x, y), final, fill=(0, 0, 0), font=notes, features=['-kern'])

    for i, sb in enumerate(sublns):
        if i == 0: space = 70
        else: space = 60*(i+1)
        paper_editable.text((x, y+space), sb, fill=(0, 0, 0), font=notes_small, features=['-kern'])

    cwd = os.getcwd()
    paper.save(os.path.join(cwd, out_file), 'PNG')