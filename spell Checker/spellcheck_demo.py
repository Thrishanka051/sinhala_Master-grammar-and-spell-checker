# Import the SpellCheck class
from spellcheck import SpellCheck

# Create an object for spell checking
spell_check = SpellCheck('merged_filtered_words2.txt')

# Get the string to be checked from the user
string_to_be_checked = input("Enter the string to be checked: ")

# Perform spell checking
spell_check.check(string_to_be_checked)

# Print suggestions for each word
print("\nSuggestions for each word:")
suggestions = spell_check.suggestions()
for idx, word_suggestions in enumerate(suggestions):
    print(f"Word {idx + 1}: {word_suggestions}")

# Print the corrected string
print("\nCorrected String:")
print(spell_check.correct())
