import React from 'react';
import SpellChecker1 from './components/SpellChecker1';
import SpellChecker2 from './components/SpellChecker2';

import './App.css'; // Include your CSS file

function App() {
  return (
    <div className="App">
      <div className="flex-container">
        <div className="spell-checker">
          <SpellChecker1 />
        </div>
        <div className="spell-checker">
          <SpellChecker2 />
        </div>
      </div>
    </div>
  );
}



export default App;
