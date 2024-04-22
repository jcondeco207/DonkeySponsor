import { Outlet } from "react-router-dom";
import DonkeyMenu from "./pages/components/DonkeyMenu";
import {
  Sticky,
} from 'semantic-ui-react'
import { useEffect, useState } from "react";
import axios from "axios";
import UserRoleContext from "./context/UserRoleContext";
import Cookies from "js-cookie";

export default function App() {
  const [userRole, setUserRole] = useState('');

  useEffect(() => {
    const csrfToken = Cookies.get("csrftoken");
    axios
      .get('/api/whoami/', {
        headers: {
          Accept: "application/json",
          "X-CSRFToken": String(csrfToken)
        },
      })
      .then((response) => {
        setUserRole(response.data.role);
        console.log(response)
      })
      .catch((error) => {
        console.log(error);
      })
  }, []);


  return (
    <UserRoleContext.Provider value={userRole}>
      <div className='app'>
        <div className='workArea'>
          <Sticky>
            <DonkeyMenu />
          </Sticky>
          <div className='contentArea'>
            <Outlet />
          </div>
        </div>
      </div>
    </UserRoleContext.Provider>

  )
}

