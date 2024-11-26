"""
In this file you can find the code to bruteforce Enigma. Enjoy!
"""
import string

from EnigmaMachine import EnigmaMachine as EM
from PermutatieMatrix import PermutatieMatrix as PM
from CribGraph import CribGraph


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
                                # # Decode with TM
                                # machine = EM(["AJDKSIRUXBLHWTMCQGZNPYFVOE", "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "BDFHJLCPRTXVZNYEIWGAKMUSQO", "THEQUICKBROWNFXJMPSVLAZYDG", "XANTIPESOKRWUDVBCFGHJLMQYZ"], "YRUHQSLDPXNGOKMIEBFZCWVJAT", [r1, r2, r3], [l1, l2, l3], pm.get_permutations())
                                # decrypted = machine.decrypt(ciphertext)
                                # with open("result_enigma.txt", "a") as file:
                                #     file.write(f"Decrypted: {decrypted}\nRotors: {[r1, r2, r3]},{[l1, l2, l3]}\nPlug: {pm.get_permutations()}\n\n")
                                with open("result_enigma.txt", "a") as file:
                                    file.write(f"Rotors: {[r1, r2, r3]},{[l1, l2, l3]}\nPlug: {pm.get_permutations()}\n\n")
                                    print("found something")
                            i += 1
                            if i % 1000 == 0:
                                print(f"Wasted {i} times")

    print(len(crib))
    # machine = EM(["AJDKSIRUXBLHWTMCQGZNPYFVOE", "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "BDFHJLCPRTXVZNYEIWGAKMUSQO", "THEQUICKBROWNFXJMPSVLAZYDG", "XANTIPESOKRWUDVBCFGHJLMQYZ"], "YRUHQSLDPXNGOKMIEBFZCWVJAT", [1, 0, 4], ["B", "E", "X"], "PBMEDFLHIZKGCNOAQRSWUVTXYJ")
