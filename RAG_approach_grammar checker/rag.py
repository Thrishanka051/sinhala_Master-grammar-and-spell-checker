from flask import Flask, request, jsonify
import json
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from uuid import uuid4
from flask_cors import CORS

app = Flask(__name__)

CORS(app)


# Load the grammar rules from JSON file
with open("sinhala_grammar.json", "r", encoding="utf-8") as file:
    rules_data = json.load(file)

# Convert rules into LangChain Documents
documents = [
    Document(
        page_content=json.dumps(rule, ensure_ascii=False, indent=2),
        metadata={
            "index": rule.get("index"),
            "rule_type": rule.get("rule_type"),
            "description": rule.get("description", ""),
        },
    )
    for rule in rules_data
]

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# Calculate the embedding dimension
embedding_dimension = len(embeddings.embed_query("test query"))

# Initialize FAISS index
index = faiss.IndexFlatL2(embedding_dimension)

# Create the vector store
vector_store = FAISS(
    embedding_function=embeddings,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
)

# Add documents to the vector store
uuids = [str(uuid4()) for _ in range(len(documents))]
vector_store.add_documents(documents=documents, ids=uuids)

# Initialize Gemini LLM
os.environ["GOOGLE_API_KEY"] = "AIzaSyBMOttuWMdq7F6_5Ffb50SRYDKPiEaj6W4"  # Replace with your API key
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Define a function to retrieve similar rules
def retrieve_similar_rules(user_input, vector_store, top_k=5):
    user_input_embedding = embeddings.embed_query(user_input)
    search_results = vector_store.similarity_search_by_vector(user_input_embedding, top_k=top_k)
    return search_results

# Flask endpoint for grammar correction
@app.route("/correct_sentence", methods=["POST"])
def correct_sentence():
    # Parse user input from the POST request
    data = request.json
    user_input = data.get("sentence", "")
    
    if not user_input:
        return jsonify({"error": "Sentence is required"}), 400

    # Retrieve the most similar rules
    retrieved_rules = retrieve_similar_rules(user_input, vector_store, top_k=3)
    
    # Construct the prompt for Gemini
    retrieved_text = "\n".join(
        [
            f"Rule {rule.metadata.get('index')}: {rule.metadata.get('description')}"
            for rule in retrieved_rules
        ]
    )
    prompt = (
        f"User input: '{user_input}'\n"
        f"Based on the following grammar rules, please correct the sentence according to:\n{retrieved_rules}\n"
        f"give only corrected sentence:"
    )

    # Use Gemini to get the corrected sentence
    try:
        corrected_sentence = llm.predict(prompt)
        return jsonify({"corrected_sentence": corrected_sentence}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
