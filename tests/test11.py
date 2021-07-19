from src.composition import Composition
from src.parser import parse
from src.lines import get_primary, gen_primary_str, rearrange, get_dur_group, match_prim_dur, add_sym
import src.config as cfg
from src.utils import element_wise_sum, arr_from_string

from PIL import Image, ImageDraw, ImageFont
import os

file = 'test_inputs/test_6.txt'
out_file = 'tester_paper.png'
paper_type = 'letter'

parsed = parse(file)
comp = Composition(parsed, paper_type=paper_type)

measured_w_bar = comp.gen_measured_notes(comp.notes, with_bar=True)
measured_no_bar = comp.gen_measured_notes(comp.notes, with_bar=False)

pl = get_primary(measured_w_bar)
notes_str, walloc = gen_primary_str(pl)
print(notes_str)
rr = rearrange(measured_no_bar)
# print(rr)

notes_lst = arr_from_string(notes_str)
dg = get_dur_group(measured_no_bar)
pd = match_prim_dur(notes_lst, dg)

tmp = add_sym(notes_str, rr, helper=pd, return_as_str=False)
final = ''.join(element_wise_sum(tmp, pd))
# print(final)
paper = Image.new('RGB', cfg.paper_sizes[paper_type], (255, 255, 255))
paper_editable = ImageDraw.Draw(paper)

notes = ImageFont.truetype("assets/jianpu2.otf", 55)
notes_small = ImageFont.truetype("assets/jianpu2_small.otf", 55)

x, y = 70, 150
paper_editable.text((x, y), final, fill=(0, 0, 0), font=notes, features=['-kern'])

cwd = os.getcwd()
paper.save(os.path.join(cwd, out_file), 'PNG')