from typing import List
import random

class ProgramGenerator:
    def generate_program(self, config):
        return Program(config)

    def crossover(self, parent_one, parent_two):
        children = []
        random_gen = random.Random()

        parent_one_tree = parent_one.get_children_as_nodes()
        parent_two_tree = parent_two.get_children_as_nodes()
        find_cross = True

        while find_cross:
            random_parent_one_node = None
            while random_parent_one_node is None or random_parent_one_node.name == "Scope":
                random_index = random_gen.randint(1, len(parent_one_tree) - 1)
                random_parent_one_node = parent_one_tree[random_index]

            for node in parent_two_tree:
                if random_parent_one_node.name == node.name:
                    Node.swap_nodes(random_parent_one_node, node)
                    children.extend([parent_one, parent_two])
                    find_cross = False
                    break

        return children

    def mutate(self, parent):
        random_gen = random.Random()
        parent_tree = parent.get_children_as_nodes()
        random_parent_one_node = None

        if len(parent_tree) - 1 == 1:
            return parent

        while random_parent_one_node is None or (random_parent_one_node.name == "ReadStatement"
                                                 or (random_parent_one_node.name == "Scope" and not random_parent_one_node.children_nodes)):
            random_index = random_gen.randint(1, len(parent_tree) - 1)
            random_parent_one_node = parent_tree[random_index]

        if random_parent_one_node.name == "Scope":
            print(random_parent_one_node)

        if isinstance(random_parent_one_node, SubtreeMutable):
            random_parent_one_node.mutate(parent.config)
        elif isinstance(random_parent_one_node, PointMutable):
            random_parent_one_node.mutate(parent.config)

        return parent


class Program(Node):
    def __init__(self, config):
        super().__init__(None, "Program")
        self.config = config
        self.variables = []
        self.generate(config)

    def get_program_variables(self) -> List[Variable]:
        return self.variables

    def get_program_config(self) -> Config:
        return self.config

    def __str__(self) -> str:
        program = ""
        for node in self.children_nodes:
            program += str(node) + "\n"
        return program

    def generate(self, config):
        self.children_nodes.append(Scope(self))

    def add_to_program_variables(self, variable):
        for var in self.variables:
            if var.variable_name == variable.variable_name:
                return
        self.variables.append(variable)


def main():
    population_size = 10
    test_file = "GpSolver/TestCases/test2.txt"

    args_length = len(sys.argv)
    if args_length == 2:
        test_file = sys.argv[1]
    elif args_length == 3:
        try:
            population_size = int(sys.argv[2])
        except ValueError:
            print("Argument", sys.argv[2], "must be an integer.")
            sys.exit(1)

    generator = ProgramGenerator()
    population = [generator.generate_program(Config()) for _ in range(population_size)]
    generation = 1

    while True:
        tournament = Tournament(test_file, 3)
        random.shuffle(population)
        winners_group_one = tournament.compete(population[:population_size // 2], 3)
        winners_group_two = tournament.compete(population[population_size // 2:], 3)

        population.clear()
        population.extend(winners_group_one)
        population.extend(winners_group_two)
        population_size = len(population)

        print("-----------------------------")
        print("WINNERS")
        print("-----------------------------")
        for program in population:
            print(program)
        print("-----------------------------")
        print("GENERATION:", generation, "BEST SCORE:", tournament.get_best_score(),
              "POPULATION SIZE:", population_size)
        print(population[0])

        if tournament.get_best_score() < 0.1:
            break

        new_programs = []
        for i in range(population_size):
            for j in range(population_size):
                if i != j:
                    new_programs.extend(generator.crossover(population[i], population[j]))

        print("CROSSOVER")
        while len(population) < 10:
            new_programs = [generator.mutate(program) for program in population]
            population.extend(new_programs)

        print("MUTATION")
        population.extend(new_programs)
        population_size = len(population)
        generation += 1

    print(population[0])


if __name__ == "__main__":
    main()
