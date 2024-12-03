import math


class TranspositionCipher:
    @staticmethod
    def encrypt(key, text):
        """
        encrypt a message using Single Column Transposition

        :param key: encryption key
        :param text: data to be encrypted
        :return: ciphertext
        """

        """
        init a matrix
        """
        data_matrix = []
        for i in range(len(key)):
            data_matrix.append([])

        """
        fill the matrix, line by line
        """
        for i, c in enumerate(text):
            data_matrix[i % len(key)].append(c)

        """
        provide the original index of the column, to each column
        """
        for i in range(len(key)):
            data_matrix[i] = (i, data_matrix[i])

        """
        Sort by the character of the key, corresponding to the original column index position (meaning that the 
        ith column will be put on the sorted position of char i from the key)
        """
        data_matrix.sort(key=lambda x: key[x[0]])

        """
        remove the column indexing
        """
        for i in range(len(key)):
            data_matrix[i] = data_matrix[i][1]

        """
        merge column by column, to the new output cipher text
        """
        out = ""
        for d in data_matrix:
            out += ''.join(d)
        return out

    @staticmethod
    def decrypt(key, text):
        """
        decrypt a message using Single Column Transposition

        :param key: encryption key
        :param text: data to be decrypted
        :return: text
        """
        data_matrix = []

        max_size = math.ceil(len(text) / len(key))

        """
        sometimes, when the length of the text is not dividable by the key length, some columns are not the same length.
        This gapped_amount, keeps into account this lack of length. It stores the amount of rows, that need an 
        additional length more than the normal column length
        """
        gapped_amount = len(key) - (max_size * len(key) - len(text))

        """
        gap_indexes store how based on the key, the encryption would have sorted these columns
        """
        gap_indexes = [(key[i], i) for i in range(len(key))]
        gap_indexes.sort(key=lambda x: x[0])
        gap_indexes = [i[1] for i in gap_indexes]

        """
        init matrix
        """
        for i in range(len(key)):
            data_matrix.append([])

        text_index = 0
        column_size = math.floor(len(text) / len(key))

        """
        store the values to there corresponding columns
        """
        for i in range(len(key)):
            length = column_size

            """
            if originally this, column would have an additional value, it will add this to the length
            """
            if gap_indexes[i] < gapped_amount and not gapped_amount == len(key):
                length += 1

            for j in range(length):
                """
                stores the text in the columns
                """
                data_matrix[i].append(text[text_index])
                text_index += 1

        """
        reverse rotate the columns
        """
        new_data_matrix = [[] for i in range(len(key))]
        for i in range(len(data_matrix)):
            new_index = gap_indexes.index(i)

            new_data_matrix[i] = data_matrix[new_index]

        """
        read row by row, the output plaintext
        """
        out = ""
        for i, c in enumerate(text):
            sub_ar = new_data_matrix[i % len(key)]
            # print(i % len(key), len(sub_ar))
            i2 = math.floor(i / len(key))
            out += sub_ar[i2]

        return out
