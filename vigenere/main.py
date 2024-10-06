import itertools
import math
from LCPCount import LCPCount
from TranspositionCipher import TranspositionCipher

string = "RIKVBIYBITHUSEVAZMMLTKASRNHPNPZICSWDSVMBIYFQEZUBZPBRGYNTBURMBECZQKBMBPAWIXSOFNUZECNRAZFPHIYBQEO" \
         "CTTIOXKUNOHMRGCNDDXZWIRDVDRZYAYYICPUYDHCKXQIECIEWUICJNNACSAZZZGACZHMRGXFTILFNNTSDAFGYWLNICFISEAMRMORPG" \
         "MJLUSTAAKBFLTIBYXGAVDVXPCTSVVRLJENOWWFINZOWEHOSRMQDGYSDOPVXXGPJNRVILZNAREDUYBTVLIDLMSXKYEYVAKAYBPVTDHMTMGITDZR" \
         "TIOVWQIECEYBNEDPZWKUNDOZRBAHEGQBXURFGMUECNPAIIYURLRIPTFOYBISEOEDZINAISPBTZMNECRIJUFUCMMUUSANMMVICNRHQJMNHPNC" \
         "EPUSQDMIVYTSZTRGXSPZUVWNORGQJMYNLILUKCPHDBYLNELPHVKYAYYBYXLERMMPBMHHCQKBMHDKMTDMSSJEVWOPNGCJMYRPYQELCDP" \
         "OPVPBIEZALKZWTOPRYFARATPBHGLWWMXNHPHXVKBAANAVMNLPHMEMMSZHMTXHTFMQVLILOVVULNIWGVFUCGRZZKAUNADVYXUDDJVKAYUYO" \
         "WLVBEOZFGTHHSPJNKAYICWITDARZPVU"

shifted = TranspositionCipher.encrypt("WISKUNDE", string)

# after change count
LCPCount(shifted).check_count()

normal = TranspositionCipher.decrypt("WISKUNDE", shifted)
LCPCount(normal).check_count()


highest_value = 0
highest_key = ""

counter = 0

min_key_length = 2
max_key_length = 8

for i in range(min_key_length, max_key_length+1):
    s = "".join([chr(65+j) for j in range(i)])
    perm_iterator = itertools.permutations(s)
    s = ''.join(next(perm_iterator))

    print("size", i)
    print("temp highest", highest_value, highest_key)

    while True:

        normal = TranspositionCipher.decrypt(s, shifted)
        count = LCPCount(normal).check_count()

        if count > highest_value:
            highest_value = count
            highest_key = s

        try:
            s = ''.join(next(perm_iterator))
        except StopIteration:
            break

        counter += 1
        if counter % 10000 == 0:
            print("counting", counter)


print("highest", highest_value, highest_key)