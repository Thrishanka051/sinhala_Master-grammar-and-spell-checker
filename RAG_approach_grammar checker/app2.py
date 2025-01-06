from flask import Flask, request, jsonify
import google.generativeai as genai
import re

# Initialize Flask app
app = Flask(__name__)

# Configure the Gemini API
genai.configure(api_key="AIzaSyBMOttuWMdq7F6_5Ffb50SRYDKPiEaj6W4")

# Function to load grammar rules from a text file
def load_grammar_rules(file_path="grammar_rules.txt"):
    rules = {}
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            print(f"Reading line: {line.strip()}")  # Debugging line
            if ":" in line:
                key, value = line.strip().split(":", 1)
                rules[key.strip()] = value.strip()
            else:
                print(f"Skipping invalid line: {line.strip()}")  # Handle invalid lines
    return rules

# Apply retrieved rules to correct the input text
def apply_retrieved_rules(input_text, rules):
    corrected_text = input_text
    for error, correction in rules.items():
        corrected_text = re.sub(error, correction, corrected_text)
    return corrected_text

def count_tokens(text):
    # Tokenize the text and count tokens (placeholder logic)
    # Replace with the actual tokenizer for Gemini if available
    return len(text.split())

@app.route('/check-grammar', methods=['POST'])
def check_grammar():
    try:
        # Parse JSON request body
        data = request.get_json()
        input_text = data.get('text', '').strip()

        if not input_text:
            return jsonify({"error": "No text provided"}), 400
        
        # Step 1: Load grammar rules
        grammar_rules = load_grammar_rules()

        # Step 2: Retrieve relevant corrections
        corrected_by_rules = apply_retrieved_rules(input_text, grammar_rules)
        
        # Count input tokens
        input_tokens = count_tokens(input_text)

        # Dynamically set max_output_tokens (e.g., 1.2x input tokens)
        max_output_tokens = int(1.2 * input_tokens)

        # Generate grammar correction using Gemini
        generation_config = {
            "temperature": 0.7,
            "max_output_tokens": 200,  # Use dynamically calculated max_output_tokens
            "top_p": 0.95,
            "top_k": 40,
        }

        # Start chat and send the input text
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config=generation_config,
        )
        chat_session = model.start_chat()
        response = chat_session.send_message(f"Correct this Sinhala text with minimal changes to ensure grammatical accuracy and return only the corrected version without any explanations: {corrected_by_rules}")

        # Extract the corrected text (assuming the first line of the response is the correction)
        corrected_text = response.text.split("\n")[0].strip() if response.text else "No correction provided."

        return jsonify({"corrected_text": corrected_text}), 200

    except Exception as e:
        # Handle errors
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
