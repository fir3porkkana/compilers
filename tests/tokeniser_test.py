from compiler.tokeniser import Location, Token, tokenise

L = Location(0,0, True)

def test_tokeniser_operators() -> None:
    assert tokenise("-") == [Token("operator", "-", L)]
    assert tokenise("=") == [Token("operator", "=", L)]
    assert tokenise("/") == [Token("operator", "/", L)]
    assert tokenise("*") == [Token("operator", "*", L)]
    assert tokenise(">") == [Token("operator", ">", L)]
    assert tokenise("==") == [Token("operator", "==", L)]
    assert tokenise("!=") == [Token("operator", "!=", L)]
    assert tokenise("<=") == [Token("operator", "<=", L)]
    assert tokenise("<==\n") == [Token("operator", "<=", L), Token("operator", "=", L)]

def test_tokeniser_parenthesis() -> None:
    assert tokenise("[") == [Token("parenthesis", "[", L)]
    assert tokenise("}") == [Token("parenthesis", "}", L)]
    assert tokenise("()") == [Token("parenthesis", "(", L), Token("parenthesis", ")", L)]
    assert tokenise("(ad-sdf)") == [Token("parenthesis", "(", L), Token("identifier", "ad", L), Token("operator", "-", L), Token("identifier", "sdf", L), Token("parenthesis", ")", L)]
    assert tokenise("([3-})") == [Token("parenthesis", "(", L), Token("parenthesis", "[", L), Token("int_literal", "3", L), Token("operator", "-", L), Token("parenthesis", "}", L), Token("parenthesis", ")", L)]

def test_tokeniser() -> None:
    assert tokenise("hi") == [Token("identifier", "hi", L)]

    assert tokenise("if  3\nwhile") == [Token("identifier", "if", L), Token("int_literal", "3", L), Token("identifier", "while", L)]

    assert tokenise("rakka #ahdfbadbfka\n makka foon\n") == [Token("identifier", "rakka", L), Token("identifier", "makka", L), Token("identifier", "foon", L)]

    assert tokenise("moi + moi") == [Token("identifier", "moi", L), Token("operator", "+", L), Token("identifier", "moi", L)]

    assert tokenise("moi, moi") == [Token("identifier", "moi", L), Token("punctuation", ",", L), Token("identifier", "moi", L)]

    assert tokenise("moi,; hallo;") == [Token("identifier", "moi", L), Token("punctuation", ",", L), Token("punctuation", ";", L), Token("identifier", "hallo", L), Token("punctuation", ";", L)]

    assert tokenise("2 < 4 - 1") == [Token("int_literal", "2", L), Token("operator", "<", L), Token("int_literal", "4", L), Token("operator", "-", L), Token("int_literal", "1", L)]
