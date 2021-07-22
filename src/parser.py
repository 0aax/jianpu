import ast
import re

def tokenize(txt, is_lst=False):
    """
    Given text of notes and 'operators', returns a string that can be evaluated easily.
    - is_lst=True, (e.g str([flat 1] 2 [trem 2]) --> '[["flat", 1], 2, ["trem", 4]]')
    - is_lst=False, (e.g str(\\flat{1} 2 \\trem{2}) --> '[["flat", 1], 2, ["trem", 4]]')
    """
    bars = {'bar', 'dbar', 'ebar', 'lrep', 'rrep'}
    always_str = {'title', 'instrument', 'composer', 'affiliation', 'key'}

    def to_lst(txt):
        """
        Change txt from command format to list format.
        """
        lst = re.sub('\\\\([a-zA-Z]+){', r'[\1 ', txt)
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
    
    def place_commas(txt):
        """
        Helper function to add commas in their proper places.
        """
        tmp = re.sub('\[([a-zA-Z]+)\s', r'[\1, ', txt)  # [op ... --> [op, ...
        tmp = re.sub('\]\s([0-9])', r'], \1', tmp)      # ] note --> ], note
        tmp = re.sub('([0-9])\s\[', r'\1, [', tmp)      # note [ --> note, [
        tmp = re.sub('\]\s\[', r'], [', tmp)            # ] [ --> ], [
        fin = re.sub('([0-9])\s', r'\1, ', tmp)         # note --> note,
        return fin

    def fix_strings(txt):
        """
        Helper function to make sure that strings will be evaluated as strings.
        """
        tmp = re.sub('\[([a-zA-Z]+),', r'["\1",', txt)   # [op, --> ['op',
        for s in always_str:
            tmp = re.sub('\["{}", (.*?)\]'.format(s), r'["{}", "\1"]'.format(s), tmp)
        fin = re.sub('\[([a-zA-Z]+)\]', r'["\1"]', tmp)  # [op] --> ['op']
        return fin

    lst = to_lst(txt) if not is_lst else txt
    cleaned = clean(lst)
    tkns = '[' + fix_strings(place_commas(cleaned)).strip() + ']'

    return tkns

def parse(file, is_lst=False):
    """
    Parses all notes into elements of an array and returns parsed array.
    - Each entry has the form [foo(s), note], where foo represents some operator on the note.
    - Foo(s) can be a single-element array or have multiple elements (i.e. [quaver, [dot, 1]]).
    """
    fl = open(file)
    txt = fl.read().replace('\n', ' ')
    tkns = ast.literal_eval(tokenize(txt, is_lst=is_lst))
                
    return tkns