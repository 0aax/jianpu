from src.composition import Composition
from src.parser import parse
from src.generate import get_dur_group_line, get_target_group_line, get_primary_line, gen_primary_line_str, match_primary_duration, match_primary_target_group
from src.config import *
from src.utils import element_wise_sum, arr_from_string
from src.misc_funcs import get_direction, get_octave, match_direction, match_octave

from PIL import Image, ImageDraw, ImageFont
import os

paper_sizes = {'a4': (2480, 3508),
               'letter': (2550, 3300)}    
paper_type = 'letter'

parsed = parse('test_inputs/test_5.txt', is_lst=False)
comp = Composition(parsed=parsed)

measured_w_bar = comp.gen_measured_notes(comp.notes, with_bar=True)
measured_no_bar = comp.gen_measured_notes(comp.notes, with_bar=False)

primary_line = get_primary_line(measured_w_bar)
direction_line = get_target_group_line(measured_no_bar, target_group=directions, target_func=get_direction)
octave_line = get_target_group_line(measured_no_bar, target_group=octaves, target_func=get_octave)
duration_line = get_dur_group_line(measured_no_bar)

# print(duration_line)

notes_str, walloc = gen_primary_line_str(primary_line)
notes_lst = arr_from_string(notes_str)
primary_direc = match_primary_target_group(notes_lst, direction_line, target_sym=match_direction)
primary_oct = match_primary_target_group(notes_lst, octave_line, target_sym=match_octave)
primary_dur = match_primary_duration(notes_lst, duration_line)
print(primary_dur)

primary_final = ''.join(element_wise_sum(notes_lst, primary_oct, primary_direc, primary_dur))
print(primary_final)

paper = Image.new('RGB', paper_sizes[paper_type], (255, 255, 255))
paper_editable = ImageDraw.Draw(paper)

NotoSerif_reg = ImageFont.truetype("assets/NotoSerifCJKsc-Regular.otf", 50)
NotoSerif_li = ImageFont.truetype("assets/NotoSerifCJKsc-Light.otf", 50)

notes = ImageFont.truetype("assets/jianpu.otf", 55)
notes_small = ImageFont.truetype("assets/jianpu_small.otf", 55)

notes2 = ImageFont.truetype("assets/jianpu2.otf", 55)

time_up = ImageFont.truetype("assets/time_up.otf", 80)
time_low = ImageFont.truetype("assets/time_low.otf", 80)

# print(primary_direc, 'end')
# print(primary_oct, 'end')
# print(notes_str, 'end')

txt = '3' + u'\u0300' + u'\u0302' + u'\u0304'
txt = '3 ' + u'\u0306' + ' ' + u'\u0306' + '3' + u'\u0304'

# primary_direc = '   \\                                         \\ / \\ /   \\     \\   /   \\  \\ /     \\   \\            \\ / \\ /   \\'
# primary_oct  = '   \'   1   2  5 6     3   3  5 6     \' \' \' \'   \'     1   1   2  5 6     3   3  5 6     3 5 3 2   3     3   3   3   3'
# primary_line = '    2.  1   2  5 6  |  3   3  5 6  |  3 5 3 2   3  |  1.  1   2  5 6  |  3   3  5 6  |  3 5 3 2   3  |  3   3   3   3  |'

x, y = 70, 150
# paper_editable.text((x, y), txt, fill=(0, 0, 0), font=notes2)
paper_editable.text((x, y), primary_final, fill=(0, 0, 0), font=notes2)
# paper_editable.text((x, y), primary_direc, fill=(0, 0, 0), font=notes2)
# paper_editable.text((x, y), primary_oct, fill=(0, 0, 0), font=notes2)
# paper_editable.text((x, y), notes_str, fill=(0, 0, 0), font=notes)
# paper_editable.text((x, y), '   _____==   ____======          ____======      ===========          ____==   ____======           ____======     ===========          ', fill=(0, 0, 0), font=notes2)

cwd = os.getcwd()
paper.save(os.path.join(cwd, 'tester_paper.png'), 'PNG')