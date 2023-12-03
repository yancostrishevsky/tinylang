import random
import sys

class Node:
    def __init__(self, parent_node, name):
        self.parent_node = parent_node
        self.children_nodes = []
        self.possible_children_nodes = None
        self.name = name
        self.depth = -1 if parent_node is None else parent_node.depth + 1

    def __str__(self):
        return ""

    @staticmethod
    def get_random_percentage():
        return random.random()

    def get_random_possible_child(self):
        if self.possible_children_nodes is None:
            return None
        return random.choice(self.possible_children_nodes)

    def get_children_as_nodes(self):
        nodes = [self]
        for node in self.children_nodes:
            nodes.extend(node.get_children_as_nodes())
        return nodes

    @staticmethod
    def swap_nodes(node1, node2):
        parent1 = node1.parent_node
        parent2 = node2.parent_node

        node1_position = parent1.children_nodes.index(node1)
        node2_position = parent2.children_nodes.index(node2)

        parent1.children_nodes[node1_position] = node2
        node2.parent_node = parent1

        parent2.children_nodes[node2_position] = node1
        node1.parent_node = parent2

    def generate(self, max_depth):
        pass

    def get_program_variables(self):
        return self.parent_node.get_program_variables()

    def add_to_program_variables(self, variable):
        self.parent_node.add_to_program_variables(variable)


class Program(Node):
    def __init__(self, max_depth):
        super().__init__(None, "Program")
        self.variables = []
        self.generate(max_depth)

    def get_program_variables(self):
        return self.variables

    def generate(self, max_depth):
        self.children_nodes.append(Scope(self, max_depth))

    def add_to_program_variables(self, variable):
        for var in self.variables:
            if var.name == variable.name:
                return
        self.variables.append(variable)

    def __str__(self):
        node_str = f"{self.name}\n"
        for child_node in self.variables:
            node_str += str(child_node.name + " ")
        return node_str

class Scope(Node):
    def __init__(self, parent_node, max_depth):
        super().__init__(parent_node, "Scope")
        self.possible_children_nodes = ["Assignment", "Loop", "Conditional", "Block", "Write"]
        self.generate(max_depth)

    def generate(self, max_depth):
        if self.depth < max_depth:
            child_name = self.get_random_possible_child()
            self.add_to_program_variables(self)
            if child_name == "Assignment":
                self.children_nodes.append(Assignment(self, max_depth))
            elif child_name == "Loop":
                self.children_nodes.append(Loop(self, max_depth))
            elif child_name == "Conditional":
                self.children_nodes.append(Conditional(self, max_depth))
            elif child_name == "Block":
                self.children_nodes.append(Block(self, max_depth))
            elif child_name == "Write":
                self.children_nodes.append(Write(self, max_depth))

class Assignment(Node):
    def __init__(self, parent_node, max_depth):
        super().__init__(parent_node, "Assignment")
        self.possible_children_nodes = ["Variable", "Expression", "Read"]
        self.generate(max_depth)

    def generate(self, max_depth):
        if self.depth < max_depth:
            self.children_nodes.append(Variable(self, max_depth))
            self.children_nodes.append(Expression(self, max_depth))
            self.add_to_program_variables(self)

class Variable(Node):
    def __init__(self, parent_node, max_depth):
        super().__init__(parent_node, "Variable")
        self.name = f"Var_{random.randint(1, 100)}"
        self.generate(max_depth)



class Expression(Node):
    def __init__(self, parent_node, max_depth):
        super().__init__(parent_node, "Expression")
        self.possible_children_nodes = ["Variable", "Number", "Operator", "Expression"]
        self.generate(max_depth)


    def generate(self, max_depth):
        if self.depth < max_depth:
            self.add_to_program_variables(self)
            child_name = self.get_random_possible_child()
            if child_name == "Variable":
                self.children_nodes.append(Variable(self, max_depth))
            elif child_name == "Number":
                self.children_nodes.append(Number(self, max_depth))
            elif child_name == "Operator":
                self.children_nodes.append(Operator(self, max_depth))
            elif child_name == "Expression":
                self.children_nodes.append(Operator(self, max_depth))


class Number(Node):
    def __init__(self, parent_node, max_depth):
        super().__init__(parent_node, "Number")
        self.value = random.randint(1, 100)
        self.add_to_program_variables(self)


class Operator(Node):
    def __init__(self, parent_node, max_depth):
        super().__init__(parent_node, "Operator")
        self.operator = random.choice(["+", "-", "*", "/"])
        self.add_to_program_variables(self)


class Loop(Node):
    def __init__(self, parent_node, max_depth):
        super().__init__(parent_node, "Loop")
        self.possible_children_nodes = ["Expression", "Scope"]
        self.generate(max_depth)

    def generate(self, max_depth):
        if self.depth < max_depth:
            self.add_to_program_variables(self)
            self.children_nodes.append(Expression(self, max_depth))
            self.children_nodes.append(Scope(self, max_depth))



class Conditional(Node):
    def __init__(self, parent_node, max_depth):
        super().__init__(parent_node, "Conditional")
        self.possible_children_nodes = ["Expression", "Scope", "Scope"]
        self.generate(max_depth)
        self.add_to_program_variables(self)

    def generate(self, max_depth):
        if self.depth < max_depth:
            self.children_nodes.append(Expression(self, max_depth))
            self.children_nodes.append(Scope(self, max_depth))
            self.children_nodes.append(Scope(self, max_depth))



class Block(Node):
    def __init__(self, parent_node, max_depth):
        super().__init__(parent_node, "Block")
        self.possible_children_nodes = ["Scope"]
        self.generate(max_depth)
        self.add_to_program_variables(self)

    def generate(self, max_depth):
        if self.depth < max_depth:
            self.children_nodes.append(Scope(self, max_depth))





class Read(Node):
    def __init__(self, parent_node, max_depth):
        super().__init__(parent_node, "Read")
        self.possible_children_nodes = ["Variable"]
        self.generate(max_depth)
        self.add_to_program_variables(self)

    def generate(self, max_depth):
        if self.depth < max_depth:
            self.children_nodes.append(Variable(self, max_depth))



class Write(Node):
    def __init__(self, parent_node, max_depth):
        super().__init__(parent_node, "Write")
        self.possible_children_nodes = ["Variable"]
        self.generate(max_depth)
        self.add_to_program_variables(self)

    def generate(self, max_depth):
        if self.depth < max_depth:
            self.children_nodes.append(Variable(self, max_depth))


program = Program(4)

print(program)