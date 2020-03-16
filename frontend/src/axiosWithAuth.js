import axios from 'axios';

export const axiosWithAuth = () => {
  const token = localStorage.getItem('token');
  console.log(token);
  return axios.create({
    headers: {
      'Authorization': `Token ${token}`,
      'withCredentials': true,
    },
    baseURL: `${process.env.REACT_APP_BACKEND || 'https://treasure-hunting-cs23.herokuapp.com/'}`
  });
};
