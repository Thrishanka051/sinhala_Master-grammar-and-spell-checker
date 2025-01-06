from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure the Gemini API
genai.configure(api_key="AIzaSyBMOttuWMdq7F6_5Ffb50SRYDKPiEaj6W4")

# Load the grammar rules from the file
def load_grammar_rules():
    try:
        with open('grammar_rules.txt', 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return str(e)

@app.route('/check-grammar', methods=['POST'])
def check_grammar():
    try:
        # Parse JSON request body
        data = request.get_json()
        input_text = data.get('text', '').strip()

        if not input_text:
            return jsonify({"error": "No text provided"}), 400

        # Load grammar rules from the file
        grammar_rules = load_grammar_rules()

        if not grammar_rules:
            return jsonify({"error": "Failed to load grammar rules"}), 500

        # Generate grammar correction using Gemini
        generation_config = {
            "temperature": 0.7,
            "max_output_tokens": 512,
            "top_p": 0.95,
            "top_k": 40,
        }

        # Start chat and send the input text with grammar rules as context
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config=generation_config,
        )
        chat_session = model.start_chat()
        
        # Send the grammar rules and input text to the AI for suggestions
        prompt = f"Here are the grammar rules: {grammar_rules}\nPlease suggest corrections for the following Sinhala text and only respond the sinhala text: {input_text}"
        response = chat_session.send_message(prompt)

        # Process Gemini API response
        suggestions = response.text.strip() if response.text else "No suggestions provided."

        return jsonify({"suggestions": suggestions}), 200

    except Exception as e:
        # Handle errors
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)