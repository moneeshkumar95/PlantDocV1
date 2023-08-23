import React, { useState } from 'react'
import BASE_URL from "../../apiConfig";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../AuthContext";
// import '../../../node_modules/bootstrap/dist/css/bootstrap.min.css'
import './Login_Register.css'

export const Login = () => {
  const navigate  = useNavigate();
  const { login } = useAuth();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleLogin = async () => {
    // event.preventDefault();
    setLoading(true);

    try {
      const post_data = {
        username: username,
        password: password
      }
      console.log(post_data)

      const response = await axios.post(
        `${BASE_URL}/auth/login`,
        JSON.stringify(post_data),
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (response.status === 200) {
        console.log("Login successful");
        const { id, access_token, full_name, user_type } = response.data.data;
        login({ id, access_token, full_name, user_type });
        navigate("/");
      }
    } catch (error) {
      console.error("Login failed:", error);
      if (error.response && error.response.status === 400) {
        setErrorMessage("Invalid credentials. Please try again");
      } else if (error.response && error.response.status === 403) {
        setErrorMessage("Your account is not activated, please contact administrator");
      } else {
        setErrorMessage("An error occurred during login.");
      }
    }

    setLoading(false);
  };

    return (
      <div className="auth-wrapper">
          <div className="auth-inner">
        <form>
          <h3>Log In</h3>

          <div className="mb-3">
            <input
              type="username"
              className="form-control"
              placeholder="Username"
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>

          <div className="mb-3">
            <input
              type="password"
              className="form-control"
              placeholder="Password"
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          
          <div className="d-grid">
            <button onClick={handleLogin} disabled={loading} type="submit" className="btn btn-primary">
              {loading ? "Logging in..." : "Login"}
            </button>
            <div>
            <p></p>
            </div>
            <p className="forgot-password text-right">
            Need a account <a href="/register">register?</a>
            </p>
            {errorMessage && <p style={{ color: "red" }}>{errorMessage}</p>}
            <div>
              <p></p>
            </div>
          </div>
          
        </form>
        </div>
      </div>
    )
  }
