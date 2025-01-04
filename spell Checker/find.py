import unicodedata

def normalize_word(word):
    """
    Normalize a Sinhala word by removing diacritical marks.
    This helps in detecting diacritical variations.
    :param word: The word to normalize
    :return: Normalized word without diacritical marks
    """
    return ''.join(
        char for char in unicodedata.normalize('NFD', word) 
        if unicodedata.category(char) != 'Mn'
    )

def load_dictionary(file_path):
    """
    Load a Sinhala word dataset from a file.
    :param file_path: Path to the dictionary file
    :return: Set of words in the dataset
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return set(file.read().split())  # Use a set for efficient lookups

def is_word_in_dictionary(word, dictionary):
    """
    Check if a word exists in the dictionary, considering diacritical variations.
    :param word: The word to check
    :param dictionary: Set of dictionary words
    :return: True if the word exists, False otherwise
    """
    normalized_word = normalize_word(word)
    for dict_word in dictionary:
        if normalize_word(dict_word) == normalized_word:
            return True
    return False

# Main function
if __name__ == "__main__":
    # Path to your Sinhala word dataset file
    dictionary_file = 'sinhala_full_word_list_2016-10-08.txt'
    dictionary = load_dictionary(dictionary_file)
    
    # Prompt the user for input
    user_word = input("Enter the word to search in the dictionary: ").strip()
    
    # Check if the word exists
    if is_word_in_dictionary(user_word, dictionary):
        print(f"The word '{user_word}' exists in the dictionary.")
    else:
        print(f"The word '{user_word}' does not exist in the dictionary.")
