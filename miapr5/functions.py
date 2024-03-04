from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

local_weights = []
base_weight = np.array([1, 4, 4, 16])


def ax_init(ax):
    ax.clear()
    ax.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.5)
    ax.set_ylim(-11, 11)
    ax.set_xlim(-11, 11)
    ax.axvline(x=0, color='black')
    ax.axhline(y=0, color='black')


def draw_figure(canvas, figure):
    tk_canvas = FigureCanvasTkAgg(figure, canvas)
    tk_canvas.draw()
    tk_canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
    return tk_canvas


def get_points(training_set, labels):
    c1_x = [vector[0] for vector_id, vector in enumerate(training_set) if labels[vector_id] == 0]
    c2_x = [vector[0] for vector_id, vector in enumerate(training_set) if labels[vector_id] == 1]
    c1_y = [vector[1] for vector_id, vector in enumerate(training_set) if labels[vector_id] == 0]
    c2_y = [vector[1] for vector_id, vector in enumerate(training_set) if labels[vector_id] == 1]
    return c1_x, c2_x, c1_y, c2_y


def get_decision_function_points(decision_function):
    x = np.linspace(-11, 11, 10000)
    denominator = (decision_function[2] + decision_function[3] * x)
    if all(denominator) != 0:
        y = -(decision_function[0] + decision_function[1] * x) / denominator
    else:
        y = np.linspace(0, 0, 10000)
    return x, y


def generate_training_set(num_vectors, num_attributes):
    global local_weights
    flatten_array = np.random.random_integers(-10, 10, num_vectors * num_attributes)
    flatten_array = flatten_array.astype(np.int64)
    labels = [0] * num_vectors
    labels[num_vectors // 2:] = [1] * (num_vectors // 2)
    training_set = flatten_array.reshape(num_vectors, num_attributes)
    local_weights = np.zeros((num_vectors, 4), dtype=np.int64)
    for vector_id, vector in enumerate(training_set):
        local_weights[vector_id] = calc_local_weight(vector, base_weight)
    return training_set, labels


def training_set_to_string(training_set, labels):
    vector_strings = []
    for vector, label in zip(training_set, labels):
        vector_strings.append(f"{str(vector)} --- {label}")
    return "\n".join(vector_strings)


def get_decision_function(training_set, labels):
    weights = np.array(local_weights[0], dtype=np.int64)
    is_correct, iteration_limit, iteration = False, 100000, 0
    while not is_correct and iteration <= iteration_limit:
        is_correct = True
        ro = 0
        for vector_id, vector in enumerate(training_set[:-1]):
            weights += ro * local_weights[vector_id]
            predicted_cls = classify(training_set[vector_id + 1], weights)
            if predicted_cls > labels[vector_id + 1]:
                ro = 1
                is_correct = False
            elif predicted_cls < labels[vector_id + 1]:
                ro = -1
                is_correct = False
            else:
                ro = 0
        predicted_cls = classify(training_set[0], weights)
        if predicted_cls > labels[0]:
            ro = 1
            is_correct = False
        elif predicted_cls < labels[0]:
            ro = -1
            is_correct = False
        else:
            ro = 0
        weights += ro * local_weights[0]
        iteration += 1
    return weights, iteration <= iteration_limit


def calc_local_weight(vector, base):
    return np.array([base[0], base[1] * vector[0], base[2] * vector[1], base[3] * vector[0] * vector[1]],
                    dtype=np.int64)


def calc_function(vector, function):
    return function[0] + function[1] * vector[0] + function[2] * vector[1] \
                + function[3] * vector[0] * vector[1]


def classify(vector, function):
    return 0 if calc_function(vector, function) > 0 else 1


def decision_function_to_string(function, ok):
    signs = ["+" if coefficient >= 0 else "-" for coefficient in function]
    function_string = f"d(x) = {signs[0]} {abs(function[0])} {signs[1]} {abs(function[1])}x1 " \
                      f"{signs[2]}{abs(function[2])}x2 {signs[3]}{abs(function[3])}x1x2 "
    if ok:
        return function_string
    else:
        return f"Превышен предел итераций!!! {function_string}"
