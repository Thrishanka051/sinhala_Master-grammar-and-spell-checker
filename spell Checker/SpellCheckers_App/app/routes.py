from flask import Blueprint, request, jsonify
from app.spellcheckers.spellchecker_1 import SpellCheck as SpellChecker1
from app.spellcheckers.spellchecker_2 import SpellChecker as SpellChecker2
#from app.spellcheckers.spellchecker_3 import SpellCheck as SpellChecker3

api_bp = Blueprint('api', __name__)

# Initialize spellcheckers
spellchecker_1 = SpellChecker1('sinhala_full_word_list_2016-10-08.txt')
spellchecker_2 = SpellChecker2('sinhala_full_word_list_2016-10-08.txt')
#spellchecker_3 = SpellChecker3('sinhala_full_word_list_2016-10-08.txt')

# Helper function to handle API responses
def handle_spellchecker(spellchecker, text, operation):
    spellchecker.check(text)
    if operation == 'suggestions':
        return spellchecker.suggestions()
    elif operation == 'correct':
        return spellchecker.correct()

# Routes for SpellChecker 1
@api_bp.route('/api/spellchecker1/suggestions', methods=['POST'])
def spellchecker1_suggestions():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "Invalid input. 'text' field is required."}), 400
    suggestions = handle_spellchecker(spellchecker_1, data['text'], 'suggestions')
    return jsonify({"suggestions": suggestions})

@api_bp.route('/api/spellchecker1/correct', methods=['POST'])
def spellchecker1_correct():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "Invalid input. 'text' field is required."}), 400
    corrected_text = handle_spellchecker(spellchecker_1, data['text'], 'correct')
    return jsonify({"corrected_text": corrected_text})

# Routes for SpellChecker 2
@api_bp.route('/api/spellchecker2/suggestions', methods=['POST'])
def spellchecker2_suggestions():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "Invalid input. 'text' field is required."}), 400
    suggestions = handle_spellchecker(spellchecker_2, data['text'], 'suggestions')
    return jsonify({"suggestions": suggestions})

@api_bp.route('/api/spellchecker2/correct', methods=['POST'])
def spellchecker2_correct():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "Invalid input. 'text' field is required."}), 400
    corrected_text = handle_spellchecker(spellchecker_2, data['text'], 'correct')
    return jsonify({"corrected_text": corrected_text})

# Routes for SpellChecker 3
"""@api_bp.route('/api/spellchecker3/suggestions', methods=['POST'])
def spellchecker3_suggestions():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "Invalid input. 'text' field is required."}), 400
    suggestions = handle_spellchecker(spellchecker_3, data['text'], 'suggestions')
    return jsonify({"suggestions": suggestions})

@api_bp.route('/api/spellchecker3/correct', methods=['POST'])
def spellchecker3_correct():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "Invalid input. 'text' field is required."}), 400
    corrected_text = handle_spellchecker(spellchecker_3, data['text'], 'correct')
    return jsonify({"corrected_text": corrected_text})"""
