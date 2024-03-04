import numpy as np


def generate_training_set(num_classes, num_vectors, num_attributes):
    flatten_array = np.random.random_integers(-100, 100, num_classes * num_vectors * num_attributes)
    return flatten_array.reshape((num_classes, num_vectors, num_attributes))


def training_set_to_string(training_set):
    class_strings = []
    for cls in training_set:
        vector_strings = []
        for vector in cls:
            vector_strings.append(str(vector))
        class_strings.append("\t\n".join(vector_strings))
    return "\n\n".join(class_strings)


def expand_set(training_set):
    expanded_shape = training_set.shape
    expanded_shape = (expanded_shape[0], expanded_shape[1], expanded_shape[2] + 1)
    expanded_set = np.ones(expanded_shape)
    for cls_id, cls in enumerate(training_set):
        for vector_id, vector in enumerate(cls):
            for attribute_id, attribute in enumerate(vector):
                expanded_set[cls_id, vector_id, attribute_id] = attribute
    return expanded_set


def get_decision_functions(training_set):
    expanded_set = expand_set(training_set)
    classes_num, attributes_num = len(expanded_set), len(expanded_set[0, 0])
    weights_set = np.zeros((classes_num, attributes_num))
    c, is_correct = 1, False
    iteration_limit, iteration = 2000, 0
    while not is_correct and iteration <= iteration_limit:
        iteration += 1
        is_correct = True
        for cls_id, cls in enumerate(expanded_set):
            for vector in cls:
                classifier_results = [class_weight.dot(vector) for class_weight in weights_set]
                for result_id, result in enumerate(classifier_results):
                    if result_id == cls_id:
                        continue
                    if result >= classifier_results[cls_id]:
                        is_correct = False
                        weights_set[result_id] -= c * vector
                if not is_correct:
                    weights_set[cls_id] += c * vector
    return iteration <= iteration_limit, weights_set


def decision_functions_to_string(functions, status):
    function_strings = []
    for function_id, function in enumerate(functions):
        function_string = f"d{function_id + 1}(x) ="
        coefficient_strings = []
        for coefficient_id, coefficient in enumerate(function):
            if int(coefficient) >= 0:
                if coefficient_id + 1 != len(function):
                    coefficient_string = f" + {abs(int(coefficient))}x{coefficient_id + 1}"
                else:
                    coefficient_string = f" + {abs(int(coefficient))}"
            else:
                if coefficient_id + 1 != len(function):
                    coefficient_string = f" - {abs(int(coefficient))}x{coefficient_id + 1}"
                else:
                    coefficient_string = f" - {abs(int(coefficient))}"
            coefficient_strings.append(coefficient_string)
        function_strings.append(function_string + "".join(coefficient_strings))
    status_string = ""
    if not status:
        status_string = "Достигнут предел итераций, решающие функции могут быть неверны"
    return "\n\n\n".join((["\n".join(function_strings), status_string]))


def classify(vector, functions):
    classifier_results = []
    vector = np.append(vector, [1])
    for decision_function in functions:
        classifier_results.append(decision_function.dot(vector))
    max_values_ids = np.argmax(classifier_results)
    return max_values_ids
