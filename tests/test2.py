from re import X
from src.composition import Composition
from src.parser import parse
from src.generate import arrange_lines

# parsed = parse('test_inputs/test_2.txt', is_lst=True)
# comp = Composition(parsed=parsed)

parsed = parse('test_inputs/test_3.txt', is_lst=False)
comp = Composition(parsed=parsed)

# print(comp.header, '\n')

# print(comp.measured_notes, '\n')
# print(comp.only_notes, '\n')
# print(comp.only_dur_group, '\n')
# print(comp.notes_height_alloc, '\n')
# print(comp.notes_width_alloc, '\n')

# print(comp.measure_heights, '\n')
print(comp.approx_measure_widths, '\n')

approx_widths = comp.approx_measure_widths
only_notes = comp.only_notes

arranged = arrange_lines(approx_widths, only_notes)
for l in arranged:
    print(l)