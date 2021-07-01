from src.composition import Composition
from src.parser import parse
from src.generate import get_direction_line, get_primary_line, gen_primary_line_str

parsed = parse('test_inputs/test_4.txt', is_lst=False)
comp = Composition(parsed=parsed)

# print(comp.header, '\n')

# print(comp.measured_notes, '\n')
# print(comp.only_notes, '\n')
# print(comp.only_dur_group, '\n')
# print(comp.notes_height_alloc, '\n')
# print(comp.approx_notes_width_alloc, '\n')

# print(comp.measure_heights, '\n')
# print(comp.approx_measure_widths, '\n')

# dur_group = comp.only_dur_group

# approx_widths = comp.approx_measure_widths
# only_notes = comp.only_notes

# arranged = arrange_lines(approx_widths, only_notes)
# for l in arranged:
#     print(l)

measured = comp.gen_measured_notes(comp.notes, with_bar=True)
print(measured, '\n')
primary_line = get_primary_line(measured)
print(primary_line, '\n')
direction_line = get_direction_line(measured)
print(direction_line, '\n')

notes, walloc = gen_primary_line_str(primary_line)
print(notes, '\n')
print(walloc, '\n')