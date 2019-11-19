import React, { useState } from 'react';
import Map from 'Map.js';

const Game = () => {
    const baseUrl = process.env.REACT_APP_BACKEND;
    
    return (<div>
        <header>LambdaMUD</header>
        <div>
            <nav></nav>
            <Map />
        </div>
        
    </div>);
}

export default Game;