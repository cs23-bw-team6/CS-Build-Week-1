import React, { useState, useEffect } from 'react';
import { axiosWithAuth } from '../axiosWithAuth';

import Compass from './Compass';
import WorldMap from './WorldMap';

import oldMap from '../assets/map.png';
import '../scss/Game.scss';

const Game = () => {
  const [rooms, setRooms] = useState(null);

  function logout() {
    window.localStorage.clear();
    window.location.reload();
  }

  async function fetchRoomData() {
    try {
      const { data } = await axiosWithAuth().get('adv/rooms/');
      const roomsDict = data.rooms;
      let roomsArray = [];
      for (let room in roomsDict) {
        let thisRoom = {
          ...roomsDict[room],
          id: room
        };
        roomsArray.push(thisRoom);
      }
      setRooms(roomsArray);
    } catch (err) {
      console.error(err);
    }
  }

  useEffect(() => {
    if (!rooms) fetchRoomData();
  }, [rooms]);

  console.log('WorldMap.js RENDER rooms', rooms);

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
        <WorldMap rooms={rooms} />
        <div className="Game__body__bottom">
          <section className="Commo">
            <div className="Room">Room Description</div>
            <div className="Inventory">Inventory</div>
          </section>
          <Compass fetchRoomData={fetchRoomData} />
        </div>
      </main>
    </section>
  );
};

export default Game;
