import datetime

from EnigmaMachine import EnigmaMachine


class PermutationNode:
    """
    Node, on the permutation matrix
    """
    def __init__(self):
        """
        initialize a node
        """
        self.propagations = []

        """
        indicate if the node is triggered
        """
        self.assign = False

    def add_propagate(self, node: "PermutationNode"):
        """
        add another node to the propagation list
        """
        self.propagations.append(node)

    def clear(self):
        """
        clear the assignment
        """
        self.assign = False

    def trigger(self):
        """
        trigger the assignment
        """

        """
        skip if assigned
        """
        if self.assign:
            return

        self.assign = True

        """
        assign all connected propagation
        """
        for p in self.propagations:
            p.trigger()

    def is_assigned(self):
        """
        check if the node is assigned
        """
        return self.assign


class PermutatieMatrix:
    """
    Advanced Turing Bombe Permutation Matrix
    """
    _char_range = [65, 91]

    """
    set default Engima settings
    """
    _rotors = ["AJDKSIRUXBLHWTMCQGZNPYFVOE",
               "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
               "BDFHJLCPRTXVZNYEIWGAKMUSQO",
               "THEQUICKBROWNFXJMPSVLAZYDG",
               "XANTIPESOKRWUDVBCFGHJLMQYZ"]
    _reflector = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
    _plug_mapping = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self, rotor_links: list[tuple[str, str, int]], rotor_positions, rotor_rotations):
        """
        :param rotor_links: list of tuples indicating the 2 char that are connected at provided index int. When the
        CRIB has an edge between 'A' and 'B' on index 0: provide ('A', 'B', 0)
        """

        """
        store the current configuration
        """
        self.rotor_positions = rotor_positions
        self.rotor_rotations = rotor_rotations

        range_options = PermutatieMatrix._char_range[1]-PermutatieMatrix._char_range[0]

        """
        set up the matrix
        """
        self.matrix = [[PermutationNode() for j in range(range_options)] for i in range(range_options)]

        """
        make all diagonal connections
        """
        for i in range(range_options):
            for j in range(range_options):
                if i == j:
                    continue

                self.matrix[i][j].add_propagate(self.matrix[j][i])

        """
        for each rotor make a connection between the node before and after going through the Enigma machine,
        In the course referred to the connection between (L1, L3) - (L2, eps(k+l)(L3))
        """
        for r in rotor_links:
            a, b, index = r

            """
            take L1 and L2 from the CRIB
            """
            L1 = ord(a) - PermutatieMatrix._char_range[0]
            L2 = ord(b) - PermutatieMatrix._char_range[0]

            machine = EnigmaMachine(self._rotors,
                                    self._reflector,
                                    self.rotor_positions,
                                    self.rotor_rotations,
                                    self._plug_mapping)

            """
            change the rotor position to the position it would be for this char, given the original configuration
            """
            for i in range(index):
                machine.do_rotors_rotation()

            """
            For each L3, check what its result is after going though the Enigma machine
            """
            for i in range(self._char_range[0], self._char_range[1]):

                link = self.get_transformed_char(chr(i), machine)

                L3 = i - PermutatieMatrix._char_range[0]
                L3_transformed = ord(link) - PermutatieMatrix._char_range[0]

                m1 = self.matrix[L1][L3]
                m2 = self.matrix[L2][L3_transformed]

                """
                add the connections
                """
                m1.add_propagate(m2)
                m2.add_propagate(m1)

    def get_transformed_char(self, char: str, machine: EnigmaMachine):
        """
        :param machine:
        :param char: check following the enigma encryption which character corresponds to the provided char
        :return: corresponing character
        """

        """
        execute the enigma machine
        """
        char_link = machine.encrypt(char, True)

        return char_link

    def trigger(self, a: str) -> bool:
        """
        Trigger a row (corresponding with row a)
        :param: the character having the most edges on the CRIB graph
        :return: returns True if valid configuration of rotors and rotor positions
        """
        L1 = ord(a) - PermutatieMatrix._char_range[0]

        """
        try first option
        """
        i = self._char_range[0]
        L2 = i - PermutatieMatrix._char_range[0]

        self.matrix[L1][L2].trigger()

        """
        if self.get_row_assignments(L1) is 1 -> valid configuration
        """
        if self.get_row_assignments(L1) == 1:
            return True

        """
        if self.get_row_assignments(L1) is 25 -> the valid value would be the only one that is False
        """
        if self.get_row_assignments(L1) != 25:
            return False

        """
        Safety, maybe redundant, check only one False as being Triggered
        """
        new_target = None
        for c in self.matrix[L1]:
            if not c.is_assigned():
                new_target = c
                break

        self.clear_assignments()

        new_target.trigger()

        if self.get_row_assignments(L1) == 1:
            return True

        return False

    def clear_assignments(self) -> None:
        """
        clear the matrix assignments
        """
        for row in self.matrix:
            for c in row:
                c.clear()

    def get_row_assignments(self, row: int):
        """
        get how many nodes on the given row are triggered
        """
        ass_count = 0

        for node in self.matrix[row]:
            if node.is_assigned():
                ass_count += 1

        return ass_count

    def print(self):
        """
        Print the permutation matrix its triggered or not status
        """
        for row in self.matrix:
            for column in row:
                print('T' if column.is_assigned() else 'F', end='|')
            print()

    def get_permutations(self) -> tuple[str, str]:
        """
        Get the plug mapping of the enigma machine used
        """
        out = []

        for i, row in enumerate(self.matrix):
            for j, column in enumerate(row):

                if i > j:
                    continue

                if not column.is_assigned():
                    continue

                out.append((chr(i + ord('A')), chr(j + ord('A'))))

        return out


if __name__ == "__main__":
    """
    below is a test, to verify the PermutatieMatrix
    """
    start = datetime.datetime.now()

    """
    Simulate permutation matrix
    """

    rotors = ["AJDKSIRUXBLHWTMCQGZNPYFVOE",
              "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
              "BDFHJLCPRTXVZNYEIWGAKMUSQO",
              "THEQUICKBROWNFXJMPSVLAZYDG",
              "XANTIPESOKRWUDVBCFGHJLMQYZ"]

    reflector = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
    plug_mapping = "PBMEDFLHIZKGCNOAQRSWUVTXYJ"

    rotor_positions = [1, 0, 4]
    rotor_rotations = ["B", "E", "X"]

    machine = EnigmaMachine(rotors,
                            reflector,
                            rotor_positions,
                            rotor_rotations,
                            plug_mapping)

    original_message = "PASOPVOORSALAMANDERISTHEVERYUSEFULLDEMOCRIBFORTHISASSIGNMENT"

    """
    make encrypted message to test
    """
    cipher = machine.encrypt(original_message)

    """
    assume first 15 char is CRIB
    """
    links_list = []
    for i in range(15):
        links_list.append((original_message[i], cipher[i], i))

    """
    do permutation Matrix run given provided setup
    """
    pm = PermutatieMatrix(links_list, [1, 0, 4], ['B', 'E', 'X'])
    triggered = pm.trigger('A')

    if triggered:
        print("this is the right setup", ['B', 'E', 'X'])

    end = datetime.datetime.now()

    print("exe time", (end - start).total_seconds())

    print(pm.get_permutations())


