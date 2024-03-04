import matplotlib
import matplotlib.pyplot as plt
import PySimpleGUI as sg
import numpy as np

from layout import layout
from functions import draw_figure, generate_training_set, training_set_to_string, \
    decision_function_to_string, get_decision_function, classify, get_points, ax_init, get_decision_function_points

matplotlib.use('TkAgg')
fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)
ax_init(ax)

window = sg.Window('MiAPR5', layout, finalize=True, element_justification='center')

canvas = draw_figure(window['-CV-'].TKCanvas, fig)

training_set, labels = generate_training_set(6, 2)
decision_function = None
window['-TS-'].update(training_set_to_string(training_set, labels))
c1_xpoints, c2_xpoints, c1_ypoints, c2_ypoints = get_points(training_set, labels)
ax.scatter(c1_xpoints, c1_ypoints, s=25, c='black')
ax.scatter(c2_xpoints, c2_ypoints, s=25, c='purple')
canvas.draw()
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == '-V-':
        training_set, labels = generate_training_set(int(values['-V-']), 2)
        decision_function = None
        window['-TS-'].update(training_set_to_string(training_set, labels))
        c1_xpoints, c2_xpoints, c1_ypoints, c2_ypoints = get_points(training_set, labels)
        ax_init(ax)
        ax.scatter(c1_xpoints, c1_ypoints, s=25, c='black')
        ax.scatter(c2_xpoints, c2_ypoints, s=25, c='purple')
        canvas.draw()
    if event == '-TR-':
        decision_function, ok = get_decision_function(training_set, labels)
        x_func, y_func = get_decision_function_points(decision_function)
        ax.scatter(x_func, y_func, s=1, c='red')
        canvas.draw()
        window['-F-'].update(decision_function_to_string(decision_function, ok))
    if event == '-CL-':
        try:
            vector = np.array(list(map(int, values['-I-'].split())))
        except Exception:
            window['-O-'].update("Образ введён неверно!")
        else:
            if decision_function is None:
                window['-O-'].update("Нет решающих функций!")
            elif len(vector) != 2:
                window['-O-'].update("Образ введён неверно!")
            else:
                class_id = classify(vector, decision_function)
                if class_id == 0:
                    ax.scatter(vector[0], vector[1], s=15, c='black')
                else:
                    ax.scatter(vector[0], vector[1], s=15, c='purple')
                canvas.draw()
                window['-O-'].update(f"Образ относится к классу {class_id}")
