import React from 'react';
import './Sidebar.css'; // Путь к вашему файлу со стилями Sidebar

function Sidebar({ activeSection, switchSection, logout }) {
  return (
    <div className="sidebar">
      <div className={`menu-item ${activeSection === 'account' ? 'active' : ''}`} onClick={() => switchSection('account')}>Аккаунт</div>
      <div className={`menu-item ${activeSection === 'inventory' ? 'active' : ''}`} onClick={() => switchSection('inventory')}>Инвентарь</div>
      <div className={`menu-item ${activeSection === 'watchlist' ? 'active' : ''}`} onClick={() => switchSection('watchlist')}>Отслеживаемое</div>
      <div className={`menu-item ${activeSection === 'settings' ? 'active' : ''}`} onClick={() => switchSection('settings')}>Настройки</div>
      <button className="logout-btn" onClick={logout}>Выйти</button>
    </div>
  );
}

export default Sidebar;
