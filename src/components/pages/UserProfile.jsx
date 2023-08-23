import React, { useEffect, useState } from "react";
import axios from "axios";
import BASE_URL from "../../apiConfig";
import { useAuth } from "../../AuthContext";
import { Card, Spinner, Form, Button } from "react-bootstrap"; 
import { useSearchParams, useNavigate } from "react-router-dom";
import "./UserProfile.css"; 


export const UserProfile = () => {
  const { user } = useAuth();
  const [userData, setUserData] = useState({});
  const [loading, setLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [ queryParameters ] = useSearchParams(); 
  const navigate  = useNavigate();
  const id = queryParameters.get("id")
  const authToken = user.access_token; 
  const user_id = id ? id : user.id

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await axios.get(`${BASE_URL}/user/${user_id}`, {
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        });

        if (response.status === 200) {
          setUserData(response.data.data);
        }
      } catch (error) {
        console.error("Failed to fetch user data:", error);
      }

      setLoading(false);
    };

    fetchUserData();
  }, []);

  const handleEditClick = () => {
    setIsEditing(true);
  };

  const handleCancelClick = () => {
    setIsEditing(false);
    setUserData(userData);
  };

  const handleSaveClick = async () => {
    setIsEditing(false);
    try {
      const response = await axios.put(
        `${BASE_URL}/user/${user_id}`,
        userData,
        {
          headers: {
            Authorization: `Bearer ${authToken}`,
            "Content-Type": "application/json",
          },
        }
      );

      if (response.status === 200) {
        alert("User data updated successfully");
      }
    } catch (error) {
      console.error("Failed to update user data:", error);
    }
  };

  const handleFieldChange = (field, value) => {
    setUserData((prevUserData) => ({
      ...prevUserData,
      [field]: value,
    }));
  };

  const handleDeleteUser = async () => {
    try {
      const authToken = user.access_token;
      const response = await axios.delete(
        `${BASE_URL}/admin/user/${id}`,
        {
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        }
      );

      if (response.status === 200) {
        navigate("/admin/users");
        alert("User deleted succesfully")
      }
    } catch (error) {
      console.error("Failed to delete user:", error);
    }
  };


  return (
    <div className="user-profile-container">
      <h2>User Profile</h2>
      <div className="card-container">
        {loading ? (
          <Spinner animation="border" variant="primary" />
        ) : (
          <Card className="profile-card">
            <Card.Body>
              <Card.Text>
              <p>
                Full Name:{" "}
                {isEditing ? (
                  <Form.Control
                    type="text"
                    value={userData.full_name}
                    onChange={(e) => handleFieldChange("full_name", e.target.value)}
                  />
                ) : (
                  userData.full_name
                  )}
                </p>

                <p>
                Email:{" "}
                  {isEditing ? (
                    <Form.Control
                      type="text"
                      value={userData.email}
                      onChange={(e) => handleFieldChange("email", e.target.value)}
                    />
                  ) : (
                    userData.email
                  )}
                </p>

                <p>
                  Area:{" "}
                  {isEditing ? (
                    <Form.Control
                      type="text"
                      value={userData.area}
                      onChange={(e) => handleFieldChange("area", e.target.value)}
                    />
                  ) : (
                    userData.area
                  )}
                </p>

                <p>
                City:{" "}
                  {isEditing ? (
                    <Form.Control
                      type="text"
                      value={userData.city}
                      onChange={(e) => handleFieldChange("city", e.target.value)}
                    />
                  ) : (
                    userData.city
                  )}
                </p>

                <p>
                State:{" "}
                  {isEditing ? (
                    <Form.Control
                      type="text"
                      value={userData.st}
                      onChange={(e) => handleFieldChange("st", e.target.value)}
                    />
                  ) : (
                    userData.st
                  )}
                </p>

                <p>
                  Pincode:{" "}
                  {isEditing ? (
                    <Form.Control
                      type="text"
                      value={userData.pincode}
                      onChange={(e) => handleFieldChange("pincode", e.target.value)}
                    />
                  ) : (
                    userData.pincode
                  )}
                </p>
              </Card.Text>
              {isEditing ? (
                <div>
                  <Button variant="primary" onClick={handleSaveClick}>
                    Save
                  </Button>{" "}
                  <Button variant="secondary" onClick={handleCancelClick}>
                    Cancel
                  </Button>
              </div>
                
              ) : (
                <>
                <Button variant="primary" onClick={handleEditClick}>
                  Edit
                </Button>{" "}
                {user.user_type === "admin" && (
                  <Button variant="danger" onClick={handleDeleteUser}>
                    Delete
                  </Button>
                )}
                </>
              )}
            </Card.Body>
          </Card>
        )}
      </div>
    </div>
  );
};

