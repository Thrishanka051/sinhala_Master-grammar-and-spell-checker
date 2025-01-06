import React, { useState } from 'react';

const SpellChecker = () => {
  const [word, setWord] = useState('');
  const [correction, setCorrection] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const styles = {
    container: {
      minHeight: '100vh',
      background: 'linear-gradient(to bottom right, #EEF2FF, #F5F3FF)',
      padding: '48px 16px'
    },
    card: {
      maxWidth: '500px',
      margin: '0 auto',
      background: 'white',
      borderRadius: '12px',
      boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
      overflow: 'hidden'
    },
    cardInner: {
      padding: '32px'
    },
    title: {
      fontSize: '32px',
      fontWeight: 'bold',
      color: '#1F2937',
      marginBottom: '32px',
      textAlign: 'center'
    },
    form: {
      display: 'flex',
      flexDirection: 'column',
      gap: '16px'
    },
    input: {
      width: '100%',
      padding: '16px 24px',
      fontSize: '18px',
      borderRadius: '8px',
      border: '1px solid #E5E7EB',
      outline: 'none',
      transition: 'all 0.2s',
    },
    button: {
      width: '100%',
      padding: '16px 24px',
      fontSize: '18px',
      fontWeight: '500',
      color: 'white',
      backgroundColor: '#4F46E5',
      border: 'none',
      borderRadius: '8px',
      cursor: 'pointer',
      transition: 'background-color 0.2s'
    },
    buttonHover: {
      backgroundColor: '#4338CA'
    },
    error: {
      marginTop: '24px',
      padding: '16px',
      backgroundColor: '#FEF2F2',
      color: '#DC2626',
      borderRadius: '8px'
    },
    resultSection: {
      marginTop: '24px'
    },
    sectionTitle: {
      fontSize: '20px',
      fontWeight: '600',
      color: '#374151',
      marginBottom: '8px'
    },
    correction: {
      padding: '16px',
      backgroundColor: '#F0FDF4',
      color: '#15803D',
      borderRadius: '8px',
      fontSize: '18px'
    },
    suggestionList: {
      listStyle: 'none',
      padding: 0,
      margin: 0,
      display: 'flex',
      flexDirection: 'column',
      gap: '8px'
    },
    suggestionItem: {
      padding: '12px',
      backgroundColor: '#F9FAFB',
      borderRadius: '8px',
      color: '#374151',
      fontSize: '18px',
      cursor: 'pointer',
      transition: 'background-color 0.2s'
    },
    spinner: {
      display: 'inline-block',
      width: '20px',
      height: '20px',
      marginRight: '8px',
      border: '2px solid white',
      borderTop: '2px solid transparent',
      borderRadius: '50%',
      animation: 'spin 1s linear infinite'
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const wordData = { text: word };
      const correctionResponse = await fetch('http://127.0.0.1:5000/api/spellchecker1/correct', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(wordData)
      });
      const suggestionsResponse = await fetch('http://127.0.0.1:5000/api/spellchecker1/suggestions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(wordData)
      });

      const correctionData = await correctionResponse.json();
      const suggestionsData = await suggestionsResponse.json();

      setCorrection(correctionData.corrected_text);
      setSuggestions(suggestionsData.suggestions);
    } catch (err) {
      setError('Error fetching data from APIs');
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <div style={styles.cardInner}>
          <h1 style={styles.title}>Spell Checker 01</h1>
          
          <form onSubmit={handleSubmit} style={styles.form}>
            <input
              type="text"
              value={word}
              onChange={(e) => setWord(e.target.value)}
              placeholder="Enter a word"
              required
              style={styles.input}
            />
            
            <button
              type="submit"
              disabled={loading}
              style={{
                ...styles.button,
                opacity: loading ? 0.5 : 1,
              }}
            >
              {loading ? (
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <div style={styles.spinner} />
                  <span>Checking...</span>
                </div>
              ) : (
                'Check Spelling'
              )}
            </button>
          </form>

          {error && <div style={styles.error}>{error}</div>}

          {correction && (
            <div style={styles.resultSection}>
              <h3 style={styles.sectionTitle}>Corrected Text</h3>
              <p style={styles.correction}>{correction}</p>
            </div>
          )}

          {suggestions.length > 0 && (
            <div style={styles.resultSection}>
              <h3 style={styles.sectionTitle}>Suggestions</h3>
              <ul style={styles.suggestionList}>
                {suggestions[0].map((suggestion, index) => (
                  <li
                    key={index}
                    style={styles.suggestionItem}
                  >
                    {suggestion}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SpellChecker;