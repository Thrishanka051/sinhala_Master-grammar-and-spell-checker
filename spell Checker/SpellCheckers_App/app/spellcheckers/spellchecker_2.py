from collections import Counter

class SpellChecker:
    def __init__(self, word_dict_file=None):
        """Initialize the spell checker with a word dictionary."""
        if word_dict_file:
            with open(word_dict_file, 'r', encoding='utf-8') as file:
                self.dictionary = Counter(file.read().split())
        else:
            self.dictionary = Counter()

        # Define Sinhala diacritical marks
        self.diacritical_marks = ['\u0dcf', '\u0dd0', '\u0dd2', '\u0dd4', '\u0dd6', '\u0dd8', '\u0df2', '\u0dcb', '\u0dd9', '\u0ddc', '\u0ddd']

    def check(self, text):
        """Store the input string to check."""
        self.text_to_check = text

    def _get_ngrams(self, word, n=2):
        """Generate character n-grams from a word."""
        return [word[i:i + n] for i in range(len(word) - n + 1)]

    def _jaccard_similarity(self, word1, word2, n=2):
        """Calculate Jaccard similarity between two words using n-grams."""
        ngrams1 = set(self._get_ngrams(word1, n))
        ngrams2 = set(self._get_ngrams(word2, n))
        intersection = len(ngrams1 & ngrams2)
        union = len(ngrams1 | ngrams2)
        return intersection / union if union != 0 else 0

    def _longest_common_subsequence(self, word1, word2):
        """Calculate the normalized length of the longest common subsequence."""
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        return dp[m][n] / max(m, n)

    def _diacritical_similarity(self, word1, word2):
        """Calculate similarity based on base characters and diacritical marks."""
        base1 = ''.join(c for c in word1 if c not in self.diacritical_marks)
        base2 = ''.join(c for c in word2 if c not in self.diacritical_marks)

        marks1 = [(i, c) for i, c in enumerate(word1) if c in self.diacritical_marks]
        marks2 = [(i, c) for i, c in enumerate(word2) if c in self.diacritical_marks]

        base_sim = self._longest_common_subsequence(base1, base2)
        mark_sim = 0

        if marks1 and marks2:
            for pos1, mark1 in marks1:
                rel_pos1 = pos1 / len(word1)
                for pos2, mark2 in marks2:
                    rel_pos2 = pos2 / len(word2)
                    if mark1 == mark2:
                        mark_sim += 1 - min(abs(rel_pos1 - rel_pos2), 0.5)
            mark_sim /= max(len(marks1), len(marks2))

        return 0.7 * base_sim + 0.3 * mark_sim

    def _calculate_similarity(self, word1, word2):
        """Combine various similarity metrics to calculate an overall score."""
        jaccard_sim = self._jaccard_similarity(word1, word2)
        lcs_sim = self._longest_common_subsequence(word1, word2)
        diac_sim = self._diacritical_similarity(word1, word2)
        len_diff = 1 - abs(len(word1) - len(word2)) / max(len(word1), len(word2))

        combined_sim = (
            0.3 * jaccard_sim +
            0.3 * lcs_sim +
            0.3 * diac_sim +
            0.1 * len_diff
        ) * 100

        return combined_sim

    def suggestions(self):
        """Provide spelling suggestions for the input text."""
        words = self.text_to_check.split()
        suggestions = []

        for word in words:
            matches = [
                (dict_word, self._calculate_similarity(word, dict_word))
                for dict_word in self.dictionary
            ]
            matches = sorted(matches, key=lambda x: x[1], reverse=True)
            suggestions.append(matches[:4])

        return suggestions

    def correct(self):
        """Correct misspelled words in the input text."""
        words = self.text_to_check.split()
        corrected_words = []

        for word in words:
            max_similarity = 0
            best_match = word

            for dict_word in self.dictionary:
                similarity = self._calculate_similarity(word, dict_word)
                if similarity > max_similarity:
                    max_similarity = similarity
                    best_match = dict_word

            corrected_words.append(best_match)

        return ' '.join(corrected_words)
