import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./styles/RegisterPage.css";

const RegisterPage: React.FC = () => {
  // State for username and password inputs
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const navigate = useNavigate();

  // Function to handle the registration process
  const handleRegister = async () => {
    try {
      const response = await fetch("http://settings.it/api/auth/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
      });

      // If registration is successful, clear inputs and navigate to login page
      if (response.ok) {
        setUsername("");
        setPassword("");
        navigate("/login");
      }
    } catch (error) {
      console.error("Registration failed", error);
    }
  };

  return (
    <div className="register-page">
      <h1>Register</h1>
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
      <button onClick={handleRegister}>Register</button>
    </div>
  );
};

export default RegisterPage;
