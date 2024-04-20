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
    Card,
} from 'semantic-ui-react'
import 'semantic-ui-css/semantic.min.css'

type Locals = {
    id: string,
    latitude: string,
    longitude: string,
    name: string,
    description: string
    owner: string
}

export default function Farms() {

    const [page, setPage] = useState<Locals[]>([])
    const [numberOfPageLoads, setNumberOfPageLoads] = useState(2);
    const [numberOfLocals, setNumberOfLocals] = useState(0);

    useEffect(() => {
        const csrfToken = Cookies.get("csrftoken");
        axios
            .get(`/api/locals/`, {
                headers: {
                    Accept: "application/json",
                    "X-CSRFToken": String(csrfToken)
                },
                params: {
                    limit: 10
                }
            })
            .then((response) => {
                console.log(response.data)
                setNumberOfLocals(response.data.count);
                console.log(response.data.results);
                setPage(response.data.results);
            })
            .catch((error) => {
                console.log(error);
            });
    }, []);

    const loadMoreContent = () => {
        var activities = page;
        const csrfToken = Cookies.get("csrftoken");
        var offset = numberOfPageLoads * 10;
        if (offset > numberOfLocals) {
            offset = numberOfLocals
        }

        axios
            .get(`/api/locals/`, {
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
                console.log(response.data.results);
                activities.push(response.data.results);
                setPage(activities);
                setNumberOfPageLoads(numberOfPageLoads + 1);
            })
            .catch((error) => {
                console.log(error);
            });
    }

    const doNothing = () => { }

    return (
        <div>
            <Visibility
                fireOnMount
                onBottomVisible={((numberOfPageLoads * 10) < numberOfLocals) ? loadMoreContent : doNothing}
            >
                <Header as='h2'>
                    <Icon name='home' />
                    <HeaderContent>Donkey Farms</HeaderContent>
                </Header>
                <ItemGroup>
                    {page.map((local) => (
                        <Card>
                            <CardContent header={local.name} />
                            <CardContent description={local.description} />
                            <CardContent extra>
                                <Icon name='sticker mule' />4 Donkeys
                            </CardContent>
                        </Card>
                    ))}
                </ItemGroup>
            </Visibility>
        </div>
    );
}