from EnigmaMachine import EnigmaMachine


class PermutationNode:
    def __init__(self):
        self.propagations = []
        self.assign = False

    def add_propagate(self, node: "PermutationNode"):
        self.propagations.append(node)

    def clear(self):
        self.assign = False

    def trigger(self):
        if self.assign:
            return

        self.assign = True

        for p in self.propagations:
            p.trigger()

    def is_assigned(self):
        return self.assign


class PermutatieMatrix:

    _char_range = [65, 91]
    _rotors = ["AJDKSIRUXBLHWTMCQGZNPYFVOE",
               "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
               "BDFHJLCPRTXVZNYEIWGAKMUSQO",
               "THEQUICKBROWNFXJMPSVLAZYDG",
               "XANTIPESOKRWUDVBCFGHJLMQYZ"]
    _reflector = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
    _plug_mapping = "PBMEDFLHIZKGCNOAQRSWUVTXYJ"

    def __init__(self, rotor_links: list[tuple[str, str, int]], rotor_positions, rotor_rotations):
        """
        :param rotor_links: list of tuples indicating the 2 char that are connected at provided index int. When the
        CRIB has an edge between 'A' and 'B' on index 0: provide ('A', 'B', 0)
        """

        self.rotor_positions = rotor_positions
        self.rotor_rotations = rotor_rotations

        range_options = PermutatieMatrix._char_range[1]-PermutatieMatrix._char_range[0]

        self.matrix = [[PermutationNode() for j in range(range_options)] for i in range(range_options)]

        """
        make diagonal connections
        """
        for i in range(range_options):
            for j in range(range_options):
                if i == j:
                    continue

                self.matrix[i][j].add_propagate(self.matrix[j][i])

        """
        for each rotor make a connection
        """
        for r in rotor_links:
            a, b, index = r

            L1 = ord(a) - PermutatieMatrix._char_range[0]
            L2 = ord(b) - PermutatieMatrix._char_range[0]

            for i in range(self._char_range[0], self._char_range[1]):
                link = self.get_transformed_char(chr(i), index)

                L3 = i - PermutatieMatrix._char_range[0]
                L3_transformed = ord(link) - PermutatieMatrix._char_range[0]

                m1 = self.matrix[L1][L3]
                m2 = self.matrix[L2][L3_transformed]

                m1.add_propagate(m2)
                m2.add_propagate(m1)

    def get_transformed_char(self, char: str, index: int):
        """

        :param char: check following the enigma encryption which character corresponds to the provided char
        :param index: the index of the message
        :return: corresponing character
        """
        machine = EnigmaMachine(self._rotors,
                                self._reflector,
                                self.rotor_positions,
                                self.rotor_rotations,
                                self._plug_mapping)

        for i in range(index):
            machine.do_rotors_rotation()

        char_link = machine.encrypt(char)
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


if __name__ == "__main__":
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
        print("this is the right setup")


