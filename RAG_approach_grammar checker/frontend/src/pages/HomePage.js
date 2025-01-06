import React, { useState } from 'react';
import GrammarForm from '../components/GrammarForm';
import { correctSentence } from '../utils/api';
import { Box, Typography } from '@mui/material';

const HomePage = () => {
  const [correctedSentence, setCorrectedSentence] = useState('');

  const handleGrammarCorrection = async (sentence) => {
    try {
      const result = await correctSentence(sentence);
      setCorrectedSentence(result.corrected_sentence);
    } catch (error) {
      alert(error.error || 'An error occurred!');
    }
  };

  return (
    <Box sx={{ padding: 4 }}>
      <Typography
        variant="h4"
        gutterBottom
        align="center"
        sx={{
          fontWeight: 'bold',
          color: '#007bff',
          fontSize: '2rem',
          textTransform: 'uppercase',
          letterSpacing: '2px',
          marginBottom: 3,
          fontFamily: "'Roboto', sans-serif",
          textShadow: '2px 2px 5px rgba(0, 123, 255, 0.3)',
          '@media (max-width:600px)': {
            fontSize: '1.5rem',
            textTransform: 'none',
          },
        }}
      >
        සිංහල Master Grammar & Spell Checker
      </Typography>

      <GrammarForm onSubmit={handleGrammarCorrection} />
{correctedSentence && (
      <Box
        sx={{
          width: '80%',
          margin: '0 auto',
          border: '1px solid #ccc',
          padding: '16px',
          borderRadius: '8px',
          backgroundColor: '#f9f9f9',
          marginTop: 4,
        }}
      >
        <Typography variant="h6">Corrected Sentence:</Typography>
        <Typography variant="body1">{correctedSentence}</Typography>
      </Box>)}
    </Box>
  );
};

export default HomePage;
