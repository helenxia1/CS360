# you can add imports but you should not rely on libraries that are not already provided in "requirements.txt #
from collections import deque
import numpy as np

class TextbookStack(object):
    """ A class that tracks the """
    def __init__(self, initial_order, initial_orientations):
        assert len(initial_order) == len(initial_orientations)
        self.num_books = len(initial_order)
        
        for i, a in enumerate(initial_orientations):
            assert i in initial_order
            assert a == 1 or a == 0

        self.order = np.array(initial_order)
        self.orientations = np.array(initial_orientations)

    def flip_stack(self, position):
        assert position <= self.num_books
        
        self.order[:position] = self.order[:position][::-1]
        self.orientations[:position] = np.abs(self.orientations[:position] - 1)[::-1]

    def check_ordered(self):
        for idx, front_matter in enumerate(self.orientations):
            if (idx != self.order[idx]) or (front_matter != 1):
                return False

        return True

    def copy(self):
        return TextbookStack(self.order, self.orientations)
    
    def __eq__(self, other):
        assert isinstance(other, TextbookStack), "equality comparison can only ba made with other __TextbookStacks__"
        return all(self.order == other.order) and all(self.orientations == other.orientations)

    def __str__(self):
        return f"TextbookStack:\n\torder: {self.order}\n\torientations:{self.orientations}"


def apply_sequence(stack, sequence):
    new_stack = stack.copy()
    for flip in sequence:
        new_stack.flip_stack(flip)
    return new_stack

def breadth_first_search(stack):
    flip_sequence = []

    # --- v ADD YOUR CODE HERE v --- #

    if stack.check_ordered():
        return flip_sequence
    
    visited = set()
    curr_stack = stack.copy()
    queue = deque([(curr_stack, flip_sequence)])
    
    while queue:
        curr_stack, curr_flip = queue.popleft() #remove the first thing in queue everytime
        state_tuple = (tuple(curr_stack.order),tuple(curr_stack.orientations))
        if state_tuple in visited:
            continue
        visited.add(state_tuple)

        n = curr_stack.num_books

        for i in range (1, n+1):
            new_stack = curr_stack.copy()
            new_stack.flip_stack(i)
            new_flip = curr_flip + [i]

            if new_stack.check_ordered(): # if list is ordered and flipped to 1 now
                return new_flip
            
            new_tuple = (tuple(new_stack.order),tuple(new_stack.orientations))

            if new_tuple not in visited:
                queue.append((new_stack, new_flip)) #not visited so add to queue

    return flip_sequence
    # ---------------------------- #


def depth_first_search(stack):
    flip_sequence = []

    # --- v ADD YOUR CODE HERE v --- #
    if stack.check_ordered():
        return flip_sequence
    
    visited = set()
    curr_stack = stack.copy()
    queue = [(stack.copy(), flip_sequence)]
    
    while queue: 
        curr_stack, flip_sequence = queue.pop()

        state_tuple = (tuple(curr_stack.order), tuple(curr_stack.orientations))
        if state_tuple in visited:
            continue
        visited.add(state_tuple)

        if curr_stack.check_ordered():
            return flip_sequence

        n = curr_stack.num_books
        for i in range(1, n+1):
            next = curr_stack.copy()
            next.flip_stack(i)
            next_sqc = flip_sequence + [i]
            queue.append((next,next_sqc))


    return flip_sequence
    # ---------------------------- #