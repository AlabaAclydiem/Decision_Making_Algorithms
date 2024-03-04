import PySimpleGUI as sg


layout_left = [
    [sg.Text("Кол-во образов в классе")],
    [sg.Slider(range=(4, 6), resolution=2, orientation="horizontal", enable_events=True, key="-V-")],
    [sg.Text("Обучающая выборка")],
    [sg.Multiline(size=(30, 10), disabled=True, key='-TS-')],
    [sg.Button(button_text="Определить решающую функцию", enable_events=True, key='-TR-')],
    [sg.Text('Решающая функция:')],
    [sg.Text("", enable_events=True, key="-F-")],
    [sg.Text("Введите образ для классификации (значения признаков через пробел):")],
    [sg.Input(enable_events=True, key="-I-")],
    [sg.Button(button_text="Классифицировать", enable_events=True, key="-CL-")],
    [sg.Text("", enable_events=True, key="-O-")],
]

layout_right = [
    [sg.Text('Графическое отображение решающей функции и точек обучающей выборки:')],
    [sg.Canvas(key='-CV-')],
]

layout = [
    [sg.Column(layout_left),
     sg.VerticalSeparator(),
     sg.Column(layout_right)],
]
