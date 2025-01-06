import axios from 'axios';

// API call for spell checker 1
export const checkSpellChecker1 = async (word) => {
  try {
    const correction = await axios.post(`http://127.0.0.1:5000/api/spellchecker1/correct?word=${word}`);
    const suggestions = await axios.post(`http://127.0.0.1:5000/api/spellchecker1/suggestions?word=${word}`);
    return { correction: correction.data, suggestions: suggestions.data };
  } catch (error) {
    console.error('Error with Spell Checker 1 API', error);
  }
};

// API call for spell checker 2
export const checkSpellChecker2 = async (word) => {
  try {
    const correction = await axios.get(`http://127.0.0.1:5000/api/spellchecker2/correct?word=${word}`);
    const suggestions = await axios.get(`http://127.0.0.1:5000/api/spellchecker2/suggestions?word=${word}`);
    return { correction: correction.data, suggestions: suggestions.data };
  } catch (error) {
    console.error('Error with Spell Checker 2 API', error);
  }
};
