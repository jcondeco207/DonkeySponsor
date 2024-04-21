import React, { useState } from 'react';
import { Button, Form, Segment, Dropdown } from 'semantic-ui-react';
import Cookies from "js-cookie";

const SignupForm: React.FC = () => {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        role: '',
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleDropdownChange = (_e: React.SyntheticEvent<HTMLElement>, data: any) => {
        setFormData({ ...formData, role: data.value });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        // Handle form submission
        try {
            const csrfToken = Cookies.get("csrftoken");
            if (csrfToken) {
                const response = await fetch('/api/users', {
                    method: 'POST',
                    headers: {
                        'Accept': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify(formData)
                });

                if (!response.ok) {
                    throw new Error('Signup request failed');
                }

                const data = await response.json();
                console.log(data);
            }

        } catch (error) {
            console.error(error);
        }
    };

    const roleOptions = [
        { key: 'dgf', value: 'DonkeyGodFather', text: 'DonkeyGodFather' },
        { key: 'dp', value: 'DonkeyProvider', text: 'DonkeyProvider' },
    ];

    return (
        <Segment>
            <Form onSubmit={handleSubmit}>
                <Form.Input
                    fluid
                    icon='user'
                    iconPosition='left'
                    placeholder='Username'
                    name='username'
                    value={formData.username}
                    onChange={handleChange}
                />
                <Form.Input
                    fluid
                    icon='mail'
                    iconPosition='left'
                    placeholder='E-mail address'
                    name='email'
                    value={formData.email}
                    onChange={handleChange}
                />
                <Form.Input
                    fluid
                    icon='lock'
                    iconPosition='left'
                    placeholder='Password'
                    type='password'
                    name='password'
                    value={formData.password}
                    onChange={handleChange}
                />
                <Dropdown
                    placeholder='Select Role'
                    fluid
                    selection
                    options={roleOptions}
                    name='role'
                    onChange={handleDropdownChange}
                />

                
                <Button color='teal' fluid size='large'>
                    Sign Up
                </Button>
            </Form>
        </Segment>
    );
};

export default SignupForm;
