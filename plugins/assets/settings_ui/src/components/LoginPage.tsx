import React, { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./styles/LoginPage.css";
import { AuthContext } from "../context/AuthContext";

const LoginPage: React.FC = () => {
  // State variables to manage username and password input
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");

  // Get the authentication context
  const authContext = useContext(AuthContext);
  const navigate = useNavigate();

  // Function to handle login action
  const handleLogin = async () => {
    await authContext?.login(username, password);
    if (authContext?.isAuthenticated) {
      setUsername("");
      setPassword("");
    }
  };

  // useEffect hook to navigate to white-list page if user is authenticated
  useEffect(() => {
    if (authContext?.isAuthenticated) {
      navigate("/white-list");
    }
  }, [authContext?.isAuthenticated, navigate]);

  return (
    <div className="login-page">
      <h1>Login</h1>
      {/* Input field for username */}
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      {/* Input field for password */}
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      {/* Button to trigger login action */}
      <button onClick={handleLogin}>Login</button>
    </div>
  );
};

export default LoginPage;
