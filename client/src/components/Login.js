import React, { useState } from 'react';
import axios from 'axios';
import oldMap from '../assets/map.png';
import '../scss/Login.scss';

const Login = () => {
  const baseUrl = process.env.REACT_APP_BACKEND || 'https://treasure-hunting-cs23.herokuapp.com/';

  const [newUser, setNewUser] = useState(true);

  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });

  const handleChange = e => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async e => {
    e.preventDefault();
    const postUrl = newUser ? `${baseUrl}api/registration/` : `${baseUrl}api/login/`;
    const postData = newUser
      ? {
          username: formData.username,
          password1: formData.password,
          password2: formData.password
        }
      : { username: formData.username, password: formData.password };
    try {
      console.log(postUrl);
      const res = await axios.post(postUrl, postData);
      window.localStorage.setItem('token', res.data.key);
      window.location.reload();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="Login__container">
      <section className="Login__left-side">
        <h1>ADVENTURE GAME</h1>
        <img src={oldMap} alt="old map with scope and compass" />
      </section>

      <section className="Login__right-side">
        <div className="Login__toggle">
          <p
            className={newUser ? 'active' : ''}
            onClick={() => setNewUser(true)}
          >
            Register
          </p>
          <p
            className={newUser ? '' : 'active'}
            onClick={() => setNewUser(false)}
          >
            Login
          </p>
        </div>
        <form className="Login__form" onSubmit={handleSubmit}>
          <label htmlFor="username">Username</label>
          <input
            id="username"
            name="username"
            type="text"
            onChange={handleChange}
          />

          <label htmlFor="password">Password</label>
          <input
            id="password"
            name="password"
            type="text"
            onChange={handleChange}
          />

          {newUser ? <button>Register</button> : <button>Login</button>}
        </form>
      </section>
    </div>
  );
};

export default Login;
