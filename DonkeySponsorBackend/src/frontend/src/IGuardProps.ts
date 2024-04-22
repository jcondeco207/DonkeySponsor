import React from "react";
import { IGuardService } from "./IGuardService";

export interface IGuardProps extends React.PropsWithChildren {
    requiredRoles: string[];
    guardService: IGuardService;
    forbidden?: () => React.ReactNode;
}