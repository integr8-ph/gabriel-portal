import React from "react";
import { Link } from "react-router-dom";

const Dashboard = () => {
    const handleLogout = () => {
        localStorage.removeItem("accessToken");
    };

    return (
        <div>
            This is Dashboard Page
            <Link to="/" onClick={handleLogout}>
                Logout
            </Link>
        </div>
    );
};

export default Dashboard;
