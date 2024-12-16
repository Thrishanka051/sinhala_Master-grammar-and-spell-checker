import math
from collections import Counter

class SpellCheck1:
    def __init__(self, word_dict_file=None):
        with open(word_dict_file, 'r') as file:
            data = file.read()
        self.dictionary = set(data.lower().split(","))  # Set for unique words

    def check(self, string_to_check):
        self.string_to_check = string_to_check

    def suggestions(self):
        string_words = self.string_to_check.split()
        suggestions = []

        for word in string_words:
            best_match, highest_score = None, 0

            for dict_word in self.dictionary:
                score = self._cosine_similarity(word, dict_word)
                
                if score > highest_score:
                    highest_score = score
                    best_match = dict_word

            suggestions.append(best_match if best_match else word)

        return suggestions

    def _cosine_similarity(self, word1, word2):
        # Get character frequency vectors for both words
        freq1, freq2 = Counter(word1), Counter(word2)
        
        # Characters present in either word
        unique_chars = set(freq1.keys()).union(freq2.keys())
        
        # Dot product and magnitudes
        dot_product = sum(freq1[char] * freq2[char] for char in unique_chars)
        magnitude1 = math.sqrt(sum(freq1[char]**2 for char in unique_chars))
        magnitude2 = math.sqrt(sum(freq2[char]**2 for char in unique_chars))
        
        return dot_product / (magnitude1 * magnitude2) if magnitude1 and magnitude2 else 0

    def correct(self):
        corrected_words = self.suggestions()
        return " ".join(corrected_words)
