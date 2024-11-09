from typing import List

class EnigmaMachine:
    def __init__(self, rotor_mappings: List[str], reflector_mapping: str, rotor_positions: List[int], rotor_rotations: List[str], plug_mapping: str):
        """
        Initializes the Enigma machine.
        Every parameter is UPPERCASE.
        Every mapping is a string of 26 characters, where the i-th character represents the mapping of the i-th letter of the alphabet.
        
        :param rotor_mappings: The mappings of the rotors.
        :param reflector_mapping: The mapping of the reflector.
        :param rotor_positions: Which rotor to use in each position. (0-indexed, slowest to fastest)
        :param rotor_rotations: The initial rotation of each rotor.
        :param plug_mapping: The mapping of the plugboard.
        
        """
        
        assert len(rotor_positions) == 3
        assert len(rotor_rotations) == 3
        assert all(len(rotation)==1 for rotation in rotor_rotations)
        assert(all(len(mapping)==26 for mapping in rotor_mappings))
        assert len(reflector_mapping) == 26
        assert len(plug_mapping) == 26
        
        
        self.mappings = {}
        self.mappings["plug"] = self.__expand_mapping_notation(plug_mapping)
        self.mappings["reflector"] = self.__expand_mapping_notation(reflector_mapping)
        self.mappings["rotors"] = [self.__expand_mapping_notation(mapping) for mapping in rotor_mappings]
        self.rotor_positions = rotor_positions
        self.rotor_rotations = [ord(rotation) - ord("A") for rotation in rotor_rotations]
        
    def __expand_mapping_notation(self, notation: str) -> dict[bool: dict[str, str]]:
        """
        Expands the mapping notation to a dictionary.
        
        :param notation: The mapping notation.
        :return: A dictionary with the mapping.
        """
        forward_mapping = {}
        reverse_mapping = {}
        for i in range(len(notation)):
            current_alphabet_letter = chr(ord("A")+i)
            forward_mapping[current_alphabet_letter] = notation[i]
            reverse_mapping[notation[i]] = current_alphabet_letter
                    
        return {True: forward_mapping, False: reverse_mapping}
        
    def __cyclic_permutation(self, char: str, shift: int) -> str:
        """
        Performs a cyclic permutation of the character.
        
        :param char: The character to be shifted.
        :param shift: The shift to be performed.
        """
        return chr((ord(char) - ord("A") + shift) % 26 + ord("A"))
    
    def __plugboard(self, char: str) -> str:
        """
        Feeds the character through the plugboard.
        
        :param char: The character to be fed through the plugboard.
        """
        return self.mappings["plug"][True][char] if char in self.mappings["plug"][True] else char
    
    def __rotor(self, char: str, rotor_index: int, direction: bool) -> str:
        """
        Feeds the character through the rotor.
        
        :param char: The character to be fed through the rotor.
        :param rotor_index: The index of the rotor to be used.
        :param direction: The direction to go through the rotor.
        """
        
        
        shift = self.rotor_rotations[rotor_index]
        rotor_to_use = self.rotor_positions[rotor_index]
        rotated_char = self.__cyclic_permutation(char, shift)
        mapped_char = self.mappings["rotors"][rotor_to_use][direction][rotated_char]
        return self.__cyclic_permutation(mapped_char, -shift)
    
    def __reflector(self, char: str) -> str:
        """
        Feeds the character through the reflector.
        
        :param char: The character to be fed through the reflector.
        """
        return self.mappings["reflector"][True][char]
    
    def __rotate_rotor(self, current_rotation: int) -> int:
        """
        Rotates a single rotor.
        
        :param current_rotation: The current rotation of the rotor.
        """
        
        return (current_rotation + 1) % 26
    
    def do_rotors_rotation(self):
        """
        Performs one rotation of the rotors.
        """
        self.rotor_rotations[2] = self.__rotate_rotor(self.rotor_rotations[2])
        if self.rotor_rotations[2] == 0:
            self.rotor_rotations[1] = self.__rotate_rotor(self.rotor_rotations[1])
            if self.rotor_rotations[1] == 0:
                self.rotor_rotations[0] = self.__rotate_rotor(self.rotor_rotations[0])
        

    def encrypt(self, message: str, reset_rotation: bool = True) -> str:
        """
        Encrypts the message using the Enigma machine.
        
        :param message: The message to be encrypted.
        :param reset_rotation: Whether to reset the rotor rotations after encryption.
        """
        original_rotor_rotations = self.rotor_rotations.copy()
        output = ""
        for char in message:
            plug_in = self.__plugboard(char)
            rotor_in = plug_in
            for i in range(2, -1, -1):
                rotor_in = self.__rotor(rotor_in, i, True)
            reflector = self.__reflector(rotor_in)
            rotor_out = reflector
            for i in range(3):
                rotor_out = self.__rotor(rotor_out, i, False)
            plug_out = self.__plugboard(rotor_out)
            output += plug_out
            self.do_rotors_rotation()
            
        if reset_rotation:
            self.rotor_rotations = original_rotor_rotations
        
        return output
    
    def decrypt(self, *args, **kwargs) -> str:
        """
        Decrypts the message using the Enigma machine.
        
        :param message: The message to be decrypted.
        :param reset_rotation: Whether to reset the rotor rotations after decryption.
        """
        return self.encrypt(*args, **kwargs)
        
        

if __name__ == "__main__":
    machine = EnigmaMachine(["AJDKSIRUXBLHWTMCQGZNPYFVOE", "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "BDFHJLCPRTXVZNYEIWGAKMUSQO", "THEQUICKBROWNFXJMPSVLAZYDG", "XANTIPESOKRWUDVBCFGHJLMQYZ"], "YRUHQSLDPXNGOKMIEBFZCWVJAT", [1, 0, 4], ["B", "E", "X"], "PBMEDFLHIZKGCNOAQRSWUVTXYJ")
    original_message = "PASOPVOORSALAMANDER"
    encrypted_message = machine.encrypt(original_message)
    decrypted_message = machine.decrypt(encrypted_message)
    print(f"Original message: {original_message}")
    print(f"Encrypted message: {encrypted_message}")
    print(f"Decrypted message: {decrypted_message}")
    
    assert original_message == decrypted_message