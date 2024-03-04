import PySimpleGUI as sg
import numpy as np
from layout import layout
from functions import generate_training_set, training_set_to_string, \
    get_decision_functions, decision_functions_to_string, classify


window = sg.Window(title='MiAPR4', layout=layout, finalize=True, element_justification='center')

training_set = generate_training_set(2, 1, 1)
decision_functions = None
window['-TS-'].update(training_set_to_string(training_set))
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event in ('-C-', '-V-', '-A-'):
        training_set = generate_training_set(int(values['-C-']), int(values['-V-']), int(values['-A-']))
        decision_functions = None
        window['-TS-'].update(training_set_to_string(training_set))
    if event == '-TR-':
        ok, decision_functions = get_decision_functions(training_set)
        window['-F-'].update(decision_functions_to_string(decision_functions, ok))
    if event == '-CL-':
        try:
            vector = np.array(list(map(int, values['-I-'].split())))
        except Exception:
            window['-O-'].update("Образ введён неверно!")
        else:
            if decision_functions is None:
                window['-O-'].update("Нет решающих функций!")
            elif len(vector) != values['-A-']:
                window['-O-'].update("Образ введён неверно!")
            else:
                class_id = classify(vector, decision_functions)
                window['-O-'].update(f"Образ относится к классу {class_id + 1}")
