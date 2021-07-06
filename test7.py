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

parsed = parse('test_inputs/test_5.txt', is_lst=False)
comp = Composition(parsed=parsed)

measured_w_bar = comp.gen_measured_notes(comp.notes, with_bar=True)
measured_no_bar = comp.gen_measured_notes(comp.notes, with_bar=False)

primary_line = get_primary_line(measured_w_bar)
direction_line = get_target_group_line(measured_no_bar, target_group=directions, target_func=get_direction)
octave_line = get_target_group_line(measured_no_bar, target_group=octaves, target_func=get_octave)

notes_str, walloc = gen_primary_line_str(primary_line)
primary_direc = match_primary_target_group(notes_str, direction_line, target_sym=match_direction)
primary_oct = match_primary_target_group(notes_str, octave_line, target_sym=match_octave)

paper = Image.new('RGB', paper_sizes[paper_type], (255, 255, 255))
paper_editable = ImageDraw.Draw(paper)

NotoSerif_reg = ImageFont.truetype("assets/NotoSerifCJKsc-Regular.otf", 50)
NotoSerif_li = ImageFont.truetype("assets/NotoSerifCJKsc-Light.otf", 50)

notes = ImageFont.truetype("assets/jianpu.otf", 55)
notes_small = ImageFont.truetype("assets/jianpu_small.otf", 55)

time_up = ImageFont.truetype("assets/time_up.otf", 80)
time_low = ImageFont.truetype("assets/time_low.otf", 80)

print(primary_direc, 'end')
print(primary_oct, 'end')
print(notes_str, 'end')

txt = ''

# primary_direc = '   \\                                         \\ / \\ /   \\     \\   /   \\  \\ /     \\   \\            \\ / \\ /   \\'
# primary_oct  = '   \'   1   2  5 6     3   3  5 6     \' \' \' \'   \'     1   1   2  5 6     3   3  5 6     3 5 3 2   3     3   3   3   3'
# primary_line = '    2.  1   2  5 6  |  3   3  5 6  |  3 5 3 2   3  |  1.  1   2  5 6  |  3   3  5 6  |  3 5 3 2   3  |  3   3   3   3  |'

x, y = 150, 150
paper_editable.text((x, y), primary_direc, fill=(0, 0, 0), font=notes)
paper_editable.text((x, y), primary_oct, fill=(0, 0, 0), font=notes)
paper_editable.text((x, y), notes_str, fill=(0, 0, 0), font=notes)
# paper_editable.text((x, y), '_____==   ____======           ____======     ===========          ____==   ____======           ____======     ===========          ', fill=(0, 0, 0), font=notes)

cwd = os.getcwd()
paper.save(os.path.join(cwd, 'tester_paper.png'), 'PNG')