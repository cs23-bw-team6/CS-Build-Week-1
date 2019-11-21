import React, { useState, useEffect } from 'react';
import { axiosWithAuth } from '../axiosWithAuth';

import '../scss/WorldMap.scss';

const WorldMap = () => {
  const [rooms, setRooms] = useState(null);

  useEffect(() => {
    const fetchRoomData = async () => {
      try {
        const { data } = await axiosWithAuth().get('adv/rooms/');
        const roomsDict = data.rooms;
        console.log('WorldMap.js useEffect() roomsDict', roomsDict);
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
    };
    if (!rooms) fetchRoomData();
  }, [rooms]);

  console.log('WorldMap.js RENDER rooms', rooms);
  return (
    <section className="WorldMap">
      {rooms &&
        rooms.map(room => {
          return (
            <div
              className={
                room.players[2] ? 'WorldMap__room active' : 'WorldMap__room'
              }
              key={`${room.x}${room.y}`}
              style={{
                gridColumn: room.x + 1,
                gridRow: room.y + 1
              }}
            >
              {room.id}
            </div>
          );
        })}
    </section>
  );
};

export default WorldMap;
