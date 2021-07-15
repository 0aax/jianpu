from src.composition import Composition
from src.parser import parse
from src.lines import add_sym_sub, get_primary, gen_primary_str, rearrange, add_sym, get_dg, match_pd, chords_arranged
from src.utils import element_wise_sum, arr_from_string
import src.config as cfg

from PIL import Image, ImageDraw, ImageFont
import os

paper_type = 'letter'
in_file, out_file = 'test_inputs/test_6.txt', 'tester_paper.png'
x, y = 70, 150

parsed = parse(in_file)
comp = Composition(parsed, paper_type=paper_type)

measured_w_bar = comp.gen_measured_notes(comp.notes, with_bar=True)
measured_no_bar = comp.gen_measured_notes(comp.notes, with_bar=False)

pl = get_primary(measured_w_bar)
notes_str, walloc = gen_primary_str(pl)
rr = rearrange(measured_no_bar)

notes_lst = arr_from_string(notes_str)
dg = get_dg(measured_no_bar)
pd = match_pd(notes_lst, dg)

tmp = add_sym(notes_str, rr, helper=pd, return_as_str=False)
final = ''.join(element_wise_sum(tmp, pd))

ca = chords_arranged(measured_no_bar)
sublns = []
sb_prim = ca[0]
for i in range(1, len(ca)):
    sb_i = rearrange([ca[i]])
    sublns.append(''.join(add_sym_sub(notes_str, sb_prim, sb_i, return_as_str=False)))

print(sublns)

paper = Image.new('RGB', cfg.paper_sizes[paper_type], (255, 255, 255))
paper_editable = ImageDraw.Draw(paper)

NotoSerif_reg = ImageFont.truetype("assets/NotoSerifCJKsc-Regular.otf", 50)
NotoSerif_li = ImageFont.truetype("assets/NotoSerifCJKsc-Light.otf", 50)

notes = ImageFont.truetype("assets/jianpu2.otf", 55)
notes_small = ImageFont.truetype("assets/jianpu2_small.otf", 55)

time_up = ImageFont.truetype("assets/time_up.otf", 80)
time_low = ImageFont.truetype("assets/time_low.otf", 80)

paper_editable.text((x, y), final, fill=(0, 0, 0), font=notes, features=['-kern'])

for i, sb in enumerate(sublns):
    if i == 0: space = 80
    else: space = 65*(i+1)
    paper_editable.text((x, y+space), sb, fill=(0, 0, 0), font=notes_small, features=['-kern'])

cwd = os.getcwd()
paper.save(os.path.join(cwd, out_file), 'PNG')