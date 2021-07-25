from PIL import Image, ImageDraw, ImageFont
import os

paper_sizes = {'a4': (2480, 3508),
               'letter': (2550, 3300)}    
paper_type = 'letter'

paper = Image.new('RGB', paper_sizes[paper_type], (255, 255, 255))
paper_editable = ImageDraw.Draw(paper)

NotoSerif_reg = ImageFont.truetype("assets/NotoSansCJKsc-Bold.otf", 50)

# notes = ImageFont.truetype("assets/jianpu.otf", 55)
# notes_small = ImageFont.truetype("assets/jianpu_small.otf", 55)
txt = '一二三四'
print(txt.encode('raw_unicode_escape'))
paper_editable.text((70, 100), txt, fill=(0, 0, 0), font=NotoSerif_reg)
# x, y = 150, 150
# paper_editable.text((x, y), '\\   /   \\  \\  /     \\    \\             \\ / \\ /   \\     \\  /   \\  \\  /     \\    \\             \\ / \\ /   \\', fill=(0, 0, 0), font=notes)
# paper_editable.text((x, y), '\'                                            \' \' \' \'   \'', fill=(0, 0, 0), font=notes)
# paper_editable.text((x, y), '2.  1   2  5  6  |  3    3  5  6  |  3 5 3 2   3  |  1. 1   2  5  6  |  3    3  5  6  |  3 5 3 2   3  |  3   3   3   3  |', fill=(0, 0, 0), font=notes)
# paper_editable.text((x, y), '_____==   ____======           ____======     ===========          ____==   ____======           ____======     ===========          ', fill=(0, 0, 0), font=notes)
# paper_editable.text((x-45, y), '2', fill=(0, 0, 0), font=time_up)
# paper_editable.text((x-45, y), '4', fill=(0, 0, 0), font=time_low)

# paper_editable.text((x, y+80), '\'', fill=(0, 0, 0), font=notes_small)
# paper_editable.text((x, y+80), '1', fill=(0, 0, 0), font=notes_small)
# paper_editable.text((x, y+80+50), '1', fill=(0, 0, 0), font=notes_small)
# paper_editable.text((x, y+80+50), '__', fill=(0, 0, 0), font=notes_small)

# paper_editable.text((x, y+80+50+80), '2.  1   2  5 6  |  3   3  5 6  |  3 5 3 2   3  |  1.  1   2  5 6  |  3   3  5 6  |  3 5 3 2   3  |  3   3   3   3  |', fill=(0, 0, 0), font=notes)
# 21, 20, 19

# paper_editable.text((x, y+100), '3 3   3   3  |', fill=(0, 0, 0), font=notes)
# paper_editable.text((x, y+200), '3', fill=(0, 0, 0), font=notes)
# paper_editable.text((x+45, y+200), '3', fill=(0, 0, 0), font=notes)
# paper_editable.text((x-45, y+80+50+80), '|                                                                                                                                                         |', fill=(0, 0, 0), font=notes)
# print(len('|                                                                                                                                                        |'))
cwd = os.getcwd()
paper.save(os.path.join(cwd, 'tester_paper.png'), 'PNG')