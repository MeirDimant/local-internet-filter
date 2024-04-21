import React, { createContext, useState, ReactNode, useEffect } from "react";

interface AuthContextProps {
  registered: boolean;
  isAuthenticated: boolean;
  loading: boolean;
  checkAuth: () => void;
  login: (username: string, password: string) => void;
}

export const AuthContext = createContext<AuthContextProps | undefined>(
  undefined
);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [registered, setRegistered] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);

  const login = async (username: string, password: string) => {
    try {
      const response = await fetch("http://settings.it/api/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
      });
      if (response.ok) {
        setIsAuthenticated(true);
      }
    } catch (error) {
      console.error("Failed to login:", error);
    }
  };

  const checkAuth = async () => {
    try {
      const response = await fetch("http://settings.it/api/auth/check");
      const { authenticated } = await response.json();
      setIsAuthenticated(authenticated);
    } catch (error) {
      console.error("Failed to check authentication status:", error);
    }
  };

  const checkIfRegistered = async () => {
    try {
      const response = await fetch("api/auth/any");
      if (response.ok) {
        setRegistered(true);
      } else {
        setRegistered(false);
      }
    } catch (error) {
      console.error("Error checking if ther are useres registered:", error);
    }
  };

  useEffect(() => {
    const initAuth = async () => {
      await checkAuth();
      await checkIfRegistered();
      setLoading(false); // Set loading to false after checks
    };

    initAuth();
  }, []);

  return (
    <AuthContext.Provider
      value={{ registered, isAuthenticated, loading, checkAuth, login }}
    >
      {children}
    </AuthContext.Provider>
  );
};
