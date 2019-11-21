import React from 'react';

import '../scss/WorldMap.scss';

const WorldMap = ({ rooms }) => {
  return (
    <section className="WorldMap">
      {rooms &&
        rooms.map(room => {
          return (
            <div
              className={
                Object.keys(room.players).length > 0
                  ? 'WorldMap__room active'
                  : 'WorldMap__room'
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
