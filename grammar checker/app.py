from flask import Flask, request, jsonify
import google.generativeai as genai

# Initialize Flask app
app = Flask(__name__)

# Configure the Gemini API
genai.configure(api_key="AIzaSyBMOttuWMdq7F6_5Ffb50SRYDKPiEaj6W4")

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
        
        # Count input tokens
        input_tokens = count_tokens(input_text)

        # Dynamically set max_output_tokens (e.g., 1.2x input tokens)
        max_output_tokens = int(1.2 * input_tokens)

        # Generate grammar correction using Gemini
        generation_config = {
            "temperature": 0.7,
            "max_output_tokens":200,
            "top_p": 0.95,
            "top_k": 40,
        }

        # Start chat and send the input text
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config=generation_config,
        )
        chat_session = model.start_chat()
        response = chat_session.send_message(f"Correct this Sinhala text with minimal changes to ensure grammatical accuracy and return only the corrected version without any explanations: {input_text}")

       # Extract the corrected text (assuming the first line of the response is the correction)
        corrected_text = response.text.split("\n")[0].strip() if response.text else "No correction provided."

        return jsonify({"corrected_text": corrected_text}), 200

    except Exception as e:
        # Handle errors
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)