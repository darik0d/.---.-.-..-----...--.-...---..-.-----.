
class CribNode:
    def __init__(self, letter: str):
        self.letter = letter.capitalize()
        self.connections = {}
    def add_connection(self, to_node, rule_numb: int):
        if not self.connections.get(to_node):
            self.connections[to_node] = {rule_numb}
        elif rule_numb not in self.connections[to_node]:
            self.connections[to_node].append(rule_numb)
class CribGraph:
    def __init__(self, crib: str, ciphertext: str):
        self.crib = crib.upper()
        self.ciphertext = ciphertext.upper()
        self.nodes = {}
        self.make_graph()
    def make_graph(self):
        i = 0
        while i != len(self.crib):
            a = self.ciphertext[i]
            b = self.crib[i]
            A = self.nodes.get(a) if self.nodes.get(a) else CribNode(a)
            B = self.nodes.get(b) if self.nodes.get(b) else CribNode(b)
            A.add_connection(B, i)
            B.add_connection(A, i)
            self.nodes[a] = A
            self.nodes[b] = B
            i += 1
    def get_the_most_connected_letter(self):
        # TODO: check if it is a correct assumption
        return max(self.nodes, key = lambda x: len(self.nodes[x].connections))


if __name__ == "__main__":
    cribgraph = CribGraph("DEOPGAVEVOORENIGMA",
                          "TUMGMTTJDSEJXVEIJSWULHAFYJEYYMDFXCOVHHUSBMLBGTXUJOTUUTHPTQQYEWVIEHWIKDXGXWPQGWHJNKGJCYLUBYUEWYOKZPGDCRIRNIHNPXCQYRGNKOCYRRJSOLQQJOWXHMGOGWGIIWUEGOQTROTAVWNKWCDVRSMURYIDKJFZXCANLEIBRKGWHHDLHHDBFWFVEGSSJVVDTVQBPACLTPZGXLMJRKZWHNZCVVDDNWSTGLTQGGBRTRTSXSGRKHCQUNIAQNHJKPIETGQMRSLJHFBUQUCCNDKQZLLOCBKOJDGSRXTFVJCOAWXIZSZVVLLFWUJCWKIEBYSTEQMGDMTSDTHDYHHUYTKRYPNOEJTUSNXZTYLTDBOEEXZWPEITOBZNCPJKTZLDFLVXHLZYSWQKIOVPTRUJFGGLCCCYKKVHKMTRKXARQGC")
    print(cribgraph.get_the_most_connected_letter())