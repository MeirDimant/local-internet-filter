import React from "react";
import {
  Navigate,
  Route,
  BrowserRouter as Router,
  Routes,
} from "react-router-dom";
import PrivateRoute from "./components/PrivateRoute";
import LoginPage from "./components/LoginPage";
import WhiteList from "./components/WhiteList";
import ContentManager from "./components/ContentManager";
import { AuthProvider } from "./context/AuthContext";
import RegisterPage from "./components/RegisterPage";
import "./AppStyles.css";
import PluginsList from "./components/PluginsList";
import AddPlugin from "./components/AddPlugin";

const App: React.FC = () => {

  return (
    // Provide authentication context to the entire app
    <AuthProvider>
      <Router>
        <Routes>
          {/* Define private routes that require authentication */}
          <Route path="/" element={<PrivateRoute />}>
            {/* Redirect the root path to the white list page */}
            <Route
              index
              element={<Navigate to="/white-list" replace />}
            ></Route>
            {/* Define routes for different components */}
            <Route path="/white-list" element={<WhiteList />}></Route>
            <Route path="/filter-content" element={<ContentManager />}></Route>
            <Route path="/plugins-list" element={<PluginsList />}></Route>
            <Route path="/plugins-manager" element={<AddPlugin />}></Route>
          </Route>
          {/* Define routes for login and register pages */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
};

export default App;
