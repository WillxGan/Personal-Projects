class Node:
    def __init__(self, char):
        if not isinstance(char, str) or len(char) != 1:
            raise ValueError("Node must contain a single character.")
        self.char = char
        self.next = None
        self.prev = None


class Text:
    def __init__(self, initial_text=None):
        self.head_node = None
        self.tail_node = None
        self.length = 0
        if initial_text:
            self.extend(initial_text)

    def head(self):
        return self.head_node

    def tail(self):
        return self.tail_node

    def __len__(self):
        return self.length

    def __str__(self):
        chars = []
        current = self.head_node
        while current:
            chars.append(current.char)
            current = current.next
        return ''.join(chars)

    def append(self, char):
        if not isinstance(char, str):  # Type check first
            raise TypeError("Only strings are allowed.")
        if len(char) != 1:
            raise ValueError("Node must contain a single character.")
        new_node = Node(char)
        if self.tail_node is None:
            self.head_node = self.tail_node = new_node
        else:
            self.tail_node.next = new_node
            new_node.prev = self.tail_node
            self.tail_node = new_node
        self.length += 1

    def prepend(self, char):
        if not isinstance(char, str):
            raise TypeError("Only strings are allowed.")
        if len(char) != 1:
            raise ValueError("Node must contain a single character.")
        new_node = Node(char)
        if self.head_node is None:
            self.head_node = self.tail_node = new_node
        else:
            new_node.next = self.head_node
            self.head_node.prev = new_node
            self.head_node = new_node
        self.length += 1

    def extend(self, text):
        if not isinstance(text, (str, Text)):
            raise TypeError("extend() requires a string or Text object.")
        if isinstance(text, str):
            for char in text:
                self.append(char)
        elif isinstance(text, Text):
            current = text.head_node
            while current:
                self.append(current.char)
                current = current.next

    def insert(self, index, char):
        if not isinstance(char, str):
            raise TypeError("Only strings are allowed.")
        if len(char) != 1:
            raise ValueError("Node must contain a single character.")

        if not isinstance(index, int):  # Ensure index is an integer
            raise TypeError("Index must be an integer.")

        if index < 0:
            index += self.length

        if index < 0 or index > self.length:
            raise IndexError("Index out of range")

        if index == 0:
            self.prepend(char)
        elif index == self.length:
            self.append(char)
        else:
            new_node = Node(char)
            current = self.head_node
            for _ in range(index):
                current = current.next
            prev_node = current.prev
            prev_node.next = new_node
            new_node.prev = prev_node
            new_node.next = current
            current.prev = new_node
            self.length += 1

    def pop(self, index=None):
        if self.length == 0:
            raise IndexError("Pop from empty text")

        if index is None:
            index = self.length - 1

        if not isinstance(index, int):
            raise TypeError("Index must be an integer.")

        if index < 0:
            index += self.length

        if index < 0 or index >= self.length:
            raise IndexError("Index out of range")

        current = self.head_node
        for _ in range(index):
            current = current.next

        if current.prev:
            current.prev.next = current.next
        else:
            self.head_node = current.next

        if current.next:
            current.next.prev = current.prev
        else:
            self.tail_node = current.prev

        self.length -= 1
        return current.char

    def clear(self):
        self.head_node = None
        self.tail_node = None
        self.length = 0

    def copy(self):
        return Text(str(self))

    def __getitem__(self, index):
        if isinstance(index, int):
            if index < 0:
                index += self.length
            if index < 0 or index >= self.length:
                raise IndexError("Index out of range")

            current = self.head_node
            for _ in range(index):
                current = current.next
            return current.char

        elif isinstance(index, slice):
            start, stop, step = index.indices(self.length)
            result = Text()

            current = self.head_node
            for _ in range(start):
                if current is None:
                    break
                current = current.next

            i = start
            while current and ((step > 0 and i < stop) or (step < 0 and i > stop)):
                result.append(current.char)

                for _ in range(abs(step)):
                    current = current.next if step > 0 else current.prev
                    if current is None:
                        break
                i += step

            return result

        else:
            raise TypeError("Index must be an integer or slice")

    def __setitem__(self, index, char):
        if not isinstance(char, str):
            raise TypeError("Only strings are allowed.")
        if len(char) != 1:
            raise ValueError("Node must contain a single character.")

        if not isinstance(index, int):
            raise TypeError("Index must be an integer.")

        if index < 0:
            index += self.length
        if index < 0 or index >= self.length:
            raise IndexError("Index out of range")

        current = self.head_node
        for _ in range(index):
            current = current.next
        current.char = char

    def __add__(self, other):
        if not isinstance(other, (str, Text)):
            raise TypeError("Can only concatenate str or Text")
        result = self.copy()
        result.extend(other)
        return result

    def __iadd__(self, other):
        self.extend(other)
        return self

    def __contains__(self, substring):
        if not isinstance(substring, str):
            raise TypeError("substring must be a string")
        return substring in str(self)

    def __iter__(self):
        return TextIterator(self.head_node)


class TextIterator:
    def __init__(self, start_node):
        self.current = start_node

    def __iter__(self):
        return self

    def __next__(self):
        if self.current is None:
            raise StopIteration
        char = self.current.char
        self.current = self.current.next
        return char
