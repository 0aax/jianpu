import ast
import re
# 1) Title, composer/instrument name, and other header stuff.
# 1.5) Note lengths and accidentals
# 2) Chords and fingering/bowing/strumming/etc. directions
# 2.5) Octaves and dynamics
# 3) Slurs and ties

def tokenize(txt):
    """
    Given text of notes and 'operators', returns a list of tokens (e.g str([flat 1] 2 [trem 2]) --> [[flat, 1], 2, [trem, 4]])
    """
    def clean(txt):
        """
        Makes text more uniform. Returns said text.
        """
        cleaned = txt.replace('[ ', '[').replace(' ]', ']')
        return cleaned
    
    def place_commas(txt):
        """
        Helper function to add commas in their proper places.
        """
        tmp = re.sub("(\w+)\s+(\d+)", r"\1, \2", txt)
        tmp = re.sub("(\d+)\s+(\d+)", r"\1, \2", tmp)
        tmp = re.sub("(\]+)\s+(\[+)", r"\1, \2", tmp)
        tmp = re.sub("(\]+)\s+(\d+)", r"\1, \2", tmp)
        fin = re.sub("(\d+)\s+(\[+)", r"\1, \2", tmp)

        return fin
    
    def fix_strings(txt):
        """
        Helper function to make sure that strings will be evaluated as strings.
        """

    cleaned = clean(txt)
    tkns_tmp = place_commas(cleaned)
    tkns = ast.literal_eval(tkns_tmp)
    # tkn_tmp = cleaned.split('\\')
    # tkn_tmp = ['\\' + t for t in tkn_tmp if t != '']
    # tkns = []
    # for t in tkn_tmp:
    #     tkns += further_tokenize(t)
    
    # i = 0
    # while i < len(tkns)-1:
    #     if tkns[i][:1] == '\\' and tkns[i+1] == '{': # apparently \\ is one element, so slice by [:1]
    #         tkns[i], tkns[i+1] = tkns[i+1], tkns[i]
    #         i += 2
    #     else: i += 1
        
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
    txt = fl.read().replace('\n', '')
    tkns = tokenize(txt)

    # def recur_parser(i):
        
    #     while i < len(tkns):
    #         if tkns[i].isnumeric(): return [['\\crochet', tkns[i]]] + recur_parser(i+1), i+1
    #         elif tkns[i] in no_param: return [[tkns[i]]] + recur_parser(i+1), i+1
    #         elif tkns[i] in single_param_text:
    #             tkn_tmp, i_tmp = tkns[i+2], i+2
    #             inner_txt = ''
    #             while tkn_tmp != '}':
    #                 inner_txt += tkn_tmp
    #                 tkn_tmp, i_tmp = tkns[i+1], i+1
    #             return [[tkns[i], inner_txt]] + recur_parser(i_tmp+1), i_tmp+1
    #         elif tkns[i] in single_param_notes:
    #             tkn_i = tkns[i]
    #             parsed = [tkn_i]
    #             while tkn_i != '}':
    #                 parsed_tmp, i_tmp = recur_parser(i+2)
    #                 parsed += parsed_tmp
    #                 tkn_i = tkns[i_tmp]
    #             return [parsed_tmp] + recur_parser(i_tmp+1), i_tmp+1
    #         elif tkns[i] in double_param_notes:
    #             tkn_i, i_tmp = tkn[i+2], i+2
    #             while tkn_i != '{':
    #                 parsed_tmp, i_tmp = recur_parser(i_tmp)
    #                 i_tmp += 1
                
    return tkns

if __name__ == '__main__':
    print(tokenize(parse('test_inputs/test_1.txt')))
