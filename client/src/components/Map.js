import React from 'react';
import axios from 'axios';
const BASE_URL = process.env.REACT_APP_BACKEND || 'https://treasure-hunting-cs23.herokuapp.com/';
const download_map = async () => {
    const url = 'api/adv/rooms/';
    try {
        const new_map = await axios.get(url);
        return new_map;
    } catch(err) {
        console.error(err);
    }
    
}

const Map = (user) => {
    const map = download_map();
    console.log(map);
    return (
        <div>

        </div>
    );
}

export default Map;