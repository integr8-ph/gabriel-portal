import React from "react";
import "../../style/Dashboard.css"
import { Link } from "react-router-dom";

const Dashboard = () => {
    const handleLogout = () => {
        localStorage.removeItem("accessToken");
    };

    const data = [
        { id: 1, username: "user1", password: "pass123" },
        { id: 2, username: "user2", password: "pass456" },
        { id: 3, username: "user3", password: "pass789" },
    ];

    return (
        <div className="body">
            <div>
                This is Dashboard Page <br />
                <Link to="/" onClick={handleLogout}>
                    Logout
                </Link>

                <div className="container-box">
                    <div className="table-container">
                        <div className="title-column">
                            <h1>User Information</h1>
                        </div>
                        <div>
                            <button className="add-button">Add</button>
                        </div>

                        <table className="table">
                            <thead className="table-header">
                                <tr>
                                    <th className="table-cell">ID</th>
                                    <th className="table-cell">Username</th>
                                    <th className="table-cell">Password</th>
                                    <th className="table-cell">Actions</th>
                                </tr>
                            </thead>
                            <tbody className="table-body">
                                {data.map((item) => (
                                    <tr key={item.id} className="table-row">
                                        <td className="table-cell">{item.id}</td>
                                        <td className="table-cell">{item.username}</td>
                                        <td className="table-cell">{item.password}</td>
                                        <td className="table-cell action-buttons">
                                            <button className="updateBtn">
                                                Update
                                            </button>
                                            <button className="deleteBtn">
                                                Delete
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

    );
};

export default Dashboard;
