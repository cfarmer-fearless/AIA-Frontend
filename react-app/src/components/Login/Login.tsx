import React, { useState } from 'react';
import PropTypes from 'prop-types';
import './Login.css';

async function loginUser(credentials) {
  const { REACT_APP_AUTH_API_ENDPOINT } = process.env;
  return fetch(REACT_APP_AUTH_API_ENDPOINT, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(credentials)
  })
    .then(data => data.json());
}

export default function Login({ setToken }) {
  const [username, setUserName] = useState();
  const [password, setPassword] = useState();

  const handleSubmit = async e => {
    e.preventDefault();
    const response = await loginUser({
      'username': username,
      'password': password
    });
    if ('token' in response) {
      setToken(response['token']);
    } else {
      alert(response['ErrorMessage']);
    }
  };
  
  return(
    <div className="login-wrapper">
      <h2>Please Log In</h2>
      <form onSubmit={handleSubmit}>
        <label>
          <p>Username</p>
          <input type="text" onChange={e => setUserName(e.target.value)}/>
        </label>
        <label>
          <p>Password</p>
          <input type="password" onChange={e => setPassword(e.target.value)}/>
        </label>
        <div>
          <button type="submit">Submit</button>
        </div>
      </form>
    </div>
  );
}

Login.propTypes = {
  setToken: PropTypes.func.isRequired
};