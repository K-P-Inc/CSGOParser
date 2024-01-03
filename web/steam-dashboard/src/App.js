// App.js
import React, { useState, useEffect } from 'react';
import './App.css';
import Sidebar from './components/Sidebar';
import MainContainer from './components/MainContainer';
import Auth from './components/Auth';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    // Используйте localStorage.getItem для чтения состояния аутентификации при загрузке
    return JSON.parse(localStorage.getItem('isAuthenticated')) || false;
  });

  const [activeSection, setActiveSection] = useState('inventory');

  const switchSection = (section) => {
    setActiveSection(section);
  };

  const logout = () => {
    // При выходе также обновляем состояние и localStorage
    setIsAuthenticated(false);
    localStorage.removeItem('isAuthenticated');
    window.location = "file:///Users/Git/skins_parser/web/auth_night.html";
  };

  useEffect(() => {
    // При изменении состояния аутентификации обновляем localStorage
    localStorage.setItem('isAuthenticated', JSON.stringify(isAuthenticated));
  }, [isAuthenticated]);

  return (
    <div className="App">
      {isAuthenticated ? (
        <>
          <Sidebar activeSection={activeSection} switchSection={switchSection} logout={logout} />
          <MainContainer activeSection={activeSection} />
        </>
      ) : (
        <Auth setIsAuthenticated={setIsAuthenticated} />
      )}
    </div>
  );
}

export default App;
