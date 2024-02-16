
from dataclasses import dataclass
from typing import Literal, Optional
import re

TokenType = Literal["int_literal", "identifier", "operator", "parenthesis", "punctuation", "end"]

@dataclass(frozen = True, eq = False)
class Location:
        line: int
        column: int
        general: Optional[bool] = None

        def __eq__(self, other: object) -> bool:
            if not isinstance(other, Location):
                return NotImplemented
            return (self.general or other.general or (self.line == other.line and self.column == other.column))

@dataclass(frozen = True)
class Token:
    type: TokenType
    text: str
    location: Location

result: list[Token] = []

newline_regex = re.compile(r"\n+")
whitespace_regex = re.compile(r"\s+")
comment_regex = re.compile(r"#.*\n") # think about what to do with comments at the end of the file without a newline at the end?
integer_regex = re.compile(r"[0-9]+")
identifier_regex = re.compile(r"[a-zA-Z0-9_]+")
operator_regex = re.compile(r"(?:>=|==|<=|!=|\+|-|\*|\/|=|<|>)")
parenthesis_regex = re.compile(r"(?:\{|\(|\[|\]|\)|\})")
punctuation_regex = re.compile(r"(?:\,|\;)")
# end_of_file_comment_regex = re.compile(r"#.*") # match this last (?) (do not use this before fixing it)

# [also fix this shit]
# def try_every_regex(regex: re.Pattern, source_string: str, position: int, token_type = None | TokenType) -> re.Match[str] | None:
#     match = regex.match(source_string, position)
#     if (token_type):
#         result.append(result.append(Token(token_type, source_string[position: match.end()])))


def tokenise(source_string: str) -> list[Token]:

    position = 0
    line = 1
    column = 1
    result: list[Token] = []

    while position < len(source_string):
        # print("wat doink")
        # print("¿no print?")
        # print(f"position: {position}")
        # temp = len(source_string)
        # print(f"len(source_string): {temp}")
        
        match = newline_regex.match(source_string, position)
        if match is not None:
            line = line + 1
            column = 1
            position = match.end()
            continue
        
        match = whitespace_regex.match(source_string, position)
        if match is not None:
            column += match.end() - position
            position = match.end()
            continue
    
        match = comment_regex.match(source_string, position)
        if match is not None:
            column += match.end() - position
            position = match.end()
            continue

        match = integer_regex.match(source_string, position)
        if match is not None:
            # print(f"integer: {match}")
            result.append(Token("int_literal", source_string[position:match.end()], Location(line, column)))
            column += match.end() - position
            position = match.end()
            continue

        match = identifier_regex.match(source_string, position)
        if match is not None:
            result.append(Token("identifier", source_string[position:match.end()], Location(line, column)))
            column += match.end() - position
            position = match.end()
            continue

        match = operator_regex.match(source_string, position)
        if match is not None:
            result.append(Token("operator", source_string[position:match.end()], Location(line, column)))
            column += match.end() - position
            position = match.end()
            continue

        match = parenthesis_regex.match(source_string, position)
        if match is not None:
            result.append(Token("parenthesis", source_string[position:match.end()], Location(line, column)))
            column += match.end() - position
            position = match.end()
            continue
        
        match = punctuation_regex.match(source_string, position)
        if match is not None:
            result.append(Token("punctuation", source_string[position:match.end()], Location(line, column)))
            column += match.end() - position
            position = match.end()
            continue

        # match = end_of_file_comment_regex.match(source_string, position)
        # if match is not None:
        #     column += match.end() - position
        #     position = match.end()
        #     continue

        raise Exception(f"tokenisation failed starting at line {line}, column {column}!")

        
    return result
