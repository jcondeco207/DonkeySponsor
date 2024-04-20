import { useState } from 'react'
import {
    MenuMenu,
    MenuItem,
    Button,
    Menu,
} from 'semantic-ui-react';
import { useNavigate } from "react-router-dom";

export default function DonkeyMenu() {
    const navigate = useNavigate();

    const [activeItem, setActiveItem] = useState("home");

    const handleItemClick = (name: string) => {
        setActiveItem(name);
    }

    return (
        <Menu size='large'>
            <MenuItem
                name='home'
                active={activeItem === 'home'}
                onClick={() => {handleItemClick('home'); navigate(`/`)} }
            />
            <MenuItem
                name='farms'
                active={activeItem === 'farms'}
                onClick={() => {handleItemClick('farms'); navigate(`/farms`)}}
            />
            <MenuItem
                name='My Farm'
                active={activeItem === 'My Farm'}
                onClick={() => {handleItemClick('My Farm'); navigate(`/my-farm`)}}
            />
            <MenuItem
                name='Donkeys'
                active={activeItem === 'Donkeys'}
                onClick={() => handleItemClick('Donkeys')}
            />
            <MenuItem
                name='My donkeys'
                active={activeItem === 'My donkeys'}
                onClick={() => handleItemClick('My donkeys')}
            />



            <MenuMenu position='right'>
                <MenuItem>
                    <Button primary>Sign Up</Button>
                </MenuItem>
            </MenuMenu>
        </Menu>
    )
}
