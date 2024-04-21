import React, { useContext } from "react";
import { Navigate, Outlet, RouteProps } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

const PrivateRoute: React.FC<RouteProps> = () => {
  const authContext = useContext(AuthContext);

  if (authContext?.loading) {
    return <div>Loding...</div>;
  }

  return authContext?.isAuthenticated ? (
    <Outlet />
  ) : (
    <Navigate to={authContext?.registered ? "/login" : "/register"} replace />
  );
};

export default PrivateRoute;
