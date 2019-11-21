import React from 'react';
import '../scss/Commo.scss';

const Commo = ({ player }) => {
  return (
    <section className="Commo">
      {player ? (
        <>
          <div className="room-description">
            <header>{player.title}</header>
            <p>{player.description}</p>
          </div>
          <div className="room-items">Items here: {player.items}</div>
          <div className="room-containers">
            Containers here: {player.containers}
          </div>
        </>
      ) : (
        <div className="loading">Loading...</div>
      )}
    </section>
  );
};

export default Commo;
