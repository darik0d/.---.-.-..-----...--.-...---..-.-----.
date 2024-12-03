import itertools
from CommonPrefixCounter import CommonPrefixCounter
from TranspositionCipher import TranspositionCipher
from VigenereSolver import VigenereSolver

string = "YZDCHLBZIANYLLXRZMMPMOVZCHWDCAKVJHAPUUNVHTGPNAEIILWXNUNLZMLGCLIIOLDZUAVNZTMPMLIIOGGRUQZPDOWLGLDZCALADVVXCXWY" \
         "UJRSIADKMKUMNEGLCSNICXVYTPERQZGHILVJASDRHLEIMKGPEUVVZXWSGBWEJZSSFYNIYSVTNUVLOGMLHWKIYHYTYLUOCTSCYAVIVWKHMKEIYA" \
         "DPYYERIHWPHSFEPXWTEPKEEUSZLFKAPRKZXVZNYZRDWFWUAREPGNVGVUXOCVLFHZEMIFXIKSVOGAPVHVXZHGPLVEMNWWEDAERMXLEFDCSZKNXHA" \
         "WIJMLPNVZEVZLFGKVEMDYCBHXWZEARXAXGOKFYZHCICXETAKVSZHWCYYFMJEWOZIEHQMVPUPSROGJPNVWIJTWXXHJIZALZMUVXHDSTYPC" \
         "EMXFNHHEEGELEBBKQZMSZYLBIJNFVMTUPKGJDTVQOIGWHXKROZTFJZBFOXYJAOXXQQDVXDDVPGKKVZTBZHKUKJSACGRVVDCKRUBMJZNDY" \
         "GYVVGLDXCYELCHEPFUASMXAEYUVIIKGEYSCSJLWTAYUOKLFLWOVIZHLSCLGRIOLPQVVVZXWTYBEMEKHYAYUJPXKYICZWPXWRYTEHMMCUUL" \
         "VTNXDZCHUWIHERTLRNDNZYZTKNOMWSELZIGXCRYKEVVTVSCYCDMWWFJNVDZBAZMDIMVBYMHZLAVTCEAUJLYLKXOHFCYWUSZSZZYLELIGRAHL" \
         "ZSJYXXNYZRJGSYPLLEOTJRDZFRMUKZZVNICKWPNKVHDLHCZHVIJMWZIJZYVMRSXLDKZLKSIADRNGVTUNJQIXUPHUCVIXMAPKVWJMYCCPCSZL" \
         "MGOVCAOTDLNHVEIXWQCUKQZKEXWZBIVMAWHHRXZXFLIVVXNXWWAOGEBWGZEAIHPDLZYOERHVHEHUKIYKUPAIVIZXWNNBVZMEVPNLVIYBTVA" \
         "JBWPHUVXITTPURLKVIAOVUEWZHVTTLFSIHCFURIHYWAPYHVIJCJPHAVIBXLPYYVSZGBPQMZMHTDWCKVKCTWEMYXIOFAOIURHZHAPQPUHEKT" \
         "ZLAYVZCWTBLYMOWZONKKSFBWZYYFRMDBYYAVRZEGEYGVEJXFLMYEHJBLLNUMTOMTPMAEHDWCNYLVIOMWCEBKQIWJTNPUINVLLMGVTZTDSHV" \
         "EXFUDOILRHOOELLLZHFOSTUYZRLHRSOZTZLYZBVOKKNQRKIZXBYJLUHAPWPYVSYZHBHIQYSVHNPUPEOZXBLZHQIWXSCIAAKOPKPYMMHOOWTP" \
         "VVDBDKEYUZIJKJLWVVIZWWYECRIIWVDNHVIJXJPYAFDGOWEYKMEQBFPHHYIZTJPNLMLYGNVYLVIZOVOLULRYKLWJHGFIPJPBVWRZNZVYBTSY" \
         "MSGHUXIVEAETIRIZWFZUQVENMWDANXQZWWYYLYOICWALZSLZXDPUVZXDAVPUARMZHWLUUZPFBNTYVXPOGMOCPIVJWVTNRZIUMJDNYYIBEWTJ" \
         "URXYWVNVCVMIXWPXZLHBHLSXYKHVGSOCKVSEGWPDPELOMJSIUJXBXSUNZMPJPLLHTVKOTCXCNERUTVPXHCPRUVRYLDOIGAZUKZICMWYHHVX" \
         "ZLYPFLMEHXWZLUEIIBVEUNRSHGWSLQVEKAWEUAFTGWSUUHZIVKAHYUVVHXJECPDRFXARIBVRHPRPB"


def find_highest_cp(cipher_string):
    """
    fnd the single column transposition resulting with the most amount of common prefixes
    :param cipher_string:
    :return: the key corresponding to the best option for single column transposition  decryption
    """
    """
    store current best
    """
    highest_value = 0
    highest_key = ""

    """
    counter, to regularly provide temporary information
    """
    counter = 0

    """
    key length check range
    """
    min_key_length = 2
    max_key_length = 10

    """
    for each key length, do the following
    """
    for i in range(min_key_length, max_key_length + 1):

        """
        Generate all permutations of the char 'A', 'B', ... to key length i
        """
        s = "".join([chr(65 + j) for j in range(i)])
        perm_iterator = itertools.permutations(s)
        s = ''.join(next(perm_iterator))

        print("size", i)
        print("temp highest", highest_value, highest_key)

        """
        loop till no more permutations exist
        """
        while True:
            """
            decrypt the transposition
            """
            normal = TranspositionCipher.decrypt(s, cipher_string)
            """
            count the amount of common prefixes
            """
            count = CommonPrefixCounter(normal).check_count()

            """
            if the count is a new maximum, store it as highest, and store the key
            """
            if count > highest_value:
                highest_value = count
                highest_key = s

            try:
                s = ''.join(next(perm_iterator))
            except StopIteration:
                break

            counter += 1
            if counter % 10000 == 0:
                print("counting", counter, highest_value, highest_key)

    print("highest", highest_value, highest_key)
    return highest_key


if __name__ == "__main__":
    """
    Solve Transposition Cipher
    UNCOMMENT the line below, to solve the single column transposition (takes SOME TIME TO EXECUTE)
    """
    #best_key = find_highest_cp(string)

    best_key = "ABECGFD"

    out = TranspositionCipher.decrypt(best_key, string)

    """
    Solve Vigenere Cipher
    """
    vs = VigenereSolver(out)
    plaintext, key = vs.crack()
    print(key, plaintext)