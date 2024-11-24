import math


class VigenereSolver:
    def __init__(self, content):
        self.content = content

    def crack(self):
        """
        Crack the vigenere cipher
        :return: Tuple: (plaintext, key)
        """

        best_length = 8

        """
        for each multiple of the key length, store the frequencies of each char
        """
        pos_map = {i: {} for i in range(best_length)}
        for i, c in enumerate(self.content):
            pos = i % best_length

            count = pos_map[pos].get(c, 0)
            pos_map[pos][c] = count+1

        """
        'e' is a very frequent character, so when a encrypted char is occurring frequently,
        it is most likely the 'e'. When discovering the distance from this character to 'E',
        it is possible to see how many cipher shifts are needed for this position
        """
        more_than_e = []
        for i in range(best_length):
            best_key = self._get_most_frequent_char(pos_map[i])
            more_than_e.append(ord(best_key)-ord('E'))

        """
        Apply the shifts on the characters to discover the plaintext
        """
        final_content = ""
        for i, c in enumerate(self.content):
            pos = i % best_length
            more = more_than_e[pos]

            ascii_val = ord(c)-more
            if ascii_val < 65:
                ascii_val += 26

            final_content += chr(ascii_val)

        return final_content, ''.join([chr(ord('A')+i) for i in more_than_e])

    @staticmethod
    def _get_most_frequent_char(mapping: dict[str, int]) -> str:
        """
        Find most frequent character in the mapping

        :param mapping: provided mapping
        :return: key of most frequenct char
        """
        best_key = None
        best_value = -math.inf
        for k, v in mapping.items():
            if v > best_value:
                best_value = v
                best_key = k

        return best_key