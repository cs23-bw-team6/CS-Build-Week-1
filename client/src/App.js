import React from 'react';
import Login from './components/Login';
import Game from './components/Game';
import './scss/App.scss';

function App() {
  const token = window.localStorage.getItem('token');
  return <div className="App">{token ? <Game /> : <Login />}</div>;
}

export default App;
