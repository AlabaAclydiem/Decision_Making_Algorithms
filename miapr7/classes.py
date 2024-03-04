import matplotlib.pyplot as plt
import numpy.random as rnd
from abc import ABC, abstractmethod

LEFT_RULE = 0
DOWN_RULE = 1


class Node(ABC):
    @abstractmethod
    def __init__(self, x, y, anomaly):
        self.parent = None
        self.left = None
        self.right = None
        self.size = 10
        self.x = x
        self.y = y
        self.salt()

    def salt(self):
        self.x += rnd.rand() * 2 - 1
        self.y += rnd.rand() * 2 - 1


class TerminalNode(Node):
    @abstractmethod
    def __init__(self, parent, x, y, anomaly):
        super().__init__(x, y, anomaly)
        self.parent = parent
        if anomaly:
            self.anomaly()

    @abstractmethod
    def plot(self, ax):
        pass

    def anomaly(self):
        self.x += (rnd.rand() - 1) * 30
        self.y += (rnd.rand() - 1) * 30


class HorizontalLine(TerminalNode):
    def __init__(self, parent, x, y, anomaly):
        super().__init__(parent, x, y, anomaly)

    def plot(self, ax):
        ax.hlines(y=self.y, xmin=self.x, xmax=self.x + self.size, colors='blue')


class VerticalLine(TerminalNode):
    def __init__(self, parent, x, y, anomaly):
        super().__init__(parent, x, y, anomaly)

    def plot(self, ax):
        ax.vlines(x=self.x, ymin=self.y, ymax=self.y + self.size, colors='blue')


class VSides(Node):
    def __init__(self, parent, x, y, anomaly):
        super().__init__(x, y, anomaly)
        self.parent = parent
        self.left = VerticalLine(self, x, y, anomaly)
        self.right = VerticalLine(self, x + self.size, y, anomaly)
        self.x = (self.left.x + self.right.x) / 2
        self.y = (self.left.y + self.right.y) / 2
        self.rule = LEFT_RULE


class VVHSides(Node):
    def __init__(self, parent, x, y, anomaly):
        super().__init__(x, y, anomaly)
        self.parent = parent
        self.left = VSides(self, x, y, anomaly)
        self.right = HorizontalLine(self, x, y + self.size, anomaly)
        self.x = (self.left.x + self.right.x) / 2
        self.y = (self.left.y + self.right.y) / 2
        self.rule = DOWN_RULE


class Square(Node):
    def __init__(self, parent, x, y, anomaly):
        super().__init__(x, y, anomaly)
        self.parent = parent
        self.left = HorizontalLine(self, x, y, anomaly)
        self.right = VVHSides(self, x, y, anomaly)
        self.x = (self.left.x + self.right.x) / 2
        self.y = (self.left.y + self.right.y) / 2
        self.rule = DOWN_RULE


class DoubleSquare(Node):
    def __init__(self, parent, x, y, anomaly):
        super().__init__(x, y, anomaly)
        self.parent = parent
        self.left = Square(self, x - self.size, y, anomaly)
        self.right = Square(self, x, y, anomaly)
        self.x = (self.left.x + self.right.x) / 2
        self.y = (self.left.y + self.right.y) / 2
        self.rule = LEFT_RULE


class TripleSquare(Node):
    def __init__(self, parent, x, y, anomaly):
        super().__init__(x, y, anomaly)
        self.parent = parent
        self.left = DoubleSquare(self, x - self.size, y, anomaly)
        self.right = Square(self, x, y, anomaly)
        self.x = (self.left.x + self.right.x) / 2
        self.y = (self.left.y + self.right.y) / 2
        self.rule = LEFT_RULE


class GForm(Node):
    def __init__(self, parent, x, y, anomaly):
        super().__init__(x, y, anomaly)
        self.parent = parent
        self.left = TripleSquare(self, x, y, anomaly)
        self.right = Square(self, x, y + self.size, anomaly)
        self.x = (self.left.x + self.right.x) / 2
        self.y = (self.left.y + self.right.y) / 2
        self.rule = DOWN_RULE

class TForm(Node):
    def __init__(self, parent, x, y, anomaly):
        super().__init__(x, y, anomaly)
        self.parent = parent
        self.left = Square(self, x, y, anomaly)
        self.right = GForm(self, x, y + self.size, anomaly)
        self.x = (self.left.x + self.right.x) / 2
        self.y = (self.left.y + self.right.y) / 2
        self.rule = DOWN_RULE


class RubicConv(Node):
    def __init__(self, x, y, anomaly):
        super().__init__(x, y, anomaly)
        self.left = TForm(self, x, y, anomaly)
        self.right = Square(self, x + self.size, y + self.size, anomaly)
        self.x = (self.left.x + self.right.x) / 2
        self.y = (self.left.y + self.right.y) / 2
        self.rule = LEFT_RULE


class Grammar:
    def __init__(self, anomaly):
        self.grammar_tree = RubicConv(0, 0, anomaly)

    def plot(self, ax, current_node=None):
        if current_node is None:
            current_node = self.grammar_tree
        if current_node.left is None:
            current_node.plot(ax)
            return
        self.plot(ax, current_node.left)
        self.plot(ax, current_node.right)

    def check_rules(self, current_node=None):
        if current_node is None:
            current_node = self.grammar_tree
        if current_node.left is None:
            return True
        correct = None
        if current_node.rule == LEFT_RULE:
            correct = current_node.left.x <= current_node.right.x
        else:
            correct = current_node.left.y <= current_node.right.y
        correct &= self.check_rules(current_node.left)
        correct &= self.check_rules(current_node.right)
        return correct

