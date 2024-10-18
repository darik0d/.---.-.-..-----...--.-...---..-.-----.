"""
This file contains code for preprocessing the corpus.
Goal: remove unwanted characters and replace some characters with their corresponding characters.
"""

import re

permittable_characters = "abcdefghiklmnopqrstuvwxyz"
# TODO: is "ß": "ss" correct?
replace_characters = {"j": "i", "ü": "u", "ö": "o", "ä": "a", "ß": "ss",
                      "é": "e", "è": "e", "ê": "e", "à": "a", "â": "a", "ç": "c",
                      "ô": "o", "û": "u", "î": "i", "ï": "i", "ë": "e", "ù": "u", "œ": "oe", "æ": "ae"}

