import React from 'react';
import "./App.scss"
import Dashboard from "./components/Dashboard/Dashboard"
import Login from "./components/Login/Login"


import {
  createBrowserRouter,
  RouterProvider
} from 'react-router-dom'


const router = createBrowserRouter([
  {
    path: '/',
    element: <div><Login /></div>
  },
  {
    path: '/dashboard',
    element: <div><Dashboard /> </div>
  },
  {
    path: '/login',
    element: <div><Login /></div>
  },
])

function App() {
  return (
   <div>
    <RouterProvider router={router}/>
   </div>
  )
}

export default App
