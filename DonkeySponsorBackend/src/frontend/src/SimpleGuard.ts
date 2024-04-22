import { useContext } from "react";
import { IGuardService } from "./IGuardService";
import UserRoleContext from "./context/UserRoleContext";

export default class SimpleGuard implements IGuardService {
    checkRole(roles: string[]) : boolean {
        let found: string | undefined = roles.find(e => e === useContext(UserRoleContext));
        return found !== undefined;
    }
}