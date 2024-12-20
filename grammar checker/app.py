from flask import Flask, request, jsonify
import google.generativeai as genai

# Initialize Flask app
app = Flask(__name__)

# Configure the Gemini API
genai.configure(api_key="AIzaSyBMOttuWMdq7F6_5Ffb50SRYDKPiEaj6W4")

@app.route('/check-grammar', methods=['POST'])
def check_grammar():
    try:
        # Parse JSON request body
        data = request.get_json()
        input_text = data.get('text', '').strip()

        if not input_text:
            return jsonify({"error": "No text provided"}), 400

        # Generate grammar correction using Gemini
        generation_config = {
            "temperature": 0.7,
            "max_output_tokens": 512,
            "top_p": 0.95,
            "top_k": 40,
        }

        # Start chat and send the input text
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config=generation_config,
        )
        chat_session = model.start_chat()
        response = chat_session.send_message(f"Correct this Sinhala text: {input_text}")

        # Process Gemini API response
        corrected_text = response.text.strip() if response.text else "No correction provided."

        return jsonify({"corrected_text": corrected_text}), 200

    except Exception as e:
        # Handle errors
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)