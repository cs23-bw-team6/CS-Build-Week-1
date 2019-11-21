import React from 'react';
import oldMap from '../assets/map.png';
import Compass from './Compass';
import '../scss/Game.scss';

const Game = () => {
  return (
    <section className="Game">
      <header className="Game__header">
        <img src={oldMap} alt="old map with scope and compass" />
        <h1>ADVENTURE GAME</h1>
      </header>

      <main className="Game__body">
        <section className="Game__body-left">
          <div className="WorldMap">WorldMap</div>
          <div className="Commo">Commo</div>
        </section>
        <section className="Game__body-right">
          <div className="Inventory">Inventory</div>
          <Compass />
        </section>
      </main>
    </section>
  );
};

export default Game;
