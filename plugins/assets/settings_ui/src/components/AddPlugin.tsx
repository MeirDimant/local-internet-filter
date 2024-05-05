import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./styles/ComponentsExtentionsClasses.css";

// Define the type for the state that handles the list of plugins
type Plugin = string; // Assuming plugin names are strings, adjust based on your actual data structure

const PluginManager: React.FC = () => {
  const [plugins, setPlugins] = useState<Plugin[]>([]);
  const [uploading, setUploading] = useState<boolean>(false);
  const navigate = useNavigate();

  const navigateToPluginsList = () => {
    navigate("/plugins-list");
  };

  // Fetch plugins from the server
  useEffect(() => {
    fetchPlugins();
  }, []);

  const fetchPlugins = async () => {
    try {
      const response = await fetch("/api/plugins");
      if (response.ok) {
        const data = await response.json();
        console.log(data);
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

  // Handle file uploads
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
        fetchPlugins(); // Refresh the list after upload
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

  // Handle plugin deletion
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
        fetchPlugins(); // Refresh the list after deletion
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
        <input
          type="file"
          className="add-input"
          onChange={handleFileUpload}
          disabled={uploading}
        />
        {uploading && <p>Uploading...</p>}
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
