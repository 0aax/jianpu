import src.config as cfg

def deep_sum(n):
    """
    Returns the sum of an array that may have nested arrays.
    """
    if isinstance(n, int): return n
    else: return sum([deep_sum(e) for e in n])

def arr_from_string(string):
    """
    Returns an array from a string.
    """
    return [e for e in string]

def element_wise_sum(*args):
    """
    Given any number of arrays with only strings as elements, returns the element-wise sum of the strings.
    """
    return list(map(''.join, zip(*args)))

def combine_arrays(arr):
    """
    Given an array of arrays, returns a single array that contains all elements.
    """
    returns = []
    for e in arr:
        if isinstance(e, list): returns += e
        else: returns.append(e)
    return returns

def sym_to_add(h, sym):
    if isinstance(sym, int): return str(sym)
    
    to_add = str(sym[1])
    for s in sym[0]:
        if s in cfg.ignore_syms: tmp = ''
        elif isinstance(s, str): tmp = cfg.sym[s]
        elif s[0] == 'oct': tmp = cfg.oct_sym[s[1]][h]
        else: raise NotImplementedError("The symbol {} is not supported".format(s))
        to_add += tmp
    return to_add
