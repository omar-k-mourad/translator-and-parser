import re

# Token types
INCLUDE = 'INCLUDE' #
STRING_CONSTANT = 'STRING_CONSTANT' #
INT = 'INT'
FLOAT = 'FLOAT'
CHAR = 'CHAR'
DOUBLE = 'DOUBLE' 
IDENTIFIER = 'IDENTIFIER'
INTEGER_CONSTANT = 'INTEGER_CONSTANT' #
FLOAT_CONSTANT = 'FLOAT_CONSTANT' #
SPECIAL_CHARACTER = 'SPECIAL_CHARACTER' #
RELATIONAL_OP = 'RELATIONAL_OP'
ADDITIVE_OP = 'ADDITIVE_OP'
MULTIPLICATIVE_OP = 'MULTIPLICATIVE_OP'
INCREMENT_OP = 'INCREMENT_OP'
DECREMENT_OP = 'DECREMENT_OP'
ASSIGNMENT_OP = 'ASSIGNMENT_OP'
LEFT_PAREN = 'LEFT_PAREN'
RIGHT_PAREN = 'RIGHT_PAREN'
LEFT_BRACE = 'LEFT_BRACE'
RIGHT_BRACE = 'RIGHT_BRACE'
LEFT_BRACKET = 'LEFT_BRACKET'
RIGHT_BRACKET = 'RIGHT_BRACKET'
COMMA = 'COMMA'
SEMICOLON = 'SEMICOLON'
NEWLINE = 'NEWLINE'
KEYWORD = 'KEYWORD'

# Token types and their Regular Expression 
token_types = [
    ("INCLUDE", r'#include'),
    ("STRING_CONSTANT", r'"([^"]*)"'),
    ("INT", r'int'),
    ("FLOAT", r'float'),
    ("CHAR", r'char'),
    ("DOUBLE", r'double'),
    ("KEYWORD", r'\b(main|printf|if|else|for|while|do|return)\b'),
    ("IDENTIFIER", r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ("FLOAT_CONSTANT", r'\d*\.\d+([eE][-+]?\d+)?'),
    ("INTEGER_CONSTANT", r'\b\d+\b'),
    ("RELATIONAL_OP", r'(<=|>=|==|!=|<|>|&&|\|\|)'),
    ("SPECIAL_CHARACTER", r'[!@#$%^&:\'"\?\\|\~]'),
    ("INCREMENT_OP", r'\+\+'),
    ("DECREMENT_OP", r'--'),
    ("ADDITIVE_OP", r'[+\-]'),
    ("MULTIPLICATIVE_OP", r'[\*/]'),
    ("ASSIGNMENT_OP", r'='),
    ("LEFT_PAREN", r'\('),
    ("RIGHT_PAREN", r'\)'),
    ("LEFT_BRACE", r'\{'),
    ("RIGHT_BRACE", r'\}'),
    ("LEFT_BRACKET", r'\['),
    ("RIGHT_BRACKET", r'\]'),
    ("COMMA", r','),
    ("SEMICOLON", r';'),
    ("NEWLINE", r'\n')
]

# Function To remove comments before parsing     
def remove_comments(code):
    # Single-line in c //....
    code = re.sub(r'\/\/.*', '', code)

    # Multi-line comment in c /* ... */
    code = re.sub(r'\/\*[\s\S]*?\*\/', '', code)

    return code

# Tokenizer     (Error Handling: if the captured token does not match any specified pattern, Code will print invaled token and the token + remaining code)
def tokenize(code):
    tokens = []
    code = code.strip()
    while code:
        for token_name, pattern in token_types:
            matchi = re.match(pattern, code)
            if matchi:
                token_value = matchi.group(0)
                tokens.append((token_name, token_value))
                code = code[len(token_value):].strip()
                break
        else:
            raise ValueError('Invalid token: ' + code)
    return tokens