import numpy as np
from collections import Counter

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
        
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
    
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return None
            node = node.children[char]
        return node if node.is_end_of_word else None

    def get_words_with_prefix(self, prefix):
        """Returns a list of words starting with the given prefix."""
        node = self.root
        words = []

        for char in prefix:
            if char not in node.children:
                return words
            node = node.children[char]

        self._collect_words_from_node(node, prefix, words)
        return words

    def _collect_words_from_node(self, node, prefix, words):
        if node.is_end_of_word:
            words.append(prefix)
        for char, child in node.children.items():
            self._collect_words_from_node(child, prefix + char, words)

class SpellCheck:
    def __init__(self, word_dict_file=None):
        self.trie = Trie()
        
        # Load the dictionary into the Trie and Counter
        with open(word_dict_file, 'r', encoding='utf-8') as file:
            self.dictionary = Counter(file.read().split())

        for word in self.dictionary:
            self.trie.insert(word)
        
        # Define Sinhala diacritical marks
        self.diacritical_marks = ['ා', 'ැ', 'ි', 'ු', 'ූ', 'ෘ', 'ෲ', 'ෟ', 'ේ', 'ෝ', 'ෞ']

    def check(self, string_to_check):
        """Store the input string for further processing."""
        self.string_to_check = string_to_check
        
    def damerau_levenshtein_distance(self, word1, word2):
        """Calculate Damerau-Levenshtein distance"""
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                cost = 0 if word1[i - 1] == word2[j - 1] else 1
                dp[i][j] = min(
                    dp[i - 1][j] + 1,    # Deletion
                    dp[i][j - 1] + 1,    # Insertion
                    dp[i - 1][j - 1] + cost,    # Substitution
                )

                if i > 1 and j > 1 and word1[i - 1] == word2[j - 2] and word1[i - 2] == word2[j - 1]:
                    dp[i][j] = min(dp[i][j], dp[i - 2][j - 2] + cost)  # Transposition

        return dp[m][n]

    def diacritical_similarity(self, word1, word2):
        """Calculate similarity based on diacritical marks"""
        base1 = ''.join(c for c in word1 if c not in self.diacritical_marks)
        base2 = ''.join(c for c in word2 if c not in self.diacritical_marks)
        
        # Calculate diacritical mark similarity
        mark_sim = sum(1 for c1, c2 in zip(word1, word2) if c1 == c2 and c1 in self.diacritical_marks)
        mark_sim /= max(len(word1), len(word2))
        
        # If the base word is the same, prioritize diacritical similarity
        base_similarity = (base1 == base2)
        
        return 0.7 * base_similarity + 0.3 * mark_sim

    def calculate_similarity(self, word1, word2):
        """Combined similarity metric"""
        # Damerau-Levenshtein distance metric
        distance = self.damerau_levenshtein_distance(word1, word2)
        max_len = max(len(word1), len(word2))
        lev_similarity = (1 - distance / max_len) * 100  # Convert to percentage

        # Diacritical similarity
        diac_sim = self.diacritical_similarity(word1, word2)

        # Return combined similarity (prioritize diacritical similarity)
        combined_sim = 0.7 * lev_similarity + 0.3 * diac_sim
        return combined_sim

    def suggestions(self):
        string_words = self.string_to_check.split()
        all_suggestions = []

        for word in string_words:
            # Use Trie to find words with the same prefix
            prefix_words = self.trie.get_words_with_prefix(word[:3])  # Use first 3 characters of the word as prefix
            
            # Calculate similarity for all prefix-matching words
            matches = [
                (dict_word, self.calculate_similarity(word, dict_word))
                for dict_word in prefix_words
            ]
            
            # Sort matches by similarity score (descending order)
            matches = sorted(matches, key=lambda x: x[1], reverse=True)
            
            # Get the top 4 suggestions
            all_suggestions.append(matches[:4])
        
        # Return suggestions along with scores
        return all_suggestions

    def correct(self):
        string_words = self.string_to_check.split()
        corrected_words = []
        
        for word in string_words:
            max_similarity = 0
            best_match = word  # Default to the input word in case no better match is found
            
            # Search the Trie for prefix-matching words
            prefix_words = self.trie.get_words_with_prefix(word[:3])
            
            for dict_word in prefix_words:
                similarity = self.calculate_similarity(word, dict_word)
                if similarity > max_similarity:
                    max_similarity = similarity
                    best_match = dict_word
            
            corrected_words.append(best_match)
        
        return " ".join(corrected_words)
