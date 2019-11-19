import React from 'react';
import Login from './components/Login';
import oldMap from './assets/map.png';
import './App.scss';

function App() {
	return (
		<div className="App">
			<section className="left-side">
				<h1>ADVENTURE GAME</h1>
				<img src={oldMap} alt="old map with scope and compass" />
			</section>
			<Login />
		</div>
	);
}

export default App;
