import React, { useEffect, useState } from "react";
import axios from "axios";
import BASE_URL from "../../apiConfig";
import { useAuth } from "../../AuthContext";
import "./PredictionHistory.css";

export const PredictionHistory = () => {
  const { user } = useAuth();
  const [predictionHistory, setPredictionHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  const [dateFilter, setDateFilter] = useState("");
  const [speciesFilter, setSpeciesFilter] = useState("");
  const [predictedClassFilter, setPredictedClassFilter] = useState("");
  const [accuracyFilter, setAccuracyFilter] = useState("");

  useEffect(() => {
    const fetchPredictionHistory = async () => {
      try {
        const authToken = user.access_token;
        const is_admin = user.user_type === "admin";
        const root = is_admin ? "admin" : "predict";

        const filter_data = {
          date: dateFilter,
          species: speciesFilter,
          predicted_class: predictedClassFilter,
          accuracy: accuracyFilter,
        };

        const response = await axios.post(
          `${BASE_URL}/${root}/prediction-history`,
          filter_data,
          {
            headers: {
              Authorization: `Bearer ${authToken}`,
            },
          }
        );

        if (response.status === 200) {
          setPredictionHistory(response.data.data);
        }
      } catch (error) {
        console.error("Failed to fetch prediction history:", error);
      }

      setLoading(false);
    };

    fetchPredictionHistory();
  }, [dateFilter, speciesFilter, predictedClassFilter, accuracyFilter, user]);

  const handleClearFilters = () => {
    setDateFilter("");
    setSpeciesFilter("");
    setPredictedClassFilter("");
    setAccuracyFilter("");
  };

  return (
    <div className="prediction-history-container">
      <h2>Prediction History</h2>
      <div className="prediction-history-filters">
        <input
          type="date"
          placeholder="Date"
          value={dateFilter}
          onChange={(e) => setDateFilter(e.target.value)}
        />
        <input
          type="text"
          placeholder="Species"
          value={speciesFilter}
          onChange={(e) => setSpeciesFilter(e.target.value)}
        />
        <input
          type="text"
          placeholder="Predicted Class"
          value={predictedClassFilter}
          onChange={(e) => setPredictedClassFilter(e.target.value)}
        />
        <input
          type="number"
          placeholder="Accuracy"
          value={accuracyFilter}
          onChange={(e) => setAccuracyFilter(e.target.value)}
        />
        <button onClick={handleClearFilters} className="btn btn-secondary">Clear Filters</button>
      </div>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <table className="table table-striped">
          <thead>
            <tr>
              <th>Date</th>
              <th>Species</th>
              <th>Predicted Class</th>
              <th>Accuracy</th>
            </tr>
          </thead>
          <tbody>
            {predictionHistory.map((entry, index) => (
              <tr key={index}>
                <td>{entry.created_at}</td>
                <td>{entry.species}</td>
                <td>{entry.predicted_class}</td>
                <td>{entry.accuracy}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};
