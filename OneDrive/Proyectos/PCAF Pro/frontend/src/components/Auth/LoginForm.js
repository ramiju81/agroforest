// src/components/Auth/LoginForm.js
import { useState } from 'react';
import './LoginForm.css';

const LoginForm = ({ onLogin }) => {
  const [credentials, setCredentials] = useState({
    email: '',
    password: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials)
      });
      const data = await response.json();
      onLogin(data.token);
    } catch (error) {
      console.error('Login error:', error);
    }
  };

  return (
    <div className="auth-container">
      <form onSubmit={handleSubmit} className="auth-form">
        <h2>Iniciar Sesión en PCAF</h2>
        <input
          type="email"
          placeholder="Correo electrónico"
          value={credentials.email}
          onChange={(e) => setCredentials({...credentials, email: e.target.value})}
          required
        />
        <input
          type="password"
          placeholder="Contraseña"
          value={credentials.password}
          onChange={(e) => setCredentials({...credentials, password: e.target.value})}
          required
        />
        <button type="submit">Entrar</button>
        <div className="auth-links">
          <a href="/forgot-password">¿Olvidaste tu contraseña?</a>
          <a href="/register">Registrarse</a>
        </div>
      </form>
    </div>
  );
};

export default LoginForm;