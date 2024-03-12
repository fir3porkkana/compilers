from compiler.tokeniser import Location, tokenise
from compiler.parser import parse
from compiler.ast import Literal, Operator, BinaryOperation, IfExpression

L = Location(0,0, True)

def test_parse_binary_math_expression() -> None:
    assert parse(tokenise("1 + 2")) == BinaryOperation(
        left=Literal(1), 
        operator=Operator("+"), 
        right=Literal(2)
        )
    
def test_parsing_single_token() -> None:
    assert parse(tokenise("1")) == Literal(1)
    
def test_parse_garbage_math_expression() -> None:
    try:
        parse(tokenise("1 + 2 -"))
        assert False, f"expected input '1 + 2 -' to raise an exception but got none"
    except Exception:
        pass

def test_empty_token_list() -> None:
    try:
        parse([])
    except Exception:
        assert False, f"parse() crashed with an empty list as an input ([])"



def test_parse_three_term_math_expression() -> None:
    assert parse(tokenise("1 + 2 - 4")) == BinaryOperation(
        left=BinaryOperation(
            left=Literal(1),
            operator=Operator("+"),
            right=Literal(2)
            ), 
        operator=Operator("-"),
        right=Literal(4)
        )
    
def test_parse_three_term_math_expression_parenthesised() -> None:
    assert parse(tokenise("1 + (2 - 4)")) == BinaryOperation(
        left=Literal(1),
        operator=Operator("+"), 
        right=BinaryOperation(
            left=Literal(2),
            operator=Operator("-"),
            right=Literal(4)
            )
        )
    
def test_parse_three_term_math_expression_with_multiplication() -> None:
    assert parse(tokenise("2 * 4 - 1")) == BinaryOperation(
        left=BinaryOperation(
            left=Literal(2), 
            operator=Operator("*"),
            right=Literal(4)
            ), 
        operator=Operator("-"), 
        right=Literal(1)
        )
    
def test_parse_simple_if_expression_structure() -> None:
    assert parse(tokenise("if - then +")) == IfExpression(
        condition=Operator("-"),
        then_clause=Operator("+"),
        else_clause=None
        )