from numpy import log10 as log
import ast
import operator as op
from ast import NodeVisitor

operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
             ast.Div: op.truediv, ast.Pow: op.pow, ast.BitXor: op.xor,
             ast.USub: op.neg}


class ExpressionParser(NodeVisitor):
    def __init__(self, **kwargs):
        self.variables = kwargs
        self.variables['log'] = log

    def visit_Name(self, node):
        if node.id in self.variables:
            return self.variables[node.id]
        else:
            return None

    def visit_Num(self, node):
        return node.n

    def visit_NameConstant(self, node):
        return node.value

    def visit_UnaryOp(self, node):
        val = self.visit(node.operand)
        return operators[type(node.op)](val)

    def visit_BinOp(self, node):
        lhs = self.visit(node.left)
        rhs = self.visit(node.right)
        return operators[type(node.op)](lhs, rhs)

    def visit_Call(self, node):
        if node.func.id in self.variables:
            function = self.visit(node.func)
            return function(self.visit(node.args[0]))
        else:
            raise ValueError("String not recognized")

    def generic_visit(self, node):
        raise ValueError("String not recognized")


def expressionEvaluator(expression, **kwargs):
    node = ast.parse(expression, mode='eval')
    parser = ExpressionParser(**kwargs)
    return parser.visit(node.body)
