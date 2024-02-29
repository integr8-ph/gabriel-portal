import React from "react";
import { Navigate, Outlet } from "react-router-dom";

const useAuth = () => {
    let isAuthenticated = false;
    const token = localStorage.getItem("accessToken");
    if (token) {
        isAuthenticated = true;
    }

    return { isAuthenticated };
};

const PrivateRoute = () => {
    const { isAuthenticated } = useAuth();

    return isAuthenticated ? <Outlet /> : <Navigate to="/login" />;
};

export default PrivateRoute;
