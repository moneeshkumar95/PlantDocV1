import React, { useState } from "react";
import axios from "axios";
import Resizer from "react-image-file-resizer";
import BASE_URL from "../../apiConfig";
import { useAuth } from "../../AuthContext";
import './Predict.css'

export const Predict = () => {
  const { user } = useAuth();
  const [selectedFile, setSelectedFile] = useState(null);
  const [species, setSpecies] = useState("");
  const [predictedClass, setPredictedClass] = useState("");
  const [accuracy, setAccuracy] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    clearResults();
    const file = event.target.files[0];
    if (file && (file.type === "image/jpeg" || file.type === "image/png")) {
      setSelectedFile(file);
    } else {
      alert("Only JPG and PNG files are allowed.");
    }
  };

  const handlePredict = async () => {
    const authToken = user.access_token; 
    if (selectedFile) {
      setLoading(true);

      try {
        const formData = new FormData();
        const image = await resizeFile(selectedFile);
        console.log(image)
        formData.append("file", image);

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
          console.log(response.data)
          const { species, predicted_class, accuracy } = response.data.data;
          setSpecies(species);
          setPredictedClass(predicted_class);
          setAccuracy(accuracy);
        }
      } catch (error) {
        console.error("Prediction failed:", error);
      }

      setLoading(false);
    }
  };

  const clearResults = () => {
    setSelectedFile("");
    setSpecies("");
    setPredictedClass("");
    setAccuracy("");
  };

  const resizeFile = (file) =>
  new Promise((resolve) => {
    Resizer.imageFileResizer(
      file,
      256,
      256,
      "JPEG",
      100,
      0,
      (uri) => {
        resolve(uri);
      },
      "file"
    );
  });

  const handleReset = () => {
    clearResults();
  };
  

  return (
    <div className="predict-container">
  <label className="file-input-label">
    Upload Image
    <input
      type="file"
      accept=".jpg, .png"
      onChange={handleFileChange}
      className="file-input"
    />
  </label>
  <div>
    <p></p>
  </div>
      {/* <input
        type="file"
        accept=".jpg, .png"
        onChange={handleFileChange}

      /> */}
      {selectedFile && (
        <div>
          <img
            src={URL.createObjectURL(selectedFile)}
            alt="Selected"
            style={{ maxWidth: "300px" }}
          />
        </div>
      )}
      <div>
        <p></p>
      </div>
      <div>
      <button onClick={handlePredict} disabled={!selectedFile || loading} className="btn btn-primary">
        {loading ? "Predicting..." : "Predict"}
      </button>
      {" "}
      <button onClick={handleReset} disabled={loading} className="btn btn-secondary">
        Reset
      </button>
      </div>
      {species && (
        <div className="result-container">
          <h4  className="result-title">Result:</h4>
          <p className="result-info"><b>Plant</b>: {species}</p>
          <p className="result-info"><b>Predicted Class</b>: {predictedClass}</p>
          <p className="result-accuracy"><b>Accuracy</b>: {accuracy}%</p>
        </div>
      )}
    </div>
  );
};

