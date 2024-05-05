import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import ApprovedDomainsList from "./ApprovedDomainsList";
import AddDomainForm from "./AddDomainForm";
import "./styles/ComponentsExtentionsClasses.css";

const WhiteList: React.FC = () => {
  const [refreshKey, setRefreshKey] = useState<number>(0);
  const navigate = useNavigate();

  const handleDomainAdded = () => {
    setRefreshKey((prevKey) => prevKey + 1);
  };

  const navigateToContentManager = () => {
    navigate("/filter-content");
  };

  const navigateToPluginsManager = () => {
    navigate("/plugins-manager");
  };

  return (
    <div className="white-list">
      <div className="container">
        <ApprovedDomainsList refreshKey={refreshKey} />
        <AddDomainForm onDomainAdded={handleDomainAdded} />
      </div>
      <button
        className="add-btn navigate-btn-extension"
        onClick={navigateToContentManager}
      >
        Go to Content Management
      </button>
      <button
        className="add-btn navigate-btn-extension"
        onClick={navigateToPluginsManager}
      >
        Plugins Manager
      </button>
    </div>
  );
};

export default WhiteList;
