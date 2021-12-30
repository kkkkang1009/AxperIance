import * as React from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Menu from '../common/Menu.js'
import FilmRate from '../service/language/FilmRate.js';
import Chatbot from '../service/language/Chatbot.js';

function App() {
  return (
    <div>
      <BrowserRouter>
        <Menu></Menu>
        <Routes>
          <Route path="/" element={<FilmRate />} />
          <Route path="/filmrate" element={<FilmRate />} />
          <Route path="/chatbot" element={<Chatbot />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
