import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../AuthContext";
import axios from "axios";
import BASE_URL from "../../apiConfig";


export const Logout = () => {
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();
    const { user } = useAuth();
    const { logout } = useAuth();
    const authToken = user.access_token; 

    useEffect(() => {
        const handleLogout = async () => {

            try {
                const response = await axios.delete(`${BASE_URL}/auth/logout`, {
                    headers: {
                    Authorization: `Bearer ${authToken}`,
                    },
                });

                if (response.status === 200) {
                    logout();
                    navigate('/login');
                    alert("Logged out succefully")
                }
                } catch (error) {
                console.error("Failed to fetch user data:", error);
                }

                setLoading(false);
             };
        handleLogout();
    }, []);
  };
  