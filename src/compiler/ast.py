from dataclasses import dataclass
@dataclass
class Expression:
    """Base class for AST nodes, which represent expressions"""

@dataclass
class Literal(Expression):
    value: int | bool | None

@dataclass
class Identifier(Expression):
    name: str

@dataclass
class Operator(Expression):
    value: str

@dataclass
class BinaryOperation(Expression):
    """"Node for a binary operation, such as A + B"""
    left: Expression
    operator: Expression
    right: Expression

@dataclass
class IfExpression(Expression):
    """"Node for an if-expression"""
    condition: Expression
    then_clause: Expression
    else_clause: Expression | None