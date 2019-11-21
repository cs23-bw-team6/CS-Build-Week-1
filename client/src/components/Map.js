import React from 'react';
import axios from 'axios';
const BASE_URL = process.env.REACT_APP_BACKEND || 'https://treasure-hunting-cs23.herokuapp.com/';
const download_map = async (token) => {
    const url = 'api/adv/rooms/';
    try {
        const new_map = await axios.get(url, { 'headers': {'Authorization': `Token ${token}`}});
        return new_map;
    } catch(err) {
        console.error(err);
    }
    
}

const Map = (token) => {
    const map = download_map(token);
    console.log(map);
    return (
        <div>

        </div>
    );
}

export default Map;