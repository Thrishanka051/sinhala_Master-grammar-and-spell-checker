from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

def load_file(filepath):
    try:
        with open(filepath, "r", encoding="UTF-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return None

def correct_sentence_with_rules(text):
    grammar_path = os.path.join(os.getcwd(), "Sinhala_grammar.text")
    subjects_path = os.path.join(os.getcwd(), "Sinhala_subjects.text")
    grammar_rules = load_file(grammar_path)
    subjects = load_file(subjects_path)

    if not grammar_rules or not subjects:
        return "Required file(s) not found."

    corrections_data = {}
    subject = None
    for line in grammar_rules:
        if ":" in line:
            subject = line[:-1]
            corrections_data[subject] = {}
        elif "->" in line:
            incorrect, correct = line.split("->")
            corrections_data[subject][incorrect.strip()] = correct.strip()

    sentences = [s.strip() for s in text.replace(",", ".").split(".") if s.strip()]
    corrected_sentences = []

    for sentence in sentences:
        words = sentence.split()
        corrections = {}
        matched_subjects = [word for word in words if word in subjects]

        if len(set(matched_subjects)) > 1:
            corrections = corrections_data.get('බහුවචනය', {})
        else:
            for subject_word in matched_subjects:
                for key, rules in corrections_data.items():
                    if subject_word in key.split(","):
                        corrections = rules
                        break

        corrected_sentence = sentence
        for incorrect, correct in corrections.items():
            if incorrect in sentence:
                corrected_sentence = corrected_sentence.replace(incorrect, correct)

        corrected_sentences.append(corrected_sentence)

    corrected_text = ".".join(corrected_sentences) + "." if corrected_sentences else ""
    return corrected_text

@app.route('/check', methods=['POST'])
def check_text():
    data = request.get_json()
    text = data.get('paragraph', '') or data.get('sentence', '')

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Perform grammar correction
    grammar_correction = correct_sentence_with_rules(text)

    return jsonify({
        "grammar_correction": grammar_correction
    })

if __name__ == '__main__':
    app.run(debug=True, port=8080)