import React, { useState } from 'react';
import Login from './components/Login';
import Game from './components/Game';
import './scss/App.scss';

function App() {
  const [token, setToken] = useState(window.localStorage.getItem('token'));

  return <div className="App">{token ? <Game /> : <Login setToken={setToken}/>}</div>;
}

export default App;
