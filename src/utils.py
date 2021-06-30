def deep_sum(n):
    """
    Returns the sum of an array that may have nested arrays.
    """
    if isinstance(n, int): return n
    else: return sum([deep_sum(e) for e in n])