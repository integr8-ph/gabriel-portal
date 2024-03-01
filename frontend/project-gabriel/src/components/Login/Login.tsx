import React, { useState } from "react";
import "../../App.css";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";

import cover from "../../assets/LoginAssets/cover1.png";
import logo from "../../assets/LoginAssets/logo.png";

import { FaUserShield } from "react-icons/fa";
import { RiLockPasswordFill } from "react-icons/ri";

const Login = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [loginStatus, setLoginStatus] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (e: React.ChangeEvent<HTMLFormElement>) => {
        e.preventDefault();

        const formData = new FormData();
        formData.append("username", username);
        formData.append("password", password);

        try {
            const response = await axios.post(
                "http://127.0.0.1:8000/login/access-token",
                formData
            );

            // Axios automatically parses the response JSON
            const data = response.data;
            localStorage.setItem("accessToken", data["access_token"]);

            navigate("/");
        } catch (error) {
            setLoginStatus("Invalid Username or Password");
        }

    };

    return (
        <div className="loginPage flex">
            <div className="container flex">
                <div className="coverDiv">
                    <img
                        src={cover}
                        className="cover"
                        alt="Background Cover"
                    ></img>
                    <center>
                        <div className="footerDiv flex">
                            <span className="text">Need Assistance? </span>
                            <Link to={"/contact"}>
                                <button className="btn">Contact Us</button>
                            </Link>
                        </div>
                    </center>
                </div>

                <div className="formDiv flex">
                    <div className="headerDiv">
                        <img src={logo} alt="Logo Image" />
                    </div>

                    <form onSubmit={handleSubmit} className="form grid">
                        <span>{loginStatus}</span>

                        <div className="inputDiv">
                            <label htmlFor="username">Username</label>
                            <div className="input flex">
                                <FaUserShield className="icon" />
                                <input
                                    type="text"
                                    id="username"
                                    name="username"
                                    placeholder="Enter username"
                                    onChange={(e) =>
                                        setUsername(e.target.value)
                                    }
                                />
                            </div>
                        </div>

                        <div className="inputDiv">
                            <label htmlFor="password">Password</label>
                            <div className="input flex">
                                <RiLockPasswordFill className="icon" />
                                <input
                                    type="password"
                                    id="password"
                                    name="password"
                                    placeholder="Enter password"
                                    onChange={(e) =>
                                        setPassword(e.target.value)
                                    }
                                />
                            </div>
                        </div>

                        <button type="submit" className="loginbtn flex">
                            <span>LOGIN</span>
                        </button>

                        <span className="forgotPassword">
                            Forgot your password? <a href="">Click Here</a>
                        </span>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default Login;
