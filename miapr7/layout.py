import PySimpleGUI as sg

layout_left = [
    [sg.Button(button_text="Сгенерировать изображение по грамматике", enable_events=True, key='-GEN-')],
    [sg.Button(button_text="Сгенерировать искажённое изображение", enable_events=True, key='-BGEN-')],
    [sg.Button(button_text="Проверить на соответстиве грамматике", enable_events=True, key="-RULE-")],
    [sg.Text("", enable_events=True, key="-O-")],
]

layout_right = [
    [sg.Text('Сгенерированное изображение')],
    [sg.Canvas(key='-CV-')],
]

layout = [
    [sg.Column(layout_left),
     sg.VerticalSeparator(),
     sg.Column(layout_right)],
]
