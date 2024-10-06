import math


class TranspositionCipher:
    @staticmethod
    def encrypt(key, text):
        data_matrix = []
        for i in range(len(key)):
            data_matrix.append([])

        for i, c in enumerate(text):
            data_matrix[i % len(key)].append(c)

        for i in range(len(key)):
            data_matrix[i] = (i, data_matrix[i])

        data_matrix.sort(key=lambda x: key[x[0]])

        for i in range(len(key)):
            data_matrix[i] = data_matrix[i][1]

        out = ""
        counter3 = 0
        for i, c in enumerate(text):
            while True:
                j = i + counter3
                sub_ar = data_matrix[j % len(key)]
                i2 = math.floor(j / len(key))

                if len(sub_ar) > i2:
                    break
                counter3 += 1

            out += sub_ar[i2]

        return out

    @staticmethod
    def decrypt(key, text):
        data_matrix = []

        max_size = math.ceil(len(text) / len(key))

        gapped_amount = len(key) - (max_size * len(key) - len(text))

        gap_indexes = [(key[i], i) for i in range(len(key))]
        gap_indexes.sort(key=lambda x: x[0])
        gap_indexes = [i[1] for i in gap_indexes]

        for i in range(len(key)):
            data_matrix.append([])

        counter3 = 0
        for i, c in enumerate(text):

            while True:
                j = i + counter3
                last_row = max_size == math.ceil((j + 1) / len(key))

                if not last_row or gap_indexes[j % len(key)] < gapped_amount:
                    break

                counter3 += 1

            data_matrix[j % len(key)].append(c)

        new_data_matrix = [[] for i in range(len(key))]
        for i in range(len(data_matrix)):
            new_index = gap_indexes.index(i)

            new_data_matrix[i] = data_matrix[new_index]

        out = ""
        for i, c in enumerate(text):
            sub_ar = new_data_matrix[i % len(key)]
            # print(i % len(key), len(sub_ar))
            i2 = math.floor(i / len(key))
            out += sub_ar[i2]

        return out
