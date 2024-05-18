from Tree import *
from lexer import *
# Parser Class
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = tokens[0] if tokens else None
        self.token_index = 0

    def match(self, token_type, token_value=None):             #(Error Handling: if the token received in this line is not as expected, it will print both the expected token and the actual token encountered)
        if self.current_token and self.current_token[0] == token_type:
            if token_value and self.current_token[1] != token_value:
                raise ValueError(f"Expected {token_type} {token_value}, but found {self.current_token}")
            print(self.current_token)
            self.token_index += 1
            if self.token_index < len(self.tokens):
                self.current_token = self.tokens[self.token_index]
            else:
                self.current_token = None
        else:
            print(self.current_token)
            raise ValueError(f"Expected {token_type}, but found {self.current_token[0]}")
        
    def __str__(self):
        if self.current_token:
            return f"Current token: {self.current_token}, index: {self.token_index}"
        else:
            return "No more tokens"

    # Context free Grammar
    def main_function(self):
        node = TreeNode('MainFunction')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(INT)
        node.add_child(TreeNode(self.current_token[1])) 
        self.match(KEYWORD,'main')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(LEFT_PAREN)
        node.add_child(TreeNode(self.current_token[1]))
        self.match(RIGHT_PAREN)
        node.add_child(TreeNode(self.current_token[1]))
        self.match(LEFT_BRACE)
        node.add_child(self.declaration_list())
        node.add_child(self.statments())
        node.add_child(TreeNode(self.current_token[1]))
        self.match(RIGHT_BRACE)
        return node
    
    def return_statement(self):
        node = TreeNode('ReturnStatement')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(KEYWORD,'return')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(INTEGER_CONSTANT)
        node.add_child(TreeNode(self.current_token[1]))
        self.match(SEMICOLON)
        return node

    def declaration_list(self):
        node = TreeNode('DeclarationList')
        while self.current_token and self.current_token[0] in (INT, FLOAT, CHAR , DOUBLE):
            node.add_child(self.declaration())
        return node

    def declaration(self):
        node = TreeNode('Declaration')
        node.add_child(self.variable_declaration())
        node.add_child(TreeNode(self.current_token[1]))
        self.match(SEMICOLON)
        return node

    def variable_declaration(self):
        node = TreeNode('VariableDeclaration')
        node.add_child(self.type_specifier())
        node.add_child(self.identifier_list())
        return node

    def type_specifier(self):
        node = TreeNode('TypeSpecifier')
        if self.current_token and self.current_token[0] in (INT, FLOAT, CHAR, DOUBLE):
            node.add_child(TreeNode(self.current_token[1]))
            self.match(self.current_token[0])
        return node

    def identifier_list(self):
        node = TreeNode('IdentifierList')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(IDENTIFIER)
        if self.current_token and self.current_token[0] == COMMA:
            node.add_child(TreeNode(self.current_token[1]))
            self.match(COMMA)
            node.add_child(self.identifier_list())
        elif self.current_token and self.current_token[0] == ASSIGNMENT_OP:
            node.add_child(TreeNode(self.current_token[1]))
            self.match(ASSIGNMENT_OP)
            node.add_child(self.expression())
        return node

    def statment(self):
        node = TreeNode('statment')
        if self.current_token[0] == KEYWORD:
            if self.current_token[1] == 'if':
                node.add_child(self.if_statement())
            elif self.current_token[1] == 'for':
                node.add_child(self.for_statement())
            elif self.current_token[1] == 'printf':
                node.add_child(self.printf_statement())
            elif self.current_token[1] == 'while':
                node.add_child(self.while_statement())
            elif self.current_token[1] == 'do':
                node.add_child(self.do_while_statement())
            elif self.current_token[1] == 'return':
                node.add_child(self.return_statement())
        elif self.current_token[0] in  (INT, FLOAT, CHAR, DOUBLE):
            node.add_child(self.declaration_list())
        elif self.current_token[0] == LEFT_BRACE: 
            node.add_child(TreeNode(self.current_token[1]))
            self.match(LEFT_BRACE)
            node.add_child(self.statments())
            node.add_child(TreeNode(self.current_token[1]))
            self.match(RIGHT_BRACE)
        else:
            node.add_child(self.assignment_statement())
        return node
    
    def statments(self):
        node = TreeNode('statments')
        node.add_child(self.statment())
        if self.current_token and self.current_token[0] == RIGHT_BRACE:
            node.add_child(TreeNode("Empty"))
        else :
            node.add_child(self.statments())
        return node
            

    def if_statement(self):
        node = TreeNode('IfStatement')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(KEYWORD, 'if')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(LEFT_PAREN)
        node.add_child(self.condition())
        node.add_child(TreeNode(self.current_token[1]))
        self.match(RIGHT_PAREN) 
        node.add_child(TreeNode(self.current_token[1]))
        self.match(LEFT_BRACE)
        node.add_child(self.statments())
        node.add_child(TreeNode(self.current_token[1]))
        self.match(RIGHT_BRACE)
        if self.current_token and self.current_token[0] == KEYWORD and self.current_token[1] == 'else':
            node.add_child(TreeNode(self.current_token[1]))
            self.match(KEYWORD, 'else')
            node.add_child(TreeNode(self.current_token[1]))
            self.match(LEFT_BRACE)
            node.add_child(self.statments())
            node.add_child(TreeNode(self.current_token[1]))
            self.match(RIGHT_BRACE)
        return node

    def for_statement(self):
        node = TreeNode('ForStatement')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(KEYWORD, 'for')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(LEFT_PAREN)
        if self.current_token and self.current_token[0] in (INT, FLOAT, CHAR, DOUBLE):
            node.add_child(self.type_specifier())
        node.add_child(self.assignment_statement())
        node.add_child(self.condition())
        node.add_child(TreeNode(self.current_token[1]))
        self.match(SEMICOLON)
        node.add_child(self.step_statement())
        node.add_child(TreeNode(self.current_token[1]))
        self.match(RIGHT_PAREN)
        node.add_child(TreeNode(self.current_token[1]))
        self.match(LEFT_BRACE)
        node.add_child(self.statments())
        node.add_child(TreeNode(self.current_token[1]))
        self.match(RIGHT_BRACE)
        return node
    
    def while_statement(self):
        node = TreeNode('WhileStatement')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(KEYWORD, 'while')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(LEFT_PAREN)
        node.add_child(self.condition())
        node.add_child(TreeNode(self.current_token[1]))
        self.match(RIGHT_PAREN)
        node.add_child(TreeNode(self.current_token[1]))
        self.match(LEFT_BRACE)
        node.add_child(self.statments())
        node.add_child(TreeNode(self.current_token[1]))
        self.match(RIGHT_BRACE)
        return node
    
    def step_statement(self):
        node = TreeNode('StepStatement')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(IDENTIFIER)
        node.add_child(TreeNode(self.current_token[1]))
        if self.current_token and self.current_token[0] == ASSIGNMENT_OP:
            self.match(ASSIGNMENT_OP)
            node.add_child(self.expression())
        elif self.current_token and self.current_token[0] == INCREMENT_OP:
            self.match(INCREMENT_OP)
        elif self.current_token and self.current_token[0] == DECREMENT_OP:
            self.match(DECREMENT_OP)
        return node


    def printf_statement(self):
        node = TreeNode('PrintfStatement')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(KEYWORD, 'printf')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(LEFT_PAREN)
        node.add_child(self.string_literal())
        if self.current_token and self.current_token[0] == COMMA:
            node.add_child(TreeNode(self.current_token[1]))
            self.match(COMMA)
            node.add_child(self.argument_list())
        node.add_child(TreeNode(self.current_token[1]))
        self.match(RIGHT_PAREN)
        node.add_child(TreeNode(self.current_token[1]))
        self.match(SEMICOLON)
        return node

    def string_literal(self):
        node = TreeNode('StringLiteral')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(STRING_CONSTANT)
        return node

    def argument_list(self):
        node = TreeNode('ArgumentList')
        node.add_child(self.expression())
        if self.current_token and self.current_token[0] == COMMA:
            node.add_child(TreeNode(self.current_token[1]))
            self.match(COMMA)
            node.add_child(self.argument_list())
        return node

    def assignment_statement(self):
        node = TreeNode('AssignmentStatement')
        node.add_child(self.identifier())
        node.add_child(TreeNode(self.current_token[1]))
        self.match(ASSIGNMENT_OP)
        node.add_child(self.expression())
        node.add_child(TreeNode(self.current_token[1]))
        self.match(SEMICOLON)
        return node
    
    def condition(self):
        node = TreeNode("Condition")
        node.add_child(self.expression())
        if self.current_token and self.current_token[0] == RELATIONAL_OP:
            node.add_child(TreeNode(self.current_token[1]))
            self.match(self.current_token[0])
        node.add_child(self.expression())

        return node

    def expression(self):
        node = TreeNode('Expression')
        node.add_child(self.term())
        node.add_child(self.rest0())
        return node
    
    def rest0(self):
        node = TreeNode("Rest0")
        if self.current_token and self.current_token[0] == ADDITIVE_OP:
            node.add_child(TreeNode(self.current_token[1]))
            self.match(self.current_token[0])
            node.add_child(self.term())
            node.add_child(self.rest0())
        else:
            node.add_child(TreeNode("Empty"))
        return node
    
    def term(self):
        node = TreeNode('Term')
        node.add_child(self.factor())
        node.add_child(self.rest1())
        return node
    
    def rest1(self):
        node = TreeNode('Rest1')
        if self.current_token and self.current_token[0] == MULTIPLICATIVE_OP:
            node.add_child(TreeNode(self.current_token[1]))
            self.match(self.current_token[0])
            node.add_child(self.factor())
            node.add_child(self.rest1())
        else:
            node.add_child(TreeNode("Empty"))
        return node 

    def factor(self):
        node = TreeNode('Factor')
        if self.current_token and self.current_token[0] == IDENTIFIER:
            node.add_child(self.identifier())
        elif self.current_token and self.current_token[0] == INTEGER_CONSTANT:
            node.add_child(TreeNode(self.current_token[1]))
            self.match(INTEGER_CONSTANT)
        elif self.current_token and self.current_token[0] == FLOAT_CONSTANT:
            node.add_child(TreeNode(self.current_token[1]))
            self.match(FLOAT_CONSTANT)
        elif self.current_token and self.current_token[0] == LEFT_PAREN:
            node.add_child(TreeNode(self.current_token[1]))
            self.match(LEFT_PAREN)
            node.add_child(self.expression())
            node.add_child(TreeNode(self.current_token[1]))
            self.match(RIGHT_PAREN)
        else:
            raise ValueError(f"Invalid factor: {self.current_token}")
        return node
    
    def identifier(self):
        node = TreeNode('Identifier')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(IDENTIFIER)
        return node