#####################
# The goal of this file is to provide some function to crack the Playfair cipher. Enjoy!
#####################
import random
import re
from abc import abstractmethod
import math
import text_splitter


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
        self.grid = new_list

    def init_from_string(self, string: str):
        self.grid = list(string)
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
        preprocessed = self.preprocess_string(string)
        bigrams = self.split_to_bigrams(string, False)

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
        self.block = block

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
            if numb % 1000 == 0:
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
    def __init__(self, string: str, block: PlayFairBlock, eval_func, initial_temp=100.0, cooling_rate=0.99,
                 min_temp=0.1, forced_decryption=None):
        super().__init__(string, block)
        self.eval_func = eval_func
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.min_temp = min_temp
        self._n = 0
        self._wasted = 0
        self.forced_decryption = forced_decryption

    def solve(self):
        current_key = self.block.grid.copy()
        best_key = current_key
        current_temp = self.initial_temp
        best_score, _ = self.eval_func(self.decrypt_with_key(current_key))

        while current_temp > self.min_temp:
            neighbor_key = self.generate_neighbor(current_key)
            if self.forced_decryption is not None and not self.checkGivenRules({"uf": "th", "kd": "he", "da": "in"}):
                self.block.init_from_list(neighbor_key)
                if not self.checkForcedRules():
                    self._wasted += 1
                    if self._wasted % 100000 == 0:
                        print("Wasted", self._wasted, "times")
                    # self.block.rand_initialize()
                    continue
                elif not self.checkGivenRules({"da": "in"}):
                    # Generate a new key
                    current_key = neighbor_key
                    self._wasted += 1
                    if self._wasted % 100000 == 0:
                        print("Wasted", self._wasted, "times")
                    continue
                elif self._wasted == 0:
                    break
                else:
                    self._wasted = 0
                    print("Found a valid key:", neighbor_key)
                    break
            self.block.init_from_list(neighbor_key)
            decrypted_text = self.decrypt_with_key(neighbor_key)
            score, _ = self.eval_func(decrypted_text) # TODO: change returns in the main code
            if current_temp < 0.1:
                break
            try:
                if eval_func.__name__ in ["score_text", "twonorm_frequency_distance"]:
                    if score < best_score:
                        current_key = neighbor_key
                        if score < best_score:
                            best_score = score
                            best_key = neighbor_key
                            # print("##############################################")
                            # print("New best score:", best_score)
                            # print("New best key:", best_key)
                            # print("Decrypted text:", decrypted_text)
                            # print("##############################################")
                            # # Write the result to file:
                            # with open("decrypted.txt", "a") as f:
                            #     f.write(decrypted_text + "\n Key: "
                            #             + str(best_key) + "\n Score: " + str(best_score) + "\n\n")
                elif eval_func.__name__ == "index_of_coincidence":
                    if score > best_score or math.exp((score - best_score) / (current_temp)) > random.random():
                        current_key = neighbor_key
                        if score > best_score:
                            best_score = score
                            best_key = neighbor_key
                            # print("##############################################")
                            # print("New best score:", best_score)
                            # print("New best key:", best_key)
                            # print("Decrypted text:", decrypted_text)
                            # print("##############################################")
                            # # Write the result to file:
                            # with open("decrypted.txt", "a") as f:
                            #     f.write(decrypted_text + "\n Key: "
                            #             + str(best_key) + "\n Score: " + str(best_score) + "\n\n")
                else:
                    print("Eval function not found")
                    return
            except OverflowError:
                print("Overflow error")
                print("Current temp:", current_temp)
                print("Score:", score)
                print("Best score:", best_score)
                # TODO: Resolve the issue?


            current_temp *= (self.cooling_rate + (1 - current_temp / self.initial_temp) * 0.001)
            if self._n % 5000 == 0:
                print(f"Generated {self._n} neighbours", "Best score:", best_score, "Best key:", best_key)

        self.block.init_from_list(best_key)
        # print("Best key found:", best_key)
        # print("Decrypted text:", self.decrypt_with_key(best_key))
        # print("Splitted text:", text_splitter.infer_spaces(self.decrypt_with_key(best_key), _))
        # print("Best score:", best_score)
        # print("Best language:", _)
        # print("Number of iterations:", self._n)

        return best_key, best_score

    def generate_neighbor(self, key):
        neighbor_key = key[:]
        if random.random() < 0.5:
            # Swap two random elements
            i, j = random.sample(range(25), 2)
            neighbor_key[i], neighbor_key[j] = neighbor_key[j], neighbor_key[i]
        else:
            # Rotate a random row or column
            if random.random() < 0.5:  # Rotate row
                row = random.randint(0, 4)
                start = row * 5
                neighbor_key[start:start + 5] = neighbor_key[start + 1:start + 5] + neighbor_key[start:start + 1]
            else:  # Rotate column
                col = random.randint(0, 4)
                col_items = [key[col + 5 * i] for i in range(5)]
                rotated = col_items[1:] + col_items[:1]
                for i in range(5):
                    neighbor_key[col + 5 * i] = rotated[i]
        self._n += 1
        return neighbor_key

    def decrypt_with_key(self, key):
        self.block.init_from_list(key)
        bigrams = self.block.split_to_bigrams(self.str, False)
        decrypted = "".join(self.block.decrypt_bigram(bigram) for bigram in bigrams)
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

# Attempt 4: Frequency heuristic / Index of coincidence

# Attempt 5: Play not fair

import time
if __name__ == "__main__":
    # block = PlayFairBlock()
    # block.init_from_string("palmerstonbcdfghikquvwxyz")
    # block.show()
    # to_encrypt = ["wi", "sk", "un", "de", "is", "le", "uk"]
    # result = ""
    # for i in to_encrypt:
    #     result += block.encrypt_bigram(i)
    # print("Result:", result)
    # string = "Maar aardrijkskunde bwe"
    # print(string)
    # bigrams = block.split_to_bigrams(string)
    # print("Bigrams:", bigrams)
    #
    # the_string = "MUHULOSFOLPVMTRUGNODKNKEUGTRFDENSVDVTPSZSLYIUFNANBNSBFKDDVENAORSSKTLUTGOVPGDSUFDFPSZSLPVRXCWSPSAAMIBVTFSPVMVDAUYDKLMEUUFASSRUFOGVBOMMDTUNFFZVTUOTLUFSKUTUIVTASSRAGRUZLOUTLBRGRYVLOSFOLPVDMLOVXLUSAKZKOUFASSRUFNFFOKDRBGNSEKVAFXAUCTATEODFALMHMTSUFVXYVRZNUSYFNOTSULZTEQIVSKERGOUVSBNUIUFSKAXNSZFNDSVVCBRSAADMTRUMVUFNDVENAURSVOTBFLZTEQIVSUFTFMTSLNAEUCMGSUFGRUTBNAVBCMVNYLODGUFTFPVKEOULMNADAVQNDSVNFMLXVAUSLSEAXBRXVGALRGNCWKCXVNDKCFDENRGPSLURODAEQNUKZFNSOMVMSHNYREYASFDRFKDTWRUUFNGLODGMVTPDALHTSRODAVQVKDAFDENDVLMFNTVVDBUFDRBOGTSNGLODGUFDATAVSOTVLDALERZLUPRTOXAAVUFVXYVRZNUSYFNOUSZSLGNMVUTKDUCLZASLMWRAGRUYVYVOLSAVMUMCMRWEMMVDAWIDKTRKSBWRULOBILMVHMLUFSKDAVUDAVPDBDAVQETCTSENDAVFDQZQBYTSPUTGOVPGDTCTRAVGNDAEUVBAUFDRBCBPVAONVUTMRMVCYRKHOPTAVGACTGVAVRGZROHUYDEASTSASRSAOLMWRVXBRFUKDVWNUPCTSUFGRSVETLOWCASRSANAULMWRVXBRKQKDSUKDVWNUVICWNVRNVSGNDAEYDENGNAVXKFTUKDOURZNDTIRUYCTFNVUFTONAVXKFTUKDRGKAFOUTRZVTBGAOKDBNAVWITRHNOLOBRNNGBDOITEAVKNXKCTSENKIQKDEOTQXACVETGAMVXKVSENAUKDVWNUPVCZDBOSDABEGAKZFNAVYCDVUTLRGNDHWILFIGPVUKTAWBVSQCNAWITRHNNDRPKDANENCWKCTOASTULUSYFUCYOGNDAOYCDVUTBNGSGNNFOTBFKDYGUOTLLTUNTUKDTWNSZFDKDVUFSTZVVPDBQCNABVKGNVXAOIGRRGLOUTOGSLASKDVWNUXRVBVATOKDUFTRYKSPUFTFOGSLMVIXETDVWCUBFDYGFTAVUTHNGNUFTFGBROOATUOGSLDKVSRGOUVSBGKERXTFOTADZRBNVZLUFDVANEVSBNSWCWNVDAVQLUFDVARLCYHNSVOLHCVSRZVLNBASLMWRVXBRKQKDSOKDUFTRYKSPUFTFUKVKTRHNKCDAXSGNDANYEFNGNDGASPSATWVSOTAMGDUHFVRBEMGNDAAUNDKCMVMBASTOXAKZKOKDZRSCNVVWUFGNLTTVDLTRSRAOMCUFVXYVRZBNVNKDSOUTZBGRRXTFOTVLLZZFVBANVDMTRUNEVSBUCYEMYVYVNUAOQTUBTRTCSEASTQUFVSDKRHLFAGVSUIRGUOUSVBYKRBDMTRCIFDWCQCIHDAUBTRGBWTRNASKDPVGQMUTDFRNUAOGAOTVYOSSKXAFRHTFOTULUKSQCTNSVUSIGEMUTLRSWSVFRMUSQ"
    # the_string = the_string.lower()
    # bigrams = block.split_to_bigrams(the_string, False)
    # numb = 0
    # # Brute force
    # brute = BruteForceSolver(the_string, block)
    # brute.solve()

    block = PlayFairBlock()
    block.rand_initialize()
    string = "MUHULOSFOLPVMTRUGNODKNKEUGTRFDENSVDVTPSZSLYIUFNANBNSBFKDDVENAORSSKTLUTGOVPGDSUFDFPSZSLPVRXCWSPSAAMIBVTFSPVMVDAUYDKLMEUUFASSRUFOGVBOMMDTUNFFZVTUOTLUFSKUTUIVTASSRAGRUZLOUTLBRGRYVLOSFOLPVDMLOVXLUSAKZKOUFASSRUFNFFOKDRBGNSEKVAFXAUCTATEODFALMHMTSUFVXYVRZNUSYFNOTSULZTEQIVSKERGOUVSBNUIUFSKAXNSZFNDSVVCBRSAADMTRUMVUFNDVENAURSVOTBFLZTEQIVSUFTFMTSLNAEUCMGSUFGRUTBNAVBCMVNYLODGUFTFPVKEOULMNADAVQNDSVNFMLXVAUSLSEAXBRXVGALRGNCWKCXVNDKCFDENRGPSLURODAEQNUKZFNSOMVMSHNYREYASFDRFKDTWRUUFNGLODGMVTPDALHTSRODAVQVKDAFDENDVLMFNTVVDBUFDRBOGTSNGLODGUFDATAVSOTVLDALERZLUPRTOXAAVUFVXYVRZNUSYFNOUSZSLGNMVUTKDUCLZASLMWRAGRUYVYVOLSAVMUMCMRWEMMVDAWIDKTRKSBWRULOBILMVHMLUFSKDAVUDAVPDBDAVQETCTSENDAVFDQZQBYTSPUTGOVPGDTCTRAVGNDAEUVBAUFDRBCBPVAONVUTMRMVCYRKHOPTAVGACTGVAVRGZROHUYDEASTSASRSAOLMWRVXBRFUKDVWNUPCTSUFGRSVETLOWCASRSANAULMWRVXBRKQKDSUKDVWNUVICWNVRNVSGNDAEYDENGNAVXKFTUKDOURZNDTIRUYCTFNVUFTONAVXKFTUKDRGKAFOUTRZVTBGAOKDBNAVWITRHNOLOBRNNGBDOITEAVKNXKCTSENKIQKDEOTQXACVETGAMVXKVSENAUKDVWNUPVCZDBOSDABEGAKZFNAVYCDVUTLRGNDHWILFIGPVUKTAWBVSQCNAWITRHNNDRPKDANENCWKCTOASTULUSYFUCYOGNDAOYCDVUTBNGSGNNFOTBFKDYGUOTLLTUNTUKDTWNSZFDKDVUFSTZVVPDBQCNABVKGNVXAOIGRRGLOUTOGSLASKDVWNUXRVBVATOKDUFTRYKSPUFTFOGSLMVIXETDVWCUBFDYGFTAVUTHNGNUFTFGBROOATUOGSLDKVSRGOUVSBGKERXTFOTADZRBNVZLUFDVANEVSBNSWCWNVDAVQLUFDVARLCYHNSVOLHCVSRZVLNBASLMWRVXBRKQKDSOKDUFTRYKSPUFTFUKVKTRHNKCDAXSGNDANYEFNGNDGASPSATWVSOTAMGDUHFVRBEMGNDAAUNDKCMVMBASTOXAKZKOKDZRSCNVVWUFGNLTTVDLTRSRAOMCUFVXYVRZBNVNKDSOUTZBGRRXTFOTVLLZZFVBANVDMTRUNEVSBUCYEMYVYVNUAOQTUBTRTCSEASTQUFVSDKRHLFAGVSUIRGUOUSVBYKRBDMTRCIFDWCQCIHDAUBTRGBWTRNASKDPVGQMUTDFRNUAOGAOTVYOSSKXAFRHTFOTULUKSQCTNSVUSIGEMUTLRSWSVFRMUSQ".lower()

    eval_func = text_splitter.twonorm_frequency_distance

    the_bestest = 0.07249154913272611
    thresh = 0.065
    while True:
        solver = SimulatedAnnealingSolver(string, block, eval_func, initial_temp=300, cooling_rate=0.999)
        solver.block.init_from_list(['i', 'o', 't', 'u', 'a', 'l', 'p', 'z', 'v', 'm', 'w', 'n', 'f', 'h', 'k', 'c', 'r', 'g', 'x', 'q', 'b', 'y', 's', 'd', 'e'])
        solver.setForcedDecryption({"uf": "th", "kd": "he", "da": "in"})
        # print(solver.checkForcedRules())
        best, best_score = solver.solve()
        if the_bestest is None or best_score < the_bestest or best_score < thresh:
            the_bestest = best_score
            print("New best score:", the_bestest)
            with open("decrypted.txt", "a") as f:
                f.write(str(time.time()) + "\n" +
                        "New best score: " + str(the_bestest) + "\n" +
                        "Best key found: " + str(best) + "\n" +
                        "Splitted text: " + text_splitter.infer_spaces(solver.decrypt_with_key(best), "en") + "\n\n")

        # Update the block
        block = PlayFairBlock().rand_initialize()
    """
    uf => th
    kd => he
    da => in
    """