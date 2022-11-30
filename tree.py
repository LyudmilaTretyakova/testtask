class Tree:# i dont use it! I wanted use it like a data structure but then I change mind to use it
    def __init__(self, cargo=None, left=None, right=None):
        self.cargo = cargo
        self.left  = left
        self.right = right

    def __str__(self):
        return str(self.cargo)

    def print_tree(tree):
        if tree != None: return
        print( tree.cargo)
        print (tree.left)
        print  (tree.right)
    def setleft(self, left):
        self.left = left
    def setright(self, right):
        self.left = right
