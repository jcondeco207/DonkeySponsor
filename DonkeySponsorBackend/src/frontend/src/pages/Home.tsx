import { useEffect, useState } from "react";
import axios from "axios";
import Cookies from "js-cookie";

import { 
    Visibility,
    // ItemImage,
    // ItemHeader,
    ItemGroup,
    // ItemExtra,
    // ItemDescription,
    // ItemContent,
    // Icon,
    // Image,
    // Item,
 } from 'semantic-ui-react'

type Activity = {
    id: string,
    description: string,
    status: boolean,
    lastUptadedAt: string,
    createdAt: string,
    activity_image: string,
    donkey_id: string[]
}

export default function Home() {

    const [page, setPage] = useState<Activity[]>([])
    const [numberOfPageLoads, setNumberOfPageLoads] = useState(2);

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

    return (
        <div>
            <Visibility
                fireOnMount
                onBottomVisible={loadMoreContent}
            >
                <ItemGroup>
                    {/* {page.map((activity, index) => (
                        <Item>
                            
                        </Item>
                    ))} */}
                </ItemGroup>


            </Visibility>
        </div>
    );
}