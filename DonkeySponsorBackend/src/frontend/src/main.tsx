import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.js'
import './App.css'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

import 'semantic-ui-css/semantic.min.css'
import Farms from './pages/Farms.js';
import Home from './pages/Home.js';
import MyFarm from './pages/MyFarm.js';
import MyFarmAddDonkey from './pages/MyFarmAddDonkey.js';

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      {
        path: "/",
        element: <Home/>,
      },
      {
        path: "/farms",
        element: <Farms/>,
      },
      {
        path: "/my-farm",
        element: <MyFarm/>,
      },
      {
        path: "/my-farm/add-donkey",
        element: <MyFarmAddDonkey/>,
      },
      {
        path: "/my-farm/publish-activity",
        element: <MyFarm/>,
      },
    ],
  }
]);

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)