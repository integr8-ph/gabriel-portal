import React from 'react';
import './Login.css'
import '../../App.css'
import { Link } from 'react-router-dom'

//Import Assets
import cover from '../../assets/LoginAssets/cover.png'
import logo from '../../assets/LoginAssets/logo.jpg'

//Import Icons
import { FaUserShield } from "react-icons/fa";
import { RiLockPasswordFill } from "react-icons/ri";
// import { MdHeight } from 'react-icons/md';

function Login() {
    return (
        // <div>
        //     <a href="/dashboard">to dashboard</a> <br />
        //     <a href="/login">to login</a> <br />
        //     This is login page
        // </div>

        <div className='loginPage flex'>
            <div className='container flex'>

                <div className="coverDiv">
                    <img src={cover} className="cover" alt="Background Cover"></img>

                    <div className="textDiv">
                        <h2 className='title'></h2>
                        <p>Adopt the fast pace innovation!</p>
                    </div>

                    <div className="footerDiv flex">
                        <span className='text'>Need Assistance? </span>
                        <Link to={'/contact'}>
                            <button className='btn'>Contact Us</button>
                        </Link>
                    </div>
                </div>
                
                <div className="formDiv flex">
                    <div className="headerDiv">
                        {/* <img src={logo} alt="Logo Image"/> */}
                        <h3>Welcome Back!</h3>
                    </div>

                    <form action="" className='form grid'>
                        <span>Login status will go here</span>
                        <div className="inputDiv">
                            <label htmlFor='username'>Username</label>
                            <div className="input flex">
                                <FaUserShield className='icon'/>
                                <input type="text" id='username' placeholder='Enter username'/>
                            </div>
                        </div>

                        <div className="inputDiv">
                            <label htmlFor='password'>Password</label>
                            <div className="input flex">
                                <RiLockPasswordFill className='icon'/>
                                <input type="password" id='password' placeholder='Enter password'/>
                            </div>
                        </div>

                        <button type='submit' className='btn flex'>
                            <span>LOGIN</span>
                        </button><br />

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