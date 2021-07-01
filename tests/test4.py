from PIL import Image, ImageDraw, ImageFont
import os

paper_sizes = {'a4': (2480, 3508),
               'letter': (2550, 3300),
               'tester': (500, 100)}
paper_type = 'letter'

paper = Image.new('RGB', paper_sizes[paper_type], (255, 255, 255))
paper_editable = ImageDraw.Draw(paper)

notes = ImageFont.truetype("assets/FreeSansBold.ttf", 50)
notes_1roct = ImageFont.truetype("assets/FreeSansBold_1roct.ttf", 50)
notes_2roct = ImageFont.truetype("assets/FreeSansBold_2roct.ttf", 50)
notes_1loct = ImageFont.truetype("assets/FreeSansBold_1loct.ttf", 50)
notes_2loct = ImageFont.truetype("assets/FreeSansBold_2loct.ttf", 50)

notes_down = ImageFont.truetype("assets/FreeSansBold_down.ttf", 50)
notes_1roct_down = ImageFont.truetype("assets/FreeSansBold_1roct_down.ttf", 50)
notes_2roct_down = ImageFont.truetype("assets/FreeSansBold_2roct_down.ttf", 50)
notes_1loct_down = ImageFont.truetype("assets/FreeSansBold_1loct_down.ttf", 50)
notes_2loct_down = ImageFont.truetype("assets/FreeSansBold_2loct_down.ttf", 50)

notes_up = ImageFont.truetype("assets/FreeSansBold_up.ttf", 50)
notes_1roct_up = ImageFont.truetype("assets/FreeSansBold_1roct_up.ttf", 50)
notes_2roct_up = ImageFont.truetype("assets/FreeSansBold_2roct_up.ttf", 50)
notes_1loct_up = ImageFont.truetype("assets/FreeSansBold_1loct_up.ttf", 50)
notes_2loct_up = ImageFont.truetype("assets/FreeSansBold_2loct_up.ttf", 50)

ys = 120
paper_editable.text((50, ys), '1   2   3   4   5   6   7', fill=(0, 0, 0), font=notes_2roct)
paper_editable.text((550, ys), '1   2   3   4   5   6   7', fill=(0, 0, 0), font=notes_1roct)
paper_editable.text((1050, ys), '1   2   3   4   5   6   7', fill=(0, 0, 0), font=notes)
paper_editable.text((1550, ys), '1   2   3   4   5   6   7', fill=(0, 0, 0), font=notes_1loct)
paper_editable.text((2050, ys), '1   2   3   4   5   6   7', fill=(0, 0, 0), font=notes_2loct)

yds = ys + 200
paper_editable.text((50, yds), '1   2   3   4   5   6   7', fill=(0, 0, 0), font=notes_2roct_down)
paper_editable.text((550, yds), '1   2   3   4   5   6   7', fill=(0, 0, 0), font=notes_1roct_down)
paper_editable.text((1050, yds), '1   2   3   4   5   6   7', fill=(0, 0, 0), font=notes_down)
paper_editable.text((1550, yds), '1   2   3   4   5   6   7', fill=(0, 0, 0), font=notes_1loct_down)
paper_editable.text((2050, yds), '1   2   3   4   5   6   7', fill=(0, 0, 0), font=notes_2loct_down)

yus = yds + 200
paper_editable.text((50, yus), '1   2   3   4   5   6   7', fill=(0, 0, 0), font=notes_2roct_up)
paper_editable.text((550, yus), '1   2   3   4   5   6   7', fill=(0, 0, 0), font=notes_1roct_up)
paper_editable.text((1050, yus), '1   2   3   4   5   6   7', fill=(0, 0, 0), font=notes_up)
paper_editable.text((1550, yus), '1   2   3   4   5   6   7', fill=(0, 0, 0), font=notes_1loct_up)
paper_editable.text((2050, yus), '1   2   3   4   5   6   7', fill=(0, 0, 0), font=notes_2loct_up)

# paper.show()
cwd = os.getcwd()
paper.save(os.path.join(cwd, 'tester_paper.png'), 'PNG')