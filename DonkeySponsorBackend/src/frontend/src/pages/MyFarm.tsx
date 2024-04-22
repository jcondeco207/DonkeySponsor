import { useEffect, useState } from "react";
import axios from "axios";
import Cookies from "js-cookie";

import {
    Header,
    HeaderContent,
    Icon,
    Grid,
    GridRow,
    GridColumn,
    ItemGroup,
    Item,
    ItemContent,
    ItemHeader,
    ItemDescription,
    // Pagination,
} from 'semantic-ui-react'
import 'semantic-ui-css/semantic.min.css'
import '../css/MyFarm.css'
import MyFarmAddDonkey from "./MyFarmAddDonkey";
import MyFarmPublishActivity from "./MyFarmPublishActivity";

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
    title: string,
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

    const [openAddDonkey, setOpenAddDonkeys] = useState(false);
    const [openPublishActivity, setOpenPublishActivity] = useState(false);

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
                // console.log(response)
                setMyFarmId(response.data.locals[0].id);
                farmId = response.data.locals[0].id;
                console.log(farmId)
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
                }
            })
            .then((response) => {
                console.log(response)
                setMyFarmDonkeys(response.data.results);
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
                }
            })
            .then((response) => {
                console.log(response)
                setMyFarmActivities(response.data.results);
            })
            .catch((error) => {
                console.log(error);
            });
    }, []);


    // useEffect(() => {
    //     var offset = donkeysActivePage * itemPerPage;
    //     if (offset > numberOfDonkeys - 1) {
    //         offset = numberOfDonkeys - 1
    //     }else if (donkeysActivePage==1){
    //         offset= 0;
    //     }

    //     const csrfToken = Cookies.get("csrftoken");
    //     axios
    //         .get(`/api/animals/`, {
    //             headers: {
    //                 Accept: "application/json",
    //                 "X-CSRFToken": String(csrfToken)
    //             },
    //             params: {
    //                 local_id: myFarmId,
    //                 limit: itemPerPage,
    //                 offset: offset
    //             }
    //         })
    //         .then((response) => {
    //             console.log(response)
    //             setMyFarmDonkeys(response.data.results);
    //         })
    //         .catch((error) => {
    //             console.log(error);
    //         });

    // }, [donkeysActivePage]);

    // useEffect(() => {
    //     var offset = activitiesActivePage * itemPerPage;
    //     if (offset > numberOfActivities - 1) {
    //         offset = numberOfActivities - 1
    //     }else if (activitiesActivePage==1){
    //         offset= 0;
    //     }

    //     const csrfToken = Cookies.get("csrftoken");
    //     axios
    //         .get(`/api/activities/`, {
    //             headers: {
    //                 Accept: "application/json",
    //                 "X-CSRFToken": String(csrfToken)
    //             },
    //             params: {
    //                 local_id: myFarmId,
    //                 limit: itemPerPage,
    //                 offset: offset
    //             }
    //         })
    //         .then((response) => {
    //             console.log("page request")
    //             console.log(response)
    //             setMyFarmActivities(response.data.results);
    //         })
    //         .catch((error) => {
    //             console.log(error);
    //         });
    // }, [activitiesActivePage])

    // const handleDonkeysPageChange = (_: any, data: any) => {
    //     setDonkeysActivePage(data.activePage);
    // }

    // const handleActivitiesPageChange = (_: any, data: any) => {
    //     setActivitiesActivePage(data.activePage);
    // }

    return (
        <div>
            <Header as='h2'>
                <Icon name='home' />
                <HeaderContent>My Farm</HeaderContent>
            </Header>
            <Grid divided='vertically'>
                <GridRow columns={2}>
                    <GridColumn>
                        <MyFarmAddDonkey farmId={myFarmId} open={openAddDonkey} setOpen={setOpenAddDonkeys} />
                    </GridColumn>
                    <GridColumn>
                        <MyFarmPublishActivity farmId={myFarmId} open={openPublishActivity} setOpen={setOpenPublishActivity} />
                    </GridColumn>
                </GridRow>
            </Grid>

            <Grid divided='vertically' className="myFarmLists">
                <GridRow columns={2}>
                    <GridColumn>
                        <Header as='h2'>
                            <HeaderContent>My Farm Donkeys</HeaderContent>
                        </Header>
                        <ItemGroup divided>
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

                        {/* <Pagination
                            boundaryRange={0}
                            activePage={donkeysActivePage}
                            onPageChange={handleDonkeysPageChange}
                            defaultActivePage={1}
                            ellipsisItem={null}
                            firstItem={null}
                            lastItem={null}
                            siblingRange={1}
                            totalPages={Math.ceil(numberOfDonkeys / itemPerPage)}
                        /> */}
                    </GridColumn>
                    <GridColumn>
                        <Header as='h2'>
                            <HeaderContent>My Farm Activities</HeaderContent>
                        </Header>
                        <ItemGroup divided>
                            {myFarmActivities.map((activity) => (
                                <Item>
                                    <ItemContent>
                                        <ItemHeader as='a'>{activity.title}</ItemHeader>
                                        <ItemDescription>
                                            <p>{activity.description}</p>
                                        </ItemDescription>
                                    </ItemContent>
                                </Item>
                            ))}
                        </ItemGroup>

                        {/* <Pagination
                            boundaryRange={0}
                            defaultActivePage={1}
                            onPageChange={handleActivitiesPageChange}
                            ellipsisItem={null}
                            firstItem={null}
                            lastItem={null}
                            siblingRange={1}
                            totalPages={Math.ceil(numberOfActivities / itemPerPage)}
                        /> */}
                    </GridColumn>
                </GridRow>
            </Grid>
        </div>
    );
}