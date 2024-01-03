import React from 'react';
import './MainContainer.css';
import AccountSection from './AccountSection';
import InventorySection from './InventorySection';
import WatchlistSection from './WatchlistSection';
import SettingsSection from './SettingsSection';

function MainContainer({ activeSection }) {
  return (
    <div className="main-container">
      {activeSection === 'account' && <AccountSection />}
      {activeSection === 'inventory' && <InventorySection />}
      {activeSection === 'watchlist' && <WatchlistSection />}
      {activeSection === 'settings' && <SettingsSection />}
    </div>
  );
}

export default MainContainer;
