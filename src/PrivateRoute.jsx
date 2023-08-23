import React from 'react';
import { Route, Navigate } from 'react-router-dom';
import { useAuth } from "./AuthContext";

export const PrivateRoute = ({ children }) => {
  const { user } = useAuth();
  return (
    user ? <>{children}</> : <Navigate to="/login" />
  )
}

export const PublicRoute = ({ children }) => {
  const { user } = useAuth();
  return (
    user ?  <Navigate to="/" /> : <>{children}</>
  )
}