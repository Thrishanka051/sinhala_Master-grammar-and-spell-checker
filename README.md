# Sinhala Grammar Checker Project

This project provides multiple approaches for building a Sinhala grammar checker, utilizing different methodologies such as Retrieval-Augmented Generation (RAG), rule-based approaches, and large language models (LLM). Additionally, it includes spell checker functionality.

## Project Structure

- **RAG Approach**: A grammar checker using the RAG approach for sentence correction.
- **Rule-Based Approach**: A traditional grammar checker based on predefined rules.
- **LLM-Based Approach**: A grammar checker leveraging a large language model for sentence correction.
- **Spell Checkers**: Spell checkers for detecting and correcting misspelled words in Sinhala.

## Setup Instructions

To run each approach, follow the steps below:

### 1. RAG Approach (Grammar Checker)
1. Navigate to the `RAG_approach_grammar_checker` folder.
2. Run the Python script:
   ```bash
   python rag.py
   ```
3. After the backend is running, navigate to the frontend folder and start the frontend server:
   ```bash
   npm start
   ```

### 2. Rule-Based Approach
1. Navigate to the rule-based approach folder.
2. Run the Python app:
   ```bash
   python app.py
   ```
3. After the backend is running, double-click on the `index.html` file in the frontend folder to open it in your browser.

### 3. LLM-Based Approach
1. Navigate to the LLM-based approach folder.
2. Run the Python app:
   ```bash
   python app.py
   ```
3. After the backend is running, double-click on the `index.html` file in the frontend folder to open it in your browser.

### 4. Spell Checkers
1. Navigate to the `spell_checker` folder, then to `spellchecker_App`.
2. Run the Python script:
   ```bash
   python run.py
   ```
3. After the backend is running, navigate to the frontend folder and start the frontend server:
   ```bash
   npm start
   ```

## Dependencies

Make sure you have the following dependencies installed:

- Python 3.x
- Node.js (for frontend)
- Necessary Python libraries (listed in the respective `requirements.txt` files for each folder)

To install Python dependencies:
```bash
pip install -r requirements.txt
```

To install frontend dependencies:
```bash
npm install
```

## Running the Application

1. For each approach, follow the setup instructions to start both the backend and frontend.
2. Open the appropriate `index.html` file or use the frontend server to interact with the application in your web browser.

## Contributing

Feel free to fork the repository, create branches, and contribute with improvements. If you'd like to propose a new feature or report an issue, please open an issue in the GitHub repository.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
