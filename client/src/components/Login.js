import React, { useState } from 'react';
import axios from 'axios';
import './Login.scss';

// process.env.REACT_APP_BACKEND = 'https://treasure-hunting-cs23.herokuapp.com';

const Login = (user, setUser) => {
	const baseUrl = 'https://treasure-hunting-cs23.herokuapp.com';

	const [newUser, setNewUser] = useState(true);

	const [formData, setFormData] = useState({
		username: '',
		password1: '',
		password2: ''
	});

	const handleChange = e => {
		setFormData({
			...formData,
			[e.target.name]: e.target.value
		});
	};

	const handleSubmit = async e => {
		e.preventDefault();
		const postUrl = newUser ? `${baseUrl}/api/registration/` : `${baseUrl}/api/login/`;
		const postData = newUser
			? formData
			: { username: formData.username, password: formData.password1 };
		try {
			console.log(postData);
			const res = await axios.post(postUrl, postData);
			window.localStorage.setItem('token', res.data.key);
		} catch (err) {
			console.error(err);
		}
	};

	return (
		<section className="Login">
			<div className="Login__toggle">
				<p className={newUser ? 'active' : ''} onClick={() => setNewUser(true)}>
					Register
				</p>
				<p
					className={newUser ? '' : 'active'}
					onClick={() => setNewUser(false)}>
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

				<label htmlFor="password1">Password</label>
				<input
					id="password1"
					name="password1"
					type="text"
					onChange={handleChange}
				/>

				{newUser ? (
					<>
						<label htmlFor="password2">Enter password again to verify</label>
						<input
							id="password2"
							name="password2"
							type="text"
							onChange={handleChange}
						/>
						<button>Register</button>
					</>
				) : (
					<button>Login</button>
				)}
			</form>
		</section>
	);
};

export default Login;
