from src.parser import parse

types_bars = {'bar', 'lrep', 'rrep'}
no_add_alloc = {'roct', 'loct'} | types_bars
add_alloc_notes = {'fing', 'down', 'up', 'trem', 'grace'}
add_alloc_misc = {'scresc', 'ecresc', 'sdim', 'edim'}

n_no_add_alloc = {'qvr', 'sqvr', 'ccht', 'mm', 'sbrve'}
n_add_alloc_notes = {'chord'}

def gen_header_info(header_info):
    header = {}
    for n in header_info:
        header[n[0]] = n[-1]
    return header

def split_header_notes(uni_parsed):
    notes_tmp = []
    header = []
    for n in uni_parsed:
        if n[0] == 'header':
            header = gen_header_info(n[1:])
        else: notes_tmp.append(n)
    return header, notes_tmp

def gen_uniform_parse(parsed):
    parse_uni = []
    for n in parsed:
        if isinstance(n, int): parse_uni.append(['qtr', n])
        else: parse_uni.append(n)
    return parse_uni

def gen_barred_notes(notes):
    barred_notes = []
    curr_bar = []
    for n in notes:
        if n[0] in types_bars:
            barred_notes.append(curr_bar)
            curr_bar = []
        else: curr_bar.append(n)
    if len(curr_bar) != 0: barred_notes.append(curr_bar)
    return barred_notes

def gen_naive_notes_alloc(barred_notes):

    def get_alloc(n):
        if isinstance(n, int) or n[0] in no_add_alloc: return 1
        elif n[0] in n_add_alloc_notes:
            n_alloc = 0
            for e in n[1:]: n_alloc += get_alloc(e)
            return n_alloc
        elif n[0] in n_no_add_alloc:
            n_alloc = []
            for e in n[1:]: n_alloc += [get_alloc(e)]
            return n_alloc
        else:
            alloc_tmp = 1 if n[0] in add_alloc_notes else 0
            return get_alloc(n[-1]) + alloc_tmp
    
    alloc = []
    for measure in barred_notes:
        measure_alloc = []
        for n in measure:
            alloc_tmp = get_alloc(n)
            if isinstance(alloc_tmp, int): measure_alloc.append(alloc_tmp)
            else: measure_alloc += alloc_tmp
        alloc.append(measure_alloc)
    return alloc

parsed = parse('test_inputs/test_1.txt', is_lst=True)
uni_parsed = gen_uniform_parse(parsed)
header, notes = split_header_notes(uni_parsed)
barred = gen_barred_notes(notes)
print(barred)
alloc = gen_naive_notes_alloc(barred)
print(alloc)