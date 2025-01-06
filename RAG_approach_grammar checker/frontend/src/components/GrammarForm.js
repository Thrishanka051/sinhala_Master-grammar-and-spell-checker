import React, { useState } from 'react';
import { TextField, Button, Box, CircularProgress, Typography } from '@mui/material';

const GrammarForm = ({ onSubmit }) => {
  const [sentence, setSentence] = useState('');
  const [loading, setLoading] = useState(false);
  const [correctedText, setCorrectedText] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const result = await onSubmit(sentence); // Assume onSubmit returns corrected sentence
      setCorrectedText(result); // Set the corrected sentence
    } catch (error) {
      console.error("Error correcting sentence:", error);
    }
    setLoading(false);
  };

  return (
    <Box
      component="form"
      onSubmit={handleSubmit}
      sx={{
        display: 'flex',
        flexDirection: 'column',
        gap: 2,
        width: '80%',
        
        margin: '0 auto',
        padding: '20px',
        borderRadius: '8px',
        boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)',
        backgroundColor: '#fff',
      }}
    >
      <TextField
        label="Enter Sentence"
        variant="outlined"
        fullWidth
        required
        multiline
        rows={4}
        value={sentence}
        onChange={(e) => setSentence(e.target.value)}
        sx={{
          '& .MuiOutlinedInput-root': {
            borderRadius: '8px',
            '& fieldset': {
              borderColor: '#007bff',
            },
            '&:hover fieldset': {
              borderColor: '#0056b3',
            },
          },
        }}
      />
      
      <Button
        type="submit"
        variant="contained"
        color="primary"
        disabled={loading}
        sx={{
          padding: '12px',
          fontSize: '1rem',
          fontWeight: 'bold',
          borderRadius: '8px',
          '&:hover': {
            backgroundColor: '#0056b3',
          },
        }}
      >
        {loading ? <CircularProgress size={24} color="inherit" /> : 'Correct Sentence'}
      </Button>

      {correctedText && (
  <Box
    sx={{
      marginTop: '20px',
      padding: '15px',
      backgroundColor: '#f9f9f9',
      borderRadius: '8px',
      width: '100%',
      textAlign: 'left',
      boxShadow: '0px 2px 6px rgba(0, 0, 0, 0.1)',
    }}
  >
    <Typography variant="h6" sx={{ fontWeight: 'bold', color: '#007bff', marginBottom: '8px' }}>
      Corrected Sentence:
    </Typography>
    <Typography variant="body1" sx={{ color: '#333', lineHeight: '1.6' }}>
      {correctedText}
    </Typography>
  </Box>
)}

    </Box>
  );
};

export default GrammarForm;
