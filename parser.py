# 1) Title, composer/instrument name, and other header stuff.
# 1.5) Note lengths and accidentals
# 2) Chords and fingering/bowing/strumming/etc. directions
# 2.5) Octaves and dynamics
# 3) Slurs and ties

def tokenize(txt):
    """
    Given text of notes and 'operators', returns a list of tokens (e.g '\\flat{1} 2 \\trem{4} --> ['\\flat{1}', '2', '\\trem{4}'])
    """
    def clean(txt):
        """
        Makes text more uniform. Returns said text.
        """
        tmp = txt.replace(' \\', '\\')
        tmp = tmp.replace('{ ', '{')
        cleaned = tmp.replace(' }', '}')
        return cleaned
    
    def prep_tkn(tkn):
        """
        Removes the spaces and commas in a token.
        """
        t_tmp = tkn.replace(' ', '')
        t_tmp = t_tmp.replace(',', '')
        return set(t_tmp)
    
    def further_tokenize(tkn):
        """
        Helper function to fully tokenize a string.
        """
        brkts = {'{', '}'}

        tkn = tkn.strip()
        t_tmp = prep_tkn(tkn)
        if len(tkn) == 0: return []
        elif tkn.isnumeric(): return [t for t in tkn]
        elif tkn[0].isnumeric() or tkn[0] in brkts: return [tkn[0]] + further_tokenize(tkn[1:])
        elif tkn[-1].isnumeric() or tkn[-1] in brkts: return further_tokenize(tkn[:-1]) + [tkn[-1]]
        elif t_tmp.isdisjoint(brkts): return [tkn]
        elif tkn[0] == '\\':
            fst_brkt = tkn.index('{')
            return [tkn[:fst_brkt]] + further_tokenize(tkn[fst_brkt:])

    cleaned = clean(txt)
    tkn_tmp = cleaned.split('\\')
    tkn_tmp = ['\\' + t for t in tkn_tmp if t != '']
    tkns = []
    for t in tkn_tmp:
        tkns += further_tokenize(t)
    return tkns

def parse(file):
    """
    Parses all notes into elements of an array and returns parsed array.
    - Each entry has the form [foo(s), note], where foo represents some operator on the note.
    - Foo(s) can be a single-element array or have multiple elements (i.e. [[quaver, dot], 1]).
    - The only exception to this format are chords, in which the array will take the form: [[chord], [[foo1, ...], note1], [[foo2, ...], note2], ...]
    """

    single = {'\\title', '\\composer', '\\instrument', '\\tempo', '\\doubledot', '\\dot', '\\quaver', '\\semiquaver', '\\crochet', '\\minim', '\\semibreve', '\\sharp', '\\flat', '\\natural', '\\grace', '\\trem', '\\down', '\\up', '\\stie', '\\etie', '\\sslur', '\\eslur', '\\p', '\\mp', '\\f', '\\mf', '\\scresc', '\\ecresc', '\\sdim', '\\edim'}

    double = {'\\time', '\\key', '\\raiseoct', '\\loweroct', '\\finger'}

    n_num = {'\\chord'}
    
    fl = open(file)
    txt = fl.read().replace('\n', '')

    return txt

if __name__ == '__main__':
    print(tokenize(parse('test_inputs/test_1.txt')))
