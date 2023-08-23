import React, { useState  } from 'react'
import BASE_URL from "../../apiConfig";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import '../../../node_modules/bootstrap/dist/css/bootstrap.min.css'
import './Login_Register.css'

export const Register = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [fullname, setFullname] = useState("");
  const [pincode, setPincode] = useState("");
  const [password, setPassword] = useState("");
  const [confirmpassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleRegister = async () => {
    event.preventDefault();
    setLoading(true);

    try {
      const post_data = {
        username: username,
        password: password,
        email: email,
        full_name: fullname,
        pincode: pincode,
      }
      console.log(post_data)

      const response = await axios.post(
        `${BASE_URL}/auth/register`,
        JSON.stringify(post_data),
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (response.status === 200) {
        console.log("Registered successful");
        alert("Success")
        window.location.reload();
        // resetForm();
        // window.location.reload();
        
      }
    } catch (error) {
      console.error("Register failed:", error);
      if (error.response && error.response.status === 409) {
        setErrorMessage("Username taken. Please try again");
      } else if (error.response && error.response.status === 422) {
        const errorData = error.response.data.detail[0];
        const fieldName = errorData.loc[1];
        const errorMessage = errorData.msg;
        setErrorMessage(`${fieldName}: ${errorMessage}`);
      } else {
        setErrorMessage("An error occurred during register.");
      }
    }

    setLoading(false);
  };


  return (
    <div className="auth-wrapper">
        <div className="auth-inner">
      <form>
        <h3>Register</h3>

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
            type="email"
            className="form-control"
            placeholder="Email"
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>

        <div className="mb-3">
          <input
            type="fullname"
            className="form-control"
            placeholder="Full name"
            onChange={(e) => setFullname(e.target.value)}
          />
        </div>

        <div className="mb-3">
          <input
            type="pincode"
            className="form-control"
            placeholder="Pincode"
            onChange={(e) => setPincode(e.target.value)}
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

        <div className="mb-3">
          <input
            type="password"
            className="form-control"
            placeholder="Confirm Password"
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
        </div>

        <div className="d-grid">
          <button onClick={handleRegister} disabled={loading} type="submit" className="btn btn-primary">
            Create
          </button>
        </div>
        <div>
          <p></p>
        </div>
        <p className="forgot-password text-right">
          Already registered <a href="/login">Login In?</a>
        </p>
        {errorMessage && <p style={{ color: "red" }}>{errorMessage}</p>}
        <div>
          <p></p>
        </div>
      </form>
      </div>
    </div>
  )
}
