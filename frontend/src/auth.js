import { useState, useEffect } from "react";
import { jwtDecode } from "jwt-decode";
import api from "./api";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "./token";


export const useAuthentication = () => {
 
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        const auth = async () => {
            const accessToken = localStorage.getItem('access_token');
            

            if (accessToken) {
                const decodedToken = jwtDecode(accessToken);
                const accessTokenExpiry = decodedToken.exp;
                const currentTime = Date.now() / 1000;

                if (accessTokenExpiry < currentTime) {
                    await refreshToken();
                } else {
                    setIsAuthenticated(true);
                }

            } else {
                setIsAuthenticated(false);
            }
                
        };
        
        auth().catch(() => setIsAuthenticated(false));  //  catch any errors and set isAuthenticated to false
    }, [])


    const refreshToken = async () => {
        const refreshToken = localStorage.getItem(REFRESH_TOKEN);

        try {
            const res = await api.post('/token/refresh/', {
                refresh: refreshToken,
            });
            if (res.status === 200) {
                localStorage.setItem('access_token', res.data.access);
                setIsAuthenticated(true);
            } else {
                setIsAuthenticated(false);
            }
        } catch (error) {
            console.error('Error refreshing token:', error);
            setIsAuthenticated(false);
        };
    }

 

    const logout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        setIsAuthenticated(false);
        window.location.href = '/';
    };
    


    return { isAuthenticated, logout };
}