import React, { useState, useEffect } from 'react';
import oldMap from '../assets/map.png';
import Compass from './Compass';
import { axiosWithAuth } from '../axiosWithAuth';
import '../scss/Game.scss';

const Game = () => {
  function logout() {
    window.localStorage.clear();
    window.location.reload();
  }

  const [rooms, setRooms] = useState(null);

  useEffect(() => {
    const fetchRoomData = async () => {
      try {
        const { data } = await axiosWithAuth().get('adv/rooms/');
        setRooms(data.rooms);
      } catch (err) {
        console.error(err);
      }
    };
    if (!rooms) fetchRoomData();
  }, [rooms]);

  console.log('Game.js RENDER rooms', rooms);

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
