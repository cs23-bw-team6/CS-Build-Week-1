import React from 'react';
import compass11 from '../assets/compass/compass11.png';
import compass12 from '../assets/compass/compass12.png';
import compass13 from '../assets/compass/compass13.png';
import compass21 from '../assets/compass/compass21.png';
import compass22 from '../assets/compass/compass22.png';
import compass23 from '../assets/compass/compass23.png';
import compass31 from '../assets/compass/compass31.png';
import compass32 from '../assets/compass/compass32.png';
import compass33 from '../assets/compass/compass33.png';
import '../scss/Compass.scss';

const Compass = () => {
  return (
    <section className="Compass">
      <img src={compass11} alt="compass piece" />
      <img
        alt="NORTH compass piece"
        className="clickable"
        name="n"
        src={compass12}
      />
      <img src={compass13} alt="compass piece" />
      <img
        alt="WEST compass piece"
        className="clickable"
        name="w"
        src={compass21}
      />
      <img src={compass22} alt="compass piece" />
      <img
        alt="EAST compass piece"
        className="clickable"
        name="e"
        src={compass23}
      />
      <img src={compass31} alt="compass piece" />
      <img
        alt="SOUTH compass piece"
        className="clickable"
        name="s"
        src={compass32}
      />
      <img src={compass33} alt="compass piece" />
    </section>
  );
};

export default Compass;
