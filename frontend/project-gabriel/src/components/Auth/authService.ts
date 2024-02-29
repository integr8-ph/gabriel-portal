import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import "../Dashboard/Dashboard"

const useAuthService = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loginStatus, setLoginStatus] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    try {
        // Make an API call to your backend to check credentials
        // Assume mockResponse.ok is true if login is successful
        const mockResponse = { ok: true, access_token: 'some_token' };
  
        if (mockResponse.ok) {
          // Save the access token in localStorage
          localStorage.setItem('access_token', mockResponse.access_token);
  
          // Redirect to the dashboard or perform any action on successful login
          navigate('../Dashboard/Dashboard');
        } else {
          setLoginStatus('Login failed. Check your credentials.');
        }
      } catch (error) {
        console.error('Error during login:', error);
      }
  };

  return {
    username,
    setUsername,
    password,
    setPassword,
    loginStatus,
    handleLogin,
  };
};

export default useAuthService;
