import { useEffect, useState } from "react";
import axios from "axios";
import Cookies from "js-cookie";

import {
    Visibility,
    ItemHeader,
    ItemGroup,
    ItemDescription,
    ItemContent,
    Item,
    Header,
    HeaderContent,
    Icon,
    Button
} from 'semantic-ui-react'
import 'semantic-ui-css/semantic.min.css'

type Notification = {
    id: string,
    content: string,
    seen: string,
    user: string,
    createdAt: string
}

export default function Home() {

    const [page, setPage] = useState<Notification[]>([])
    const [numberOfPageLoads, setNumberOfPageLoads] = useState(2);
    const [numberOfNotifications, setNumberOfNotifications] = useState(0);

    useEffect(() => {
        const csrfToken = Cookies.get("csrftoken");
        axios
            .get(`/api/notifications`, {
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
                setNumberOfNotifications(response.data.count);
                // console.log(response.data.results);
                setPage(response.data.results);
            })
            .catch((error) => {
                console.log(error);
            });
    }, []);

    const loadMoreContent = () => {
        var notifications = page;
        const csrfToken = Cookies.get("csrftoken");
        var offset = numberOfPageLoads * 10;
        if (offset > numberOfNotifications - 1) {
            offset = numberOfNotifications - 1
        }

        axios
            .get(`/api/notifications`, {
                headers: {
                    Accept: "application/json",
                    "X-CSRFToken": String(csrfToken)
                },
                params: {
                    limit: 10,
                    offset: offset
                }
            })
            .then((response) => {
                // console.log(response.data.results);
                notifications.push(response.data.results);
                setPage(notifications);
                setNumberOfPageLoads(numberOfPageLoads + 1);
            })
            .catch((error) => {
                console.log(error);
            });
    }

    const doNothing = () => { }

    const seeNotif = (id: string) => {
        const csrfToken = Cookies.get("csrftoken");
        if (csrfToken) {
            fetch(`/api/notifications/${id}/check`, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'X-CSRFToken': csrfToken
                }
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(_json => {
                    window.location.reload();
                })
                .catch(error => {
                    console.log(error);
                });
        }

    }

    return (
        <div>
            <Visibility
                fireOnMount
                onBottomVisible={((numberOfPageLoads * 10) < numberOfNotifications) ? loadMoreContent : doNothing}
            >
                <Header as='h2'>
                    <Icon name='bell' />
                    <HeaderContent>Notifications</HeaderContent>
                </Header>
                <ItemGroup divided>
                    {page.map((notif) => (
                        <Item>
                            <ItemContent>
                                <ItemHeader as='a'>New notification</ItemHeader>
                                <ItemDescription>
                                    <p>{notif.content}</p>
                                </ItemDescription>
                            </ItemContent>
                            <Button onClick={() => { seeNotif(notif.id) }}>Seen</Button>
                        </Item>
                    ))}
                </ItemGroup>
            </Visibility>
        </div>
    );
}