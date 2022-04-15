import math

LIMIT_INFINITY = 99999999999

opPrecedence = {
    '(': 5, ')': 5,
    "sin": 4, "cos": 4, "tan": 4,
    "ln": 4, "log": 4,
    "sqrt": 4,
    '^': 3,
    '*': 2, '/': 2,
    '+': 1, '-': 1
}

opLambdas = {
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "ln": math.log, "log": math.log10,
    "sqrt": math.sqrt
}

class BinaryTreeNode:
    def __init__(self, value = "", left = None, right = None, transform = lambda x: x):
        self.transform = transform
        self.left = left
        self.right = right
        self.value = value #either an operator or an operand

def infix_to_postfix(infix):
    postFix = []
    opStack = []

    operand = ""
    op = ""

    i = 0
    while i < len(infix):
        c = infix[i]

        if c.isdigit() or c == '.' or c == 'x':
            operand += c
        else:
            op += c

        if op in opPrecedence:
            if operand != "":
                postFix.append(operand)
                operand = ""

            if op == ')':
                while opStack[-1] != '(': postFix.append(opStack.pop())
                opStack.pop()
                i += 1
                op = ""
                continue

            if len(opStack) == 0 or opStack[-1] == '(' or opPrecedence[op] > opPrecedence[opStack[-1]]:
                opStack.append(op)
            elif opPrecedence[op] == opPrecedence[opStack[-1]]:
                postFix.append(opStack.pop())
                opStack.append(op)
            elif opPrecedence[op] < opPrecedence[opStack[-1]] and opStack[-1] != '(':
                postFix.append(opStack.pop())
                i -= 1
            
            op = ""
        i += 1

    if operand != "":
        postFix.append(operand)

    while (len(opStack) > 0):
        postFix.append(opStack.pop())

    return postFix

#converts an algerbraic expression to a binary expression tree
def get_binary_expresion_tree(sf):
    #STEP 1: conversion to postfix notation
    postfix = infix_to_postfix(sf)   

    print(postfix)

    #STEP 2: create binary expresion tree
    stack = []
    for op in postfix:
        if op in opPrecedence:
            if opPrecedence[op] != 4:
                r = stack.pop()
                l = stack.pop()
                stack.append(BinaryTreeNode(op, l, r))
            else:
                stack[-1].transform = opLambdas[op]
        else:
            stack.append(BinaryTreeNode(op))

    return stack[0]

def evaluate_binary_expression_tree(root, value):
    result = 0
    
    if root.value == 'x':
        result = value
    elif root.value == '+':
        result = evaluate_binary_expression_tree(root.left, value) + evaluate_binary_expression_tree(root.right, value)
    elif root.value == '-':
        result = evaluate_binary_expression_tree(root.left, value) - evaluate_binary_expression_tree(root.right, value)
    elif root.value == '*':
        result = evaluate_binary_expression_tree(root.left, value) * evaluate_binary_expression_tree(root.right, value)
    elif root.value == '/':
        l = evaluate_binary_expression_tree(root.left, value)
        r = evaluate_binary_expression_tree(root.right, value)
        if r == 0:
            result = LIMIT_INFINITY
        else:
            result =  l / r
    elif root.value == '^':
        result = math.pow(evaluate_binary_expression_tree(root.left, value), evaluate_binary_expression_tree(root.right, value))
    else:
        result = float(root.value)

    return root.transform(result)
