import { useState } from 'react'
import {
    MenuMenu,
    MenuItem,
    Button,
    Menu,
} from 'semantic-ui-react';
import { useNavigate } from "react-router-dom";
import { Guard } from '../../Guard';
import SimpleGuard from '../../SimpleGuard';

export default function DonkeyMenu() {
    const navigate = useNavigate();
    const guardService = new SimpleGuard();

    const [activeItem, setActiveItem] = useState("home");

    const handleItemClick = (name: string) => {
        setActiveItem(name);
    }

    return (
        <Menu size='large'>
            <MenuItem
                name='home'
                active={activeItem === 'home'}
                onClick={() => { handleItemClick('home'); navigate(`/`) }}
            />
            <MenuItem
                name='farms'
                active={activeItem === 'farms'}
                onClick={() => { handleItemClick('farms'); navigate(`/farms`) }}
            />
            <Guard requiredRoles={["DonkeyAdmin", "DonkeyProvider"]} guardService={guardService}>
                <MenuItem
                    name='My Farm'
                    active={activeItem === 'My Farm'}
                    onClick={() => { handleItemClick('My Farm'); navigate(`/my-farm`) }}
                />
            </Guard>

            <MenuItem
                name='Donkeys'
                active={activeItem === 'Donkeys'}
                onClick={() => { handleItemClick('Donkeys'); navigate(`/donkeys`) }}
            />

            <Guard requiredRoles={["DonkeyAdmin", "DonkeySponsor"]} guardService={guardService}>
                <MenuItem
                    name='My donkeys'
                    active={activeItem === 'My donkeys'}
                    onClick={() => { handleItemClick('My donkeys'); navigate(`my_donkeys`) }}
                />
            </Guard>

            <MenuMenu position='right'>
                <MenuItem>
                    <Button primary onClick={() => { handleItemClick('Sign Up'); navigate(`signup`) }} >Sign Up</Button>
                </MenuItem>
                <MenuItem>
                    <Button primary onClick={() => { handleItemClick('Login'); navigate(`/account/login/?next=/`) }} >Login</Button>
                </MenuItem>
            </MenuMenu>
        </Menu>
    )
}
