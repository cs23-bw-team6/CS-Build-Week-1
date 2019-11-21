import React, { useState } from 'react';
import axios from 'axios';
const BASE_URL = process.env.REACT_APP_BACKEND || 'https://treasure-hunting-cs23.herokuapp.com/';


const Map = () => {
    const [rooms, setRooms] = useState('');
    const [grid, setGrid] = useState([]);

    const download_rooms = async () => {
        const url = `${BASE_URL}api/adv/rooms/`;
        try {
            const new_map = await axios.get(url);
            setRooms(new_map.data.rooms);
        } catch(err) {
            return console.error(err);
        }
        
    }
    if (rooms === '') {
        download_rooms();
    }
    if (!(rooms==='')) {
        console.log(rooms);
        for (let i in rooms) {
            let dupeGrid = grid;
            dupeGrid[rooms[i].x][rooms[i].y] = rooms[i];
            setGrid(dupeGrid);
        }
        console.log(grid);
    }
    return (
        <div>

        </div>
    );
}

export default Map;