import { Outlet } from "react-router-dom";
import DonkeyMenu from "./pages/components/DonkeyMenu";

export default function App() {

  return (
    <div className='app'>
      <div className='workArea'>
        <DonkeyMenu />
        <div className='contentArea'>
          <Outlet />
        </div>
      </div>
    </div>
  )
}

