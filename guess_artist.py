#
# Name: 
#
import sys

from hw6_tree import printTree

#
# The following two trees are useful for testing.
#
smallTree = \
    ("Is your favorite artist male?", ("an elephant", None, None), ("a mouse", None, None))
mediumTree = \
    ("Is your favorite artist male?",
        ("Is he from United States?",
            ("Juice WRLD", None, None),
            ("Justin", None, None)),
        ("a mouse", None, None))

def main():
    """DOCSTRING!"""
    # Write the "main" function for 20 Questions here.  Although
    # main() is traditionally placed at the top of a file, it is the
    # last function you will write.

def simplePlay(tree):
    """DOCSTRING!"""
    text, left, right = tree
    if left is None and right is None:
        inp = input("Is your favorite artist {}?".format(text))
        if inp == "yes":
            return True
        else:
            return False
    else:
        inp = input("Is your favorite artist {}?".format(text))
        if inp == "yes":
            simplePlay(left)
        else:
            simplePlay(right)

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
         self.val = val
         self.left = left
         self.right = right

def build_tree(tree):
    if not tree:
        return None
    text, left, right = tree
    root = TreeNode(text, None, None)
    root.left = build_tree(left)
    root.right = build_tree(right)
    return root

def decode_tree(root):
    if not root:
        return None
    tree = (root.val, decode_tree(root.left), decode_tree(root.right))
    return tree

def playLeaf(root):
    """DOCSTRING!"""
    if not root.left and not root.left:
        inp = input("Is it {}?".format(root.val))
        if inp == "yes":
            print('I got it!')
            return
        else:
            correct = input("Drats!  What was it?")
            incorrect = root.val
            inp = input("What's a question that distinguishes between {} and {}?"
                         .format(correct, incorrect))
            root.val = inp
            side = input("And what's the answer for {}?".format(correct))
            if side == "yes":
                root.left = TreeNode(correct, None, None)
                root.right = TreeNode(incorrect, None, None)
            else:
                root.right = TreeNode(correct, None, None)
                root.left = TreeNode(incorrect, None, None)
            return
    else:
        inp = input(root.val)
        if inp == "yes":
            playLeaf(root.left)
        else:
            playLeaf(root.right)

def play(tree):
    """DOCSTRING!"""
    root = build_tree(tree)
    playLeaf(root)
    return decode_tree(root)

def save_helper(tree, f):
    text, left, right = tree
    if left is None and right is None:
        f.write("Leaf\n")
        f.write("{}\n".format(text))
    else:
        f.write("Internal node\n")
        f.write("{}\n".format(text))
        save_helper(left, f)
        save_helper(right, f)

def saveTree(tree, treeFile):
    """ Pre order traversal"""
    f = open(treeFile, "w")
    save_helper(tree, f)
    f.close()



#
# The following two-line "magic sequence" must be the last thing in
# your file.  After you write the main() function, this line it will
# cause the program to automatically play 20 Questions when you run
# it.
#
if __name__ == '__main__':
    print("Guess your favorite artist!")
    prev = mediumTree
    while True:
        tree = play(prev)
        prev = tree
        inp = input("Would you like to play again?")
        if inp == "no":
            is_save = input("Would you like to save this tree for later?")
            if is_save == "yes":
                file = input("Please enter a file name:")
                saveTree(tree, file)
                print("Thank you! The file has been saved.")
            break
    print("Bye!")
    main()
