import React from 'react';
import axios from 'axios';

const download_map = async () => {
    const url = 'https://treasure-hunting-cs23.herokuapp.com/api/adv/rooms';
    try {
        const new_map = await axios.get(url)
        return new_map
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