import src.config as cfg

def get_note(n):
    if isinstance(n, int): return n
    else: return get_note(n[1])

get_direction = (lambda n: [[n[0], get_note(n[1])]])
get_octave = (lambda n: [[n[0], get_note(n[1]), n[2]]])
get_ts = (lambda n: [[n[0], get_note(n[1])]])

match_direction = (lambda cd, _: cfg.sym[cd[0]])
match_octave = (lambda cd, ch: cfg.oct_sym[cd[2]] if cd[2] > 0 else cfg.oct_sym[cd[2]][ch])