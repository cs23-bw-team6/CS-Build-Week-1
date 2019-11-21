import React from 'react';
import oldMap from '../assets/map.png';
import Compass from './Compass';
import '../scss/Game.scss';

const baseUrl = process.env.REACT_APP_BACKEND

const initializeUser = async token => {
	let user = {}
	const postUrl = `${baseUrl}/api/adv/initialize/`;
	try{
		user = await axios.get(postUrl, { headers: {'Authorization': `Token ${token}`} });
	} catch(err) {
		console.error(err);
		localStorage.removeItem('token');
		return null;
	}
	return user;


}

const Game = (token) => {
  const [user, setUser] = useState(initializeUser)
  function logout() {
    window.localStorage.clear();
    window.location.reload();
  }

  return (
    <section className="Game">
      <header className="Game__header">
        <img
          onClick={logout}
          src={oldMap}
          alt="old map with scope and compass"
        />
        <h1>ADVENTURE GAME</h1>
      </header>

      <main className="Game__body">
        <div className="WorldMap">WorldMap</div>
        <div className="Game__body__bottom">
          <section className="Commo">
            <div className="Room">Room Description</div>
            <div className="Inventory">Inventory</div>
          </section>
          <Compass />
        </div>
      </main>
    </section>
  );
};

export default Game;
