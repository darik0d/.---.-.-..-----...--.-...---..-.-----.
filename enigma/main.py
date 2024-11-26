"""
In this file you can find the code to bruteforce Enigma. Enjoy!
"""
import string

from EnigmaMachine import EnigmaMachine as EM
from PermutatieMatrix import PermutatieMatrix as PM
from CribGraph import CribGraph

def _tibo_2_jesse(plug: list[tuple[str]]):
    to_return = string.ascii_uppercase
    for i in plug:
        if i[0] == i[1]: continue
        to_return = to_return.replace(i[0], '!').replace(i[1], i[0]).replace('!', i[1])
    return to_return

if __name__ == "__main__":
    ciphertext = "TUMGMTTJDSEJXVEIJSWULHAFYJEYYMDFXCOVHHUSBMLBGTXUJOTUUTHPTQQYEWVIEHWIKDXGXWPQGWHJNKGJCYLUBYUEWYOKZPGDCRIRNIHNPXCQYRGNKOCYRRJSOLQQJOWXHMGOGWGIIWUEGOQTROTAVWNKWCDVRSMURYIDKJFZXCANLEIBRKGWHHDLHHDBFWFVEGSSJVVDTVQBPACLTPZGXLMJRKZWHNZCVVDDNWSTGLTQGGBRTRTSXSGRKHCQUNIAQNHJKPIETGQMRSLJHFBUQUCCNDKQZLLOCBKOJDGSRXTFVJCOAWXIZSZVVLLFWUJCWKIEBYSTEQMGDMTSDTHDYHHUYTKRYPNOEJTUSNXZTYLTDBOEEXZWPEITOBZNCPJKTZLDFLVXHLZYSWQKIOVPTRUJFGGLCCCYKKVHKMTRKXARQGC"
    crib = "DEOPGAVEVOORENIGMA"
    cribGraph = CribGraph(crib, ciphertext)
    the_best_letter = cribGraph.get_the_most_connected_letter()
    links_list = []
    for i in range(len(crib)):
        links_list.append((crib[i], ciphertext[i], i))
    i = 0
    for r1 in range(5):
        for r2 in range(5):
            for r3 in range(5):
                for l1 in list(string.ascii_uppercase):
                    for l2 in list(string.ascii_uppercase):
                        for l3 in list(string.ascii_uppercase):
                            if r1 in [r2, r3] or r2 == r3:
                                continue
                            pm = PM(links_list, [r1, r2, r3], [l1, l2, l3])
                            if pm.trigger(the_best_letter):
                                # Decode with TM
                                machine = EM(["AJDKSIRUXBLHWTMCQGZNPYFVOE", "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "BDFHJLCPRTXVZNYEIWGAKMUSQO", "THEQUICKBROWNFXJMPSVLAZYDG", "XANTIPESOKRWUDVBCFGHJLMQYZ"], "YRUHQSLDPXNGOKMIEBFZCWVJAT", [r1, r2, r3], [l1, l2, l3], _tibo_2_jesse(pm.get_permutations()))
                                decrypted = machine.decrypt(ciphertext)
                                with open("result_enigma.txt", "a") as file:
                                    file.write(f"Decrypted: {decrypted}\nRotors: {[r1, r2, r3]},{[l1, l2, l3]}\nPlug: {pm.get_permutations()}\nAnother notation: {_tibo_2_jesse(pm.get_permutations())}\n\n")
                                    print("found something")
                                    print(f"Decrypted: {decrypted}\nRotors: {[r1, r2, r3]},{[l1, l2, l3]}\nPlug: {pm.get_permutations()}\nAnother notation: {_tibo_2_jesse(pm.get_permutations())}\n\n")
                                    file.close()
                            i += 1
                            if i % 1000 == 0:
                                print(f"Wasted {i} times")

    print(len(crib))
    # The plug from the algo above
    plug = [('A', 'K'), ('D', 'X'), ('E', 'E'), ('F', 'U'), ('G', 'G'), ('H', 'N'), ('I', 'S'), ('J', 'W'), ('M', 'M'), ('O', 'O'), ('P', 'P'), ('R', 'R'), ('T', 'T'), ('V', 'V')]
    plug = _tibo_2_jesse(plug)
    machine = EM(["AJDKSIRUXBLHWTMCQGZNPYFVOE", "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "BDFHJLCPRTXVZNYEIWGAKMUSQO", "THEQUICKBROWNFXJMPSVLAZYDG", "XANTIPESOKRWUDVBCFGHJLMQYZ"], "YRUHQSLDPXNGOKMIEBFZCWVJAT", [1, 3, 4],['E', 'F', 'I'], plug)
    decrypted = machine.decrypt(ciphertext)
    print(decrypted)
    file = open("decrypted_enigma.txt", "w")
    file.write(decrypted)

