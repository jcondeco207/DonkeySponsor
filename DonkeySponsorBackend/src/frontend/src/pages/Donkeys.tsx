import { useEffect, useState } from "react";
import axios from "axios";
import Cookies from "js-cookie";

import {
    Visibility,
    ItemGroup,
    Header,
    HeaderContent,
    Icon,
    CardContent,
    Image,
    Card,
    Button
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

async function sponsor(animal: { donkey_id: string, value: number }): Promise<void> {
    const url = '/api/animals/new';
    const csrfToken = Cookies.get("csrftoken");

    try {
        if (csrfToken) {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(animal)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            console.log('Animal created successfully');
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

    useEffect(() => {
        const csrfToken = Cookies.get("csrftoken");
        axios
            .get(`/api/animals/`, {
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
            .get(`/api/animals/`, {
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
                    <HeaderContent>Donkeys</HeaderContent>
                </Header>
                <ItemGroup>
                    {page.map((donkey) => (
                        <Card>
                            <Image src={String(donkey.animal_image[0].image)} wrapped ui={false} />
                            <CardContent header={donkey.name} />
                            <CardContent description={donkey.color} />
                            <CardContent extra>
                                <Icon name='sticker mule' />{donkey.sponsor_count} sponsors
                            </CardContent>
                            <CardContent extra>
                                <div className='ui two buttons'>
                                    <Button basic onClick={() => sponsor({ "donkey_id": donkey.id, value: 10 })}>
                                        Sponsor
                                    </Button>
                                    <Button basic onClick={() => seeDetail(donkey.id)}>
                                        Activities
                                    </Button>
                                </div>
                            </CardContent>
                        </Card>
                    ))}
                </ItemGroup>
            </Visibility>
        </div>
    );
}