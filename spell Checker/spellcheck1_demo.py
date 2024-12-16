# spellchecker_demo.py
from spellcheck1 import SpellCheck1

# Initialize with a dictionary file
spell_check = SpellCheck1('words.txt')

# Set the word to be checked
string_to_be_checked = "gld narow"
spell_check.check(string_to_be_checked)

# Print the list of suggested words for each misspelled word
print("Suggestions:", spell_check.suggestions())

# Print the corrected sentence with the best match replacements
print("Corrected sentence:", spell_check.correct())
