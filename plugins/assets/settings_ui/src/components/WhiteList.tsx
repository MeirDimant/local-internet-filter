import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import ApprovedDomainsList from "./ApprovedDomainsList";
import AddDomainForm from "./AddDomainForm";
import "./styles/ComponentsExtentionsClasses.css";

const WhiteList: React.FC = () => {
  const [refreshKey, setRefreshKey] = useState<number>(0);
  const navigate = useNavigate();

  // Handler for when a domain is added to rerender the component
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
        {/* List of approved domains, re-rendered when refreshKey changes */}
        <ApprovedDomainsList refreshKey={refreshKey} />
        {/* Form to add a new domain, triggers handleDomainAdded on submission */}
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
