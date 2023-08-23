import React, { useEffect, useState } from "react";
import axios from "axios";
import BASE_URL from "../../apiConfig";
import { useAuth } from "../../AuthContext";
import "./PredictionHistory.css";
import { Link } from "react-router-dom";

export const UserList = () => {
  const { user } = useAuth();
  const [userList, setUserList] = useState([]);
  const [loading, setLoading] = useState(true);

  const [dateFilter, setDateFilter] = useState("");
  const [usernameFilter, setUsernameFilter] = useState("");
  const [fullNameFilter, setFullNameFilter] = useState("");
  const [userTypeFilter, setUserTypeFilter] = useState("");
  const [isActiveFilter, setIsActiveFilter] = useState(null);

  useEffect(() => {
    const fetchUserList = async () => {
      try {
        const authToken = user.access_token;
        const filter_data = {
          date: dateFilter,
          username: usernameFilter,
          full_name: fullNameFilter,
          user_type: userTypeFilter,
          is_active: isActiveFilter,
        };

        const response = await axios.post(
          `${BASE_URL}/admin/users`,
          filter_data,
          {
            headers: {
              Authorization: `Bearer ${authToken}`,
            },
          }
        );

        if (response.status === 200) {
          setUserList(response.data.data);
        }
      } catch (error) {
        console.error("Failed to fetch user list:", error);
      }

      setLoading(false);
    };
    fetchUserList();
  }, [
    dateFilter,
    usernameFilter,
    fullNameFilter,
    userTypeFilter,
    isActiveFilter,
    user,
  ]);

  const handleStatusChange = async (userId, newStatus) => {
    try {
      const authToken = user.access_token;
      const payload = { id: userId, status: newStatus };

      const response = await axios.put(
        `${BASE_URL}/admin/activate-deactivate-user`,
        payload,
        {
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        }
      );

      if (response.status === 200) {
        const updatedUserList = userList.map((user) => {
          if (user.id === userId) {
            return { ...user, is_active: newStatus };
          }
          return user;
        });
        setUserList(updatedUserList);
      }
    } catch (error) {
      console.error("Failed to update user status:", error);
    }
  };

  const handleClearFilters = () => {
    setDateFilter("");
    setUsernameFilter("");
    setFullNameFilter("");
    setUserTypeFilter("");
    setIsActiveFilter(null);
  };

  return (
    <div className="prediction-history-container">
      <h2>Users</h2>
      <div className="prediction-history-filters">
        <input
          type="date"
          placeholder="Date"
          value={dateFilter}
          onChange={(e) => setDateFilter(e.target.value)}
        />
        <input
          type="text"
          placeholder="Username"
          value={usernameFilter}
          onChange={(e) => setUsernameFilter(e.target.value)}
        />
        <input
          type="text"
          placeholder="Full Name"
          value={fullNameFilter}
          onChange={(e) => setFullNameFilter(e.target.value)}
        />
        <input
          type="text"
          placeholder="User Type"
          value={userTypeFilter}
          onChange={(e) => setUserTypeFilter(e.target.value)}
        />
      <select
        value={isActiveFilter}
        onChange={(e) => setIsActiveFilter(e.target.value)}
      >
        <option value="">Status</option>
        <option value="true">Active</option>
        <option value="false">Inactive</option>
      </select>
  <button onClick={handleClearFilters} className="btn btn-secondary">Clear Filters</button>
      </div>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <table className="table table-striped">
          <thead>
            <tr>
              <th>Registred At</th>
              <th>Username</th>
              <th>Fullname</th>
              <th>User Type</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {userList.map((entry, index) => (
              <tr key={index}>
                <td>{entry.created_at}</td>
                <td>
                  <Link to={`/user/profile?id=${entry.id}`}>{entry.username}</Link>
                </td>
                <td>{entry.full_name}</td>
                <td>{entry.user_type}</td>
                <td>
                  <button
                    className={entry.is_active ? "btn btn-success" : "btn btn-danger"}
                    onClick={() => handleStatusChange(entry.id, !entry.is_active)}
                  >
                    {entry.is_active ? "Active" : "Inactive"}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};
