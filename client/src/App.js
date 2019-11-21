import React from 'react';
import Login from './components/Login';
import Map from './components/Map';
import oldMap from './assets/map.png';
import axios from 'axios';
import './App.scss';

const initializeUser = async token => {
	let user = {}
	const postUrl = 'https://treasure-hunting-cs23.herokuapp.com/api/adv/initialize/';
	try{
		user = await axios.get(postUrl, { headers: {'Authorization': `Token ${token}`} });
	} catch(err) {
		console.error(err);
		localStorage.removeItem('token');
		return null;
	}
	return user;


}


function App() {
	// const baseUrl = 'https://treasure-hunting-cs23.herokuapp.com';
	const token = window.localStorage.getItem('token') || '';
	const [user, setUser] = React.useState(null);
	if (!(token === '') && user === null) {
		setUser(initializeUser(token));
	}
	
	return (
		<div className="App">
			<section className="left-side">
				<h1>ADVENTURE GAME</h1>
				<img src={oldMap} alt="old map with scope and compass" />
			</section>
			{user !== null ? (<Map user={user} />) : (<Login user={user} setUser={setUser}/>)}
			{/* <Map /> */}
		</div>
	);
}

export default App;
