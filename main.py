
grammar = {
    'compilationUnit': [['statement+']],
    'type': [['Int'], ['Bool'],  ['String']],
    'declarationStatement': [['type', 'Identifier', 'Equals', 'primaryExpression', 'Semicolon']],
    'statement': [['declarationStatement'], ['assignmentStatement'], ['ifStatement'], ['whileStatement'], ['expressionStatement'], ['printStatement']],
    'assignmentStatement': [['Identifier', 'Equals', 'expression', 'Semicolon'], ['Identifier', 'Equals', 'StringLiteral', 'Semicolon'], ['Identifier', 'Equals', 'IntegerLiteral', 'Semicolon'], ['Identifier', 'Equals', 'BoolLiteral', 'Semicolon'], ['Identifier', 'Equals', 'readStatement', 'Semicolon']],
    'printStatement': [['Print', 'LeftParen', 'printExpression', 'RightParen', 'Semicolon']],
    'readStatement': [['Read', 'readExpression']],
    'ifStatement': [['If', 'LeftParen', 'expression', 'RightParen', 'LeftCurly', 'statement+', 'RightCurly', 'elseStatement?']],
    'elseStatement': [['Else', 'LeftCurly', 'statement+', 'RightCurly']],
    'whileStatement': [['While', 'LeftParen', 'expression', 'RightParen', 'LeftCurly', 'statement+', 'RightCurly']],
    'expressionStatement': [['expression', 'Semicolon']],
    'expression': [['logicalExpression']],
    'logicalExpression': [['comparisonExpression'], ['comparisonExpression', '&&', 'comparisonExpression'], ['comparisonExpression', '||', 'comparisonExpression']],
    'comparisonExpression': [['mathExpression'], ['mathExpression', '<', 'mathExpression'], ['mathExpression', '>', 'mathExpression'], ['mathExpression', '<=', 'mathExpression'], ['mathExpression', '>=', 'mathExpression'], ['mathExpression', '==', 'mathExpression'], ['mathExpression', '!=', 'mathExpression']],


    'primaryExpression': [['IntegerLiteral'], ['LeftParen', 'expression', 'RightParen']],
    'printExpression': [['StringLiteral'], ['Identifier'], ['printExpression', 'Plus', 'StringLiteral'], ['printExpression', 'Plus', 'Identifier']],
    'readExpression': [['Read','LeftParen', 'RightParen']]
}
import random
import string

tokens = {
    'String': 'String',
    'Int': 'int',
    'Bool': 'boolean',
    'If': 'if',
    'Else': 'else',
    'While': 'while',
    'Print': 'print',
    'Read': 'read',
    'Plus': '+',
    'Minus': '-',
    'Multiply': '*',
    'Divide': '/',
    'Equals': '=',
    'GreaterThan': '>',
    'LessThan': '<',
    'DoubleQuote': '"',
    'LessThanOrEqual': '<=',
    'GreaterThanOrEqual': '>=',
    'Equal': '==',
    'NotEqual': '!=',
    'And': '&&',
    'Or': '||',
    'Dot': '.',
    'Semicolon': ';',
    'Comma': ',',
    'LeftParen': '(',
    'RightParen': ')',
    'LeftCurly': '{',
    'RightCurly': '}'
}

def generate_identifier():
    return ''.join(random.choice(string.ascii_letters) for _ in range(5))

def generate_value(symbol):
    if symbol == 'IntegerLiteral':
        return str(random.randint(0, 100))
    elif symbol == 'BoolLiteral':
        return random.choice(['true', 'false'])
    elif symbol == 'StringLiteral':
        return '"' + ''.join(random.choice(string.ascii_letters) for _ in range(5)) + '"'
    elif symbol == 'Identifier':
        return generate_identifier()
    else:
        return tokens.get(symbol, symbol)


def dfs_generate_tree(max_depth, current_symbol, current_depth=0):
    if current_depth >= max_depth or current_symbol not in grammar:
        return generate_value(current_symbol)
    else:
        production_rule = random.choice(grammar[current_symbol])
        tree = []
        for symbol in production_rule:
            if symbol in tokens and symbol not in grammar:
                # Dodaj tylko symbole terminalne do drzewa
                tree.append(generate_value(symbol))
            else:
                subtree = dfs_generate_tree(max_depth, symbol, current_depth + 1)
                if subtree is not None:
                    tree.append(subtree)
        return ' '.join(tree)

def dfs(max_depth, current_symbol, current_depth=0):
    stack = [(current_symbol, current_depth)]
    while stack:
        node, depth = stack.pop()
        if depth < max_depth:
            if node in grammar:
                for production in grammar[node]:
                    for symbol in production:
                        stack.append((symbol, depth + 1))
        else:
            tree = dfs_generate_tree(max_depth - depth, node)
            if tree is not None:
                print(generate_value(tree))



dfs(15,'statement')