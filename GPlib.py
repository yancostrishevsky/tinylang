import random
import string

grammar = {
    'compilationUnit': [['statement+']],
    'type': [['Int'], ['Char'], ['Bool'], ['Float'], ['String']],
    'incrementStatement': [['Identifier', 'Increment', 'Semicolon']],
    'decrementStatement': [['Identifier', 'Decrement', 'Semicolon']],
    'declarationStatement': [['type', 'Identifier', 'Equals', 'primaryExpression', 'Semicolon']],
    'statement': [['declarationStatement'], ['assignmentStatement'], ['ifStatement'], ['whileStatement'], ['expressionStatement'], ['incrementStatement'], ['decrementStatement'], ['printStatement']],
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
    'mathExpression': [['unaryExpression'], ['unaryExpression', '+', 'unaryExpression'], ['unaryExpression', '-', 'unaryExpression'], ['unaryExpression', '*', 'unaryExpression'], ['unaryExpression', '/', 'unaryExpression']],
    'unaryExpression': [['primaryExpression'], ['+', 'unaryExpression'], ['-', 'unaryExpression']],
    'primaryExpression': [['IntegerLiteral'], ['BoolLiteral'], ['StringLiteral'], ['Identifier'], ['LeftParen', 'expression', 'RightParen']],
    'printExpression': [['StringLiteral'], ['Identifier'], ['printExpression', 'Plus', 'StringLiteral'], ['printExpression', 'Plus', 'Identifier']],
    'readExpression': [['LeftParen', 'RightParen']]
}

terminals = {
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
    'Increment': '++',
    'Decrement': '--',
    'Semicolon': ';',
    'Comma': ',',
    'LeftParen': '(',
    'RightParen': ')',
    'LeftCurly': '{',
    'RightCurly': '}',
    '': ''
}

def generate_program(rule):
    production = random.choice(grammar[rule])
    program = []
    for symbol in production:
        if symbol.endswith('*'):
            for _ in range(random.randint(0, 3)):
                program.extend(generate_program(symbol[:-1]))
        elif symbol.endswith('+'):
            for _ in range(random.randint(1, 3)):
                program.extend(generate_program(symbol[:-1]))
        elif symbol.endswith('?'):
            if random.random() < 0.5:
                program.extend(generate_program(symbol[:-1]))
        elif symbol in grammar:
            program.extend(generate_program(symbol))
        else:
            if symbol == 'Identifier':
                program.append(''.join(random.choices(string.ascii_letters + string.digits, k=5)))
            elif symbol in ['IntegerLiteral', 'BoolLiteral']:
                program.append(str(random.randint(0, 100)))
            elif symbol == 'StringLiteral':
                program.append('"' + ''.join(random.choices(string.ascii_letters + string.digits, k=5)) + '"')
            else:
                program.append(terminals.get(symbol, symbol))
    return program

program = generate_program('compilationUnit')
print(' '.join(program))
