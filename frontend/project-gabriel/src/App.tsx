import React from "react";

import { useRoutes } from "react-router-dom";


import Dashboard from "./components/Dashboard/Dashboard";
import Login from "./components/Login/Login";
import PrivateRoute from "./components/Auth/auth";
import Table from "./components//Table";

const App = () => {
    const routes = useRoutes([
        {
            path: "/",
            element: <PrivateRoute />,
            children: [{ path: "/", element: <Dashboard /> }],
        },
        {
            path: "/login",
            element: <Login />,
        },
        {
            path: "/table",
            element: <Table />,
        },
    ]);

    return <>{routes}</>;
};

export default App;