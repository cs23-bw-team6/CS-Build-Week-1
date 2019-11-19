import React, { useState } from 'react';
import axios from 'axios';


const Map = () => {
    const baseUrl = process.env.REACT_APP_BACKEND;
    const map = await axios.post(postUrl, postData);
    return (
        <div>

        </div>
    );
}

export default Map;