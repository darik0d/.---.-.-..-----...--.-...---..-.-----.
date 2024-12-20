
class CommonPrefixCounter:
    """
    This tool is a tool to find common prefixes
    It is based on the algorithm of a suffix array to find the longest common prefix,
    but this tool just provides the count of common prefixes of a provided length
    (this is useful for attacks on a vigenere cipher, that has done a single column permutation afterwards)
    """
    def __init__(self, string):
        self.string = string
        self.suffix_array = self.to_suffix_array(string)

    @staticmethod
    def to_suffix_array(string: str) -> list[int]:
        """
        Make a suffix array (sorted array, so that only the common prefix of 2 following entries need to be checked)
        A list (considered to be an array), will be returned, with the indexes of the string in a sorted way,
        to follow the suffix array order. The reason indexes were choses instead of sub strings,
        is to maintain performance and reduce memory usage.
        """
        suffix_array = []

        for index in range(len(string)):
            suffix_array.append(index)

        suffix_array.sort(key=lambda x: string[x:])

        return suffix_array

    def print_suffix_array(self):
        """
        Print tool for the suffix array, no use except debugging
        :return:
        """
        print("---")
        for i in self.suffix_array:
            print(self.string[i:])
        print("---")

    def get_lcp(self):
        """
        for each entry in the suffix array, store a LCP value
        The suffix array is sorted based on prefix characters, so by comparing 2 neighbouring list items,
        it is possible to check the most common prefix repetitions
        """
        lcp = [0]

        for k in range(len(self.suffix_array) - 1):
            i = self.suffix_array[k]
            i2 = self.suffix_array[k + 1]
            sub1 = self.string[i:]
            sub2 = self.string[i2:]

            counter = 0
            for j, c in enumerate(sub1):
                if sub2[j] != c:
                    break
                counter += 1

            lcp.append(counter)
        return lcp

    def check_count(self, length=3):
        """
        return the amount of common prefixes found from the provided length
        """
        lcp = self.get_lcp()
        frequency_count = lcp.count(length)
        return frequency_count
