import PySimpleGUI as sg

layout_left = [
    [sg.Text("Кол-во классов")],
    [sg.Slider(range=(2, 10), orientation="horizontal", enable_events=True, key="-C-")],
    [sg.Text("Кол-во образов в классе")],
    [sg.Slider(range=(1, 15), orientation="horizontal", enable_events=True, key="-V-")],
    [sg.Text("Кол-во признаков в образе")],
    [sg.Slider(range=(1, 10), orientation="horizontal", enable_events=True, key="-A-")],
    [sg.Button(button_text="Определить решающие функции", enable_events=True, key='-TR-')],
    [sg.Text("Введите образ для классификации (значения признаков через пробел):")],
    [sg.Input(enable_events=True, key="-I-")],
    [sg.Button(button_text="Классифицировать", enable_events=True, key="-CL-")],
    [sg.Input(enable_events=True, key="-O-", disabled=True)],
]

layout_center = [
    [sg.Text("Обучающая выборка")],
    [sg.Multiline(size=(60, 40), disabled=True, key='-TS-')],
]

layout_right = [
    [sg.Text("Решающие функции")],
    [sg.Multiline(size=(60, 40), disabled=True, key='-F-')],
]

layout = [
    [sg.Column(layout_left),
     sg.VerticalSeparator(),
     sg.Column(layout_center),
     sg.VerticalSeparator(),
     sg.Column(layout_right)],
]
