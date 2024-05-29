import React, { useContext } from "react";
import { Navigate, Outlet, RouteProps } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

const PrivateRoute: React.FC<RouteProps> = () => {
  const authContext = useContext(AuthContext);

  // Show loading state if authentication status is still being determined
  if (authContext?.loading) {
    return <div>Loding...</div>;
  }

  // If user is authenticated, render the child components via <Outlet />
  // Otherwise, redirect to login or register page based on the registered status
  return authContext?.isAuthenticated ? (
    <Outlet />
  ) : (
    <Navigate to={authContext?.registered ? "/login" : "/register"} replace />
  );
};

export default PrivateRoute;
