import React from "react";
import "../../style/Dashboard.css"
import { Link } from "react-router-dom";


const Dashboard = () => {
    const handleLogout = () => {
        localStorage.removeItem("accessToken");
    };

    

    return (
        <div className="body">
            <div>
                This is Dashboard Page <br />
                <Link to="/" onClick={handleLogout}>
                    Logout
                </Link>

                



            </div>
        </div>

    );
};

export default Dashboard;
