import React, { useState, useEffect } from 'react';
import { axiosWithAuth } from '../axiosWithAuth';
import regeneratorRuntime from "regenerator-runtime";

import Commo from './Commo';
import Compass from './Compass';
import WorldMap from './WorldMap';

import oldMap from '../assets/map.png';
import '../scss/Game.scss';

const baseUrl = process.env.REACT_APP_BACKEND || 'https://treasure-hunting-cs23.herokuapp.com/';

const Game = () => {
  const [rooms, setRooms] = useState(null);
  const [player, setPlayer] = useState(null);
  const [holding, pickup] = useState([]);

  function logout() {
    window.localStorage.clear();
    window.location.reload();
  }

  async function fetchRoomData() {
    try {
      const { data } = await axiosWithAuth().get(`${baseUrl}api/adv/rooms/`);
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

  async function fetchPlayerData() {
    try {
      const { data } = await axiosWithAuth().get(`${baseUrl}api/adv/init/`);
      console.log('fetchplayerdata ', data);
      setPlayer(data);
    } catch (err) {
      console.error(err);
    }
  }

  useEffect(() => {
    if (!rooms) fetchRoomData();
    if (!player) fetchPlayerData();
  }, [player, rooms]);

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
          <Commo
            player={player}
            fetchPlayerData={fetchPlayerData}
            holding={holding}
            pickup={pickup}
          />
          <Compass
            fetchRoomData={fetchRoomData}
            fetchPlayerData={fetchPlayerData}
          />
        </div>
      </main>
    </section>
  );
};

export default Game;
