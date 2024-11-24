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

    highest_value = 0
    highest_key = ""

    counter = 0

    min_key_length = 2
    max_key_length = 10

    for i in range(min_key_length, max_key_length + 1):
        s = "".join([chr(65 + j) for j in range(i)])
        perm_iterator = itertools.permutations(s)
        s = ''.join(next(perm_iterator))

        print("size", i)
        print("temp highest", highest_value, highest_key)

        while True:

            normal = TranspositionCipher.decrypt(s, cipher_string)
            count = CommonPrefixCounter(normal).check_count()

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
    """

    #best_key = find_highest_cp(string)
    #print(best_key)

    out = TranspositionCipher.decrypt("ABECGFD", string)

    """
    Solve Vigenere Cipher
    """
    vs = VigenereSolver(out)
    plaintext, key = vs.crack()
    print(key, plaintext)