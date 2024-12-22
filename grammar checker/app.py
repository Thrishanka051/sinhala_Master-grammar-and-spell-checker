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

        grammar_rules = """
                1. Ensure proper subject-verb-object (SVO) structure.
                Example: "මම පොතක් කියවමි." is correct. Avoid: "මම කියවමි පොතක්."

                2. Avoid redundant particles such as "ක්", "ම", and "ක්වෙ." Use minimal particles.
                Example: "පොතක් කියවමි." is preferred over "පොතක් කියවමිනි."

                3. Use correct verb conjugation depending on tense.
                Example: 
                    Present: "කැවිමි" 
                    Past: "කෑවෙමි" 
                    Future: "කනවා."

                4. Keep sentence length concise. Break long sentences into simpler parts.
                Example: "මම පොත් දෙකක් කියවා පාඩම් ලිවිය." is preferred over "මම පොත් දෙකක් කියවා සිටිමි එසේ මට පාඩම් ලිවිය."

                5. Proper spacing between words is critical.
                Example: Avoid: "මමපොතක්." Correct: "මම පොතක්."

                6. Ensure proper verb ending according to subject type across all tenses:

                Present Tense:
                    - First Person Singular (මම): ends with මි
                        Correct: "මම යමි" (I go)
                        Incorrect: "මම යයි"
                    - First Person Plural (අපි): ends with මු
                        Correct: "අපි යමු" (We go)
                        Incorrect: "අපි යමි"
                    - Third Person Singular (ඔහු/ඇය): ends with යි
                        Correct: "ඔහු/ඇය යයි" (He/She goes)
                        Incorrect: "ඔහු යමි"
                    - Third Person Plural (ඔවුන්): ends with ති
                        Correct: "ඔවුන් යති" (They go)
                        Incorrect: "ඔවුන් යයි"

                Past Tense:
                    - First Person Singular (මම): ends with ෙමි
                        Correct: "මම ගියෙමි" (I went)
                        Incorrect: "මම ගියා"
                    - First Person Plural (අපි): ends with ෙමු
                        Correct: "අපි ගියෙමු" (We went)
                        Incorrect: "අපි ගියෙමි"
                    - Third Person Singular Male (ඔහු): ends with ේය
                        Correct: "ඔහු ගියේය" (He went)
                        Incorrect: "ඔහු ගියෙමි"
                    - Third Person Singular Female (ඇය): ends with ාය
                        Correct: "ඇය ගියාය" (She went)
                        Incorrect: "ඇය ගියේය"
                    - Third Person Plural (ඔවුන්): ends with ෝය
                        Correct: "ඔවුන් ගියෝය" (They went)
                        Incorrect: "ඔවුන් ගියේය"

                Future Tense:
                    - First Person Singular (මම): ends with න්නෙමි
                        Correct: "මම යන්නෙමි" (I will go)
                        Incorrect: "මම යාවි"
                    - First Person Plural (අපි): ends with න්නෙමු
                        Correct: "අපි යන්නෙමු" (We will go)
                        Incorrect: "අපි යන්නෙමි"
                    - Third Person Singular (ඔහු/ඇය): ends with ාවි
                        Correct: "ඔහු/ඇය යාවි" (He/She will go)
                        Incorrect: "ඔහු යන්නෙමි"
                    - Third Person Plural (ඔවුන්): ends with ාවිත්
                        Correct: "ඔවුන් යාවිත්" (They will go)
                        Incorrect: "ඔවුන් යාවි"
                """

        # Prepare the prompt with grammar rules
        prompt = f"""
        Below are some Sinhala grammar correction rules:
        {grammar_rules}
        
        Correct the following Sinhala sentence based on the rules above and return only the corrected version without any explanations:
        {input_text}
        """
        # Start chat and send the input text
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config=generation_config,
        )
        chat_session = model.start_chat()
        response = chat_session.send_message(prompt)

       # Extract the corrected text (assuming the first line of the response is the correction)
        corrected_text = response.text.split("\n")[0].strip() if response.text else "No correction provided."

        return jsonify({"corrected_text": corrected_text}), 200

    except Exception as e:
        # Handle errors
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)