# Import the rapidfuzz module
from rapidfuzz import fuzz
from collections import Counter

# SpellCheck main class
class SpellCheck:
    # Initialization method
    def __init__(self, word_dict_file=None):
        # Open the dictionary file with the correct encoding (UTF-8 for Sinhala)
        with open(word_dict_file, 'r', encoding='utf-8') as file:
            # Read and split the file into words, removing duplicates
            self.dictionary = Counter(file.read().split())  # Frequency counts

    # String setter method
    def check(self, string_to_check):
        # Store the string to be checked in a class variable
        self.string_to_check = string_to_check

    # Method to get suggestions for each word
    def suggestions(self):
        # Split the input into words
        string_words = self.string_to_check.split()

        # A list to store suggestions for all input words
        all_suggestions = []

        # Loop through each word in the input string
        for word in string_words:
            # Get all potential matches from the dictionary
            matches = [
                (dict_word, fuzz.ratio(word, dict_word)) 
                for dict_word in self.dictionary
                if fuzz.ratio(word, dict_word) >= 60  # Adjust threshold here
            ]
            # Sort matches by similarity and dataset frequency
            matches = sorted(matches, key=lambda x: (x[1], self.dictionary[x[0]]), reverse=True)
            # Get only the words (top 5 suggestions)
            all_suggestions.append([match[0] for match in matches[:5]])

        return all_suggestions

    # Method to get the corrected string
    def correct(self):
        # Split the input into words
        string_words = self.string_to_check.split()

        # Correct each word based on suggestions
        corrected_words = []
        for word in string_words:
            max_percent = 0  # Highest similarity score
            best_match = word  # Default to the original word

            # Loop through dictionary words
            for dict_word in self.dictionary:
                percent = fuzz.ratio(word, dict_word)
                if percent > max_percent and percent >= 60:  # Adjust threshold here
                    max_percent = percent
                    best_match = dict_word

            corrected_words.append(best_match)

        return " ".join(corrected_words)
