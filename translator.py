def translate_c_to_python(tokens):
    python_code = []
    indent_level = 0

    def indent():
        return '    ' * indent_level

    i = 0
    while i < len(tokens):
        if len(tokens[i]) != 2:
            i += 1
            continue

        token_type, token_value = tokens[i]

        if token_type == 'INCLUDE':
            # Skip include statements
            i += 2  # Skip include and the string constant
        elif token_type == 'INT' and tokens[i+1][0] == 'KEYWORD' and tokens[i+1][1] == 'main':
            python_code.append(f"{indent()}def main():")
            indent_level += 1
            i += 4  # Skip 'int main() {'
        elif token_type == 'INT':
            # Handle variable declarations
            var_name = tokens[i+1][1]
            if tokens[i+2][0] == 'ASSIGNMENT_OP':
                var_value = tokens[i+3][1]
                python_code.append(f"{indent()}{var_name} = {var_value}")
                i += 5  # Skip 'int var_name = value;'
            else:
                python_code.append(f"{indent()}{var_name} = None")
                i += 3  # Skip 'int var_name;'
        elif token_type == 'KEYWORD' and token_value == 'if':
            condition = []
            i += 2  # Skip 'if ('
            while tokens[i][0] != 'RIGHT_PAREN':
                if tokens[i][1] == '&&':
                    condition.append("and")
                elif tokens[i][1] == '||':
                    condition.append("or")
                else:
                    condition.append(tokens[i][1])
                i += 1
            condition_str = ' '.join(condition)
            python_code.append(f"{indent()}if {condition_str}:")
            indent_level += 1
            i += 2  # Skip ') {'
        elif token_type == 'KEYWORD' and token_value == 'for':
            # Handle for loop
            init_var = tokens[i+3][1]
            init_val = tokens[i+5][1]
            cond_var = tokens[i+8][1]
            cond_op = tokens[i+9][1]
            cond_val = tokens[i+9][1]
            iter_var = tokens[i+12][1]
            if cond_op == '<':
                range_end = cond_val
            else:
                # Handle other relational operators if needed
                range_end = cond_val
                python_code.append(f"{indent()}for {init_var} in range({init_val}, {range_end}):")
                indent_level += 1
                i += 14  # Skip 'for (int var = val; var < val; var++) {'
        elif token_type == 'KEYWORD' and token_value == 'while':
            condition = []
            i += 2  # Skip 'while ('
            while tokens[i][0] != 'RIGHT_PAREN':
                condition.append(tokens[i][1])
                i += 1
            condition_str = ' '.join(condition)
            python_code.append(f"{indent()}while {condition_str}:")
            indent_level += 1
            i += 2  # Skip ') {'
        elif token_type == 'KEYWORD' and token_value == 'printf':
            message = tokens[i+2][1].strip('"')
            if tokens[i+3][0] == 'COMMA':
                var_name = tokens[i+4][1]
                python_code.append(f"{indent()}print(\"{message}\" % {var_name})")
                i += 7  # Skip 'printf("message", var_name);'
            else:
                python_code.append(f"{indent()}print(\"{message}\")")
                i += 5  # Skip 'printf("message");'
        elif token_type == 'IDENTIFIER' and tokens[i+1][0] == 'ASSIGNMENT_OP':
            var_name = token_value
            var_value = tokens[i+2][1]
            python_code.append(f"{indent()}{var_name} = {var_value}")
            i += 4  # Skip 'var_name = value;'
        elif token_type == 'KEYWORD' and token_value == 'return':
            return_value = tokens[i+1][1]
            python_code.append(f"{indent()}return {return_value}")
            i += 3  # Skip 'return value;'
        elif token_type == 'LEFT_BRACE':
            i += 1  # Skip '{'
        elif token_type == 'RIGHT_BRACE':
            indent_level -= 1
            i += 1  # Skip '}'
        else:
            i += 1  # Skip other tokens

    return '\n'.join(python_code)