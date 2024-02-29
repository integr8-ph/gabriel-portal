import { useState } from 'react';
import React from 'react';


import '../../App.css'
import cover from '../../assets/LoginAssets/cover1.png'
import logo from '../../assets/LoginAssets/logo.png'


import { Link } from 'react-router-dom'
import { FaUserShield } from "react-icons/fa";
import { RiLockPasswordFill } from "react-icons/ri";


function Login() {

    const [username, setUsername] = useState<string>('');
    const [password, setPassword] = useState<string>('');

    const handleLogin = async () => {
        try {
            const response = await fetch('http://127.0.0.1:8000/login/access-token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });

            if (response.ok) {
                const data = await response.json();
                const accessToken = data.access_token;

                // Save the access token to local storage
                localStorage.setItem('access_token', accessToken);

                // Optionally, you can redirect to another page using React Router
                // Example: history.push('/dashboard');
            } else {
                // Handle login failure, show error message, etc.
                console.error('Login failed:', response.status);
            }
        } catch (error) {
            console.error('Login error:', error);
        }
    };


    return (
        <div className='loginPage flex'>
            <div className='container flex'>

                <div className="coverDiv">
                    <img src={cover} className="cover" alt="Background Cover"></img>
                    <center>
                        <div className="footerDiv flex">
                            <span className='text'>Need Assistance? </span>
                            <Link to={'/contact'}>
                                <button className='btn'>Contact Us</button>
                            </Link>
                        </div>
                    </center>
                </div>
                
                <div className="formDiv flex">
                    <div className="headerDiv">
                        <img src={logo} alt="Logo Image"/>
                    </div>

                    <form onSubmit={handleLogin} className='form grid'>

                        {/* <span>Login status will go here</span> */}
                        
                        <div className="inputDiv">
                            <label htmlFor='username'>Username</label>
                            <div className="input flex">
                                <FaUserShield className='icon'/>
                                <input 
                                    type="text" 
                                    id='username' 
                                    name="username" 
                                    placeholder='Enter username'
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                />
                            </div>
                        </div>

                        <div className="inputDiv">
                            <label htmlFor='password'>Password</label>
                            <div className="input flex">
                                <RiLockPasswordFill className='icon'/>
                                <input 
                                    type="password"
                                    id='password'
                                    name="password"
                                    placeholder='Enter password'
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                />
                            </div>
                        </div>

                        <button type='submit' className='loginbtn flex'>
                            <span>LOGIN</span>
                        </button>

                        <span className='forgotPassword'>
                            Forgot your password? <a href="">Click Here</a>
                        </span>
                    </form>
                </div>
                
            </div>
        </div>
    )
}

export default Login