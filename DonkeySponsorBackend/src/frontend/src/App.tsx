import { Outlet } from "react-router-dom";
import DonkeyMenu from "./pages/components/DonkeyMenu";
import {
  Sticky,
} from 'semantic-ui-react'

export default function App() {

  return (
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
  )
}

