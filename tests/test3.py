import re

def to_lst(txt):
    """
    Change txt from command format to list format.
    """
    bars = {'bar', 'lrep', 'rrep'}

    lst = re.sub('\\\\([a-zA-Z]+){', r'[\1', txt)
    lst = lst.replace('}', ']')
    for b in bars: lst = lst.replace('\\{}'.format(b), '[{}]'.format(b))

    return lst

def clean(txt):
    """
    Makes text more uniform. Returns said text.
    """
    cleaned = txt.replace('[ ', '[').replace(' ]', ']').replace('][', '] [')
    cleaned =  re.sub('[ ]+', ' ', cleaned)
    cleaned = re.sub('([0-9])\[', r'\1 [', cleaned)
    cleaned = re.sub('\]([0-9])', r'] \1', cleaned)
    return cleaned

fl = open('test_inputs/test_3.txt')
txt = fl.read().replace('\n', ' ')
print(to_lst(txt))