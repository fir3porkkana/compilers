from compiler.tokeniser import Location, Token
import compiler.ast as  ast

def parse(tokens: list[Token]) -> ast.Expression:
    position = 0

    def peek() -> Token:
        if len(tokens) == 0:
            return Token("end", "end", Location(0, 0, True))            
        elif position < len(tokens):
            return tokens[position]
        else:
            return Token(
                "end",
                "",
                tokens[-1].location
            )
        
    def consume(expected: str | list[str] | None = None) -> Token:
        # print(f"consume invoked")
        nonlocal position
        token = peek()
        if isinstance(expected, str) and token.text != expected:
            raise Exception(f"@{token.location}: expected token text to be '{expected}'")
        if isinstance(expected, list) and token.text not in expected:
            list_as_string = ", ".join(f"'{value}'" for value in expected)
            raise Exception(f"@{token.location}: expected token text to be one of '{list_as_string}'")
        position += 1
        return token
    
    def parse_int_literal() -> ast.Literal:
        if peek().type != "int_literal":
            raise Exception(f"@{peek().location}: expected an integer literal, got '{peek().type}' instead")
        token = consume()
        return ast.Literal(int(token.text))
    
    def parse_identifier() -> ast.Identifier:
        if peek().type != "identifier":
            raise Exception(f"@{peek().location}: expected an identifier, got '{peek().type}' instead")
        token = consume()
        return ast.Identifier(token.text)
    
    def parse_operator() -> ast.Operator:
        # print(f"parse_operator invoked")

        if peek().type != "operator":
            raise Exception(f"@{peek().location}: expected an identifier, got '{peek().type}' instead")
        token = consume()
        # print(f"token text: {token.text}")
        return ast.Operator(token.text)
    
    def parse_parenthesised() -> ast.Expression:
        consume("(")
        expression = parse_expression()
        consume(")")

        return expression
    
    def parse_if_expression() -> ast.Expression:
        consume("if")
        condition = parse_expression()
        consume("then")
        then_clause = parse_expression()
        if peek().text == "else":
            consume("else")
            else_clause = parse_expression()
        else:
            else_clause = None
        
        return ast.IfExpression(condition, then_clause, else_clause)
    
    def parse_factor() -> ast.Expression:
        if peek().type == "end":
            return ast.Literal(None)
        elif peek().text == "(":
            return parse_parenthesised()
        elif peek().text == "if":
            return parse_if_expression()
        elif peek().type == "int_literal":
            return parse_int_literal()
        elif peek().type == "identifier":
            return parse_identifier()
        elif peek().type == "operator":
            return parse_operator()
        else:
            raise Exception(f"@{peek().location}: expected token text to be either an integer literal or an identifier, got '{peek()}'")
        
    # an identifier or an integer literal
    # is called a "term"
    def parse_term() -> ast.Expression:
        expression = parse_factor()

        while peek().text in ["*", "/"]:
            operator = parse_factor()

            right_expression = parse_factor()

            expression = ast.BinaryOperation(
                expression,
                operator,
                right_expression
            )
        return expression
        
    def parse_polynomial() -> ast.Expression:
        expression = parse_term()
        
        while peek().text in ["-", "+"]:
            operator = parse_term()

            right_expression = parse_term()

            expression = ast.BinaryOperation(
                expression,
                operator,
                right_expression
            )
        return expression
    
    def parse_expression() -> ast.Expression:
        expression = parse_polynomial()

        while peek().text in ["<"]:
            operator = parse_term()

            right_expression = parse_polynomial()

            expression = ast.BinaryOperation(
                expression,
                operator,
                right_expression
            )
        return expression
                
    # We now have a pretty good parser for simple math expressions! => Clean up some details that we’ve glossed over:

    return parse_expression()