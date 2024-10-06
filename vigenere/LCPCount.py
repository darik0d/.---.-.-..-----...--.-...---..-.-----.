
class LCPCount:
    def __init__(self, string):
        self.string = string
        self.suffix_array = self.to_suffix_array(string)

    @staticmethod
    def to_suffix_array(string):
        suffix_array = []

        for index in range(len(string)):
            suffix_array.append(index)

        suffix_array.sort(key=lambda x: string[x:])

        return suffix_array

    def print_suffix_array(self):
        print("---")
        for i in self.suffix_array:
            print(self.string[i:])
        print("---")

    def get_lcp(self):

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

    def check_count(self):
        lcp = self.get_lcp()
        three_frequency = lcp.count(3)
        return three_frequency
