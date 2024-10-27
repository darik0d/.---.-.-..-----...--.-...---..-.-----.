#####################
# The goal of this file is to provide some function to crack the Playfair cipher. Enjoy!
#####################
import random
import re


# Attempt #1: Bruteforce & manually check

class PlayFairBlock:

    def __init__(self):
        self.grid = ["?" for b in range(25)]

    def rand_initialize(self):

        letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i",
                        "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        random.shuffle(letters)
        self.grid = letters

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


# Attempt 2: Bruteforce with autocheck

# Attempt 3: Simulated annealing: https://en.wikipedia.org/wiki/Simulated_annealing

# Attempt 4: Frequency heuristic

# Attempt 5: Play not fair


if __name__ == "__main__":
    block = PlayFairBlock()
    block.init_from_string("palmerstonbcdfghikquvwxyz")
    block.show()
    to_encrypt = ["wi", "sk", "un", "de", "is", "le", "uk"]
    result = ""
    for i in to_encrypt:
        result += block.encrypt_bigram(i)
    print("Result:", result)
    string = "Maar aardrijkskunde bwe"
    print(string)
    bigrams = block.split_to_bigrams(string)
    print("Bigrams:", bigrams)

    the_string = "MUHULOSFOLPVMTRUGNODKNKEUGTRFDENSVDVTPSZSLYIUFNANBNSBFKDDVENAORSSKTLUTGOVPGDSUFDFPSZSLPVRXCWSPSAAMIBVTFSPVMVDAUYDKLMEUUFASSRUFOGVBOMMDTUNFFZVTUOTLUFSKUTUIVTASSRAGRUZLOUTLBRGRYVLOSFOLPVDMLOVXLUSAKZKOUFASSRUFNFFOKDRBGNSEKVAFXAUCTATEODFALMHMTSUFVXYVRZNUSYFNOTSULZTEQIVSKERGOUVSBNUIUFSKAXNSZFNDSVVCBRSAADMTRUMVUFNDVENAURSVOTBFLZTEQIVSUFTFMTSLNAEUCMGSUFGRUTBNAVBCMVNYLODGUFTFPVKEOULMNADAVQNDSVNFMLXVAUSLSEAXBRXVGALRGNCWKCXVNDKCFDENRGPSLURODAEQNUKZFNSOMVMSHNYREYASFDRFKDTWRUUFNGLODGMVTPDALHTSRODAVQVKDAFDENDVLMFNTVVDBUFDRBOGTSNGLODGUFDATAVSOTVLDALERZLUPRTOXAAVUFVXYVRZNUSYFNOUSZSLGNMVUTKDUCLZASLMWRAGRUYVYVOLSAVMUMCMRWEMMVDAWIDKTRKSBWRULOBILMVHMLUFSKDAVUDAVPDBDAVQETCTSENDAVFDQZQBYTSPUTGOVPGDTCTRAVGNDAEUVBAUFDRBCBPVAONVUTMRMVCYRKHOPTAVGACTGVAVRGZROHUYDEASTSASRSAOLMWRVXBRFUKDVWNUPCTSUFGRSVETLOWCASRSANAULMWRVXBRKQKDSUKDVWNUVICWNVRNVSGNDAEYDENGNAVXKFTUKDOURZNDTIRUYCTFNVUFTONAVXKFTUKDRGKAFOUTRZVTBGAOKDBNAVWITRHNOLOBRNNGBDOITEAVKNXKCTSENKIQKDEOTQXACVETGAMVXKVSENAUKDVWNUPVCZDBOSDABEGAKZFNAVYCDVUTLRGNDHWILFIGPVUKTAWBVSQCNAWITRHNNDRPKDANENCWKCTOASTULUSYFUCYOGNDAOYCDVUTBNGSGNNFOTBFKDYGUOTLLTUNTUKDTWNSZFDKDVUFSTZVVPDBQCNABVKGNVXAOIGRRGLOUTOGSLASKDVWNUXRVBVATOKDUFTRYKSPUFTFOGSLMVIXETDVWCUBFDYGFTAVUTHNGNUFTFGBROOATUOGSLDKVSRGOUVSBGKERXTFOTADZRBNVZLUFDVANEVSBNSWCWNVDAVQLUFDVARLCYHNSVOLHCVSRZVLNBASLMWRVXBRKQKDSOKDUFTRYKSPUFTFUKVKTRHNKCDAXSGNDANYEFNGNDGASPSATWVSOTAMGDUHFVRBEMGNDAAUNDKCMVMBASTOXAKZKOKDZRSCNVVWUFGNLTTVDLTRSRAOMCUFVXYVRZBNVNKDSOUTZBGRRXTFOTVLLZZFVBANVDMTRUNEVSBUCYEMYVYVNUAOQTUBTRTCSEASTQUFVSDKRHLFAGVSUIRGUOUSVBYKRBDMTRCIFDWCQCIHDAUBTRGBWTRNASKDPVGQMUTDFRNUAOGAOTVYOSSKXAFRHTFOTULUKSQCTNSVUSIGEMUTLRSWSVFRMUSQ"
    the_string = the_string.lower()
    bigrams = block.split_to_bigrams(the_string, False)
    numb = 0
    # Brute force
    while True:
        block.rand_initialize()
        decrypted = ""
        for i in bigrams:
            decrypted += block.decrypt_bigram(i)
        # Save the decrypted text and the key
        with open("decrypted.txt", "a") as f:
            f.write(decrypted + "\n Key: " + str(block.grid) + "\n\n")

        numb += 1
        if numb % 1000 == 0:
            print("Tried", numb, "times")
