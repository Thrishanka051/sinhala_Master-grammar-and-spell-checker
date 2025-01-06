from collections import Counter
from rapidfuzz import fuzz

class SpellCheck:
    def __init__(self, word_dict_file=None):
        """Initialize the SpellCheck class with a word dictionary file."""
        if word_dict_file is None:
            raise ValueError("A valid word dictionary file must be provided.")

        # Load the dictionary file and count word frequencies
        with open(word_dict_file, 'r', encoding='utf-8') as file:
            self.dictionary = Counter(file.read().split())

    def check(self, string_to_check):
        """Set the string to be checked."""
        if not string_to_check:
            raise ValueError("Input string cannot be empty.")
        
        self.string_to_check = string_to_check

    def suggestions(self):
        """Generate spelling suggestions for each word in the input string."""
        # Split the input string into individual words
        string_words = self.string_to_check.split()

        # Store suggestions for all words
        all_suggestions = []

        for word in string_words:
            # Calculate similarity scores for each dictionary word
            matches = [
                (dict_word, fuzz.ratio(word, dict_word))
                for dict_word in self.dictionary
                if fuzz.ratio(word, dict_word) >= 60  # Threshold for similarity
            ]

            # Sort matches by similarity score and frequency in the dictionary
            matches = sorted(matches, key=lambda x: (x[1], self.dictionary[x[0]]), reverse=True)

            # Extract the top 5 suggestions
            all_suggestions.append([match[0] for match in matches[:5]])

        return all_suggestions

    def correct(self):
        """Return a corrected version of the input string."""
        # Split the input string into individual words
        string_words = self.string_to_check.split()

        # List to hold corrected words
        corrected_words = []

        for word in string_words:
            max_similarity = 0
            best_match = word  # Default to the original word

            # Find the best match in the dictionary
            for dict_word in self.dictionary:
                similarity = fuzz.ratio(word, dict_word)
                if similarity > max_similarity and similarity >= 60:  # Threshold for correction
                    max_similarity = similarity
                    best_match = dict_word

            corrected_words.append(best_match)

        # Combine corrected words into a single string
        return " ".join(corrected_words)
