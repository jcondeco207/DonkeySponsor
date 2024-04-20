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

export default function MyFarm() {

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
                        
                    </GridColumn>
                    <GridColumn>
                        
                    </GridColumn>
                </GridRow>
            </Grid>

        </div>
    );
}