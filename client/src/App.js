import React, { useState } from 'react';
import Login from './components/Login';
import Game from './components/Game';
import './scss/App.scss';

const comps = {
  'Game': Game,
  'Login': Login
}

function App() {
  const token = window.localStorage.getItem('token');
  const [activeComponent, setActiveComponent] = useState(token ? 'Game' : 'Login');
  let CurrentComponent = comps[activeComponent];
  function componentWillUpdate(nP, nS) {
    CurrentComponent = comps[activeComponent];
  }
  
  return (<div className="App">
            <CurrentComponent token={token} setActiveComponent={setActiveComponent}/>
          </div>);
}

export default App;
