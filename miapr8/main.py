import PySimpleGUI as sg
from layout import layout
from functions import generate_word_set, get_cool_grammar, \
    words_to_string, grammar_to_string, strings_list

window = sg.Window(title='MiAPR8', layout=layout, finalize=True, element_justification='center')

word_set, added_set = generate_word_set(7, 5)
if len(added_set) != 0:
    window["-T-"].update(words_to_string(word_set) + "\n ДОПОЛНИТЕЛЬНЫЕ СЛОВА \n" + words_to_string(added_set))
else:
    window["-T-"].update(words_to_string(word_set))
word_set.extend(added_set)
grammar = get_cool_grammar(word_set)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event in ("-TERMINAL-", "-LEN-"):
        word_set, added_set = generate_word_set(int(values['-TERMINAL-']), int(values['-LEN-']))
        if len(added_set) != 0:
            window["-T-"].update(words_to_string(word_set) + "\n ДОПОЛНИТЕЛЬНЫЕ СЛОВА \n" + words_to_string(added_set))
        else:
            window["-T-"].update(words_to_string(word_set))
        word_set.extend(added_set)
        grammar = get_cool_grammar(word_set)
        window["-G-"].update("")
        window["-W-"].update("")
    if event == "-GRAMMAR-":
        window["-G-"].update(grammar_to_string(grammar))
        window["-W-"].update("")
    if event == "-WORDS-":
        window["-W-"].update(strings_list(grammar, 10))
