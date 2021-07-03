import src.config as cfg

def get_note(n):
    if isinstance(n, int): return n
    else: return get_note(n[1])

get_direction = (lambda n: [[n[0], get_note(n[1])]])
get_octave = (lambda n: [[n[0], get_note(n[1]), n[2]]])

match_direction = (lambda cd: cfg.sym[cd[0]])
match_octave = (lambda cd: cfg.oct_sym[cd[2]])