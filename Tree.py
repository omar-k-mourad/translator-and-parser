from nltk.tree import Tree

# Tree Class                     to Draw tree which save in text file 
class TreeNode:
    def __init__(self, label=None):
        self.label = label
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __str__(self, level=0):
        tree_str = "  " * level + "|_" + str(self.label) + "\n"
        for child in self.children:
            tree_str += child.__str__(level + 1)
        return tree_str

    def to_nltk_tree(self):             #to Draw tree in runtime using NLTK lib
        if self.children:
            return Tree(self.label, [child.to_nltk_tree() for child in self.children])
        return self.label