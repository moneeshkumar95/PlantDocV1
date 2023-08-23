import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../AuthContext";
import axios from "axios";
import BASE_URL from "../apiConfig";

import "./Navbar.css";
import { Link, NavLink } from "react-router-dom";

export const Navbar = () => {
  const [menuOpen, setMenuOpen] = useState(false);
  const navigate = useNavigate();
  const { user } = useAuth();
  const { logout } = useAuth();

  const handleTitleClick = () => {
    window.location.reload();
  };

  // const handleLogout = async () => {
  //   const [loading, setLoading] = useState(false);
  //   // const { user } = useAuth();
  //   const authToken = user.access_token; 

  //   try {
  //     const response = await axios.get(`${BASE_URL}/user/logout`, {
  //       headers: {
  //         Authorization: `Bearer ${authToken}`,
  //       },
  //     });

  //     if (response.status === 200) {
  //       logout();
  //       navigate('/login');
  //     }
  //   } catch (error) {
  //     console.error("Failed to fetch user data:", error);
  //   }

  //   setLoading(false);
  // };

  return (
    <nav>
      <Link to="/" className="title">
        PlantDoc
      </Link>
      <div className="menu" onClick={() => setMenuOpen(!menuOpen)}>
        <span></span>
        <span></span>
        <span></span>
      </div>
      <ul className={menuOpen ? "open" : ""}>
        {user ? (
          <>
            <li>
              <NavLink to="/predict">Predict</NavLink>
            </li>
            <li>
              <NavLink to="/predication-history">History</NavLink>
            </li>

            {user.user_type === "admin" && (
              <>
                <li>
                  <NavLink to="/admin/users">Users</NavLink>
                </li>
              </>
            )}
            <li>
              <NavLink to="/user/profile">Profile</NavLink>
            </li>
            <li>
              <NavLink to="/logout">Logout</NavLink>
            </li>
            {/* <li>
              <button onClick={handleLogout} className="btn btn-dark">Logout</button>
            </li> */}
          </>
        ) : (
          <>
            <li>
              <NavLink to="/login">Login</NavLink>
            </li>
            <li>
              <NavLink to="/register">Register</NavLink>
            </li>
          </>
        )}
      </ul>
    </nav>
  );
};
