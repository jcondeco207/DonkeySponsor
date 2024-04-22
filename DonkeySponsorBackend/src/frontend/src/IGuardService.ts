export interface IGuardService {
    checkRole: (roles: string[]) => boolean; 
}