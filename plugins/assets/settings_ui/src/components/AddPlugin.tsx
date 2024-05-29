import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./styles/ComponentsExtentionsClasses.css";

type Plugin = string;

const PluginManager: React.FC = () => {
  // State variables to manage the list of plugins and the uploading state
  const [plugins, setPlugins] = useState<Plugin[]>([]);
  const [uploading, setUploading] = useState<boolean>(false);
  const navigate = useNavigate();

  // Function to navigate to the plugins list page
  const navigateToPluginsList = () => {
    navigate("/plugins-list");
  };

  // useEffect hook to fetch the list of plugins when the component mounts
  useEffect(() => {
    fetchPlugins();
  }, []);

  // Function to fetch the list of plugins from the server
  const fetchPlugins = async () => {
    try {
      const response = await fetch("/api/plugins");
      if (response.ok) {
        const data = await response.json();
        console.log(data);

        // Extract request and response plugins lists
        const requestPluginObject = data.find(
          (item: any) => item.request_plugins_list !== undefined
        );

        const requestPluginsList =
          requestPluginObject?.request_plugins_list ?? [];

        const responsePluginObject = data.find(
          (item: any) => item.response_plugins_list !== undefined
        );
        const responsePluginsList =
          responsePluginObject?.response_plugins_list ?? [];

        // Combine and deduplicate the plugins lists
        const combinedPlugins: Plugin[] = [
          ...requestPluginsList,
          ...responsePluginsList,
        ];

        const uniquePlugins = new Set(combinedPlugins);
        setPlugins(Array.from(uniquePlugins));
      } else {
        throw new Error("Failed to fetch plugins");
      }
    } catch (error) {
      console.error("Failed to fetch plugins:", error);
    }
  };

  // Function to handle the plugin's file upload
  const handleFileUpload = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    setUploading(true);
    try {
      const response = await fetch("/api/plugins", {
        method: "POST",
        body: formData,
      });
      if (response.ok) {
        fetchPlugins(); // Refresh the plugins list after upload
        alert("File uploaded successfully");
      } else {
        throw new Error("Failed to upload file");
      }
    } catch (error) {
      console.error("Failed to upload file:", error);
      alert("Failed to upload file");
    }
    setUploading(false);
  };

  // Function to handle plugin deletion
  const handleDelete = async (pluginName: Plugin) => {
    try {
      const response = await fetch(`/api/plugins`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ plugin_name: pluginName }),
      });
      if (response.ok) {
        fetchPlugins();
        alert("Plugin removed successfully");
      } else {
        throw new Error("Failed to delete plugin");
      }
    } catch (error) {
      console.error("Failed to delete plugin:", error);
      alert("Failed to delete plugin");
    }
  };

  return (
    <div className="plugin-manager">
      <div className="container">
        <h1>Plugin Manager</h1>
        {/* Input field for file upload */}
        <input
          type="file"
          className="add-input"
          onChange={handleFileUpload}
          disabled={uploading}
        />
        {uploading && <p>Uploading...</p>}
        {/* List of plugins with delete buttons */}
        <ul className="list">
          {plugins.map((plugin, index) => (
            <li className="list-item" key={index}>
              {plugin}
              <button
                className="delete-btn"
                onClick={() => handleDelete(plugin)}
              >
                Delete
              </button>
            </li>
          ))}
        </ul>
      </div>
      {/* Button to navigate to the plugins list page */}
      <button
        className="add-btn navigate-btn-extension"
        onClick={navigateToPluginsList}
      >
        Define Plugins Order
      </button>
    </div>
  );
};

export default PluginManager;
