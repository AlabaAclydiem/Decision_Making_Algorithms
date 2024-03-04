import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
from classes import Grammar
from layout import layout


def ax_init(ax):
    ax.clear()


def draw_figure(canvas, figure):
    tk_canvas = FigureCanvasTkAgg(figure, canvas)
    tk_canvas.draw()
    tk_canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
    return tk_canvas


matplotlib.use('TkAgg')
fig = matplotlib.figure.Figure(figsize=(5, 5), dpi=100)
ax = fig.add_subplot(111)
ax_init(ax)

window = sg.Window('MiAPR7', layout, finalize=True, element_justification='center')

canvas = draw_figure(window['-CV-'].TKCanvas, fig)

grammar = Grammar(anomaly=False)
grammar.plot(ax)
canvas.draw()

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == '-GEN-':
        ax_init(ax)
        grammar = Grammar(anomaly=False)
        grammar.plot(ax)
        canvas.draw()
    if event == '-BGEN-':
        ax_init(ax)
        grammar = Grammar(anomaly=True)
        grammar.plot(ax)
        canvas.draw()
    if event == '-RULE-':
        if grammar.check_rules():
            window['-O-'].update("Изображение соответствует грамматике")
        else:
            window['-O-'].update("Изображение не сооответствует грамматике")
