import React from 'react';
import { useNavigate } from 'react-router-dom';

const HomePage = () => {
  const navigate = useNavigate();

  const styles = {
    container: {
      height: '100vh',
      display: 'flex',
      background: 'linear-gradient(to bottom right, #EEF2FF, #F5F3FF)',
      padding: '24px',
      gap: '24px'
    },
    box: {
      flex: 1,
      background: 'white',
      borderRadius: '12px',
      boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      cursor: 'pointer',
      transition: 'transform 0.2s, box-shadow 0.2s',
      padding: '24px',
      textDecoration: 'none',
      color: '#1F2937'
    },
    boxHover: {
      transform: 'translateY(-4px)',
      boxShadow: '0 8px 12px rgba(0, 0, 0, 0.15)'
    },
    title: {
      fontSize: '24px',
      fontWeight: 'bold',
      marginBottom: '12px'
    },
    description: {
      fontSize: '16px',
      textAlign: 'center',
      color: '#6B7280'
    }
  };

  return (
    <div style={styles.container}>
      <div 
        onClick={() => navigate('/spellchecker1')}
        style={styles.box}
        onMouseOver={e => {
          e.currentTarget.style.transform = 'translateY(-4px)';
          e.currentTarget.style.boxShadow = '0 8px 12px rgba(0, 0, 0, 0.15)';
        }}
        onMouseOut={e => {
          e.currentTarget.style.transform = 'translateY(0)';
          e.currentTarget.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
        }}
      >
        <h2 style={styles.title}>Spell Checker 1</h2>
        <p style={styles.description}>Advanced spell checking with suggestions</p>
      </div>

      <div 
        onClick={() => navigate('/spellchecker2')}
        style={styles.box}
        onMouseOver={e => {
          e.currentTarget.style.transform = 'translateY(-4px)';
          e.currentTarget.style.boxShadow = '0 8px 12px rgba(0, 0, 0, 0.15)';
        }}
        onMouseOut={e => {
          e.currentTarget.style.transform = 'translateY(0)';
          e.currentTarget.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
        }}
      >
        <h2 style={styles.title}>Spell Checker 2</h2>
        <p style={styles.description}>Alternative spell checking interface</p>
      </div>
    </div>
  );
};

export default HomePage;