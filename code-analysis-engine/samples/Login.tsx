import React, { useState } from 'react';
import { tokenAPICall } from './services/AuthService';

type LoginProps = {
  onLogin?: (username: string) => void;
};

export default function Login({ onLogin }: LoginProps) {
  const [username, setUsername] = useState('');

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    onLogin?.(username);
    tokenAPICall();
  }

  return (
    <form
      onSubmit={handleSubmit}
      style={{ display: 'flex', gap: 8, alignItems: 'center' }}
    >
      <label style={{ display: 'flex', gap: 6, alignItems: 'center' }}>
        <span>Username</span>
        <input
          value={username}
          onChange={(e) => setUsername((e.target as HTMLInputElement).value)}
          placeholder='Enter username'
        />
      </label>
      <button type='submit'>Login</button>
    </form>
  );
}

export { Login };
