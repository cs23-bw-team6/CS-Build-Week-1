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
                gridRow: room.y + 1,
                borderTop: `${room.n_to ? '0' : '2'}px solid beige`,
                borderRight: `${room.w_to ? '0' : '2'}px solid beige`,
                borderBottom: `${room.s_to ? '0' : '2'}px solid beige`,
                borderLeft: `${room.e_to ? '0' : '2'}px solid beige`
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
