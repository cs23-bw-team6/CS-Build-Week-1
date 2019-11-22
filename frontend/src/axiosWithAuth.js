import axios from 'axios';

export const axiosWithAuth = () => {
  const token = localStorage.getItem('token');

  return axios.create({
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Token ${token}`
    },
    baseURL: `${process.env.REACT_APP_BACKEND || 'https://treasure-hunting-cs23.herokuapp.com/'}`
  });
};
