import PySimpleGUI as sg

layout_left = [
    [sg.Text("Количество терминальных цепочек")],
    [sg.Slider(range=(7, 15), orientation="horizontal", enable_events=True, key="-TERMINAL-")],
    [sg.Text("Предел длины терминальных цепочек")],
    [sg.Slider(range=(5, 20), orientation="horizontal", enable_events=True, key="-LEN-")],
    [sg.Button(button_text="Сгенерировать грамматику", enable_events=True, key='-GRAMMAR-')],
    [sg.Button(button_text="Сгенерировать набор слов по грамматике", enable_events=True, key="-WORDS-")],
]

layout_center_left = [
    [sg.Text("Терминальные цепочки")],
    [sg.Multiline(size=(30, 20), disabled=True, key='-T-')],
]

layout_center_right = [
    [sg.Text("Грамматика")],
    [sg.Multiline(size=(30, 20), disabled=True, key='-G-')],
]

layout_right = [
    [sg.Text("Сгенерированные слова")],
    [sg.Multiline(size=(30, 20), disabled=True, key='-W-')],
]

layout = [
    [sg.Column(layout_left),
     sg.VerticalSeparator(),
     sg.Column(layout_center_left),
     sg.VerticalSeparator(),
     sg.Column(layout_center_right),
     sg.VerticalSeparator(),
     sg.Column(layout_right)],
]
