import React from 'react';
import HomePage from './pages/HomePage';
import { Box } from '@mui/material';

const App = () => {
  return (
    <Box
      sx={{
        minHeight: '100vh', // Ensures the background color covers the entire viewport height
        backgroundColor: '#f0f8ff' // Light blue
        
        
      }}
    >
      <HomePage />
    </Box>
  );
};

export default App;
