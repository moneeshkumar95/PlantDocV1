import { BrowserRouter } from "react-router-dom";
import React from "react";
import ReactDOM from "react-dom"; 
import App from "./App.jsx";
import "./main.css";
import { AuthProvider } from "./AuthContext";

ReactDOM.createRoot(document.getElementById("root")).render(
  // <React.StrictMode>
  <AuthProvider>
    <BrowserRouter basename="/">
      <App />
    </BrowserRouter>
  </AuthProvider>
  // </React.StrictMode>
);
