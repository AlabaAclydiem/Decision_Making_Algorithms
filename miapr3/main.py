import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib

matplotlib.use('TkAgg')
fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)


def draw_figure(canvas, figure):
    tk_canvas = FigureCanvasTkAgg(figure, canvas)
    tk_canvas.draw()
    tk_canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
    return tk_canvas


def pdf_normal(x, mean, sigma):
    return np.exp(-0.5 * ((x - mean) / sigma) ** 2) / (np.sqrt(2 * np.pi) * sigma)


layout = [
    [sg.Text('Вероятность попадания случайной величины в первый класс:')],
    [sg.Slider(range=(0.0, 1.0), resolution=0.01, default_value=0.3, expand_x=True, enable_events=True,
               orientation='horizontal', key='-SL-')],
    [sg.Canvas(key='-CV-')],
    [sg.Text('Вероятность ложной тревоги:')],
    [sg.Text('', enable_events=True, key="-LT-")],
    [sg.Text('Вероятность пропуска обнаружения ошибки:')],
    [sg.Text('', enable_events=True, key="-POO-")],
    [sg.Text('Вероятность суммарной ошибки классификаиции:')],
    [sg.Text('', enable_events=True, key="-SOK-")],
]

CLASS_ONE_MEAN, CLASS_ONE_SIGMA = 3, 3
CLASS_TWO_MEAN, CLASS_TWO_SIGMA = -4, 4

PROB_C1 = 0.3
PROB_C2 = 1 - PROB_C1

LT, POO, SOK = 0, 0, 0


def count_and_plot():
    global LT, POO, SOK
    LT = 0
    POO = 0
    SOK = 0
    x, step = np.linspace(-10, 10, 1000, retstep=True)
    y1 = np.zeros(1000)
    y2 = np.zeros(1000)
    c, id = None, None
    for i, el in enumerate(x):
        y1[i] = pdf_normal(el, CLASS_ONE_MEAN, CLASS_ONE_SIGMA) * PROB_C1
        y2[i] = pdf_normal(el, CLASS_TWO_MEAN, CLASS_TWO_SIGMA) * PROB_C2
        if c is None or abs(y1[i] - y2[i]) < abs(y1[id] - y2[id]):
            c = el
            id = i

    ax.clear()
    ax.set_ylim(0, 0.15)
    ax.plot(x, y1)
    ax.plot(x, y2)
    ax.plot(np.zeros(len(x)) + c, np.linspace(0, 0.15, 1000))

    for c1, c2 in zip(y1[:id], y2[:id]):
        LT += min(c1, c2) * step
    for c1, c2 in zip(y1[id:], y2[id:]):
        POO += min(c1, c2) * step
    SOK = LT + POO


window = sg.Window('MiAPR3', layout, size=(715, 700), finalize=True, element_justification='center')
count_and_plot()
window['-LT-'].update(value=LT)
window['-POO-'].update(value=POO)
window['-SOK-'].update(value=SOK)
canvas = draw_figure(window['-CV-'].TKCanvas, fig)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == '-SL-':
        PROB_C1 = values['-SL-']
        PROB_C2 = 1 - PROB_C1
        count_and_plot()
        window['-LT-'].update(value=LT)
        window['-POO-'].update(value=POO)
        window['-SOK-'].update(value=SOK)
        canvas.draw()
