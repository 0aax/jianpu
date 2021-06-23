import ast
import re

def tokenize(txt):
    """
    Given text of notes and 'operators', returns a string that can be evaluated easily (e.g str([flat 1] 2 [trem 2]) --> '[["flat", 1], 2, ["trem", 4]]')
    """
    def clean(txt):
        """
        Makes text more uniform. Returns said text.
        """
        cleaned = txt.replace('[ ', '[').replace(' ]', ']')
        cleaned =  re.sub('[ ]+', ' ', cleaned)
        return cleaned
    
    def place_commas(txt):
        """
        Helper function to add commas in their proper places.
        """
        tmp = re.sub('\[([a-zA-Z]+)\s', r'[\1, ', txt)  # [op ... --> [op, ...
        tmp = re.sub('\]\s([0-9])', r'], \1', tmp)      # ] note --> ], note
        tmp = re.sub('([0-9])\s\[', r'\1, [', tmp)      # note [ --> note, [
        tmp = re.sub('\]\s\[', r'], [', tmp)            # ] [ --> ], [
        fin = re.sub('([0-9])\s', r'\1, ', tmp)         # char/note --> char/note
        return fin

    def fix_strings(txt):
        """
        Helper function to make sure that strings will be evaluated as strings.
        """
        tmp = re.sub('\[(\w+),', r'["\1",', txt)             # [op, ... --> ['op', ...
        tmp = re.sub(',\s([a-zA-Z ]+)\]', r', "\1"]', tmp)   # , text] ---> , 'text']
        fin = re.sub('\[([a-zA-Z]+)\]', r'["\1"]', tmp)      # [op] ---> ['op']

        return fin

    cleaned = clean(txt)
    tkns = '[' + fix_strings(place_commas(cleaned)) + ']'

    return tkns

def parse(file):
    """
    Parses all notes into elements of an array and returns parsed array.
    - Each entry has the form [foo(s), note], where foo represents some operator on the note.
    - Foo(s) can be a single-element array or have multiple elements (i.e. [[quaver, dot], 1]).
    - The only exception to this format are chords, in which the array will take the form: [[chord], [[foo1, ...], note1], [[foo2, ...], note2], ...]
    """

    no_param = {'\\bar', '\\lrepeat', '\\rrepeat'}
    single_param_notes = {'\\doubledot', '\\dot', '\\quaver', '\\semiquaver', '\\crochet', '\\minim', '\\semibreve', '\\sharp', '\\flat', '\\natural', '\\grace', '\\trem', '\\down', '\\up', '\\stie', '\\etie', '\\sslur', '\\eslur', '\\p', '\\mp', '\\f', '\\mf', '\\scresc', '\\ecresc', '\\sdim', '\\edim'}
    single_param_text = {'\\title', '\\composer', '\\instrument', '\\tempo'}
    double_param_notes = {'\\time', '\\key', '\\raiseoct', '\\loweroct', '\\finger'}
    n_param = {'\\chord'}
    
    fl = open(file)
    txt = fl.read().replace('\n', ' ')
    tkns = ast.literal_eval(tokenize(txt))
                
    return tkns

if __name__ == '__main__':
    print(parse('test_inputs/test_1.txt'))
