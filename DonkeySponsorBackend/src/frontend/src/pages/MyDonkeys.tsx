import { useEffect, useState } from "react";
import axios from "axios";
import Cookies from "js-cookie";
import React from 'react'

import {
    Visibility,
    ItemGroup,
    Header,
    HeaderContent,
    Icon,
    CardContent,
    Image,
    Card,
    Button,
    Modal,
    ModalContent,
    ModalActions,
    ModalHeader
} from 'semantic-ui-react'
import 'semantic-ui-css/semantic.min.css'
import { useNavigate } from "react-router-dom";

type AnimalImage = {
    id: string;
    image: string;
}

type Animal = {
    id: string;
    name: string;
    color: string;
    status: boolean;
    local: string;
    animal_image: AnimalImage[];
    sponsor_count: number;
}

function exampleReducer(state: { log: any; }, action: { type: any; event: any; name: any; }) {
    switch (action.type) {
        case 'CLEAR_LOG':
            return { ...state, log: [] }
        case 'OPEN_MODAL':
            return {
                log: [
                    {
                        event: action.event,
                        date: new Date().toLocaleTimeString(),
                        name: action.name,
                        value: true,
                    },
                    ...state.log,
                ],
                open: true,
            }
        case 'CLOSE_MODAL':
            return {
                log: [
                    {
                        event: action.event,
                        date: new Date().toLocaleTimeString(),
                        name: action.name,
                        value: true,
                    },
                    ...state.log,
                ],
                open: false,
            }
        default:
            throw new Error()
    }
}

async function removeSponsor(donkey_id: string): Promise<void> {
    const url = `/api/animals/${donkey_id}/remove_sponsor`;
    try {
        const csrfToken = Cookies.get("csrftoken");
        if (csrfToken) {
            const response = await fetch(url, {
                method: 'DELETE',
                headers: {
                    'Accept': 'application/json',
                    'X-CSRFToken': csrfToken
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            console.log('Sponsor removed successfully');
        }

    } catch (error) {
        console.error('An error occurred:', error);
    }
}

export default function Donkeys() {
    const navigate = useNavigate();
    const [page, setPage] = useState<Animal[]>([])
    const [numberOfPageLoads, setNumberOfPageLoads] = useState(2);
    const [numberOfAnimals, setNumberOfAnimals] = useState(0);
    const [state, dispatch] = React.useReducer(exampleReducer, {
        log: [],
        open: false,
    })
    const { log, open } = state
    console.log(log);

    useEffect(() => {
        const csrfToken = Cookies.get("csrftoken");
        axios
            .get(`/api/animals/sponsored`, {
                headers: {
                    Accept: "application/json",
                    "X-CSRFToken": String(csrfToken)
                },
                params: {
                    limit: 10
                }
            })
            .then((response) => {
                // console.log(response.data)
                setNumberOfAnimals(response.data.count);
                // console.log(response.data.results);
                setPage(response.data.results);
            })
            .catch((error) => {
                console.log(error);
            });
    }, []);

    const loadMoreContent = () => {
        var donkeys = page;
        const csrfToken = Cookies.get("csrftoken");
        var offset = numberOfPageLoads * 10;
        if (offset > numberOfAnimals) {
            offset = numberOfAnimals
        }

        axios
            .get(`/api/animals/sponsored`, {
                headers: {
                    Accept: "application/json",
                    "X-CSRFToken": String(csrfToken)
                },
                params: {
                    limit: 10,
                    offset: numberOfPageLoads * 10
                }
            })
            .then((response) => {
                console.log(response.data);
                donkeys.push(response.data.results);
                setPage(donkeys);
                setNumberOfPageLoads(numberOfPageLoads + 1);
            })
            .catch((error) => {
                console.log(error);
            });
    }

    const doNothing = () => { }
    const seeDetail = (id: string) => {
        navigate(`/activities?donkey_id=${id}`)
    }

    return (
        <div>
            <Visibility
                fireOnMount
                onBottomVisible={((numberOfPageLoads * 10) < numberOfAnimals) ? loadMoreContent : doNothing}
            >
                <Header as='h2'>
                    <Icon name='home' />
                    <HeaderContent>My Sponsored Donkeys</HeaderContent>
                </Header>
                <ItemGroup>
                    {page.map((donkey) => (
                        <Card>
                            <Image src={(donkey.animal_image && donkey.animal_image.length) > 0 ? String(donkey.animal_image[0].image) : ""} wrapped ui={false} />
                            <CardContent header={donkey.name} />
                            <CardContent description={donkey.color} />
                            <CardContent extra>
                                <Icon name='sticker mule' />{donkey.sponsor_count} sponsors
                            </CardContent>
                            <CardContent extra>
                                <div className='ui two buttons'>
                                    <Modal
                                        onOpen={(e) =>
                                            dispatch({ event: e.type, name: 'onOpen', type: 'OPEN_MODAL' })
                                        }
                                        onClose={(e) =>
                                            dispatch({ event: e.type, name: 'onClose', type: 'CLOSE_MODAL' })
                                        }
                                        open={open}
                                        trigger={<Button basic>Remove</Button>}
                                    >
                                        <ModalHeader>Remove Sponsoring</ModalHeader>
                                        <ModalContent>
                                            <p>Are you sure you want to remove sponsoring?</p>
                                        </ModalContent>
                                        <ModalActions>
                                            <Button
                                                onClick={(e) =>
                                                    dispatch({
                                                        event: e.type,
                                                        name: 'onClick',
                                                        type: 'CLOSE_MODAL',
                                                    })
                                                }
                                                negative
                                            >
                                                No
                                            </Button>
                                            <Button
                                                onClick={(e) => {
                                                    dispatch({
                                                        event: e.type,
                                                        name: 'onClick',
                                                        type: 'CLOSE_MODAL',
                                                    });
                                                    removeSponsor(donkey.id)
                                                }
                                                }
                                                positive
                                            >
                                                Yes
                                            </Button>
                                        </ModalActions>
                                    </Modal>
                                    <Button basic onClick={() => seeDetail(donkey.id)}>
                                        Activities
                                    </Button>
                                </div>
                            </CardContent>
                        </Card>
                    ))}
                </ItemGroup>
            </Visibility>


        </div >
    );
}