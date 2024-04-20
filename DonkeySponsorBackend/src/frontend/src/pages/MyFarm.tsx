import { useEffect, useState } from "react";
import axios from "axios";
import Cookies from "js-cookie";

import {
    Header,
    HeaderContent,
    Icon,
    Button,
    ButtonContent,
    Grid,
    GridRow,
    GridColumn,
    ItemGroup,
    Item,
    ItemContent,
    ItemHeader,
    ItemDescription,
    Pagination,
} from 'semantic-ui-react'
import 'semantic-ui-css/semantic.min.css'

// type Local = {
//     id: string,
//     latitude: string,
//     longitude: string,
//     name: string,
//     description: string
//     owner: string
// }

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

type Activity = {
    id: string,
    description: string,
    status: boolean,
    lastUptadedAt: string,
    createdAt: string,
    activity_image: [
        {
            id: string,
            image: string,
            activity: string
        }
    ],
    donkey_id: string[]
}

export default function MyFarm() {
    const [myFarmId, setMyFarmId] = useState("");
    const [myFarmDonkeys, setMyFarmDonkeys] = useState<Donkey[]>([]);
    const [myFarmActivities, setMyFarmActivities] = useState<Activity[]>([]);
    const [numberOfDonkeys, setNumberOfDonkeys] = useState(0);
    const [numberOfActivities, setNumberOfActivities] = useState(0);
    // const [donkeysActivePage, setDonkeysActivePage] = useState(1);
    // const [activitiesActivePage, setActivitiesActivePage] = useState(1);
    const itemPerPage = 5;

    useEffect(() => {
        const csrfToken = Cookies.get("csrftoken");
        var farmId = "";
        axios
            .get(`/api/whoami/`, {
                headers: {
                    Accept: "application/json",
                    "X-CSRFToken": String(csrfToken)
                }
            })
            .then((response) => {
                console.log(response)
                setMyFarmId(response.data.locals[0].id);
                farmId = response.data.locals[0].id;
            })
            .catch((error) => {
                console.log(error);
            });

        axios
            .get(`/api/animals/`, {
                headers: {
                    Accept: "application/json",
                    "X-CSRFToken": String(csrfToken)
                },
                params: {
                    local_id: farmId,
                    limit: itemPerPage
                }
            })
            .then((response) => {
                console.log(response)
                setMyFarmDonkeys(response.data.results);
                setNumberOfDonkeys(response.data.count);
                console.log(myFarmId)
            })
            .catch((error) => {
                console.log(error);
            });

        axios
            .get(`/api/activities/`, {
                headers: {
                    Accept: "application/json",
                    "X-CSRFToken": String(csrfToken)
                },
                params: {
                    local_id: farmId,
                    limit: itemPerPage
                }
            })
            .then((response) => {
                console.log(response)
                setMyFarmActivities(response.data.results);
                setNumberOfActivities(response.data.count);
            })
            .catch((error) => {
                console.log(error);
            });
    }, []);

    return (
        <div>
            <Header as='h2'>
                <Icon name='home' />
                <HeaderContent>My Farm</HeaderContent>
            </Header>
            <div>
                <Button animated>
                    <ButtonContent visible>Add Donkey</ButtonContent>
                    <ButtonContent hidden>
                        <Icon name='arrow right' />
                    </ButtonContent>
                </Button>
                <Button animated>
                    <ButtonContent visible>Publish Activity</ButtonContent>
                    <ButtonContent hidden>
                        <Icon name='arrow right' />
                    </ButtonContent>
                </Button>
            </div>

            <Grid divided='vertically'>
                <GridRow columns={2}>
                    <GridColumn>
                        <ItemGroup>
                            {myFarmDonkeys.map((donkey) => (
                                <Item>
                                    <ItemContent>
                                        <ItemHeader as='a'>{donkey.name}</ItemHeader>
                                        <ItemDescription>
                                            <p>{donkey.color}</p>
                                        </ItemDescription>
                                    </ItemContent>
                                </Item>
                            ))}
                        </ItemGroup>

                        <Pagination
                            boundaryRange={0}
                            defaultActivePage={1}
                            ellipsisItem={null}
                            firstItem={null}
                            lastItem={null}
                            siblingRange={1}
                            totalPages={Math.ceil(numberOfDonkeys / itemPerPage)}
                        />
                    </GridColumn>
                    <GridColumn>
                        <ItemGroup>
                            {myFarmActivities.map((activity) => (
                                <Item>
                                    <ItemContent>
                                        <ItemHeader as='a'>{activity.donkey_id[0]}</ItemHeader>
                                        <ItemDescription>
                                            <p>{activity.description}</p>
                                        </ItemDescription>
                                    </ItemContent>
                                </Item>
                            ))}
                        </ItemGroup>

                        <Pagination
                            boundaryRange={0}
                            defaultActivePage={1}
                            ellipsisItem={null}
                            firstItem={null}
                            lastItem={null}
                            siblingRange={1}
                            totalPages={Math.ceil(numberOfActivities / itemPerPage)}
                        />
                    </GridColumn>
                </GridRow>
            </Grid>
        </div>
    );
}