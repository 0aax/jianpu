from PIL import Image, ImageDraw

def arrange_notes(approx_widths, only_notes, available_horiz_space=2550):
    lines_prelim = {}
    curr_line_num = 0
    curr_avail_space = available_horiz_space

    for i, measure_width in enumerate(approx_widths):
        if measure_width > curr_avail_space:
            curr_avail_space = available_horiz_space
            curr_line_num += 1

        if curr_line_num in lines_prelim:
            lines_prelim[curr_line_num]['measures'].append(i)
        else:
            lines_prelim[curr_line_num] = {}
            lines_prelim[curr_line_num]['measures'] = [i]
        
        curr_avail_space -= measure_width
        lines_prelim[curr_line_num]['avail_space'] = curr_avail_space
    
    lines = []
    for l, v in lines_prelim.items():
        curr_line = v['measures']
        expanded_line = [only_notes[i] for i in curr_line]
        lines.append(expanded_line)

    return lines

