import { useEffect, useState } from "react";
import axios from "axios";
import Cookies from "js-cookie";

import {
    Visibility,
    ItemImage,
    ItemHeader,
    ItemGroup,
    ItemDescription,
    ItemContent,
    Item,
    Header,
    HeaderContent,
    Icon,
} from 'semantic-ui-react'
import 'semantic-ui-css/semantic.min.css'

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

export default function Home() {

    const [page, setPage] = useState<Activity[]>([])
    const [numberOfPageLoads, setNumberOfPageLoads] = useState(2);
    const [numberOfActivities, setNumberOfActivities] = useState(0);

    useEffect(() => {
        const csrfToken = Cookies.get("csrftoken");
        axios
            .get(`/api/activities/`, {
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
                setNumberOfActivities(response.data.count);
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
        if (offset > numberOfActivities) {
            offset = numberOfActivities
        }

        axios
            .get(`/api/activities/`, {
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
                onBottomVisible={((numberOfPageLoads * 10) < numberOfActivities) ? loadMoreContent : doNothing}
            >
                <Header as='h2'>
                    <Icon name='sticker mule' />
                    <HeaderContent>Donkey Activities</HeaderContent>
                </Header>
                <ItemGroup>
                    {page.map((activity) => (
                        <Item>
                            <ItemImage size='small' src={activity.activity_image[0]?.image} />

                            <ItemContent>
                                <ItemHeader as='a'>{activity.donkey_id[0]}</ItemHeader>
                                <ItemDescription>
                                    <p>{activity.description}</p>
                                </ItemDescription>
                            </ItemContent>
                        </Item>
                    ))}
                </ItemGroup>
            </Visibility>
        </div>
    );
}