import React, { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./styles/LoginPage.css";
import { AuthContext } from "../context/AuthContext";

const LoginPage: React.FC = () => {
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const authContext = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogin = async () => {
    await authContext?.login(username, password);
    if (authContext?.isAuthenticated) {
      setUsername("");
      setPassword("");
    }
  };

  useEffect(() => {
    if (authContext?.isAuthenticated) {
      navigate("/white-list");
    }
  }, [authContext?.isAuthenticated, navigate]);

  return (
    <div className="login-page">
      <h1>Login</h1>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleLogin}>Login</button>
    </div>
  );
};

export default LoginPage;
