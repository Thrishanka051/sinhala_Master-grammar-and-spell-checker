from collections import Counter
import numpy as np

class SpellCheck:
    def __init__(self, word_dict_file=None):
        with open(word_dict_file, 'r', encoding='utf-8') as file:
            self.dictionary = Counter(file.read().split())
        
        # Define Sinhala diacritical marks
        self.diacritical_marks = ['ා', 'ැ', 'ි', 'ු', 'ූ', 'ෘ', 'ෲ', 'ෟ', 'ේ', 'ෝ', 'ෞ']
        
    def check(self, string_to_check):
        self.string_to_check = string_to_check

    def get_ngrams(self, word, n=2):
        """Generate character n-grams from word"""
        return [word[i:i+n] for i in range(len(word)-n+1)]

    def jaccard_similarity(self, word1, word2, n=2):
        """Calculate Jaccard similarity between two words using n-grams"""
        ngrams1 = set(self.get_ngrams(word1, n))
        ngrams2 = set(self.get_ngrams(word2, n))
        
        intersection = len(ngrams1.intersection(ngrams2))
        union = len(ngrams1.union(ngrams2))
        
        return intersection / union if union != 0 else 0

    def longest_common_subsequence(self, word1, word2):
        """Calculate length of longest common subsequence"""
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i-1] == word2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        return dp[m][n] / max(m, n)  # Normalize by longer word length

    def diacritical_similarity(self, word1, word2):
        """Calculate similarity based on diacritical marks"""
        # Extract base characters and diacritical marks
        base1 = ''.join(c for c in word1 if c not in self.diacritical_marks)
        base2 = ''.join(c for c in word2 if c not in self.diacritical_marks)
        
        marks1 = [(i, c) for i, c in enumerate(word1) if c in self.diacritical_marks]
        marks2 = [(i, c) for i, c in enumerate(word2) if c in self.diacritical_marks]
        
        # Base similarity
        base_sim = self.longest_common_subsequence(base1, base2)
        
        # Diacritical mark similarity
        mark_sim = 0
        if marks1 and marks2:
            for pos1, mark1 in marks1:
                rel_pos1 = pos1 / len(word1)
                for pos2, mark2 in marks2:
                    rel_pos2 = pos2 / len(word2)
                    # Compare both mark type and relative position
                    if mark1 == mark2:
                        mark_sim += 1 - min(abs(rel_pos1 - rel_pos2), 0.5)
            
            mark_sim = mark_sim / max(len(marks1), len(marks2))
        
        return 0.7 * base_sim + 0.3 * mark_sim

    def calculate_similarity(self, word1, word2):
        """Combined similarity metric"""
        # Calculate different similarity measures
        jaccard_sim = self.jaccard_similarity(word1, word2)
        lcs_sim = self.longest_common_subsequence(word1, word2)
        diac_sim = self.diacritical_similarity(word1, word2)
        
        # Length difference penalty
        len_diff = 1 - abs(len(word1) - len(word2)) / max(len(word1), len(word2))
        
        # Combine similarities with weights
        combined_sim = (
            0.3 * jaccard_sim +  # Character n-gram similarity
            0.3 * lcs_sim +      # Sequence similarity
            0.3 * diac_sim +     # Diacritical mark similarity
            0.1 * len_diff       # Length similarity
        ) * 100  # Convert to percentage
        
        return combined_sim

    def suggestions(self):
        string_words = self.string_to_check.split()
        all_suggestions = []

        for word in string_words:
            # Calculate similarity for all words in the dictionary
            matches = [
                (dict_word, self.calculate_similarity(word, dict_word))
                for dict_word in self.dictionary
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
            
            for dict_word in self.dictionary:
                similarity = self.calculate_similarity(word, dict_word)
                if similarity > max_similarity:
                    max_similarity = similarity
                    best_match = dict_word
            
            corrected_words.append(best_match)
        
        return " ".join(corrected_words)
