from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def load_files():
    try:
        with open("./Dictionary/Sinhala_Grammer.text", "r", encoding="UTF-8") as f:
            grammar_rules = f.read()

        with open("./Dictionary/Sinhala_Subjects.text", "r", encoding="UTF-8") as f:
            subjects = [line.strip() for line in f.readlines() if line.strip()]

        return grammar_rules, subjects

    except FileNotFoundError as e:
        return str(e), []

def parse_grammar_rules(grammar_rules):
    corrections_data = {}
    subject = None

    for line in grammar_rules.splitlines():
        line = line.strip()
        if not line:
            continue
        if ":" in line:
            subject = line[:-1]
            corrections_data[subject] = {}
        elif "->" in line:
            incorrect, correct = line.split("->")
            corrections_data[subject][incorrect.strip()] = correct.strip()

    return corrections_data

def correct_sentence_with_rules(text, grammar_rules, subjects):
    corrections_data = parse_grammar_rules(grammar_rules)
    sentences = [s.strip() for s in text.replace(",", ".").split(".") if s.strip()]
    corrected_sentences = []

    for sentence in sentences:
        words = sentence.split()
        if not words:
            corrected_sentences.append(sentence)
            continue

        corrections = {}
        matched_subjects = []

        for word in words:
            if word in subjects:
                matched_subjects.append(word)
                for key, rules in corrections_data.items():
                    if word in key.split(","):
                        corrections = rules
                        break

        if len(set(matched_subjects)) > 1:
            corrections = corrections_data.get('බහුවචනය', {})

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

    grammar_rules, subjects = load_files()
    if isinstance(grammar_rules, str):
        return jsonify({"error": grammar_rules}), 500

    grammar_correction = correct_sentence_with_rules(text, grammar_rules, subjects)

    return jsonify({
        "grammar_correction": grammar_correction
    })

if __name__ == '__main__':
    app.run(debug=True, port=8080)
