def get_note(n):
    if isinstance(n, int): return n
    else: return get_note(n[1])

direction = (lambda n: [[n[0], get_note(n[1])]])
octave = (lambda n: [[n[0], get_note(n[1]), n[2]]])