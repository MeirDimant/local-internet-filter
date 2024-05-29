import React, { useState, useEffect } from "react";

interface AddContentFormProps {
  onContentAdded: () => void;
}

const AddContentForm: React.FC<AddContentFormProps> = ({ onContentAdded }) => {
  // State variables to manage domains, selected domain, content type, and loading state
  const [domains, setDomains] = useState<string[]>([]);
  const [domainName, setDomainName] = useState("");
  const [content, setContent] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  // useEffect hook to fetch approved domains when the component mounts
  useEffect(() => {
    const fetchDomains = async () => {
      setIsLoading(true);
      try {
        const response = await fetch("http://settings.it/api/approved-domains");
        const data: string[] = await response.json();
        setDomains(data);
        if (data.length > 0) {
          setDomainName(data[0]); // Set the first domain as the default selected domain
        }
        setIsLoading(false);
      } catch (error) {
        console.error("Error fetching approved domains:", error);
        setIsLoading(false);
      }
    };

    fetchDomains();
  }, []);

  // Function to handle adding content to the selected domain
  const handleAddContent = async () => {
    try {
      const response = await fetch("http://settings.it/api/contents", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ domain_name: domainName, content }),
      });
      if (response.ok) {
        setContent(""); // Reset content input
        onContentAdded(); // Callback to indicate content was added
      }
    } catch (error) {
      console.error("Error adding content:", error);
    }
  };

  // Show loading message while fetching domains
  if (isLoading) {
    return <div>Loading...</div>; 
  }

  // Show message if no approved domains are available
  if (domains.length === 0) {
    return <div>There are no approved domains added.</div>; 
  }

  return (
    <div className="add-section">
      {/* Dropdown to select the domain */}
      <select
        className="add-input"
        value={domainName}
        onChange={(e) => setDomainName(e.target.value)}
      >
        {domains.map((domain) => (
          <option key={domain} value={domain}>
            {domain}
          </option>
        ))}
      </select>

      {/* Dropdown to select the content type */}
      <select
        className="add-input"
        value={content}
        onChange={(e) => setContent(e.target.value)}
      >
        <option value="" disabled selected>
          Please select
        </option>
        <option value="application">Application</option>
        <option value="audio">Audio</option>
        <option value="image">Image</option>
        <option value="multipart">Multipart</option>
        <option value="text">Text</option>
        <option value="video">Video</option>
      </select>

      {/* Button to add content to the selected domain */}
      <button className="add-btn" onClick={handleAddContent}>
        Update allowed content to the chosen domain
      </button>
    </div>
  );
};

export default AddContentForm;
