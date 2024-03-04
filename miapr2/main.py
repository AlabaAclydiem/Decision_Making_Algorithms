import matplotlib.pyplot as plt
import numpy as np
from time import perf_counter

N = np.random.randint(9999, 10000)
POINTS = np.random.rand(1, 2 * N).reshape(2, N)


class Group:
    def __init__(self, base_kernel):
        self.kernel = base_kernel
        self.furthest_point = None
        self.x = list()
        self.y = list()
        self.color = np.random.rand(1, 3)


def norm(point):
    return (point[0] * point[0] + point[1] * point[1]) ** 0.5


def init_groups():
    kernel_index = np.random.choice(N)
    groups = list()
    groups.append(Group(np.array([POINTS[0][kernel_index], POINTS[1][kernel_index]])))
    count_furthest_point(groups[0], POINTS[0], POINTS[1])
    groups.append(Group(groups[0].furthest_point))
    groups = connect_points_to_kernels(groups)
    return groups


def count_furthest_point(group, x_list, y_list):
    best_point = group.kernel
    for index in range(1, len(x_list) - 1):
        cur_point = np.array([x_list[index], y_list[index]])
        if norm(group.kernel - cur_point) > norm(group.kernel - best_point):
            best_point = cur_point
    group.furthest_point = best_point


def connect_points_to_kernels(groups):
    for group in groups:
        group.x = list()
        group.y = list()
    for index in range(N):
        distances = list()
        point = np.array([POINTS[0][index], POINTS[1][index]])
        for group in groups:
            distances.append(norm(group.kernel - point))
        group_index = distances.index(min(distances))
        groups[group_index].x.append(point[0])
        groups[group_index].y.append(point[1])
    for group in groups:
        count_furthest_point(group, group.x, group.y)
    return groups


def create_groups_plots(groups, iteration):
    plt.figure(iteration)
    plt.suptitle(f"Iteration {iteration}")
    for index in range(len(groups)):
        plt.scatter(groups[index].x, groups[index].y, s=5, c=groups[index].color)
        plt.scatter(groups[index].kernel[0], groups[index].kernel[1], s=15, c="black")


def count_threshold(groups):
    threshold = 0
    for i, i_group in enumerate(groups):
        for j_group in groups[i + 1:]:
            threshold += norm(i_group.kernel - j_group.kernel)
    threshold /= len(groups) * (len(groups) - 1) * 1.2
    return threshold


def get_new_kernel(groups, threshold):
    group_with_furthest_point = max(groups, key=lambda group: norm(group.kernel - group.furthest_point))
    return group_with_furthest_point.furthest_point, norm(group_with_furthest_point.furthest_point -
                                                          group_with_furthest_point.kernel) >= threshold


if __name__ == "__main__":
    group_list = init_groups()
    step = 0
    t0 = perf_counter()
    while True:
        create_groups_plots(group_list, step)
        limit = count_threshold(group_list)
        kernel, success = get_new_kernel(group_list, limit)
        if not success:
            break
        group_list.append(Group(kernel))
        group_list = connect_points_to_kernels(group_list)
        print(step)
        step += 1
    t1 = perf_counter()
    print(t1 - t0)
    plt.show()
