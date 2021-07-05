from src.composition import Composition
from src.parser import parse
from src.generate import get_target_group_line, get_primary_line, gen_primary_line_str, match_primary_target_group
from src.config import *
from src.target_funcs import get_direction, get_octave, match_direction, match_octave

from PIL import Image, ImageDraw, ImageFont
import os

paper_sizes = {'a4': (2480, 3508),
               'letter': (2550, 3300)}    
paper_type = 'letter'

parsed = parse('test_inputs/test_4.txt', is_lst=False)
comp = Composition(parsed=parsed)

measured_w_bar = comp.gen_measured_notes(comp.notes, with_bar=True)
measured_no_bar = comp.gen_measured_notes(comp.notes, with_bar=False)
# print(measured, '\n')
primary_line = get_primary_line(measured_w_bar)
# print(primary_line, '\n')
direction_line = get_target_group_line(measured_no_bar, target_group=directions, target_func=get_direction)
# print(direction_line, '\n')
octave_line = get_target_group_line(measured_no_bar, target_group=octaves, target_func=get_octave)
# print(octave_line, '\n')

notes_str, walloc = gen_primary_line_str(primary_line)
print(notes_str, '\n')
primary_direc = match_primary_target_group(notes_str, direction_line, target_sym=match_direction)
print(primary_direc, '\n')
primary_oct = match_primary_target_group(notes_str, octave_line, target_sym=match_octave)
print(primary_oct, '\n')

paper = Image.new('RGB', paper_sizes[paper_type], (255, 255, 255))
paper_editable = ImageDraw.Draw(paper)

NotoSerif_reg = ImageFont.truetype("assets/NotoSerifCJKsc-Regular.otf", 50)
NotoSerif_li = ImageFont.truetype("assets/NotoSerifCJKsc-Light.otf", 50)

notes = ImageFont.truetype("assets/jianpu.otf", 55)
notes_small = ImageFont.truetype("assets/jianpu_small.otf", 55)

time_up = ImageFont.truetype("assets/time_up.otf", 80)
time_low = ImageFont.truetype("assets/time_low.otf", 80)

x, y = 150, 150
paper_editable.text((x, y), primary_direc, fill=(0, 0, 0), font=notes)
paper_editable.text((x, y), primary_oct, fill=(0, 0, 0), font=notes)
paper_editable.text((x, y), notes_str, fill=(0, 0, 0), font=notes)
# paper_editable.text((x, y), '_____==   ____======           ____======     ===========          ____==   ____======           ____======     ===========          ', fill=(0, 0, 0), font=notes)

cwd = os.getcwd()
paper.save(os.path.join(cwd, 'tester_paper.png'), 'PNG')