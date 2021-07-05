from PIL import Image, ImageDraw, ImageFont
import os

paper_sizes = {'a4': (2480, 3508),
               'letter': (2550, 3300)}    
paper_type = 'letter'

paper = Image.new('RGB', paper_sizes[paper_type], (255, 255, 255))
paper_editable = ImageDraw.Draw(paper)

NotoSerif_reg = ImageFont.truetype("assets/NotoSerifCJKsc-Regular.otf", 50)
NotoSerif_li = ImageFont.truetype("assets/NotoSerifCJKsc-Light.otf", 50)

notes = ImageFont.truetype("assets/jianpu.otf", 55)
notes_small = ImageFont.truetype("assets/jianpu_small.otf", 55)

time_up = ImageFont.truetype("assets/time_up.otf", 80)
time_low = ImageFont.truetype("assets/time_low.otf", 80)

x, y = 150, 150
paper_editable.text((x, y), '\\   /   \\  \\  /     \\    \\             \\ / \\ /   \\     \\  /   \\  \\  /     \\    \\             \\ / \\ /   \\', fill=(0, 0, 0), font=notes)
paper_editable.text((x, y), '\'                                            \' \' \' \'   \'', fill=(0, 0, 0), font=notes)
paper_editable.text((x, y), '2.  1   2  5  6  |  3    3  5  6  |  3 5 3 2   3  |  1. 1   2  5  6  |  3    3  5  6  |  3 5 3 2   3  |  3   3   3   3  |', fill=(0, 0, 0), font=notes)
paper_editable.text((x, y), '_____==   ____======           ____======     ===========          ____==   ____======           ____======     ===========          ', fill=(0, 0, 0), font=notes)

cwd = os.getcwd()
paper.save(os.path.join(cwd, 'tester_paper.png'), 'PNG')