import React, { useState } from "react";
import axios from "axios";
import { BASE_URL } from "../apiConfig";

export const Home = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [prediction, setPrediction] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handlePredict = async () => {
    if (selectedFile) {
      setLoading(true);

      try {
        const formData = new FormData();
        formData.append("file", selectedFile);

        const authToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIwZWE1ZTQwZi1mODNhLTQwMWYtOGM3ZS0yNGI5NzRmZGY4NTUiLCJyb2xlIjoiZmFybWVyIiwiZXhwIjoxNjkyMjE4OTYxLCJqdGkiOiJmZGJmMDYzNS1iYjdhLTRjNjItYWJkNi02ZWRiZjY1ODU1MTYiLCJ0eXBlIjoiYWNjZXNzIn0.01fuCPBfgckgGQtbuKRAQgWKj-FMbPWmk6b790tjAvY"

        const response = await axios.post(
          `${BASE_URL}/predict`,
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
              Authorization: `Bearer ${authToken}`,

            },
          }
        );

        if (response.status === 200) {
          setPrediction(response.data.predicted_class);
          console.log(response.data)
        }
      } catch (error) {
        console.error("Prediction failed:", error);
      }

      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Upload and Predict</h2>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      <button onClick={handlePredict} disabled={!selectedFile || loading}>
        {loading ? "Predicting..." : "Predict"}
      </button>
      {prediction && <p>Prediction: {prediction}</p>}
    </div>
  );
};
