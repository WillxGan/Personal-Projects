class Node:
    def __init__(self, data):  # makes a node
        self.data = data
        self.left = None  # left nodes are set to none
        self.right = None  # right nodes are set to none


class Tree:
    def __init__(self):  # make the tree start as empty
        self.root = None  # Start with an empty tree
        self.size = 0     # the size of the tree starts at 0

    def clear(self):
        # removes all the nodes and resets the tree
        count = self.size
        self.root = None  # erases all of the nodes
        self.size = 0  # makes the size set to zero
        return count  # this updates the count

    def insert(self, item):
        # if _insert finds an empty position, it inserts a new node with a value
        def _insert(node, item):
            # check if the current node is none, if so, that means we're at the end of the tree
            if node is None:
                return Node(item)  # Found the right spot, so add the node
            elif item < node.data:
                if node.left is None:  # this traverses through the left part of the tree
                    # if it is none, we're at the end of the tree, so we traverse through it
                    node.left = Node(item)  # Insert a node value in the left side at the end
                    return True  # return true to indicate a successful insertion
                else:
                    return _insert(node.left, item)  # if there is a left child, call insert on the left subtree
            elif item > node.data:  # this is talking about the right subtree
                if node.right is None:  # if there is no right child, insert a new node
                    node.right = Node(item)  # create a new node and insert it on the right
                    return True  # return true to indicate it works
                else:
                    return _insert(node.right, item)  # Continue in the right subtree

            return False  # if the values are equal, return false and do nothing

        # Insert the value
        if self.root is None:  # If the tree is empty, add the first node as the root
            self.root = Node(item)
            self.size = 1
            return 1
        else:
            if _insert(self.root, item):  # if an insert takes place, you count +1 for each one added
                self.size += 1
                return 1
            return 0  # if the item already exists, nothing is added

    def remove(self, item):
        # Removes a node with the specified value from the tree.
        def _remove(node, item):
            if node is None:
                # Base case: If the node is None, the value is not in the tree.
                return None, 0

            if item < node.data:
                # If the value to remove is smaller, look in the left subtree.
                node.left, count = _remove(node.left, item)
            elif item > node.data:
                # If the value to remove is larger, look in the right subtree.
                node.right, count = _remove(node.right, item)
            else:
                # Found the node to remove.

                # Case 1: Node is a leaf or has only a right child.
                if node.left is None:
                    # If the node is a leaf, it is deleted by returning (None, 1) to the parent node.
                    return node.right, 1

                if node.right is None:
                    # If node.right is None, it indicates the node has only a left child or is a leaf.
                    return node.left, 1

                # Case 3: Node has two children.
                # Find the in-order predecessor (largest value in the left subtree).
                predecessor = find_max(node.left)

                # Replace the value of the node with the predecessor's value.
                node.data = predecessor.data

                # Recursively remove the predecessor node from the left subtree.
                node.left, _ = _remove(node.left, predecessor.data)

                count = 1  # One node removed.

            return node, count

        def find_max(node):
            # Helper function to find the in-order predecessor (largest node in the left subtree).
            while node.right:
                node = node.right
            return node

        # Call the helper function to remove the node.
        self.root, count = _remove(self.root, item)
        if count > 0:
            self.size -= count  # Update the tree size
        return count

    def __len__(self):  # this checks the size of the tree
        return self.size

    def __contains__(self, item):  # this function checks if the tree contains a desired item
        def _contains(node, item):
            if node is None:
                return False  # Item not found.
            if item == node.data:
                return True  # Item found.
            elif item < node.data:
                return _contains(node.left, item)  # Check left subtree.
            else:
                return _contains(node.right, item)  # Check right subtree.

        return _contains(self.root, item)

    def __str__(self):
        """
        Converts the tree to a string in Tree Notation.
        """
        if self.root is None:  # If the tree is empty
            return "-"  # Explicitly handle the case of an empty tree

        # Special case: Single-node tree
        if self.size == 1:
            return str(self.root.data)  # Return the single node's value directly

        def to_notation(node):
            if node is None:
                return "-"  # Represent missing nodes as '-'

            # Get the notation for the left and right subtrees
            left_str = to_notation(node.left)
            right_str = to_notation(node.right)

            # Leaf node: no parentheses, just the value
            if node.left is None and node.right is None:
                return f"{node.data}"

            # Non-leaf node: include parentheses for children
            return f"({left_str} {node.data} {right_str})"

        return to_notation(self.root)

    def __getitem__(self, index):
        if not isinstance(index, int):  # Make sure the index is an integer
            raise TypeError("Index must be an integer.")

        if index < 0:  # Handle negative indexing
            index += self.size

        if index < 0 or index >= self.size:  # Check if the index is out of range
            raise IndexError("Index out of range.")

        def in_order(node):
            if node is None:
                return []  # Base case: return an empty list for None nodes
            return in_order(node.left) + [node.data] + in_order(node.right)  # In-order traversal

        sorted_items = in_order(self.root)  # Get all the items in sorted order
        return sorted_items[index]
