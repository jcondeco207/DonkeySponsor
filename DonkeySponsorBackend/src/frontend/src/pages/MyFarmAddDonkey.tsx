import {
    Icon,
    FormGroup,
    Form,
    FormInput,
    Button,
    Modal,
    ModalHeader,
    ModalContent,
    ModalActions,
    ButtonContent,
} from 'semantic-ui-react'
import 'semantic-ui-css/semantic.min.css'
import { useState } from 'react';
import axios from "axios";
import Cookies from "js-cookie";


type MyFarmAddDonkeyProps = {
    open: boolean,
    setOpen: React.Dispatch<React.SetStateAction<boolean>>,
    farmId: string
}

export default function MyFarmAddDonkey(props: MyFarmAddDonkeyProps) {

    const [name, setName] = useState("");
    const [color, setcolor] = useState("");

    const handleColorChange = (_: any, data: any) => {
        setcolor(data.value);
    }

    const handleNameChange = (_: any, data: any) => {
        setName(data.value);
    }

    const createDonkey = () => {
        const csrfToken = Cookies.get("csrftoken");
        axios
            .post(`/api/animals/`, {
                name: name,
                color: color,
                status: true,
                local: props.farmId
            }, {
                headers: {
                    Accept: "application/json",
                    "X-CSRFToken": csrfToken
                },
            })
            .then((response) => {
                console.log(response)
            })
            .catch((error) => {
                console.log(error);
            });
    }

    return (

        <div>
            <Modal
                onClose={() => props.setOpen(false)}
                onOpen={() => props.setOpen(true)}
                open={props.open}
                trigger={<Button animated>
                    <ButtonContent visible>Add Donkey</ButtonContent>
                    <ButtonContent hidden>
                        <Icon name='arrow right' />
                    </ButtonContent>
                </Button>}
            >
                <ModalHeader>Add Donkey</ModalHeader>
                <ModalContent>
                    <Form>
                        <FormGroup widths='equal'>
                            <FormInput label='Name' placeholder='Name' onChange={handleNameChange} />
                            <FormInput label='Color' placeholder='Color' onChange={handleColorChange} />
                        </FormGroup>
                    </Form>
                </ModalContent>
                <ModalActions>
                    <Button color='black' onClick={() => props.setOpen(false)}>
                        Nope
                    </Button>
                    <Button
                        content="Add Donkey"
                        labelPosition='right'
                        icon='checkmark'
                        onClick={() => { createDonkey(); props.setOpen(false) }}
                        positive
                    />
                </ModalActions>
            </Modal>
        </div>
    );
}