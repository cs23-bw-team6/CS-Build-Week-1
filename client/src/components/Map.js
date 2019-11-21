import React, { useState } from 'react';
import axios from 'axios';
const BASE_URL = process.env.REACT_APP_BACKEND || 'https://treasure-hunting-cs23.herokuapp.com/';


const Map = () => {
    const [map, setMap] = useState('');
    const download_map = async () => {
        const url = `${BASE_URL}api/adv/rooms/`;
        try {
            const new_map = await axios.get(url);
            setMap(new_map.data.rooms);
        } catch(err) {
            return console.error(err);
        }
        
    }
    if (map === '') {
        download_map();
    }
    if (!(map==='')) {
        console.log(map);
    }
    return (
        <div>

        </div>
    );
}

export default Map;