import { IGuardProps } from "./IGuardProps";

export const Guard = (props: IGuardProps) => {
    if(props.guardService.checkRole(props.requiredRoles)) {
        return (
            <>
                {props.children}
            </>
        )
    } else if (props.forbidden === undefined){
        return <></>
    } else {
        return (
            <>
                {props.forbidden()}
            </>
        );
    }
}