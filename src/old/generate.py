from src.composition import Composition
from src.parser import parse
from src.lines import get_dur_group_line, get_target_group_line, get_primary_line, gen_primary_line_str, match_primary_duration, match_primary_target_group
from src.utils import element_wise_sum, arr_from_string
from src.misc_funcs import get_direction, get_octave, get_ts
from src.misc_funcs import match_direction, match_octave

from PIL import Image, ImageDraw, ImageFont

import os
import src.config as cfg

def generate_str(file, paper_type='letter'):
    parsed = parse(file)
    comp = Composition(parsed, paper_type=paper_type)

    measured_w_bar = comp.gen_measured_notes(comp.notes, with_bar=True)
    measured_no_bar = comp.gen_measured_notes(comp.notes, with_bar=False)

    primary_line = get_primary_line(measured_w_bar)
    direction_line = get_target_group_line(measured_no_bar, target_group=cfg.directions, target_func=get_direction)
    octave_line = get_target_group_line(measured_no_bar, target_group=cfg.octaves, target_func=get_octave)
    duration_line = get_dur_group_line(measured_no_bar)

    notes_str, walloc = gen_primary_line_str(primary_line)
    notes_lst = arr_from_string(notes_str)
    primary_direc = match_primary_target_group(notes_lst, direction_line, target_sym=match_direction)
    primary_dur = match_primary_duration(notes_lst, duration_line)
    primary_oct = match_primary_target_group(notes_lst, octave_line, helper=primary_dur, target_sym=match_octave)

    primary_final = ''.join(element_wise_sum(notes_lst, primary_oct, primary_direc, primary_dur))

    return primary_final

def write_to_paper(x, y, in_file, out_file, paper_type='letter'):
    paper = Image.new('RGB', cfg.paper_sizes[paper_type], (255, 255, 255))
    paper_editable = ImageDraw.Draw(paper)

    NotoSerif_reg = ImageFont.truetype("assets/NotoSerifCJKsc-Regular.otf", 50)
    NotoSerif_li = ImageFont.truetype("assets/NotoSerifCJKsc-Light.otf", 50)

    notes = ImageFont.truetype("assets/jianpu2.otf", 55)

    time_up = ImageFont.truetype("assets/time_up.otf", 80)
    time_low = ImageFont.truetype("assets/time_low.otf", 80)

    primary_final = generate_str(in_file, paper_type=paper_type)

    paper_editable.text((x, y), primary_final, fill=(0, 0, 0), font=notes, features=['-kern'])

    cwd = os.getcwd()
    paper.save(os.path.join(cwd, out_file), 'PNG')