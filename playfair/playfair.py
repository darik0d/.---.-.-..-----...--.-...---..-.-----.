#####################
# The goal of this file is to provide some function to crack the Playfair cipher. Enjoy!
#####################
import random
import re
import string
from abc import abstractmethod
import math
import text_splitter
import string as letter_list
import copy


# Attempt #1: Bruteforce & manually check

class PlayFairBlock:

    def __init__(self):
        self.grid = ["?" for b in range(25)]

    def rand_initialize(self):

        letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i",
                        "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        random.shuffle(letters)
        self.grid = letters
        return self

    def init_from_list(self, new_list: list):
        self.grid = copy.deepcopy(new_list)

    def init_from_string(self, s: str):
        self.grid = list(s)
    def get_char(self, row, col):
        assert row <= 5, row >= 0
        assert col >= 0, col <= 0

        return self.grid[row*5 + col]

    def set_char(self, row, col, new_char):
        assert row <= 5, row >= 0
        assert col >= 0, col <= 0

        self.grid[row*5 + col] = new_char

    def show(self):

        for i in range(5):
            for j in range(5):
                print(self.get_char(i, j), end=" ")
            print()

    def get_position(self, c):

        pos = self.grid.index(c)

        return pos // 5, pos % 5

    def encrypt_bigram(self, bigram: str):
        return self.decrypt_bigram(bigram)
    def decrypt_bigram(self, bigram: str):
        a = bigram[0]
        b = bigram[1]

        assert a != b

        rowa, cola = self.get_position(a)
        rowb, colb = self.get_position(b)

        # Case 1: Normal
        if rowa != rowb and cola != colb:
            return str(self.get_char(rowa, colb) + self.get_char(rowb, cola))
        elif rowa != rowb:
            return str(self.get_char((rowa + 1) % 5, cola) + self.get_char((rowb + 1) % 5, colb))
        elif cola != colb:
            return str(self.get_char(rowa, (cola + 1) % 5) + self.get_char(rowa, (colb + 1) % 5))
        else:
            print("Preprocess the text!")
            raise("PREPROCESS!!!!!!!!!!!")

    def encrypt_string(self, string):
        bigrams = self.split_to_bigrams(string, False)
        to_return = ""
        for bi in bigrams:
            to_return += self.encrypt_bigram(bi)
        return to_return

    def split_to_bigrams(self, string, preprocess=True):
        to_return = string
        if preprocess:
            to_return = self.preprocess_string(to_return)
        return re.findall(r".{1,2}", to_return)

    def preprocess_string(self, string):
        string = string.lower()
        string = re.sub(r"[^a-z]", "", string)
        string = re.sub(r"j", "i", string)
        string = re.sub(r" ", "", string)
        # Add an x if two letters are the same
        i = 0
        while i < len(string) - 1:
            if string[i] == string[i + 1]:
                string = string[:i + 1] + "x" + string[i + 1:]
            i += 2
        # Add an x if the length is odd
        if len(string) % 2 == 1:
            string += "x"
        return string

class Solver:
    def __init__(self, string: str, block: PlayFairBlock):
        self.str = string.lower()
        self.block = copy.deepcopy(block)

    @abstractmethod
    def solve(self):
        pass

class BruteForceSolver(Solver):
    def solve(self):
        bigrams = self.block.split_to_bigrams(self.str, False)
        numb = 0
        # Brute force
        while True:
            self.block.rand_initialize()
            decrypted = ""
            for i in bigrams:
                decrypted += self.block.decrypt_bigram(i)
            # Save the decrypted text and the key
            with open("decrypted.txt", "a") as f:
                f.write(decrypted + "\n Key: " + str(self.block.grid) + "\n\n")

            numb += 1
            if numb % 10000 == 0:
                print("Tried", numb, "times")


# Attempt 2: Bruteforce with autocheck

class BruteforceWithAutocheck(Solver):

    def __init__(self, string: str, block: PlayFairBlock, threshold: float, languages: list):
        super().__init__(string, block)
        self.threshold = threshold
        self.languages = languages
    def solve(self):
        bigrams = self.block.split_to_bigrams(self.str, False)
        numb = 0
        # Brute force
        while True:
            self.block.rand_initialize()
            decrypted = ""
            for i in bigrams:
                decrypted += self.block.decrypt_bigram(i)
            # Save the decrypted text and the key
            with open("decrypted.txt", "a") as f:
                f.write(decrypted + "\n Key: " + str(self.block.grid) + "\n\n")

            numb += 1
            if numb % 1000 == 0:
                print("Tried", numb, "times")
            # Check if the decrypted text is in the language


# Attempt 3: Simulated annealing: https://en.wikipedia.org/wiki/Simulated_annealing
class SimulatedAnnealingSolver(Solver):
    def __init__(self, string: str, block: PlayFairBlock, eval_func, number_of_steps=1000, forced_decryption=None):
        super().__init__(string, block)
        self.eval_func = eval_func
        self.steps = number_of_steps
        self._n = 0
        self._start_temperature = 50
        self._cooling_index = 0.5
        self._wasted = 0
        self.forced_decryption = forced_decryption

    def solve(self):
        current_key = copy.deepcopy(self.block.grid)
        best_key = copy.deepcopy(current_key)
        best_score, _ = self.eval_func(self.decrypt_with_key(copy.deepcopy(current_key)))
        current_score = best_score
        current_temp = self._start_temperature

        while current_temp > 0:
            current_temp -= self._cooling_index
            for step in range(self.steps):
                if current_temp == 0:
                    break
                self._n += 1
                if self._n % 10000 == 1:
                    print("Steps made:", self._n - 1)
                neighbor_key = copy.deepcopy(self.generate_neighbor(copy.deepcopy(current_key)))
                self.block.init_from_list(copy.deepcopy(neighbor_key))
                decrypted_text = self.decrypt_with_key(copy.deepcopy(neighbor_key))
                score, _ = self.eval_func(decrypted_text)
                if score >= current_score:
                    current_key = copy.deepcopy(neighbor_key)
                    current_score = score
                    if score > best_score:
                        best_score = score
                        best_key = copy.deepcopy(neighbor_key)
                else:
                    lucky_chance = math.exp((score - current_score)/current_temp)
                    r = random.uniform(0, 1)
                    if lucky_chance > r:
                        current_key = copy.deepcopy(neighbor_key)
                        current_score = score
                        self._wasted += 1
                        if self._wasted % 10000 == 0:
                            print(f"Wasted {self._wasted} times."
                                  f" Step: {step} Temperature: {current_temp} "
                                  f"Randomness: {math.exp((score - current_score)/current_temp)}")
        self.block.init_from_list(copy.deepcopy(best_key))
        print(text_splitter.infer_spaces(self.decrypt_with_key(best_key), "en"))

        return best_key, best_score

    def generate_neighbor(self, key):
        neighbor_key = copy.deepcopy(key)
        # Swap two random elements
        i, j = random.sample(range(25), 2)
        while i == j:
            i, j = random.sample(range(25), 2)
        neighbor_key[i], neighbor_key[j] = neighbor_key[j], neighbor_key[i]

        self._n += 1
        return neighbor_key

    def decrypt_with_key(self, key):
        old_key = copy.deepcopy(self.block.grid)
        self.block.init_from_list(key)
        bigrams = self.block.split_to_bigrams(self.str, False)
        decrypted = "".join(self.block.decrypt_bigram(bigram) for bigram in bigrams)
        self.block.init_from_list(old_key)
        return decrypted

    def setForcedDecryption(self, forced_decryption: dict):
        self.forced_decryption = forced_decryption

    def checkForcedRules(self):
        for forced in self.forced_decryption:
            if self.block.decrypt_bigram(forced) != self.forced_decryption[forced]:
                return False
        return True

    def checkGivenRules(self, forced_decryption):
        for forced in forced_decryption:
            if self.block.decrypt_bigram(forced) != forced_decryption[forced]:
                return False
        return True

import time
if __name__ == "__main__":

    block = PlayFairBlock()
    block.init_from_string("abcdefghiklmnopqrstuvwxyz")
    cipher = "MUHULOSFOLPVMTRUGNODKNKEUGTRFDENSVDVTPSZSLYIUFNANBNSBFKDDVENAORSSKTLUTGOVPGDSUFDFPSZSLPVRXCWSPSAAMIBVTFSPVMVDAUYDKLMEUUFASSRUFOGVBOMMDTUNFFZVTUOTLUFSKUTUIVTASSRAGRUZLOUTLBRGRYVLOSFOLPVDMLOVXLUSAKZKOUFASSRUFNFFOKDRBGNSEKVAFXAUCTATEODFALMHMTSUFVXYVRZNUSYFNOTSULZTEQIVSKERGOUVSBNUIUFSKAXNSZFNDSVVCBRSAADMTRUMVUFNDVENAURSVOTBFLZTEQIVSUFTFMTSLNAEUCMGSUFGRUTBNAVBCMVNYLODGUFTFPVKEOULMNADAVQNDSVNFMLXVAUSLSEAXBRXVGALRGNCWKCXVNDKCFDENRGPSLURODAEQNUKZFNSOMVMSHNYREYASFDRFKDTWRUUFNGLODGMVTPDALHTSRODAVQVKDAFDENDVLMFNTVVDBUFDRBOGTSNGLODGUFDATAVSOTVLDALERZLUPRTOXAAVUFVXYVRZNUSYFNOUSZSLGNMVUTKDUCLZASLMWRAGRUYVYVOLSAVMUMCMRWEMMVDAWIDKTRKSBWRULOBILMVHMLUFSKDAVUDAVPDBDAVQETCTSENDAVFDQZQBYTSPUTGOVPGDTCTRAVGNDAEUVBAUFDRBCBPVAONVUTMRMVCYRKHOPTAVGACTGVAVRGZROHUYDEASTSASRSAOLMWRVXBRFUKDVWNUPCTSUFGRSVETLOWCASRSANAULMWRVXBRKQKDSUKDVWNUVICWNVRNVSGNDAEYDENGNAVXKFTUKDOURZNDTIRUYCTFNVUFTONAVXKFTUKDRGKAFOUTRZVTBGAOKDBNAVWITRHNOLOBRNNGBDOITEAVKNXKCTSENKIQKDEOTQXACVETGAMVXKVSENAUKDVWNUPVCZDBOSDABEGAKZFNAVYCDVUTLRGNDHWILFIGPVUKTAWBVSQCNAWITRHNNDRPKDANENCWKCTOASTULUSYFUCYOGNDAOYCDVUTBNGSGNNFOTBFKDYGUOTLLTUNTUKDTWNSZFDKDVUFSTZVVPDBQCNABVKGNVXAOIGRRGLOUTOGSLASKDVWNUXRVBVATOKDUFTRYKSPUFTFOGSLMVIXETDVWCUBFDYGFTAVUTHNGNUFTFGBROOATUOGSLDKVSRGOUVSBGKERXTFOTADZRBNVZLUFDVANEVSBNSWCWNVDAVQLUFDVARLCYHNSVOLHCVSRZVLNBASLMWRVXBRKQKDSOKDUFTRYKSPUFTFUKVKTRHNKCDAXSGNDANYEFNGNDGASPSATWVSOTAMGDUHFVRBEMGNDAAUNDKCMVMBASTOXAKZKOKDZRSCNVVWUFGNLTTVDLTRSRAOMCUFVXYVRZBNVNKDSOUTZBGRRXTFOTVLLZZFVBANVDMTRUNEVSBUCYEMYVYVNUAOQTUBTRTCSEASTQUFVSDKRHLFAGVSUIRGUOUSVBYKRBDMTRCIFDWCQCIHDAUBTRGBWTRNASKDPVGQMUTDFRNUAOGAOTVYOSSKXAFRHTFOTULUKSQCTNSVUSIGEMUTLRSWSVFRMUSQ".lower()
    eval_func = text_splitter.twonorm_frequency_distance_with_quadrams

    the_bestest_score = -math.inf
    thresh = the_bestest_score
    the_bestest_key = copy.deepcopy(block.grid)
    it = 0 # Iteration counter
    while True:
        block.init_from_list(the_bestest_key)
        if it % 3 == 0 and it != 0:
            # Update the block
            block.init_from_string("abcdefghiklmnopqrstuvwxyz")
        print("Current key:", block.grid)
        solver = SimulatedAnnealingSolver(cipher, block, eval_func, 500)
        best_key, best_score = solver.solve()
        if best_score > the_bestest_score or best_score > thresh:
            the_bestest_score = best_score
            the_bestest_key = copy.deepcopy(best_key)
            print("\033[92mNew best score:\033[00m", the_bestest_score)
            with open("decrypted.txt", "a") as f:
                f.write(str(time.time()) + "\n" +
                        "New best score: " + str(the_bestest_score) + "\n" +
                        "Best key found: " + str(best_key) + "\n" +
                        "Split text: " + text_splitter.infer_spaces(solver.decrypt_with_key(best_key), "en") + "\n\n")
        it += 1