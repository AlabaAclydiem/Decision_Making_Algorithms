import matplotlib.pyplot as plt
import numpy as np
from time import perf_counter

K = np.random.randint(2, 20)
N = np.random.randint(9999, 10000)
POINTS = np.random.rand(1, 2 * N).reshape(2, N)


class Group:
    def __init__(self, kernel):
        self.old_kernel = None
        self.kernel = kernel
        self.x = list()
        self.y = list()
        self.color = np.random.rand(1, 3)

    def change_kernel(self):
        self.old_kernel = self.kernel
        average_point = np.array([sum(self.x) / len(self.x), sum(self.y) / len(self.y)])
        best_point = np.array([self.x[0], self.y[0]])
        for index in range(1, len(self.x) - 1):
            cur_point = np.array([self.x[index], self.y[index]])
            if norm(average_point - cur_point) < norm(average_point - best_point):
                best_point = cur_point
        self.kernel = best_point


def norm(point):
    return (point[0] * point[0] + point[1] * point[1]) ** 0.5


def init_groups():
    kernel_indexes = np.random.permutation(np.arange(N))[:K]
    groups = list()
    for index in kernel_indexes:
        groups.append(Group(np.array([POINTS[0][index], POINTS[1][index]])))
    return groups


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

    return groups


def create_groups_plots(groups, iteration):
    plt.figure(iteration)
    plt.suptitle(f"Iteration {iteration}")
    for index in range(K):
        plt.scatter(groups[index].x, groups[index].y, s=5, c=groups[index].color)
        plt.scatter(groups[index].kernel[0], groups[index].kernel[1], s=15, c="black")


def centers_changed(groups):
    for group in groups:
        if group.old_kernel is None or not np.array_equal(group.old_kernel, group.kernel):
            return True
        return False


if __name__ == "__main__":
    group_list = init_groups()
    group_list = connect_points_to_kernels(group_list)

    step = 0
    t0 = perf_counter()
    while centers_changed(group_list):
        create_groups_plots(group_list, step)
        for group_el in group_list:
            group_el.change_kernel()
        print(step)
        step += 1
        group_list = connect_points_to_kernels(group_list)
    t1 = perf_counter()
    print(t1 - t0)
    plt.show()
