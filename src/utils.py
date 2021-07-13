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
