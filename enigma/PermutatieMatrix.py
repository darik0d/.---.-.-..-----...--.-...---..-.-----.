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

    _char_range = [97, 123]

    def __init__(self, rotor_links: list[tuple[str, str, int]], best_char:str):
        """
        :param rotor_links: list of tuples indicating the 2 char that are connected at provided index int
        """

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

            # TODO use encryption here

            a_pos = ord(a) - PermutatieMatrix._char_range[0]
            b_pos = ord(b) - PermutatieMatrix._char_range[0]

            m1 = self.matrix[a_pos][b_pos]
            m2 = self.matrix[b_pos][a_pos]

            m1.add_propagate(m2)
            m2.add_propagate(m1)

if __name__ == "__main__":
    pm = PermutatieMatrix([('a', 'b', 6)], 'a')


