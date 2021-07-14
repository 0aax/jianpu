from src.composition import Composition
from src.parser import parse
from src.lines import rearrange

from PIL import Image, ImageDraw, ImageFont
import os

paper_sizes = {'a4': (2480, 3508),
               'letter': (2550, 3300)}    
paper_type = 'letter'

parsed = parse('test_inputs/test_5.txt', is_lst=False)
comp = Composition(parsed=parsed)

measured_no_bar = comp.gen_measured_notes(comp.notes, with_bar=False)

print(rearrange(measured_no_bar))