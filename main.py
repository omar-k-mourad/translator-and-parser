import os
from translator import translate_c_to_python
from lexer import tokenize
from lexer import remove_comments
from my_parser import Parser


#Take Current Directory of python file 
current_directory = os.path.dirname(os.path.abspath(__file__))

# Read the C code from a file
input_file =  os.path.join(current_directory, "input.txt")

with open(input_file, 'r') as f:
    code_with_comments = f.read()

# Remove comments
c_program = remove_comments(code_with_comments)


# Tokenize the C code
tokenizer = tokenize(c_program)
translated_content = translate_c_to_python(tokenizer)

print("Translation completed")  #only for debuging

# Create the parser
parser = Parser(tokenizer)
syntax_tree = parser.main_function()

# Print the parse tree
tree = syntax_tree.to_nltk_tree()

output_file = os.path.join(current_directory, "output.txt")
with open(output_file, "w") as f:
    f.write("code without comments")
    f.write("\n__________________________________________________________\n\n\n")
    f.write(str(c_program))
    f.write("\n\nTranslate C code To Python Code")
    f.write("\n__________________________________________________________\n\n")
    f.write(str(translated_content))

tree.draw()
print("Tree Drawn")   #only for debuging

# Save the parse tree to a file