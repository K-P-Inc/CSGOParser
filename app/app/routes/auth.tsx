
// import './Auth.css';

import React, { useState } from 'react';

export default function Index() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e: any) => {
    e.preventDefault();

    // Perform authentication logic here (e.g., check credentials)
    // For simplicity, assume authentication is successful
    // setIsAuthenticated(true);
  };

  return (
    <>
      <div className="login-container">
        <h2>Вход</h2>
        <form className="login-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">Имя пользователя:</label>
            <input
              type="text"
              id="username"
              name="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Пароль:</label>
            <input
              type="password"
              id="password"
              name="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <button type="submit">Войти</button>
          </div>
        </form>
      </div>
    </>
  );
}