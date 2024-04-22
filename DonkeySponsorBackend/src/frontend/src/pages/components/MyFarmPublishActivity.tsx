import {
    Icon,
    FormGroup,
    Form,
    FormInput,
    FormTextArea,
    Button,
    Modal,
    ModalHeader,
    ModalContent,
    ModalActions,
    ButtonContent,
    Dropdown,
} from 'semantic-ui-react'
import 'semantic-ui-css/semantic.min.css'
import { useEffect, useState } from 'react';
import axios from "axios";
import Cookies from "js-cookie";


type MyFarmPublishActivityProps = {
    open: boolean,
    setOpen: React.Dispatch<React.SetStateAction<boolean>>,
    farmId: string
}

type Donkey = {
    id: string,
    name: string,
    color: string,
    status: boolean,
    local: string,
    animal_image: [
        {
            id: string,
            image: string
        }
    ]
}

export default function MyFarmPublishActivity(props: MyFarmPublishActivityProps) {

    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [donkey, setDonkey] = useState("");

    const [myFarmDonkeys, setMyFarmDonkeys] = useState<Donkey[]>([]);

    useEffect(() => {
        const csrfToken = Cookies.get("csrftoken");

        axios
            .get(`/api/animals/`, {
                headers: {
                    Accept: "application/json",
                    "X-CSRFToken": String(csrfToken)
                },
                params: {
                    local_id: props.farmId,                
                }
            })
            .then((response) => {
                console.log(response)
                setMyFarmDonkeys(response.data.results.map((obj: { id: string; name: string; }) => ({
                    key: obj.id,
                    text: obj.name,
                    value: obj.id
                })))
                console.log(myFarmDonkeys)

            })
            .catch((error) => {
                console.log(error);
            });

    }, []);

    const handleTitleChange = (_: any, data: any) => {
        setTitle(data.value);
    }

    const handleDescriptionChange = (_: any, data: any) => {
        setDescription(data.value);
    }

    const handleDonkeyChange = (_: any, data: any) => {
        setDonkey(data.value);
    }

    const publishActivity = () => {
        const csrfToken = Cookies.get("csrftoken");
        axios
            .post(`/api/activity/new`, {
                title: title,
                description: description,
                status: true,
                local: props.farmId,
                donkey_id: donkey
            }, {
                headers: {
                    Accept: "application/json",
                    "X-CSRFToken": csrfToken
                },
            })
            .then((response) => {
                console.log(response)
                window.location.reload()
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
                    <ButtonContent visible>Publish Activity</ButtonContent>
                    <ButtonContent hidden>
                        <Icon name='arrow right' />
                    </ButtonContent>
                </Button>}
            >
                <ModalHeader>Publish Activity</ModalHeader>
                <ModalContent>
                    <Form>
                        <FormGroup widths='equal'>
                            <FormInput label='Title' placeholder='Title' onChange={handleTitleChange} />
                        </FormGroup>
                        <FormTextArea label='Description' placeholder='Activity description...' onChange={handleDescriptionChange} />
                        <Dropdown
                            placeholder='Select Donkey'
                            fluid
                            search
                            selection
                            options={myFarmDonkeys}
                            onChange={handleDonkeyChange}
                        />
                    </Form>
                </ModalContent>
                <ModalActions>
                    <Button color='black' onClick={() => props.setOpen(false)}>
                        Close
                    </Button>
                    <Button
                        content="Publish Activity"
                        labelPosition='right'
                        icon='checkmark'
                        onClick={() => { publishActivity(); props.setOpen(false) }}
                        positive
                    />
                </ModalActions>
            </Modal>
        </div>
    );
}