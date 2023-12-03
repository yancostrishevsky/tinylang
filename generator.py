import random

mapa = {
    "NUMBER": 0,
    "Expression": 1,
    "Write": 1,
    "Read": 0,
    "Assignment": 2,
    "Statement": 1,
    "Loop": 2,
    "Conditional": 2,
    "Block": 2,
    "Program": 2,
    "Variable": 0,
    "ID": 0,
}


class Node:
    def __init__(self, parent_node, name):
        self.parent_node = parent_node
        self.children_nodes = []
        self.name = name
        self.min_depth = 0
        self.max_depth = 0
        self.depth = -1 if parent_node is None else parent_node.depth + self.min_depth

    def generate(self, max_depth):
        pass

    def __str__(self, level=0):
        ret = "\t" * level + f"{self.name}\n"
        for child in self.children_nodes:
            ret += child.__str__(level + 1)
        return ret


class Program(Node):
    def __init__(self, max_depth):
        super().__init__(None, "Program")
        self.max_depth = max_depth
        self.generate(max_depth)

    def generate(self, max_depth):
        self.children_nodes.append(Statement(None, max_depth))


class Statement(Node):
    def __init__(self, parent_node, max_depth):
        super().__init__(parent_node, "Statement")
        self.possible_children_nodes = [Loop, Conditional, Block, Assignment, Write]
        self.min_depth = 1
        self.max_depth = max_depth - self.min_depth
        if self.max_depth > 0:
            self.generate(max_depth)

    def generate(self, max_depth):

        possible_child = []

        for child in self.possible_children_nodes:
            name = child(self, 0).name
            if (mapa[name] <= self.max_depth):
                possible_child.append(child)

        if len(possible_child) == 0:
            self.parent_node.children_nodes.remove(self)
        else:
            child_node = random.choice(possible_child)
            child_instance = child_node(self, max_depth)
            self.children_nodes.append(child_instance)


class Loop(Node):
    def __init__(self, parent_node, max_depth):
        super().__init__(parent_node, "Loop")
        self.possible_children_nodes = [Expression, Statement]
        self.min_depth = 2
        self.max_depth = max_depth - self.min_depth
        if self.max_depth > 0:
            self.generate(max_depth)

    def generate(self, max_depth):
        child_instance = Expression(self, max_depth)
        child_instance2 = Statement(self, max_depth)
        if (child_instance.min_depth < self.max_depth) and (child_instance2.min_depth < self.max_depth):
            self.children_nodes.append(child_instance)
            self.children_nodes.append(child_instance2)
        else:
             if self in self.parent_node.children_nodes:
                 self.parent_node.children_nodes.remove(self)



class Conditional(Node):
    def __init__(self, parent_node, max_depth):
        super().__init__(parent_node, "Conditional")
        self.possible_children_nodes = [Expression, Statement, Statement]
        self.min_depth = 2
        self.max_depth = max_depth - self.min_depth
        if self.max_depth > 0:
            self.generate(max_depth)

    def generate(self, max_depth):
        child_instance = Expression(self, max_depth)
        child_instance2 = Statement(self, max_depth)
        if (child_instance.min_depth < self.max_depth) and (child_instance2.min_depth < self.max_depth):
            self.children_nodes.append(Expression(self, max_depth))
            self.children_nodes.append(Statement(self, max_depth))

            # self.children_nodes.append(Statement(self, max_depth))
        else:
            if self in self.parent_node.children_nodes:
                self.parent_node.children_nodes.remove(self)


class Block(Node):
    def __init__(self, parent_node, max_depth):
        super().__init__(parent_node, "Block")
        self.possible_children_nodes = [Statement]
        self.min_depth = 2
        self.max_depth = max_depth - self.min_depth
        if self.max_depth > 0:
            self.generate(max_depth)

    def generate(self, max_depth):
        nums = [1, 2, 3]
        num_of_stat = random.choice(nums)

        for num in range(num_of_stat):
            child_instance = Statement(self, max_depth)
            if child_instance.min_depth < self.max_depth:
                self.children_nodes.append(child_instance)
            else:
                if self in self.parent_node.children_nodes:
                    self.parent_node.children_nodes.remove(self)



class Assignment(Node):
    def __init__(self, parent_node, max_depth):
        super().__init__(parent_node, "Assignment")
        self.possible_children_nodes = [Variable, Expression, Read]
        self.min_depth = 2
        self.max_depth = max_depth - self.min_depth
        if self.max_depth > 0:
            self.generate(max_depth)

    def generate(self, max_depth):
        child_instance_1 = Variable(self, max_depth)
        if child_instance_1.min_depth < self.max_depth:
            self.children_nodes.append(child_instance_1)
        else:
            if self in self.parent_node.children_nodes:
                self.parent_node.children_nodes.remove(self)


        if self.min_depth + 1 < self.max_depth:
            self.children_nodes.append(child_instance_1)
            self.children_nodes.append(Read())


class Write(Node):
    def __init__(self, parent_node, max_depth):
        super().__init__(parent_node, "Write")
        self.possible_children_nodes = [Variable]
        self.min_depth = 1
        self.max_depth = max_depth - self.min_depth
        if self.max_depth > 0:
            self.generate(max_depth)

    def generate(self, max_depth):
        if self.min_depth + 1 < self.max_depth:
            self.children_nodes.append(Variable(self, max_depth))
        else:
            if self in self.parent_node.children_nodes:
                self.parent_node.children_nodes.remove(self)


class ID(Node):
    def __init__(self, parent_node, max_depth):
        super().__init__(parent_node, "ID")
        self.value = f"Var_{random.randint(1, 100)}"


class NUMBER(Node):
    def __init__(self, parent_node, max_depth):
        super().__init__(parent_node, "NUMBER")
        self.value = random.randint(1, 100)


class Expression(Node):
    def __init__(self, parent_node, max_depth):
        super().__init__(parent_node, "Expression")
        self.possible_children_nodes = [ID, NUMBER, Expression]
        self.min_depth = 2
        self.max_depth = max_depth - self.min_depth
        if self.max_depth > 0:
            self.generate(max_depth)

    def generate(self, max_depth):
        possible_child = []

        for child in self.possible_children_nodes:
            name = child(self, 0).name
            if (mapa[name] <= self.max_depth):
                possible_child.append(child)
        if(len(possible_child)==0):
            if self in self.parent_node.children_nodes:
                self.parent_node.children_nodes.remove(self)

        child_node = random.choice(possible_child)
        child_instance_1 = child_node(self, max_depth)
        if child_instance_1.__class__ == Expression:
            child_instance_2 = Operator(self, max_depth)
            child_instance_3 = Expression(self, max_depth)

            self.children_nodes.append(child_instance_1)
            self.children_nodes.append(child_instance_2)
            self.children_nodes.append(child_instance_3)

        else:
            self.children_nodes.append(child_instance_1)


class Operator(Node):
    def __init__(self, parent_node, max_depth):
        super().__init__(parent_node, "Operator")
        self.operator = random.choice(["+", "-", "*", "/"])

    def __str__(self, level=0):
        ret = "\t" * level + f"{self.name}: {self.operator}\n"
        return ret


class Variable(Node):
    def __init__(self, parent_node, max_depth):
        super().__init__(parent_node, "Variable")
        self.name = f"Var_{random.randint(1, 100)}"


class Read(Node):
    def __init__(self):
        super().__init__(None, "Read")


program = Program(3)
print(program)
